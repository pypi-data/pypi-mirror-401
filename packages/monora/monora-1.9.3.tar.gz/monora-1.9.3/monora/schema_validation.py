"""JSON Schema validation helpers for Monora event contracts."""
from __future__ import annotations

import json
from importlib import resources
from typing import Any, Dict, List, Optional

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover - handled at runtime
    jsonschema = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


_SCHEMA_CACHE: Dict[str, Dict[str, Any]] = {}
_VALIDATOR_CACHE: Dict[str, Any] = {}


def _load_schema(name: str) -> Dict[str, Any]:
    if name in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[name]
    if _IMPORT_ERROR is not None:
        raise RuntimeError(
            "jsonschema is required for schema validation. "
            "Install monora with jsonschema support."
        ) from _IMPORT_ERROR
    schema_path = resources.files("monora.schemas").joinpath(name)
    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    _SCHEMA_CACHE[name] = schema
    return schema


def _get_validator(name: str) -> Any:
    if name in _VALIDATOR_CACHE:
        return _VALIDATOR_CACHE[name]
    schema = _load_schema(name)
    validator = jsonschema.Draft202012Validator(schema)
    _VALIDATOR_CACHE[name] = validator
    return validator


def _format_errors(errors: List[Any]) -> str:
    messages = []
    for error in errors:
        path = "/" + "/".join(str(p) for p in error.path) if error.path else "/"
        messages.append(f"{path}: {error.message}")
    return "; ".join(messages)


def validate_event_schema(event: Dict[str, Any]) -> Optional[str]:
    validator = _get_validator("event.schema.json")
    errors = sorted(validator.iter_errors(event), key=lambda e: e.path)
    if errors:
        return _format_errors(errors)
    return None


def validate_trust_summary_schema(summary: Dict[str, Any]) -> Optional[str]:
    validator = _get_validator("trust_summary.schema.json")
    errors = sorted(validator.iter_errors(summary), key=lambda e: e.path)
    if errors:
        return _format_errors(errors)
    return None


def validate_config_schema(config: Dict[str, Any]) -> Optional[str]:
    validator = _get_validator("config.schema.json")
    errors = sorted(validator.iter_errors(config), key=lambda e: e.path)
    if errors:
        return _format_errors(errors)
    return None
