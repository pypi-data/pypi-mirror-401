"""HTTP sink."""
from __future__ import annotations

import json
import os
import random
import threading
import time
import uuid
from typing import Any, Dict, Iterable, List, Optional

try:
    import requests
except ImportError as exc:  # pragma: no cover - optional dependency
    requests = None
    _requests_import_error = exc
else:
    _requests_import_error = None

from .base import Sink, SinkError
from monora.circuit_breaker import CircuitBreaker
from monora.logger import logger
from monora.verify import compute_events_digest


class HttpRetryQueue:
    def __init__(
        self,
        path: str,
        *,
        max_items: int = 10000,
    ):
        self.path = path
        self.max_items = max_items
        self._lock = threading.Lock()
        self._drain_lock = threading.Lock()
        os.makedirs(self.path, exist_ok=True)

    def enqueue(self, events: List[dict]) -> None:
        if not events:
            return
        with self._lock:
            self._prune_if_needed()
            filename = f"{int(time.time() * 1000)}_{uuid.uuid4().hex}.json"
            filepath = os.path.join(self.path, filename)
            payload = {
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "events": events,
            }
            with open(filepath, "w", encoding="utf-8") as handle:
                json.dump(payload, handle)

    def drain(self, send_func) -> None:
        if not self._drain_lock.acquire(blocking=False):
            return
        try:
            files = self._list_files()
            for filepath in files:
                try:
                    with open(filepath, "r", encoding="utf-8") as handle:
                        payload = json.load(handle)
                except Exception as exc:
                    logger.warning("Failed to read retry batch %s: %s", filepath, exc)
                    self._remove_file(filepath)
                    continue

                events = payload.get("events", [])
                if not isinstance(events, list):
                    logger.warning("Retry batch invalid in %s; dropping.", filepath)
                    self._remove_file(filepath)
                    continue

                try:
                    send_func(events)
                except Exception:
                    # Stop draining on first failure to preserve ordering
                    return
                self._remove_file(filepath)
        finally:
            self._drain_lock.release()

    def _list_files(self) -> List[str]:
        try:
            entries = [entry for entry in os.listdir(self.path) if entry.endswith(".json")]
        except FileNotFoundError:
            return []
        entries.sort()
        return [os.path.join(self.path, entry) for entry in entries]

    def _remove_file(self, filepath: str) -> None:
        try:
            os.remove(filepath)
        except FileNotFoundError:
            return
        except Exception as exc:
            logger.warning("Failed to remove retry batch %s: %s", filepath, exc)

    def _prune_if_needed(self) -> None:
        if self.max_items <= 0:
            return
        files = self._list_files()
        if len(files) < self.max_items:
            return
        excess = len(files) - self.max_items + 1
        logger.warning(
            "HTTP retry queue full; dropping %d oldest batch(es).", excess
        )
        for filepath in files[:excess]:
            self._remove_file(filepath)


class HttpSink(Sink):
    """HTTP sink with circuit breaker support.

    The circuit breaker prevents cascading failures when the endpoint
    is unavailable. After a configurable number of consecutive failures,
    the circuit opens and requests fail fast without attempting the request.
    """

    def __init__(
        self,
        endpoint: str,
        headers: Dict[str, str],
        *,
        batch_size: int = 50,
        timeout_sec: float = 10.0,
        retry_attempts: int = 3,
        backoff_base_sec: float = 0.5,
        circuit_breaker: Optional[Dict[str, Any]] = None,
        retry_queue: Optional[Dict[str, Any]] = None,
        idempotency: Optional[Dict[str, Any]] = None,
    ):
        if requests is None:
            raise SinkError(
                "requests is required for HttpSink. Install with monora[https]."
            ) from _requests_import_error
        self.endpoint = endpoint
        self.headers = headers
        self.batch_size = batch_size
        self.timeout = timeout_sec
        self.retries = retry_attempts
        self.backoff_base_sec = backoff_base_sec
        self.buffer: List[dict] = []
        self.lock = threading.Lock()
        self._retry_queue: Optional[HttpRetryQueue] = None
        self._retry_stop = threading.Event()
        self._retry_thread: Optional[threading.Thread] = None
        self._retry_interval_sec = 5.0
        self._idempotency_enabled = True
        self._idempotency_header = "Idempotency-Key"

        # Initialize circuit breaker
        cb_config = circuit_breaker or {}
        if cb_config.get("enabled", True):
            self._circuit_breaker: Optional[CircuitBreaker] = CircuitBreaker(
                failure_threshold=cb_config.get("failure_threshold", 5),
                success_threshold=cb_config.get("success_threshold", 2),
                reset_timeout_sec=cb_config.get("reset_timeout_sec", 60.0),
                name=f"HttpSink({endpoint})",
            )
        else:
            self._circuit_breaker = None

        queue_cfg = retry_queue or {}
        if queue_cfg.get("enabled", True):
            self._retry_interval_sec = max(
                0.1, float(queue_cfg.get("flush_interval_sec", 5.0))
            )
            self._retry_queue = HttpRetryQueue(
                path=str(queue_cfg.get("path", "./monora_http_queue")),
                max_items=int(queue_cfg.get("max_items", 10000)),
            )
            self._retry_thread = threading.Thread(target=self._retry_worker, daemon=True)
            self._retry_thread.start()

        idempotency_cfg = idempotency or {}
        self._idempotency_enabled = bool(idempotency_cfg.get("enabled", True))
        header_name = idempotency_cfg.get("header_name", "Idempotency-Key")
        if isinstance(header_name, str) and header_name.strip():
            self._idempotency_header = header_name.strip()

    def emit(self, events: Iterable[dict]) -> None:
        with self.lock:
            self.buffer.extend(events)
            if len(self.buffer) >= self.batch_size:
                self._flush_internal()

    def flush(self) -> None:
        with self.lock:
            self._flush_internal()

    def close(self) -> None:
        self._retry_stop.set()
        if self._retry_thread:
            self._retry_thread.join(timeout=2.0)
        self.flush()

    def _flush_internal(self) -> None:
        if self._retry_queue:
            self._retry_queue.drain(self._send_payload)

        if not self.buffer:
            return

        try:
            self._send_payload(self.buffer)
            self.buffer.clear()
        except Exception as exc:
            if self._retry_queue:
                self._retry_queue.enqueue(self.buffer)
                self.buffer.clear()
                logger.warning("HTTP sink queued batch after failure: %s", exc)
                return
            raise

    def _retry_worker(self) -> None:
        while not self._retry_stop.wait(self._retry_interval_sec):
            if not self._retry_queue:
                return
            try:
                self._retry_queue.drain(self._send_payload)
            except Exception as exc:
                logger.warning("HTTP retry drain failed: %s", exc)

    def _build_headers(self, events: List[dict]) -> Dict[str, str]:
        headers = dict(self.headers)
        if self._idempotency_enabled:
            headers[self._idempotency_header] = compute_events_digest(events)
        return headers

    def _send_payload(self, events: List[dict]) -> None:
        if not events:
            return

        # Check circuit breaker state
        if self._circuit_breaker and not self._circuit_breaker.can_execute():
            raise SinkError(
                f"Circuit breaker OPEN for {self.endpoint} "
                f"(state: {self._circuit_breaker.state.value})"
            )

        payload = {"events": events}
        headers = self._build_headers(events)
        for attempt in range(self.retries):
            try:
                response = requests.post(
                    self.endpoint,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                if self._circuit_breaker:
                    self._circuit_breaker.record_success()
                return
            except requests.RequestException as exc:
                if attempt == self.retries - 1:
                    if self._circuit_breaker:
                        self._circuit_breaker.record_failure()
                    raise SinkError(
                        f"HTTP sink failed after {self.retries} attempts"
                    ) from exc
                backoff = self.backoff_base_sec * (2**attempt) + random.uniform(0, 0.1)
                time.sleep(backoff)
