"""CLI reporting for Monora logs."""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Set

import click

from monora.config import load_config
from monora.policy import compile_patterns
from monora.schema_validation import (
    validate_event_schema,
    validate_trust_summary_schema,
)
from monora.signing import verify_event_signature
from monora.verify import detect_sequence_gaps, verify_chain
from monora.cli.init import init_command
from monora.cli.diagnostics import validate_command, doctor_command

def _load_jsonl(path: str) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"Monora: skipping invalid JSON line: {exc}", file=sys.stderr)
    return events


def _validate_events_schema(events: List[Dict[str, Any]]) -> None:
    for idx, event in enumerate(events):
        error = validate_event_schema(event)
        if error:
            event_id = event.get("event_id") or f"index {idx}"
            raise click.ClickException(
                f"Event schema validation failed for {event_id}: {error}"
            )
        if event.get("event_type") == "trust_summary":
            body = event.get("body")
            if not isinstance(body, dict):
                raise click.ClickException(
                    f"Trust summary body is not an object for {event.get('event_id') or idx}"
                )
            trust_error = validate_trust_summary_schema(body)
            if trust_error:
                event_id = event.get("event_id") or f"index {idx}"
                raise click.ClickException(
                    f"Trust summary schema validation failed for {event_id}: {trust_error}"
                )


def _collect_schema_errors(events: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    for idx, event in enumerate(events):
        error = validate_event_schema(event)
        if error:
            event_id = event.get("event_id") or f"index {idx}"
            errors.append(f"event {event_id}: {error}")
        if event.get("event_type") == "trust_summary":
            body = event.get("body")
            if not isinstance(body, dict):
                event_id = event.get("event_id") or f"index {idx}"
                errors.append(f"trust_summary {event_id}: body is not an object")
                continue
            trust_error = validate_trust_summary_schema(body)
            if trust_error:
                event_id = event.get("event_id") or f"index {idx}"
                errors.append(f"trust_summary {event_id}: {trust_error}")
    return errors


def _load_config_safe(config_path: Optional[str]) -> Dict[str, Any]:
    try:
        return load_config(config_path=config_path)
    except Exception as exc:
        raise click.ClickException(f"Failed to load config: {exc}") from exc


def _resolve_retry_queue_paths(
    config: Dict[str, Any],
    override_path: Optional[str],
) -> Tuple[List[str], List[str]]:
    warnings: List[str] = []
    if override_path:
        return [override_path], warnings

    sinks = config.get("sinks", []) if isinstance(config, dict) else []
    paths: List[str] = []
    for sink in sinks:
        if not isinstance(sink, dict):
            continue
        sink_type = str(sink.get("type", "")).lower()
        if sink_type != "https":
            continue
        queue_cfg = sink.get("retry_queue")
        if queue_cfg is None:
            continue
        if isinstance(queue_cfg, dict) and not queue_cfg.get("enabled", True):
            continue
        queue_path = "./monora_http_queue"
        if isinstance(queue_cfg, dict):
            queue_path = str(queue_cfg.get("path", queue_path))
        paths.append(queue_path)

    if not paths:
        warnings.append(
            "no https retry_queue configured; using default path ./monora_http_queue"
        )
        paths.append("./monora_http_queue")

    deduped: List[str] = []
    for path in paths:
        if path not in deduped:
            deduped.append(path)
    return deduped, warnings


def _inspect_retry_queue(path: str, *, clear: bool) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "path": path,
        "batches": 0,
        "events": 0,
        "oldest": None,
        "newest": None,
        "cleared": 0 if clear else None,
        "warnings": [],
        "errors": [],
    }

    if not os.path.exists(path):
        info["warnings"].append("queue path not found")
        return info

    try:
        entries = [entry for entry in os.listdir(path) if entry.endswith(".json")]
    except Exception as exc:
        info["errors"].append(f"failed to list queue directory: {exc}")
        return info

    entries.sort()
    files = [os.path.join(path, entry) for entry in entries]
    info["batches"] = len(files)

    mtimes: List[float] = []
    for filepath in files:
        try:
            stat = os.stat(filepath)
            mtimes.append(stat.st_mtime)
        except Exception as exc:
            info["errors"].append(f"{filepath}: stat failed: {exc}")

    if mtimes:
        info["oldest"] = datetime.fromtimestamp(min(mtimes), tz=timezone.utc).isoformat()
        info["newest"] = datetime.fromtimestamp(max(mtimes), tz=timezone.utc).isoformat()

    for filepath in files:
        payload = None
        try:
            with open(filepath, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except Exception as exc:
            info["errors"].append(f"{filepath}: read failed: {exc}")

        if isinstance(payload, dict):
            events = payload.get("events")
            if isinstance(events, list):
                info["events"] += len(events)
            else:
                info["errors"].append(f"{filepath}: invalid events payload")

        if clear:
            try:
                os.remove(filepath)
                info["cleared"] += 1
            except Exception as exc:
                info["errors"].append(f"{filepath}: clear failed: {exc}")

    return info


def _emit_retry_queue_results(results: Dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        click.echo(json.dumps(results, indent=2))
        return

    queues = results.get("queues", [])
    for queue in queues:
        click.echo(f"Queue: {queue.get('path')}")
        click.echo(f"  batches: {queue.get('batches')}")
        click.echo(f"  events: {queue.get('events')}")
        if queue.get("oldest"):
            click.echo(f"  oldest: {queue.get('oldest')}")
        if queue.get("newest"):
            click.echo(f"  newest: {queue.get('newest')}")
        if queue.get("cleared") is not None:
            click.echo(f"  cleared: {queue.get('cleared')}")
        for warning in queue.get("warnings", []):
            click.echo(f"  warning: {warning}")

    for warning in results.get("warnings", []):
        click.echo(f"Warning: {warning}")
    for error in results.get("errors", []):
        click.echo(f"Error: {error}")

def _group_events_by_trace(events: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for event in events:
        trace_id = event.get("trace_id")
        if not trace_id:
            continue
        grouped.setdefault(trace_id, []).append(event)
    return grouped


def _sort_events_for_chain(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def sort_key(event: Dict[str, Any]) -> Tuple[int, Any]:
        sequence = event.get("event_sequence")
        if isinstance(sequence, int):
            return (0, sequence)
        return (1, event.get("timestamp") or "")

    return sorted(events, key=sort_key)


def _verify_hash_chain(events: List[Dict[str, Any]], config: Dict[str, Any]) -> None:
    immutability = config.get("immutability", {}) if isinstance(config, dict) else {}
    if immutability.get("enabled") is False:
        click.echo(
            "Warning: immutability disabled; hash verification skipped.",
            err=True,
        )
        return
    scope = immutability.get("scope", "per_trace")
    if scope == "global":
        is_valid, error = verify_chain(events)
        if not is_valid:
            raise click.ClickException(f"Hash chain verification failed: {error}")
        return

    grouped = _group_events_by_trace(events)
    if not grouped:
        click.echo(
            "Warning: no trace_id values found; hash verification skipped.",
            err=True,
        )
        return
    for trace_id, trace_events in grouped.items():
        is_valid, error = verify_chain(trace_events)
        if not is_valid:
            raise click.ClickException(
                f"Hash chain verification failed for trace {trace_id}: {error}"
            )


def _verify_signatures(events: List[Dict[str, Any]], config: Dict[str, Any]) -> None:
    signed_events = [event for event in events if event.get("event_signature")]
    if not signed_events:
        click.echo(
            "Warning: no event signatures found; signature verification skipped.",
            err=True,
        )
        return
    signing = config.get("signing", {}) if isinstance(config, dict) else {}
    key_file = signing.get("key_file")
    key_env = signing.get("key_env", "MONORA_SIGNING_KEY")
    key_data = None
    if key_file:
        try:
            with open(key_file, "rb") as handle:
                key_data = handle.read()
        except OSError as exc:
            raise click.ClickException(
                f"Failed to read signing key file {key_file}: {exc}"
            ) from exc

    if key_data is None and not os.getenv(key_env):
        raise click.ClickException(
            f"Signature verification failed: no key available "
            f"(set {key_env} or signing.key_file)."
        )

    for event in signed_events:
        if not verify_event_signature(event, key_data=key_data, key_env=key_env):
            event_id = event.get("event_id") or "unknown"
            raise click.ClickException(
                f"Signature verification failed for event {event_id}"
            )


def _check_hash_chain(events: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
    immutability = config.get("immutability", {}) if isinstance(config, dict) else {}
    scope = immutability.get("scope", "per_trace")
    if immutability.get("enabled") is False:
        return {
            "status": "skipped",
            "reason": "unavailable",
            "scope": scope,
            "verified_traces": 0,
            "total_traces": 0,
            "errors": [],
            "warnings": ["immutability disabled"],
        }

    if scope == "global":
        is_valid, error = verify_chain(events)
        return {
            "status": "verified" if is_valid else "failed",
            "scope": scope,
            "verified_traces": 1 if is_valid else 0,
            "total_traces": 1 if events else 0,
            "errors": [error] if error else [],
            "warnings": [],
        }

    grouped = _group_events_by_trace(events)
    if not grouped:
        return {
            "status": "skipped",
            "reason": "unavailable",
            "scope": scope,
            "verified_traces": 0,
            "total_traces": 0,
            "errors": [],
            "warnings": ["no trace_id values found"],
        }

    errors = []
    verified = 0
    for trace_id, trace_events in grouped.items():
        is_valid, error = verify_chain(_sort_events_for_chain(trace_events))
        if not is_valid:
            errors.append(f"{trace_id}: {error}")
        else:
            verified += 1
    return {
        "status": "verified" if not errors else "failed",
        "scope": scope,
        "verified_traces": verified,
        "total_traces": len(grouped),
        "errors": errors,
        "warnings": [],
    }


def _check_signatures(events: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
    signed_events = [event for event in events if event.get("event_signature")]
    if not signed_events:
        return {
            "status": "skipped",
            "reason": "unavailable",
            "verified_events": 0,
            "total_signed_events": 0,
            "errors": [],
            "warnings": ["no event signatures found"],
        }

    signing = config.get("signing", {}) if isinstance(config, dict) else {}
    key_file = signing.get("key_file")
    key_env = signing.get("key_env", "MONORA_SIGNING_KEY")
    key_data = None
    if key_file:
        try:
            with open(key_file, "rb") as handle:
                key_data = handle.read()
        except OSError as exc:
            return {
                "status": "failed",
                "verified_events": 0,
                "total_signed_events": len(signed_events),
                "errors": [f"failed to read key file {key_file}: {exc}"],
                "warnings": [],
            }

    if key_data is None and not os.getenv(key_env):
        return {
            "status": "failed",
            "verified_events": 0,
            "total_signed_events": len(signed_events),
            "errors": [f"no signing key available (set {key_env} or signing.key_file)"],
            "warnings": [],
        }

    errors = []
    verified = 0
    for event in signed_events:
        if verify_event_signature(event, key_data=key_data, key_env=key_env):
            verified += 1
        else:
            event_id = event.get("event_id") or "unknown"
            errors.append(f"{event_id}: signature verification failed")
    return {
        "status": "verified" if not errors else "failed",
        "verified_events": verified,
        "total_signed_events": len(signed_events),
        "errors": errors,
        "warnings": [],
    }


def _check_sequence_gaps(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not events:
        return {
            "status": "skipped",
            "reason": "unavailable",
            "gaps": [],
            "errors": [],
            "warnings": ["no events provided"],
        }
    gaps = detect_sequence_gaps(events)
    return {
        "status": "verified" if not gaps else "failed",
        "gaps": gaps,
        "errors": [f"{len(gaps)} traces with sequence gaps"] if gaps else [],
        "warnings": [],
    }


def _parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _format_timestamp(value: Optional[str]) -> Optional[str]:
    parsed = _parse_timestamp(value)
    if parsed is None:
        return value
    return parsed.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _normalize_model(model: Optional[str]) -> Optional[str]:
    if not model:
        return None
    return str(model).strip().lower()


def _coerce_token(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number


def _resolve_policy_name(body: Dict[str, Any]) -> str:
    for key in ("policy_name", "policy", "policy_id", "policyId"):
        value = body.get(key)
        if value:
            candidate = str(value).strip()
            if candidate:
                return candidate
    policy = body.get("policy")
    if isinstance(policy, dict):
        for key in ("name", "id", "policy_name"):
            value = policy.get(key)
            if value:
                candidate = str(value).strip()
                if candidate:
                    return candidate
    data_handling = body.get("data_handling")
    if isinstance(data_handling, dict) and data_handling.get("action"):
        return "data_handling.block"
    return "UNKNOWN_POLICY"


def _resolve_policy_message(body: Dict[str, Any]) -> str:
    message = body.get("message")
    if message:
        candidate = str(message).strip()
        if candidate:
            return candidate
    data_handling = body.get("data_handling")
    if isinstance(data_handling, dict):
        rules = data_handling.get("rules")
        if rules:
            rule_list = ", ".join(str(rule) for rule in rules)
            return f"Sensitive data matched rules: {rule_list}"
        action = data_handling.get("action")
        if action:
            return f"Data handling policy violation ({action})"
    return "Policy violation recorded"


def _normalize_usage(usage: Any) -> Optional[Tuple[int, int, int]]:
    if not isinstance(usage, dict):
        return None
    prompt_val = _coerce_token(usage.get("prompt_tokens"))
    completion_val = _coerce_token(usage.get("completion_tokens"))
    if prompt_val is None:
        prompt_val = _coerce_token(usage.get("input_tokens"))
    if completion_val is None:
        completion_val = _coerce_token(usage.get("output_tokens"))
    total_val = _coerce_token(usage.get("total_tokens"))
    if prompt_val is None and completion_val is None and total_val is None:
        return None
    prompt = prompt_val or 0
    completion = completion_val or 0
    total = total_val if total_val is not None else prompt + completion
    return prompt, completion, total


def _extract_usage(body: Dict[str, Any]) -> Optional[Tuple[int, int, int]]:
    response = body.get("response")
    if isinstance(response, dict):
        normalized = _normalize_usage(response.get("usage"))
        if normalized is not None:
            return normalized
    normalized = _normalize_usage(body.get("usage"))
    if normalized is not None:
        return normalized
    normalized = _normalize_usage(body.get("token_usage"))
    if normalized is not None:
        return normalized
    return None


def _classify_policy_violation(policy_name: str) -> Optional[str]:
    lowered = policy_name.lower()
    if "unknown_model" in lowered:
        return "unknown"
    if any(token in lowered for token in ("denylist", "blocklist", "forbidden")):
        return "forbidden"
    return None


def _build_report(
    events: List[Dict[str, Any]], policies: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    filtered_events = [
        event for event in events if event.get("event_type") != "trust_summary"
    ]
    trace_ids = {e.get("trace_id") for e in filtered_events if e.get("trace_id")}
    timestamps = [
        ts
        for ts in (_parse_timestamp(e.get("timestamp")) for e in filtered_events)
        if ts is not None
    ]
    start = min(timestamps).astimezone(timezone.utc).isoformat() if timestamps else None
    end = max(timestamps).astimezone(timezone.utc).isoformat() if timestamps else None

    by_event_type = Counter(
        e.get("event_type") for e in filtered_events if e.get("event_type")
    )
    by_purpose = Counter(e.get("purpose") for e in filtered_events if e.get("purpose"))
    by_classification = Counter(
        e.get("data_classification")
        for e in filtered_events
        if e.get("data_classification")
    )

    by_model = Counter()
    token_usage = {
        "total_prompt_tokens": 0,
        "total_completion_tokens": 0,
        "total_tokens": 0,
        "by_model": defaultdict(lambda: {"prompt": 0, "completion": 0, "total": 0}),
        "missing_usage_events": 0,
        "missing_usage_models": set(),
    }

    violations = []
    errors = []
    models_used = set()
    forbidden_models_blocked = set()
    unknown_models_used = set()
    allowed_models_used = set()
    allowlist_patterns: List[Tuple[str, Any]] = []
    denylist_patterns: List[Tuple[str, Any]] = []
    used_allowlist_patterns: Set[str] = set()

    for event in filtered_events:
        body = event.get("body")
        if not isinstance(body, dict):
            body = {}
        if body.get("status") == "policy_violation":
            policy_name = _resolve_policy_name(body) or "UNKNOWN_POLICY"
            message = _resolve_policy_message(body) or "Policy violation recorded"
            violations.append(
                {
                    "timestamp": _format_timestamp(event.get("timestamp")),
                    "model": _normalize_model(body.get("model")),
                    "policy": policy_name,
                    "message": message,
                }
            )
            model = _normalize_model(body.get("model"))
            if model:
                classification = _classify_policy_violation(policy_name)
                if classification == "forbidden":
                    forbidden_models_blocked.add(model)
                elif classification == "unknown":
                    unknown_models_used.add(model)

    for event in filtered_events:
        body = event.get("body")
        if not isinstance(body, dict):
            body = {}
        event_type = event.get("event_type")
        if event_type == "llm_call":
            model = _normalize_model(body.get("model"))
            is_blocked = body.get("status") == "policy_violation"
            if model and not is_blocked:
                by_model[model] += 1
                models_used.add(model)
            if is_blocked:
                usage = None
            else:
                usage = _extract_usage(body)
            if is_blocked:
                pass
            elif usage is None:
                token_usage["missing_usage_events"] += 1
                if model:
                    token_usage["missing_usage_models"].add(model)
            else:
                prompt, completion, total = usage
                token_usage["total_prompt_tokens"] += prompt
                token_usage["total_completion_tokens"] += completion
                token_usage["total_tokens"] += total
                if model:
                    token_usage["by_model"][model]["prompt"] += prompt
                    token_usage["by_model"][model]["completion"] += completion
                    token_usage["by_model"][model]["total"] += total

        if body.get("error"):
            errors.append(
                {
                    "timestamp": event.get("timestamp"),
                    "event_type": event_type,
                    "error": body.get("error"),
                }
            )

    if policies:
        allowlist_patterns = compile_patterns(policies.get("model_allowlist", []))
        denylist_patterns = compile_patterns(policies.get("model_denylist", []))

        for model in models_used:
            if model in forbidden_models_blocked:
                continue
            allow_match = (
                bool(allowlist_patterns)
                and _matches_any(allowlist_patterns, model, used_allowlist_patterns)
            )
            deny_match = bool(denylist_patterns) and _matches_any(
                denylist_patterns, model, None
            )
            if allow_match:
                allowed_models_used.add(model)
            elif deny_match:
                forbidden_models_blocked.add(model)
            elif allowlist_patterns:
                unknown_models_used.add(model)
            else:
                allowed_models_used.add(model)
    else:
        allowed_models_used = set(models_used)

    forbidden_models_blocked -= models_used
    unknown_models_used -= allowed_models_used
    unknown_models_used -= forbidden_models_blocked

    unused_allowlist_patterns = []
    if allowlist_patterns:
        unused_allowlist_patterns = sorted(
            {raw for raw, _ in allowlist_patterns if raw not in used_allowlist_patterns}
        )

    unknown_models_payload = (
        sorted(unknown_models_used) if policies or unknown_models_used else []
    )

    model_compliance = {
        "allowed_models_used": sorted(allowed_models_used),
        "forbidden_models_blocked": sorted(forbidden_models_blocked),
        "unknown_models_used": unknown_models_payload,
        "unused_allowlist_patterns": unused_allowlist_patterns,
    }

    return {
        "total_events": len(filtered_events),
        "traces": len(trace_ids),
        "date_range": {"start": start, "end": end},
        "by_event_type": dict(by_event_type),
        "by_model": dict(by_model),
        "by_purpose": dict(by_purpose),
        "by_classification": dict(by_classification),
        "violations": violations,
        "errors": errors,
        "token_usage": {
            "total_prompt_tokens": token_usage["total_prompt_tokens"],
            "total_completion_tokens": token_usage["total_completion_tokens"],
            "total_tokens": token_usage["total_tokens"],
            "by_model": dict(token_usage["by_model"]),
            "missing_usage_events": token_usage["missing_usage_events"],
            "missing_usage_models": sorted(token_usage["missing_usage_models"]),
        },
        "model_compliance": model_compliance,
    }


def _write_json(path: str, report: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)


def _write_markdown(path: str, report: Dict[str, Any]) -> None:
    lines = [
        "# Monora Compliance Report",
        f"**Period:** {report['date_range']['start']} to {report['date_range']['end']}",
        f"**Total Events:** {report['total_events']}",
        f"**Traces:** {report['traces']}",
        "",
        "## Event Breakdown",
    ]
    for event_type, count in report["by_event_type"].items():
        lines.append(f"- **{event_type}:** {count}")

    lines.append("")
    lines.append("## Models Used")
    for model, count in report["by_model"].items():
        lines.append(f"- {model}: {count} calls")

    violations = report.get("violations", [])
    lines.append("")
    lines.append(f"## Policy Violations ({len(violations)})")
    if violations:
        lines.append("| Timestamp | Model | Policy | Message |")
        lines.append("|-----------|-------|--------|---------|")
        for violation in violations:
            lines.append(
                f"| {violation['timestamp']} | {violation['model']} | {violation['policy']} | {violation['message']} |"
            )

    errors = report.get("errors", [])
    lines.append("")
    lines.append(f"## Errors ({len(errors)})")
    for error in errors:
        lines.append(
            f"- {error['timestamp']} ({error['event_type']}): {error['error']}"
        )

    compliance = report.get("model_compliance", {})
    if compliance:
        lines.append("")
        lines.append("## Model Compliance")
        lines.append(f"- Allowed models used: {', '.join(compliance.get('allowed_models_used', [])) or 'None'}")
        lines.append(
            f"- Forbidden models blocked: {', '.join(compliance.get('forbidden_models_blocked', [])) or 'None'}"
        )
        lines.append(
            f"- Unknown models used: {', '.join(compliance.get('unknown_models_used', [])) or 'None'}"
        )
        lines.append(
            f"- Unused allowlist patterns: {', '.join(compliance.get('unused_allowlist_patterns', [])) or 'None'}"
        )

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def _build_usage_summary(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    filtered = [event for event in events if event.get("event_type") != "trust_summary"]
    trace_ids: Set[str] = set()
    timestamps: List[datetime] = []
    daily_counts: Counter[str] = Counter()
    api_status_counts: Counter[str] = Counter()
    api_by_type: Counter[str] = Counter()
    model_counts: Counter[str] = Counter()
    sdk_inits = 0

    for event in filtered:
        trace_id = event.get("trace_id")
        if trace_id:
            trace_ids.add(trace_id)
        parsed = _parse_timestamp(event.get("timestamp"))
        if parsed is not None:
            timestamps.append(parsed)
            daily_counts[parsed.date().isoformat()] += 1
        event_type = event.get("event_type")
        if event_type == "sdk_init":
            sdk_inits += 1
        if event_type in ("llm_call", "tool_call", "agent_step"):
            api_by_type[event_type] += 1
            body = event.get("body") if isinstance(event.get("body"), dict) else {}
            status = body.get("status") if isinstance(body, dict) else None
            api_status_counts[status or "unknown"] += 1
            if event_type == "llm_call":
                model = _normalize_model(body.get("model") if isinstance(body, dict) else None)
                if model:
                    model_counts[model] += 1

    start = min(timestamps).astimezone(timezone.utc).isoformat() if timestamps else None
    end = max(timestamps).astimezone(timezone.utc).isoformat() if timestamps else None
    total_api_calls = sum(api_by_type.values())
    error_count = api_status_counts.get("error", 0)
    error_rate = (error_count / total_api_calls) if total_api_calls else None

    daily_activity = [
        {"date": date, "events": count}
        for date, count in sorted(daily_counts.items())
    ]

    top_models = [
        {"model": model, "count": count}
        for model, count in model_counts.most_common(5)
    ]

    return {
        "period": {"start": start, "end": end},
        "total_events": len(filtered),
        "unique_traces": len(trace_ids),
        "sdk_inits": sdk_inits,
        "api_calls": {
            "total": total_api_calls,
            "by_type": dict(api_by_type),
            "status_counts": dict(api_status_counts),
            "error_rate": error_rate,
        },
        "active_days": len(daily_counts),
        "daily_activity": daily_activity,
        "top_models": top_models,
    }


def _write_usage_markdown(path: str, summary: Dict[str, Any]) -> None:
    period = summary.get("period", {})
    start = period.get("start") or "N/A"
    end = period.get("end") or "N/A"
    api_calls = summary.get("api_calls", {})
    status_counts = api_calls.get("status_counts", {})
    error_rate = api_calls.get("error_rate")
    error_rate_display = f"{error_rate:.2%}" if isinstance(error_rate, float) else "N/A"

    lines = [
        "# Monora Usage Summary",
        f"**Period:** {start} to {end}",
        f"**Total Events:** {summary.get('total_events', 0)}",
        f"**Unique Traces:** {summary.get('unique_traces', 0)}",
        f"**SDK Inits:** {summary.get('sdk_inits', 0)}",
        "",
        "## API Calls",
        f"- Total: {api_calls.get('total', 0)}",
        f"- Error rate: {error_rate_display}",
    ]

    by_type = api_calls.get("by_type", {})
    if by_type:
        lines.append("- By type:")
        for event_type, count in by_type.items():
            lines.append(f"  - {event_type}: {count}")

    if status_counts:
        lines.append("- Status counts:")
        for status, count in status_counts.items():
            lines.append(f"  - {status}: {count}")

    lines.append("")
    lines.append("## Daily Activity")
    for entry in summary.get("daily_activity", []):
        lines.append(f"- {entry['date']}: {entry['events']} events")

    lines.append("")
    lines.append("## Top Models")
    top_models = summary.get("top_models", [])
    if top_models:
        for entry in top_models:
            lines.append(f"- {entry['model']}: {entry['count']} calls")
    else:
        lines.append("- None")

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


@click.group()
def cli() -> None:
    """Monora CLI."""


cli.add_command(init_command)
cli.add_command(validate_command)
cli.add_command(doctor_command)


@cli.command(name="retry-queue")
@click.option("--config", "config_path", default="monora.yml", show_default=True)
@click.option("--path", "queue_path", required=False, help="Override retry queue path")
@click.option("--json", "as_json", is_flag=True, help="Output JSON")
@click.option("--clear", "clear_queue", is_flag=True, help="Clear queued batches")
def retry_queue_command(
    config_path: str,
    queue_path: Optional[str],
    as_json: bool,
    clear_queue: bool,
) -> None:
    """Inspect or clear the HTTPS retry queue."""
    config = _load_config_safe(config_path) if not queue_path else {}
    paths, warnings = _resolve_retry_queue_paths(config, queue_path)
    queues = [_inspect_retry_queue(path, clear=clear_queue) for path in paths]
    errors: List[str] = []
    for queue in queues:
        errors.extend(queue.get("errors", []))

    results = {
        "queues": queues,
        "warnings": warnings,
        "errors": errors,
    }
    _emit_retry_queue_results(results, as_json=as_json)
    if errors:
        raise SystemExit(1)


@cli.command()
@click.option("--input", "input_path", required=True, help="Path to JSON-lines event log")
@click.option("--output", "output_path", required=True, help="Output file path")
@click.option("--config", "config_path", required=False, help="Path to config YAML/JSON")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "markdown"]),
    default="json",
)
@click.option(
    "--no-schema",
    is_flag=True,
    help="Skip event schema validation",
)
@click.option(
    "--no-verify",
    is_flag=True,
    help="Skip hash chain verification",
)
@click.option(
    "--no-signature-verify",
    is_flag=True,
    help="Skip event signature verification",
)
def report(
    input_path: str,
    output_path: str,
    output_format: str,
    config_path: Optional[str],
    no_schema: bool,
    no_verify: bool,
    no_signature_verify: bool,
) -> None:
    """Generate a compliance report from JSON-lines logs."""
    events = _load_jsonl(input_path)
    if not no_schema:
        _validate_events_schema(events)
    config = _load_config_safe(config_path)
    if not no_verify:
        _verify_hash_chain(events, config)
    if not no_signature_verify:
        _verify_signatures(events, config)
    policies = config.get("policies") if isinstance(config, dict) else None
    report_data = _build_report(events, policies=policies)
    if output_format == "json":
        _write_json(output_path, report_data)
    else:
        _write_markdown(output_path, report_data)


@cli.command("usage-report")
@click.option("--input", "input_path", required=True, help="Path to JSON-lines event log")
@click.option("--output", "output_path", required=True, help="Output file path")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "markdown"]),
    default="json",
)
@click.option(
    "--no-schema",
    is_flag=True,
    help="Skip event schema validation",
)
def usage_report(
    input_path: str, output_path: str, output_format: str, no_schema: bool
) -> None:
    """Generate a lightweight usage summary from JSON-lines logs."""
    events = _load_jsonl(input_path)
    if not no_schema:
        _validate_events_schema(events)
    summary = _build_usage_summary(events)
    if output_format == "json":
        _write_json(output_path, summary)
    else:
        _write_usage_markdown(output_path, summary)


@cli.command()
@click.option("--input", "input_path", required=True, help="Path to JSON-lines event log")
@click.option("--output", "output_path", required=True, help="Output file path")
@click.option("--config", "config_path", required=False, help="Path to config YAML/JSON")
@click.option(
    "--sign",
    "signing_type",
    type=click.Choice(["gpg"]),
    required=False,
    help="Create a signed attestation bundle",
)
@click.option("--gpg-key", "gpg_key", required=False, help="GPG key ID/email for signing")
@click.option("--gpg-home", "gpg_home", required=False, help="GPG home directory")
@click.option(
    "--bundle",
    "bundle_path",
    required=False,
    help="Output path for attestation bundle (defaults to <output>.bundle.json)",
)
@click.option(
    "--no-schema",
    is_flag=True,
    help="Skip event schema validation",
)
def security_review(
    input_path: str,
    output_path: str,
    config_path: Optional[str],
    signing_type: Optional[str],
    gpg_key: Optional[str],
    gpg_home: Optional[str],
    bundle_path: Optional[str],
    no_schema: bool,
) -> None:
    """Generate a security review report with attestations."""
    from monora.cli.security_report import generate_security_report
    from monora.attestation import (
        AttestationError,
        build_attestation_bundle,
        serialize_report,
        sign_report_gpg,
    )

    events = _load_jsonl(input_path)
    if not no_schema:
        _validate_events_schema(events)
    report = generate_security_report(events, config_path=config_path)

    report_bytes = serialize_report(report)
    with open(output_path, "wb") as f:
        f.write(report_bytes)

    bundle_output = None
    if signing_type:
        try:
            if signing_type == "gpg":
                signature = sign_report_gpg(
                    report_bytes, key_id=gpg_key, gpg_home=gpg_home
                )
            else:
                raise AttestationError(f"Unsupported signing type: {signing_type}")
        except AttestationError as exc:
            raise click.ClickException(f"Signing failed: {exc}") from exc

        bundle = build_attestation_bundle(report, report_bytes, signature)
        bundle_output = bundle_path or f"{output_path}.bundle.json"
        with open(bundle_output, "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=2)

    click.echo(f"Security review report generated: {output_path}")
    if bundle_output:
        click.echo(f"Attestation bundle generated: {bundle_output}")


@cli.command("trust-package")
@click.option("--input", "input_path", required=True, help="Path to JSON-lines event log")
@click.option("--trace-id", "trace_id", required=True, help="Trace ID to export")
@click.option("--output", "output_path", required=True, help="Output file path")
@click.option("--config", "config_path", required=False, help="Path to config YAML/JSON")
@click.option(
    "--sign",
    "signing_type",
    type=click.Choice(["gpg"]),
    required=False,
    help="Create a signed trust package",
)
@click.option("--gpg-key", "gpg_key", required=False, help="GPG key ID/email for signing")
@click.option("--gpg-home", "gpg_home", required=False, help="GPG home directory")
@click.option(
    "--no-schema",
    is_flag=True,
    help="Skip event schema validation",
)
@click.option(
    "--no-verify",
    is_flag=True,
    help="Skip hash chain verification",
)
@click.option(
    "--no-signature-verify",
    is_flag=True,
    help="Skip event signature verification",
)
def trust_package(
    input_path: str,
    trace_id: str,
    output_path: str,
    config_path: Optional[str],
    signing_type: Optional[str],
    gpg_key: Optional[str],
    gpg_home: Optional[str],
    no_schema: bool,
    no_verify: bool,
    no_signature_verify: bool,
) -> None:
    """Generate a vendor trust package for a specific trace."""
    from monora.trust_package import export_trust_package

    events = _load_jsonl(input_path)
    if not no_schema:
        _validate_events_schema(events)
    config = _load_config_safe(config_path)
    if not no_verify:
        _verify_hash_chain(events, config)
    if not no_signature_verify:
        _verify_signatures(events, config)
    if signing_type and signing_type != "gpg":
        raise click.ClickException(f"Unsupported signing type: {signing_type}")

    export_trust_package(
        trace_id=trace_id,
        events=events,
        config_dict=config,
        sign=bool(signing_type),
        gpg_key=gpg_key,
        gpg_home=gpg_home,
        output_path=output_path,
    )
    click.echo(f"Trust package generated: {output_path}")


@cli.command("ai-act-report")
@click.option("--input", "input_path", required=True, help="Path to JSON-lines event log")
@click.option("--output", "output_path", required=True, help="Output file path")
@click.option("--config", "config_path", required=False, help="Path to config YAML/JSON")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "markdown"]),
    default="json",
)
@click.option(
    "--no-schema",
    is_flag=True,
    help="Skip event schema validation",
)
def ai_act_report(
    input_path: str,
    output_path: str,
    output_format: str,
    config_path: Optional[str],
    no_schema: bool,
) -> None:
    """Generate EU AI Act transparency report.

    Creates a transparency report compliant with the EU AI Act (2024/1689),
    including risk classification, model inventory, and compliance metrics.
    """
    from monora.ai_act_report import build_ai_act_report, write_ai_act_report

    events = _load_jsonl(input_path)
    if not no_schema:
        _validate_events_schema(events)
    config = _load_config_safe(config_path)
    report = build_ai_act_report(events, config)
    write_ai_act_report(report, output_path, output_format)
    click.echo(f"AI Act transparency report generated: {output_path}")


@cli.command()
@click.option("--input", "input_path", required=True, help="Path to JSON-lines event log")
@click.option("--config", "config_path", required=False, help="Path to config YAML/JSON")
@click.option("--no-schema", is_flag=True, help="Skip event schema validation")
@click.option("--no-verify", is_flag=True, help="Skip hash chain verification")
@click.option("--no-signature-verify", is_flag=True, help="Skip event signature verification")
@click.option("--no-sequence", is_flag=True, help="Skip event sequence gap checks")
@click.option("--pretty", is_flag=True, help="Pretty-print JSON output")
def verify(
    input_path: str,
    config_path: Optional[str],
    no_schema: bool,
    no_verify: bool,
    no_signature_verify: bool,
    no_sequence: bool,
    pretty: bool,
) -> None:
    """Verify event log integrity and schema compliance."""
    events = _load_jsonl(input_path)
    config = _load_config_safe(config_path)

    warnings: List[str] = []
    checks: Dict[str, Any] = {}

    if no_schema:
        checks["schema"] = {
            "status": "skipped",
            "reason": "disabled",
            "errors": [],
            "warnings": ["schema check disabled"],
        }
    else:
        schema_errors = _collect_schema_errors(events)
        checks["schema"] = {
            "status": "verified" if not schema_errors else "failed",
            "errors": schema_errors,
            "warnings": [],
        }

    if no_verify:
        checks["hash_chain"] = {
            "status": "skipped",
            "reason": "disabled",
            "scope": config.get("immutability", {}).get("scope", "per_trace"),
            "verified_traces": 0,
            "total_traces": 0,
            "errors": [],
            "warnings": ["hash chain check disabled"],
        }
    else:
        checks["hash_chain"] = _check_hash_chain(events, config)

    if no_signature_verify:
        checks["signatures"] = {
            "status": "skipped",
            "reason": "disabled",
            "verified_events": 0,
            "total_signed_events": 0,
            "errors": [],
            "warnings": ["signature check disabled"],
        }
    else:
        checks["signatures"] = _check_signatures(events, config)

    if no_sequence:
        checks["sequence"] = {
            "status": "skipped",
            "reason": "disabled",
            "gaps": [],
            "errors": [],
            "warnings": ["sequence check disabled"],
        }
    else:
        checks["sequence"] = _check_sequence_gaps(events)

    for check in checks.values():
        warnings.extend(check.get("warnings", []))

    errors = []
    for check in checks.values():
        errors.extend(check.get("errors", []))

    ok = all(
        check.get("status") == "verified"
        or (check.get("status") == "skipped" and check.get("reason") == "disabled")
        for check in checks.values()
    )

    summary = {
        "total_events": len(events),
        "traces": len({event.get("trace_id") for event in events if event.get("trace_id")}),
        "signed_events": len([event for event in events if event.get("event_signature")]),
        "trust_summary_events": len(
            [event for event in events if event.get("event_type") == "trust_summary"]
        ),
    }

    result = {
        "ok": ok,
        "summary": summary,
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
    }

    output = json.dumps(result, indent=2 if pretty else None)
    click.echo(output)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    cli()


def _matches_any(
    patterns: List[Tuple[str, Any]],
    model: str,
    used_patterns: Optional[set],
) -> bool:
    for raw, pattern in patterns:
        if pattern.match(model):
            if used_patterns is not None:
                used_patterns.add(raw)
            return True
    return False
