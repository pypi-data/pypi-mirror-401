"""Circuit breaker pattern for fault tolerance.

Implements the circuit breaker pattern to prevent cascading failures
when external services become unavailable. The circuit breaker has
three states:

- CLOSED: Normal operation, requests pass through
- OPEN: Circuit tripped, requests fail fast without attempting
- HALF_OPEN: Testing recovery, limited requests allowed
"""
from __future__ import annotations

import time
from enum import Enum
from threading import Lock
from typing import Optional

from monora.logger import logger


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""

    def __init__(self, message: str, state: CircuitState):
        super().__init__(message)
        self.state = state


class CircuitBreaker:
    """Circuit breaker for protecting external service calls.

    Example usage:
        cb = CircuitBreaker(failure_threshold=5, reset_timeout_sec=60)

        def call_external_service():
            if not cb.can_execute():
                raise CircuitBreakerError("Circuit is open")
            try:
                result = make_request()
                cb.record_success()
                return result
            except Exception:
                cb.record_failure()
                raise

    Configuration:
        failure_threshold: Number of consecutive failures to open circuit
        success_threshold: Number of successes in half-open to close circuit
        reset_timeout_sec: Time to wait before transitioning to half-open
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        reset_timeout_sec: float = 60.0,
        name: Optional[str] = None,
    ):
        """Initialize circuit breaker.

        Args:
            failure_threshold: Consecutive failures before opening circuit.
            success_threshold: Successes needed in half-open to close.
            reset_timeout_sec: Seconds before attempting half-open.
            name: Optional name for logging identification.
        """
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.reset_timeout_sec = reset_timeout_sec
        self.name = name or "circuit_breaker"

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: float = 0
        self._lock = Lock()

    @property
    def state(self) -> CircuitState:
        """Get current circuit state, checking for timeout transition."""
        with self._lock:
            if self._state == CircuitState.OPEN:
                elapsed = time.time() - self._last_failure_time
                if elapsed >= self.reset_timeout_sec:
                    logger.debug(
                        "[%s] Circuit transitioning OPEN -> HALF_OPEN after %.1fs",
                        self.name,
                        elapsed,
                    )
                    self._state = CircuitState.HALF_OPEN
                    self._success_count = 0
            return self._state

    @property
    def failure_count(self) -> int:
        """Get current failure count."""
        with self._lock:
            return self._failure_count

    @property
    def success_count(self) -> int:
        """Get current success count (relevant in half-open state)."""
        with self._lock:
            return self._success_count

    def can_execute(self) -> bool:
        """Check if request can proceed.

        Returns:
            True if circuit is closed or half-open, False if open.
        """
        return self.state != CircuitState.OPEN

    def record_success(self) -> None:
        """Record a successful operation.

        In half-open state, increments success count and may close circuit.
        In closed state, resets failure count.
        """
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                logger.debug(
                    "[%s] Success recorded in HALF_OPEN (%d/%d)",
                    self.name,
                    self._success_count,
                    self.success_threshold,
                )
                if self._success_count >= self.success_threshold:
                    logger.info(
                        "[%s] Circuit CLOSED after %d consecutive successes",
                        self.name,
                        self._success_count,
                    )
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
            elif self._state == CircuitState.CLOSED:
                # Reset failure count on success
                self._failure_count = 0

    def record_failure(self) -> None:
        """Record a failed operation.

        Increments failure count and may open circuit if threshold reached.
        In half-open state, immediately reopens circuit.
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == CircuitState.HALF_OPEN:
                logger.warning(
                    "[%s] Circuit reopening HALF_OPEN -> OPEN after failure",
                    self.name,
                )
                self._state = CircuitState.OPEN
            elif self._failure_count >= self.failure_threshold:
                logger.warning(
                    "[%s] Circuit OPEN after %d consecutive failures",
                    self.name,
                    self._failure_count,
                )
                self._state = CircuitState.OPEN

    def reset(self) -> None:
        """Manually reset circuit breaker to closed state."""
        with self._lock:
            logger.info("[%s] Circuit manually reset to CLOSED", self.name)
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = 0

    def __repr__(self) -> str:
        """Return string representation."""
        with self._lock:
            name = self.name
            state_value = self._state.value
            failure_count = self._failure_count
            failure_threshold = self.failure_threshold
        return (
            f"CircuitBreaker(name={name!r}, state={state_value}, "
            f"failures={failure_count}, threshold={failure_threshold})"
        )


__all__ = [
    "CircuitState",
    "CircuitBreaker",
    "CircuitBreakerError",
]
