"""Config schema migrations for Monora."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Optional

LATEST_CONFIG_VERSION = "1.0.0"
_DEFAULT_SINKS = [{"type": "stdout", "format": "json"}]


def apply_migrations(config: Dict[str, Any]) -> Dict[str, Any]:
    version = str(config.get("config_version") or "0.0.0")
    if _compare_versions(version, LATEST_CONFIG_VERSION) >= 0:
        if "config_version" not in config:
            config["config_version"] = LATEST_CONFIG_VERSION
        return config

    if _compare_versions(version, "1.0.0") < 0:
        _migrate_0_0_0_to_1_0_0(config)
        config["config_version"] = LATEST_CONFIG_VERSION
    return config


def _compare_versions(left: str, right: str) -> int:
    left_tuple = _parse_version(left)
    right_tuple = _parse_version(right)
    if left_tuple < right_tuple:
        return -1
    if left_tuple > right_tuple:
        return 1
    return 0


def _parse_version(value: str) -> tuple[int, int, int]:
    parts = str(value).split(".")
    major = _coerce_int(parts, 0)
    minor = _coerce_int(parts, 1)
    patch = _coerce_int(parts, 2)
    return major, minor, patch


def _coerce_int(parts: list[str], idx: int) -> int:
    if idx >= len(parts):
        return 0
    raw = parts[idx].split("-")[0].split("+")[0]
    try:
        return int(raw)
    except ValueError:
        return 0


def _migrate_0_0_0_to_1_0_0(config: Dict[str, Any]) -> None:
    defaults = config.setdefault("defaults", {})
    env_value = config.get("env")
    if env_value and defaults.get("environment") in (None, "dev"):
        defaults["environment"] = env_value

    policies = config.get("policies")
    if isinstance(policies, dict):
        if "allowed_models" in policies and "model_allowlist" not in policies:
            policies["model_allowlist"] = policies.get("allowed_models", [])
        if "forbidden_models" in policies and "model_denylist" not in policies:
            policies["model_denylist"] = policies.get("forbidden_models", [])

    logging_cfg = config.get("logging")
    http_cfg = config.get("http_sink")
    sinks = config.get("sinks")
    if isinstance(logging_cfg, dict) and _uses_default_sinks(sinks):
        sink_config = _sink_from_logging(logging_cfg, http_cfg if isinstance(http_cfg, dict) else {})
        if sink_config:
            config["sinks"] = [sink_config]

    _normalize_data_handling(config)
    _normalize_error_handling(config)


def _uses_default_sinks(sinks: Optional[list[Any]]) -> bool:
    if sinks is None:
        return True
    return sinks == _DEFAULT_SINKS


def _sink_from_logging(logging_cfg: Dict[str, Any], http_cfg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    sink_type = (logging_cfg.get("sink") or "").lower()
    if sink_type == "stdout":
        return {"type": "stdout"}
    if sink_type == "file":
        return {
            "type": "file",
            "path": logging_cfg.get("file_path", "./monora.log"),
        }
    if sink_type == "https":
        endpoint = http_cfg.get("endpoint")
        if not endpoint:
            return None
        sink: Dict[str, Any] = {"type": "https", "endpoint": endpoint}
        if "headers" in http_cfg:
            sink["headers"] = http_cfg["headers"]
        if "api_key" in http_cfg:
            sink["api_key"] = http_cfg["api_key"]
        return sink
    return None


def _normalize_data_handling(config: Dict[str, Any]) -> None:
    data_handling = config.get("data_handling")
    if not isinstance(data_handling, dict):
        return
    mode = data_handling.get("mode")
    if isinstance(mode, str):
        lowered = mode.lower()
        if lowered in {"mask", "encrypt"}:
            data_handling["mode"] = "redact"
        elif lowered in {"redact", "block", "allow"}:
            data_handling["mode"] = lowered

    if "targets" in data_handling and "apply_to" not in data_handling:
        data_handling["apply_to"] = deepcopy(data_handling.get("targets"))

    rules = data_handling.get("rules")
    if isinstance(rules, list):
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            if "targets" in rule and "apply_to" not in rule:
                rule["apply_to"] = deepcopy(rule.get("targets"))


def _normalize_error_handling(config: Dict[str, Any]) -> None:
    error_handling = config.get("error_handling")
    if not isinstance(error_handling, dict):
        return
    mode = error_handling.get("sink_failure_mode")
    if isinstance(mode, str):
        lowered = mode.lower()
        if lowered == "ignore":
            error_handling["sink_failure_mode"] = "silent"
        elif lowered in {"warn", "raise", "silent"}:
            error_handling["sink_failure_mode"] = lowered
