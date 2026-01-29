"""Event enrichers that add metadata to events."""
from datetime import datetime, timezone
import socket
import os
from typing import Dict, Optional


class Enricher:
    """Base enricher interface."""

    def enrich(self, event: Dict) -> None:
        """Enrich the event dict in-place."""
        raise NotImplementedError


class TimestampEnricher(Enricher):
    """Add ISO 8601 UTC timestamp."""

    def enrich(self, event: Dict) -> None:
        event["timestamp"] = datetime.now(timezone.utc).isoformat(timespec="milliseconds")


class ServiceNameEnricher(Enricher):
    """Add service name from config or process name."""

    def __init__(self, config: Dict):
        defaults = config.get("defaults", {})
        self.service_name = self._resolve_service_name(defaults)

    def _resolve_service_name(self, defaults: Dict) -> str:
        candidate = (
            defaults.get("service_name")
            or os.getenv("SERVICE_NAME")
            or os.getenv("MONORA_SERVICE_NAME")
        )
        service_name = self._sanitize_service_name(candidate)
        if not service_name:
            service_name = self._sanitize_service_name(self._get_process_name())
        return service_name or "monora"

    def _sanitize_service_name(self, value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        candidate = str(value).strip()
        if not candidate:
            return None
        candidate = os.path.basename(candidate)
        if candidate in {"__main__.py", "__main__", "unknown"}:
            return None
        return candidate

    def _get_process_name(self) -> str:
        """Get the process name from argv or fallback."""
        import sys

        if sys.argv:
            return os.path.basename(sys.argv[0]) or "unknown"
        return "unknown"

    def enrich(self, event: Dict) -> None:
        event["service_name"] = self.service_name


class EnvironmentEnricher(Enricher):
    """Add environment (dev/staging/production)."""

    def __init__(self, config: Dict):
        defaults = config.get("defaults", {})
        self.environment = defaults.get("environment", "dev")

    def enrich(self, event: Dict) -> None:
        event["environment"] = self.environment


class HostEnricher(Enricher):
    """Add hostname."""

    def __init__(self):
        self.host = self._resolve_host()

    def _resolve_host(self) -> Optional[str]:
        override = os.getenv("HOST_IN_PROOF")
        if override is not None:
            candidate = str(override).strip()
            if not candidate:
                return None
            if candidate.lower() in {"omit", "none", "redact"}:
                return None
            return candidate.split()[0]
        try:
            return socket.gethostname()
        except Exception:
            return None

    def enrich(self, event: Dict) -> None:
        if self.host is not None:
            event["host"] = self.host


class ProcessEnricher(Enricher):
    """Add process ID."""

    def __init__(self):
        self.process_id = os.getpid()

    def enrich(self, event: Dict) -> None:
        event["process_id"] = self.process_id
