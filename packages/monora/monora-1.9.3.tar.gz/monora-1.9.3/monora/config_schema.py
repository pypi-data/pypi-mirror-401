"""Pydantic schema validation for Monora configuration.

Provides optional validation of configuration dictionaries using Pydantic v2.
Gracefully degrades if Pydantic is not installed.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

try:
    from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    BaseModel = object  # type: ignore
    ConfigDict = None  # type: ignore
    Field = lambda *a, **kw: None  # type: ignore
    ValidationError = Exception  # type: ignore
    field_validator = lambda *a, **kw: lambda f: f  # type: ignore


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""

    def __init__(self, message: str, errors: Optional[List[Dict[str, Any]]] = None):
        super().__init__(message)
        self.errors = errors or []


# Enums for constrained values
class SinkType(str, Enum):
    STDOUT = "stdout"
    FILE = "file"
    HTTPS = "https"


class SinkFailureMode(str, Enum):
    WARN = "warn"
    RAISE = "raise"
    SILENT = "silent"


class QueueFullMode(str, Enum):
    WARN = "warn"
    RAISE = "raise"
    BLOCK = "block"


class DataHandlingMode(str, Enum):
    REDACT = "redact"
    BLOCK = "block"
    ALLOW = "allow"


class HashScope(str, Enum):
    PER_TRACE = "per_trace"
    GLOBAL = "global"


class HashAlgorithm(str, Enum):
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"


class SigningAlgorithm(str, Enum):
    ED25519 = "ed25519"
    HMAC_SHA256 = "hmac-sha256"


class WalSyncMode(str, Enum):
    FSYNC = "fsync"
    ASYNC = "async"
    NONE = "none"


class RiskCategory(str, Enum):
    MINIMAL = "minimal"
    LIMITED = "limited"
    HIGH = "high"
    UNACCEPTABLE = "unacceptable"


if PYDANTIC_AVAILABLE:
    class DefaultsConfig(BaseModel):
        """Default values for events."""
        model_config = ConfigDict(extra="allow")

        service_name: Optional[str] = None
        environment: Optional[str] = None
        data_classification: Optional[str] = "internal"
        purpose: Optional[str] = "general"

    # Forward reference for CircuitBreakerConfig (defined later)
    class SinkConfig(BaseModel):
        """Configuration for a single sink."""
        model_config = ConfigDict(extra="allow")

        type: SinkType
        path: Optional[str] = None
        endpoint: Optional[str] = None
        headers: Optional[Dict[str, str]] = None
        api_key: Optional[str] = None
        batch_size: Optional[int] = Field(default=None, ge=1)
        flush_interval_sec: Optional[float] = Field(default=None, ge=0)
        timeout_sec: Optional[float] = Field(default=None, ge=0)
        retry_attempts: Optional[int] = Field(default=None, ge=0)
        backoff_base_sec: Optional[float] = Field(default=None, ge=0)
        rotation: Optional[str] = None
        max_size_mb: Optional[int] = Field(default=None, ge=1)
        format: Optional[str] = None
        circuit_breaker: Optional[Dict[str, Any]] = None  # CircuitBreakerConfig
        retry_queue: Optional["RetryQueueConfig"] = None
        idempotency: Optional["IdempotencyConfig"] = None

        @field_validator("path")
        @classmethod
        def path_required_for_file(cls, v: Optional[str], info) -> Optional[str]:
            if info.data.get("type") == SinkType.FILE and not v:
                raise ValueError("path is required for file sink")
            return v

        @field_validator("endpoint")
        @classmethod
        def endpoint_required_for_https(cls, v: Optional[str], info) -> Optional[str]:
            if info.data.get("type") == SinkType.HTTPS and not v:
                raise ValueError("endpoint is required for https sink")
            return v

    class ImmutabilityConfig(BaseModel):
        """Hash chain configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = True
        scope: HashScope = HashScope.PER_TRACE
        hash_algorithm: HashAlgorithm = HashAlgorithm.SHA256
        verify_on_emit: bool = False
        verify_on_shutdown: bool = True
        persist_chain: bool = False

    class GpgConfig(BaseModel):
        """GPG signing configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = False
        key_id: Optional[str] = None
        gpg_home: Optional[str] = None

    class CircuitBreakerConfig(BaseModel):
        """Circuit breaker configuration for sinks."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = True
        failure_threshold: int = Field(default=5, ge=1)
        success_threshold: int = Field(default=2, ge=1)
        reset_timeout_sec: float = Field(default=60.0, ge=1.0)

    class RetryQueueConfig(BaseModel):
        """Durable retry queue configuration for HTTP sinks."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = True
        path: str = "./monora_http_queue"
        max_items: int = Field(default=10000, ge=1)
        flush_interval_sec: float = Field(default=5.0, ge=0.1)

    class IdempotencyConfig(BaseModel):
        """Idempotency header configuration for HTTP sinks."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = True
        header_name: str = "Idempotency-Key"

    class AttestationConfig(BaseModel):
        """Attestation and signing configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = False
        gpg: Optional[GpgConfig] = None

    class ProviderConfig(BaseModel):
        """Provider configuration for model registry."""
        model_config = ConfigDict(extra="allow")

        name: str
        model_patterns: List[str] = Field(default_factory=list)
        version_range: Optional[str] = None
        deprecated: bool = False
        deprecation_message: Optional[str] = None
        risk_category: RiskCategory = RiskCategory.LIMITED
        capabilities: List[str] = Field(default_factory=list)
        intended_use: Optional[str] = None
        deployment_regions: List[str] = Field(default_factory=list)

    class RegistryHistory(BaseModel):
        """Registry change log entry."""
        model_config = ConfigDict(extra="allow")

        version: Optional[str] = None
        date: Optional[str] = None
        changes: List[str] = Field(default_factory=list)

    class RegistryConfig(BaseModel):
        """Model registry configuration."""
        model_config = ConfigDict(extra="allow")

        version: str = "1.0.0"
        providers: List[ProviderConfig] = Field(default_factory=list)
        allow_unknown: bool = True
        default_provider: Optional[str] = None
        registry_path: Optional[str] = None
        history: Optional[List[RegistryHistory]] = None

    class InstrumentationConfig(BaseModel):
        """Auto-instrumentation configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = False
        auto_patch: bool = True
        targets: List[str] = Field(default_factory=lambda: ["openai", "anthropic"])
        fail_fast: bool = False
        default_purpose: Optional[str] = None
        data_classification: Optional[str] = None
        reason: Optional[str] = None
        log_report: bool = False

    class TracingConfig(BaseModel):
        """Tracing configuration."""
        model_config = ConfigDict(extra="allow")

        emit_span_events: bool = True

    class ReportingConfig(BaseModel):
        """Report generation configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = True
        emit_trust_summary: bool = True
        output_dir: Optional[str] = "./monora_reports"
        formats: List[str] = Field(default_factory=lambda: ["json"])
        include_security_report: bool = False
        include_executive_summary: bool = False
        max_events_per_trace: Optional[int] = Field(default=None, ge=1)
        redact_host: bool = True

    class RedactionRule(BaseModel):
        """Data redaction rule."""
        model_config = ConfigDict(extra="allow")

        pattern: str
        replacement: str = "[REDACTED]"
        apply_to: Optional[List[str]] = None
        classifications: Optional[List[str]] = None

    class DataHandlingConfig(BaseModel):
        """Data handling and redaction configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = False
        mode: DataHandlingMode = DataHandlingMode.REDACT
        apply_to: List[str] = Field(
            default_factory=lambda: [
                "request",
                "response",
                "tool_args",
                "tool_result",
                "agent_input",
                "agent_output",
                "custom",
            ]
        )
        rules: List[RedactionRule] = Field(default_factory=list)

    class PoliciesConfig(BaseModel):
        """Model policy configuration."""
        model_config = ConfigDict(extra="allow")

        model_allowlist: List[str] = Field(default_factory=list)
        model_denylist: List[str] = Field(default_factory=list)
        classification_max_models: Dict[str, Any] = Field(default_factory=dict)
        enforce: bool = False

    class AlertsConfig(BaseModel):
        """Violation alerting configuration."""
        model_config = ConfigDict(extra="allow")

        violation_webhook: Optional[str] = None
        headers: Dict[str, str] = Field(default_factory=dict)
        timeout_sec: float = 5.0
        retry_attempts: int = 3
        backoff_base_sec: float = 0.5
        queue_size: int = 200

    class ErrorHandlingConfig(BaseModel):
        """Error handling configuration."""
        model_config = ConfigDict(extra="allow")

        sink_failure_mode: SinkFailureMode = SinkFailureMode.WARN
        queue_full_mode: QueueFullMode = QueueFullMode.WARN
        fallback_path: Optional[str] = None
        log_user_exceptions: bool = True

    class BufferingConfig(BaseModel):
        """Event buffering configuration."""
        model_config = ConfigDict(extra="allow")

        queue_size: int = Field(default=1000, ge=1)
        batch_size: int = Field(default=50, ge=1)
        flush_interval_sec: float = Field(default=1.0, ge=0)
        queue_full_timeout_sec: Optional[float] = Field(default=None, ge=0)
        adaptive_batching: bool = Field(default=True)
        min_batch_size: int = Field(default=10, ge=1)
        max_batch_size: int = Field(default=500, ge=1)

    class WalConfig(BaseModel):
        """Write-ahead log configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = False
        path: str = "./monora_wal"
        sync_mode: WalSyncMode = WalSyncMode.FSYNC
        max_file_size_mb: int = Field(default=100, ge=1)
        retention_hours: int = Field(default=24, ge=1)
        recovery_on_startup: bool = True

    class SigningConfig(BaseModel):
        """Event signing configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = False
        algorithm: SigningAlgorithm = SigningAlgorithm.ED25519
        key_id: Optional[str] = None
        key_file: Optional[str] = None
        key_env: Optional[str] = None

    class AIActConfig(BaseModel):
        """EU AI Act compliance configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = False
        organization_name: Optional[str] = None
        contact_email: Optional[str] = None
        default_risk_category: RiskCategory = RiskCategory.LIMITED
        generate_transparency_report: bool = True
        transparency_report_formats: List[str] = Field(default_factory=lambda: ["json"])

    class PrometheusConfig(BaseModel):
        """Prometheus telemetry configuration."""
        model_config = ConfigDict(extra="allow")

        port: int = Field(default=9090, ge=1, le=65535)
        start_server: bool = True
        push_gateway: Optional[str] = None
        job_name: str = "monora"

    class StatsdConfig(BaseModel):
        """StatsD telemetry configuration."""
        model_config = ConfigDict(extra="allow")

        host: str = "localhost"
        port: int = Field(default=8125, ge=1, le=65535)
        prefix: str = "monora"

    class TelemetryConfig(BaseModel):
        """Telemetry and metrics configuration."""
        model_config = ConfigDict(extra="allow")

        enabled: bool = False
        backend: str = "prometheus"  # 'prometheus' or 'statsd'
        prometheus: Optional[PrometheusConfig] = None
        statsd: Optional[StatsdConfig] = None

    class MonoraConfig(BaseModel):
        """Complete Monora configuration schema."""
        model_config = ConfigDict(extra="allow")

        config_version: str = "1.0.0"
        defaults: Optional[DefaultsConfig] = None
        sinks: List[SinkConfig] = Field(default_factory=list)
        immutability: Optional[ImmutabilityConfig] = None
        attestation: Optional[AttestationConfig] = None
        registry: Optional[RegistryConfig] = None
        instrumentation: Optional[InstrumentationConfig] = None
        tracing: Optional[TracingConfig] = None
        reporting: Optional[ReportingConfig] = None
        data_handling: Optional[DataHandlingConfig] = None
        policies: Optional[PoliciesConfig] = None
        alerts: Optional[AlertsConfig] = None
        error_handling: Optional[ErrorHandlingConfig] = None
        buffering: Optional[BufferingConfig] = None
        wal: Optional[WalConfig] = None
        signing: Optional[SigningConfig] = None
        ai_act: Optional[AIActConfig] = None
        telemetry: Optional[TelemetryConfig] = None


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a configuration dictionary against the schema.

    Args:
        config: Configuration dictionary to validate.

    Returns:
        Validated configuration dictionary (with defaults applied).

    Raises:
        ConfigValidationError: If validation fails.
        RuntimeError: If Pydantic is not installed.
    """
    if not PYDANTIC_AVAILABLE:
        raise RuntimeError(
            "Pydantic is required for config validation. "
            "Install with: pip install pydantic>=2.0.0"
        )

    try:
        validated = MonoraConfig.model_validate(config)
        return validated.model_dump(exclude_none=True)
    except ValidationError as exc:
        errors = [
            {
                "loc": list(e["loc"]),
                "msg": e["msg"],
                "type": e["type"],
            }
            for e in exc.errors()
        ]
        error_messages = [
            f"  - {'.'.join(str(loc) for loc in e['loc'])}: {e['msg']}"
            for e in errors
        ]
        raise ConfigValidationError(
            f"Configuration validation failed:\n" + "\n".join(error_messages),
            errors=errors,
        ) from exc


def is_valid_config(config: Dict[str, Any]) -> bool:
    """Check if a configuration dictionary is valid.

    Args:
        config: Configuration dictionary to check.

    Returns:
        True if valid, False otherwise.
    """
    if not PYDANTIC_AVAILABLE:
        return True  # Gracefully degrade if Pydantic not installed

    try:
        MonoraConfig.model_validate(config)
        return True
    except ValidationError:
        return False


def get_validation_errors(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get validation errors for a configuration dictionary.

    Args:
        config: Configuration dictionary to validate.

    Returns:
        List of error dictionaries with 'loc', 'msg', and 'type' keys.
        Empty list if valid or Pydantic not installed.
    """
    if not PYDANTIC_AVAILABLE:
        return []

    try:
        MonoraConfig.model_validate(config)
        return []
    except ValidationError as exc:
        return [
            {
                "loc": list(e["loc"]),
                "msg": e["msg"],
                "type": e["type"],
            }
            for e in exc.errors()
        ]


__all__ = [
    "PYDANTIC_AVAILABLE",
    "ConfigValidationError",
    "validate_config",
    "is_valid_config",
    "get_validation_errors",
    # Enums
    "SinkType",
    "SinkFailureMode",
    "QueueFullMode",
    "DataHandlingMode",
    "HashScope",
    "HashAlgorithm",
    "SigningAlgorithm",
    "WalSyncMode",
    "RiskCategory",
]

if PYDANTIC_AVAILABLE:
    __all__.extend([
        "MonoraConfig",
        "DefaultsConfig",
        "SinkConfig",
        "CircuitBreakerConfig",
        "RetryQueueConfig",
        "IdempotencyConfig",
        "ImmutabilityConfig",
        "AttestationConfig",
        "RegistryConfig",
        "RegistryHistory",
        "InstrumentationConfig",
        "TracingConfig",
        "ReportingConfig",
        "DataHandlingConfig",
        "PoliciesConfig",
        "AlertsConfig",
        "ErrorHandlingConfig",
        "BufferingConfig",
        "WalConfig",
        "SigningConfig",
        "AIActConfig",
        "TelemetryConfig",
        "PrometheusConfig",
        "StatsdConfig",
    ])
