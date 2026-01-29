"""Monora SDK public API."""
from .__version__ import __version__
from .api import call_agent, call_llm, call_tool, log_event
from .config_schema import (
    PYDANTIC_AVAILABLE,
    ConfigValidationError,
    get_validation_errors,
    is_valid_config,
    validate_config,
)
from .data_handling import DataHandlingViolation
from .context import Span, bind_context, capture_context, run_in_context
from .decorators import agent_step, llm_call, tool_call
from .lineage import (
    add_data_source,
    add_input_event,
    set_prompt_id,
    set_template_id,
    with_data_sources,
    with_inputs,
    with_prompt,
)
from .logger import get_logger, set_level as set_log_level
from .pdf_report import (
    WEASYPRINT_AVAILABLE,
    PDFGenerationError,
    generate_compliance_pdf,
    generate_ai_act_pdf,
    compute_pdf_sha256,
)
from .policy import PolicyViolation
from .runtime import init, set_violation_handler, shutdown
from .streaming import subscribe, unsubscribe
from .telemetry import (
    PROMETHEUS_AVAILABLE,
    STATSD_AVAILABLE,
    MetricsCollector,
    get_metrics_collector,
    init_metrics,
    close_metrics,
    record_event,
    record_api_call,
    record_violation,
    record_tokens,
)
from .tracing import trace
from .trust_package import export_trust_package

__all__ = [
    "init",
    "trace",
    "llm_call",
    "tool_call",
    "agent_step",
    "call_llm",
    "call_tool",
    "call_agent",
    "export_trust_package",
    "log_event",
    "set_violation_handler",
    "shutdown",
    "subscribe",
    "unsubscribe",
    "PolicyViolation",
    "DataHandlingViolation",
    "Span",
    "bind_context",
    "capture_context",
    "run_in_context",
    "add_input_event",
    "add_data_source",
    "set_prompt_id",
    "set_template_id",
    "with_inputs",
    "with_data_sources",
    "with_prompt",
    # Logger
    "get_logger",
    "set_log_level",
    # Config validation
    "validate_config",
    "is_valid_config",
    "get_validation_errors",
    "ConfigValidationError",
    "PYDANTIC_AVAILABLE",
    # PDF report generation
    "WEASYPRINT_AVAILABLE",
    "PDFGenerationError",
    "generate_compliance_pdf",
    "generate_ai_act_pdf",
    "compute_pdf_sha256",
    # Telemetry
    "PROMETHEUS_AVAILABLE",
    "STATSD_AVAILABLE",
    "MetricsCollector",
    "get_metrics_collector",
    "init_metrics",
    "close_metrics",
    "record_event",
    "record_api_call",
    "record_violation",
    "record_tokens",
    "__version__",
]
