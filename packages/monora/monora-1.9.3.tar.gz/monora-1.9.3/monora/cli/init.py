"""Interactive setup wizard for Monora configuration."""
from __future__ import annotations

import json
import os
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

import click

from monora.autodetect import detect_environment, detect_installed_sdks, detect_service_name
from monora.config import DEFAULT_CONFIG, PRESETS, get_preset_config

try:  # Optional YAML support
    import yaml
except Exception:  # pragma: no cover - optional import
    yaml = None


PRESET_DESCRIPTIONS = {
    "minimal": "Bare minimum - stdout only, no features",
    "development": "Local development - stdout + file, relaxed policies",
    "production": "Production-ready - file sink, WAL, strict policies",
    "compliance": "Full compliance - signing, attestation, AI Act support",
}


def build_config_from_preset(preset: str, service_name: Optional[str] = None) -> Dict[str, Any]:
    """Build configuration from a preset name."""
    config = deepcopy(DEFAULT_CONFIG)
    preset_config = get_preset_config(preset)
    _merge_dicts(config, preset_config)

    if service_name:
        config.setdefault("defaults", {})["service_name"] = service_name
    elif not config.get("defaults", {}).get("service_name"):
        config.setdefault("defaults", {})["service_name"] = os.path.basename(os.getcwd()) or "monora-app"

    return config


def _merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    """Merge override dict into base dict recursively."""
    for key, value in (override or {}).items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _merge_dicts(base[key], value)
        else:
            base[key] = value


def build_config(answers: Dict[str, Any]) -> Dict[str, Any]:
    config = deepcopy(DEFAULT_CONFIG)
    defaults = config.setdefault("defaults", {})
    defaults["service_name"] = answers["service_name"]
    defaults["environment"] = answers["environment"]

    sinks = []
    if answers.get("stdout_sink"):
        sinks.append({"type": "stdout", "format": "json"})
    if answers.get("file_sink"):
        sinks.append(
            {
                "type": "file",
                "path": answers["file_path"],
                "rotation": "daily",
                "max_size_mb": 100,
                "batch_size": 100,
                "flush_interval_sec": 5.0,
            }
        )
    if answers.get("https_sink"):
        headers = {}
        if answers.get("https_auth_header"):
            headers["Authorization"] = answers["https_auth_header"]
        sinks.append(
            {
                "type": "https",
                "endpoint": answers["https_endpoint"],
                "headers": headers,
                "batch_size": 50,
                "timeout_sec": 10.0,
                "retry_attempts": 3,
                "backoff_base_sec": 0.5,
            }
        )
    if not sinks:
        sinks.append({"type": "stdout", "format": "json"})
    config["sinks"] = sinks

    policies = config.setdefault("policies", {})
    policies["model_allowlist"] = answers.get("allowlist", [])
    policies["model_denylist"] = answers.get("denylist", [])
    policies["enforce"] = bool(answers.get("enable_policies"))

    instrumentation = config.setdefault("instrumentation", {})
    instrumentation["enabled"] = bool(answers.get("enable_instrumentation", False))
    if answers.get("instrumentation_purpose"):
        instrumentation["default_purpose"] = answers["instrumentation_purpose"]

    data_handling = config.setdefault("data_handling", {})
    if answers.get("enable_data_handling"):
        data_handling["enabled"] = True
        data_handling["mode"] = answers.get("data_handling_mode", "redact")
        data_handling["rules"] = [
            {
                "name": "email",
                "pattern": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                "replace": "[REDACTED_EMAIL]",
                "classifications": ["confidential", "secret"],
                "apply_to": ["request", "response"],
            }
        ]
    else:
        data_handling["enabled"] = False
        data_handling["rules"] = []

    alerts = config.setdefault("alerts", {})
    alerts["violation_webhook"] = answers.get("violation_webhook")
    if answers.get("alerts_auth_header"):
        alerts["headers"] = {"Authorization": answers["alerts_auth_header"]}

    error_handling = config.setdefault("error_handling", {})
    error_handling["queue_full_mode"] = answers.get("queue_full_mode", "warn")

    buffering = config.setdefault("buffering", {})
    timeout = answers.get("queue_full_timeout_sec")
    if timeout is not None:
        buffering["queue_full_timeout_sec"] = timeout

    return config


def render_config(config: Dict[str, Any], fmt: str) -> Tuple[str, str]:
    fmt = fmt.lower()
    if fmt == "yaml":
        if yaml is None:
            return json.dumps(config, indent=2), "json"
        return (
            yaml.safe_dump(config, sort_keys=False, default_flow_style=False),
            "yaml",
        )
    if fmt == "json":
        return json.dumps(config, indent=2), "json"
    return json.dumps(config, indent=2), "json"


def run_wizard(
    *,
    config_path: str,
    fmt: str,
    assume_yes: bool,
    force: bool,
) -> Tuple[Dict[str, Any], str]:
    if os.path.exists(config_path) and not force:
        if assume_yes:
            raise click.ClickException(
                f"{config_path} already exists. Use --force to overwrite."
            )
        overwrite = click.confirm(
            f"{config_path} already exists. Overwrite?", default=False
        )
        if not overwrite:
            raise click.ClickException("Aborted.")

    # Auto-detect project info
    detected_service = detect_service_name() or os.path.basename(os.getcwd()) or "monora-app"
    detected_env = detect_environment()
    detected_sdks = detect_installed_sdks()

    # Show auto-detection results
    click.echo("")
    click.echo("=== Monora Setup Wizard ===")
    click.echo("")
    click.echo("Auto-detected configuration:")
    click.echo(f"  Service name: {detected_service}")
    click.echo(f"  Environment:  {detected_env}")
    if detected_sdks:
        click.echo(f"  AI SDKs:      {', '.join(detected_sdks)}")
    else:
        click.echo("  AI SDKs:      (none detected)")
    click.echo("")

    # Generate smart defaults based on detection
    if "openai" in detected_sdks and "anthropic" in detected_sdks:
        smart_allowlist = ["gpt-4*", "gpt-4o*", "claude-3-*"]
    elif "openai" in detected_sdks:
        smart_allowlist = ["gpt-4*", "gpt-4o*", "o1-*"]
    elif "anthropic" in detected_sdks:
        smart_allowlist = ["claude-3-*", "claude-sonnet-4-*", "claude-opus-4-*"]
    else:
        smart_allowlist = []

    if assume_yes:
        # Smart defaults for --yes mode
        click.echo("Using smart defaults based on auto-detection...")
        click.echo("")
        answers = {
            "service_name": detected_service,
            "environment": detected_env,
            "stdout_sink": detected_env == "dev",
            "file_sink": True,
            "file_path": "./logs/monora_events.jsonl" if detected_env == "production" else "./monora_events.jsonl",
            "https_sink": False,
            "enable_policies": len(smart_allowlist) > 0,
            "allowlist": smart_allowlist,
            "denylist": [],
            "enable_instrumentation": len(detected_sdks) > 0,
            "instrumentation_purpose": "general",
            "enable_data_handling": False,
            "data_handling_mode": "redact",
            "violation_webhook": None,
            "alerts_auth_header": None,
            "queue_full_mode": "warn",
            "queue_full_timeout_sec": None,
        }
        return build_config(answers), fmt

    answers = {
        "service_name": click.prompt("Service name", default=detected_service),
        "environment": click.prompt(
            "Environment",
            type=click.Choice(["dev", "staging", "production"]),
            default=detected_env,
        ),
    }

    answers["stdout_sink"] = click.confirm("Enable stdout sink?", default=detected_env == "dev")
    answers["file_sink"] = click.confirm("Enable file sink?", default=True)
    if answers["file_sink"]:
        default_path = "./logs/monora_events.jsonl" if answers["environment"] == "production" else "./monora_events.jsonl"
        answers["file_path"] = click.prompt("File sink path", default=default_path)
    answers["https_sink"] = click.confirm("Enable HTTPS sink?", default=False)
    if answers["https_sink"]:
        answers["https_endpoint"] = click.prompt("HTTPS endpoint URL")
        if click.confirm("Add Authorization header using MONORA_API_KEY?", default=False):
            answers["https_auth_header"] = "Bearer ${MONORA_API_KEY}"

    answers["enable_policies"] = click.confirm(
        "Configure model allowlist?", default=len(smart_allowlist) > 0
    )
    if answers["enable_policies"]:
        default_allowlist = ",".join(smart_allowlist) if smart_allowlist else "gpt-4*,claude-3-*"
        allowlist_raw = click.prompt(
            "Allowlist patterns (comma-separated)",
            default=default_allowlist,
        )
        denylist_raw = click.prompt(
            "Denylist patterns (comma-separated)",
            default="",
        )
        answers["allowlist"] = _parse_list(allowlist_raw)
        answers["denylist"] = _parse_list(denylist_raw)
    else:
        answers["allowlist"] = []
        answers["denylist"] = []

    answers["enable_instrumentation"] = click.confirm(
        "Enable auto-instrumentation?", default=len(detected_sdks) > 0
    )
    if answers["enable_instrumentation"]:
        answers["instrumentation_purpose"] = click.prompt(
            "Default purpose for instrumentation", default="general"
        )

    answers["enable_data_handling"] = click.confirm(
        "Enable data redaction rules?", default=False
    )
    if answers["enable_data_handling"]:
        answers["data_handling_mode"] = click.prompt(
            "Data handling mode",
            type=click.Choice(["redact", "block", "allow"]),
            default="redact",
        )

    answers["violation_webhook"] = click.prompt(
        "Violation webhook URL (blank to skip)", default="", show_default=False
    ).strip() or None
    if answers["violation_webhook"] and click.confirm(
        "Add Authorization header using MONORA_ALERTS_KEY?", default=False
    ):
        answers["alerts_auth_header"] = "Bearer ${MONORA_ALERTS_KEY}"

    answers["queue_full_mode"] = click.prompt(
        "Queue overflow mode",
        type=click.Choice(["warn", "raise", "block"]),
        default="warn",
    )
    if answers["queue_full_mode"] == "block":
        while True:
            timeout_raw = click.prompt(
                "Queue full timeout (seconds, blank for no timeout)",
                default="",
                show_default=False,
            ).strip()
            if not timeout_raw:
                answers["queue_full_timeout_sec"] = None
                break
            try:
                answers["queue_full_timeout_sec"] = float(timeout_raw)
                break
            except ValueError:
                click.echo("Please enter a valid number or leave blank.")

    return build_config(answers), fmt


def _parse_list(raw: str) -> List[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


@click.command(name="init")
@click.option("--path", "config_path", default="monora.yml", show_default=True)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    show_default=True,
)
@click.option(
    "--preset",
    type=click.Choice(["minimal", "development", "production", "compliance"]),
    default=None,
    help="Use a preset configuration (skips wizard)",
)
@click.option("--service-name", default=None, help="Service name for the config")
@click.option("--yes", "assume_yes", is_flag=True, help="Accept defaults without prompts")
@click.option("--force", is_flag=True, help="Overwrite existing config file")
def init_command(
    config_path: str,
    fmt: str,
    preset: Optional[str],
    service_name: Optional[str],
    assume_yes: bool,
    force: bool,
) -> None:
    """Interactive configuration wizard.

    Quick setup with presets:

        monora init --preset development

        monora init --preset production --service-name my-app

    Available presets:

        minimal     - Bare minimum logging (stdout only)

        development - Local dev with debugging (stdout + file)

        production  - Production-ready (file sink, WAL, strict policies)

        compliance  - Full EU AI Act compliance (signing, attestation)
    """
    # Check for existing file
    if os.path.exists(config_path) and not force:
        if assume_yes or preset:
            raise click.ClickException(
                f"{config_path} already exists. Use --force to overwrite."
            )
        overwrite = click.confirm(
            f"{config_path} already exists. Overwrite?", default=False
        )
        if not overwrite:
            raise click.ClickException("Aborted.")

    # Fast path: use preset directly
    if preset:
        config = build_config_from_preset(preset, service_name)
        output, rendered_format = render_config(config, fmt)
        with open(config_path, "w", encoding="utf-8") as handle:
            handle.write(output)

        if fmt == "yaml" and rendered_format != "yaml":
            click.echo("PyYAML not available; wrote JSON content instead.")

        click.echo(f"Monora config ({preset} preset) written to {config_path}")
        click.echo("")
        click.echo("Quick start:")
        click.echo("  import monora")
        click.echo(f'  monora.init("{preset}")  # or monora.init(config_path="{config_path}")')
        return

    # Interactive wizard path
    config, requested_format = run_wizard(
        config_path=config_path,
        fmt=fmt,
        assume_yes=assume_yes,
        force=True,  # Already checked above
    )
    output, rendered_format = render_config(config, requested_format)
    with open(config_path, "w", encoding="utf-8") as handle:
        handle.write(output)

    if requested_format == "yaml" and rendered_format != "yaml":
        click.echo("PyYAML not available; wrote JSON content instead.")

    click.echo("")
    click.echo(f"Monora config written to {config_path}")
    click.echo("")
    click.echo("=== Next Steps ===")
    click.echo("")
    click.echo("Option 1: Zero-config (recommended)")
    click.echo("  Just call init() - Monora auto-detects everything:")
    click.echo("")
    click.echo("  import monora")
    click.echo("  monora.init()")
    click.echo("")
    click.echo("Option 2: Use generated config file")
    click.echo("  import monora")
    click.echo(f'  monora.init(config_path="{config_path}")')
    click.echo("")
    detected_sdks = detect_installed_sdks()
    if detected_sdks:
        click.echo(f"Detected SDKs ({', '.join(detected_sdks)}) will be auto-instrumented.")
