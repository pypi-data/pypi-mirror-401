"""Executive summary generator for compliance reports.

Generates a one-page Markdown summary for sales and executive review.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def calculate_compliance_score(
    report: Dict[str, Any],
    chain_status: str,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Calculate compliance score (0-100) based on governance controls.

    Scoring breakdown:
    - Base score: 100
    - Policy violations: -10 per violation (max -50)
    - Chain integrity: -30 if failed, -10 if disabled
    - Signing enabled: +10 bonus (if disabled: -5)
    - WAL enabled: +5 bonus (if disabled: -5)
    - Unknown models used: -5 per model (max -15)

    Returns:
        Dictionary with score and breakdown
    """
    score = 100
    breakdown: Dict[str, int] = {}

    # Policy violations
    violations = report.get("violations", [])
    violation_count = len(violations)
    violation_penalty = min(violation_count * 10, 50)
    if violation_penalty > 0:
        breakdown["policy_violations"] = -violation_penalty
        score -= violation_penalty

    # Chain integrity
    if chain_status == "failed":
        breakdown["chain_integrity_failed"] = -30
        score -= 30
    elif chain_status == "disabled":
        breakdown["chain_integrity_disabled"] = -10
        score -= 10
    else:
        breakdown["chain_integrity_verified"] = 0  # No bonus, just baseline

    # Signing
    signing = config.get("signing", {}) if isinstance(config, dict) else {}
    if signing.get("enabled"):
        breakdown["signing_enabled"] = 10
        score += 10
    else:
        breakdown["signing_disabled"] = -5
        score -= 5

    # WAL (crash resilience)
    wal = config.get("wal", {}) if isinstance(config, dict) else {}
    if wal.get("enabled"):
        breakdown["wal_enabled"] = 5
        score += 5
    else:
        breakdown["wal_disabled"] = -5
        score -= 5

    # Unknown models used
    compliance = report.get("model_compliance", {}) if isinstance(report, dict) else {}
    unknown_models = compliance.get("unknown_models_used", [])
    unknown_penalty = min(len(unknown_models) * 5, 15)
    if unknown_penalty > 0:
        breakdown["unknown_models"] = -unknown_penalty
        score -= unknown_penalty

    # Clamp score to 0-100
    score = max(0, min(100, score))

    # Determine grade
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    return {
        "score": score,
        "grade": grade,
        "breakdown": breakdown,
        "max_score": 100,
    }


def generate_executive_summary(
    report: Dict[str, Any],
    events: List[Dict[str, Any]],
    chain_status: str,
    config: Dict[str, Any],
    trace_id: Optional[str] = None,
) -> str:
    """Generate a one-page Markdown executive summary.

    Args:
        report: Compliance report from _build_report()
        events: List of events for this trace
        chain_status: Chain verification status
        config: Monora configuration
        trace_id: Optional trace identifier

    Returns:
        Markdown string containing the executive summary
    """
    # Calculate compliance score
    score_data = calculate_compliance_score(report, chain_status, config)
    score = score_data["score"]
    grade = score_data["grade"]

    # Extract key data from report
    model_usage = report.get("model_usage", {})
    violations = report.get("violations", [])
    model_compliance = report.get("model_compliance", {})
    total_events = report.get("total_events", len(events))

    # Get service info from config
    defaults = config.get("defaults", {}) if isinstance(config, dict) else {}
    service_name = defaults.get("service_name", "Unknown Service")
    environment = defaults.get("environment", "unknown")

    # Build summary sections
    lines: List[str] = []

    # Header
    lines.append("# AI Governance Executive Summary")
    lines.append("")
    lines.append(f"**Service:** {service_name}  ")
    lines.append(f"**Environment:** {environment}  ")
    lines.append(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ")
    if trace_id:
        lines.append(f"**Trace ID:** `{trace_id}`  ")
    lines.append("")

    # Compliance Score Box
    lines.append("---")
    lines.append("")
    lines.append("## Compliance Score")
    lines.append("")
    lines.append(f"### {score}/100 (Grade: {grade})")
    lines.append("")

    # Score interpretation
    if score >= 90:
        lines.append("> **Excellent** - All governance controls are properly configured and verified.")
    elif score >= 80:
        lines.append("> **Good** - Minor improvements recommended for full compliance.")
    elif score >= 70:
        lines.append("> **Acceptable** - Some governance gaps should be addressed.")
    elif score >= 60:
        lines.append("> **Needs Improvement** - Significant compliance issues detected.")
    else:
        lines.append("> **Critical** - Major compliance failures require immediate attention.")
    lines.append("")

    # Key Metrics
    lines.append("---")
    lines.append("")
    lines.append("## Key Metrics")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total AI Calls | {total_events} |")
    lines.append(f"| Models Used | {len(model_usage)} |")
    lines.append(f"| Policy Violations | {len(violations)} |")
    lines.append(f"| Chain Integrity | {chain_status.replace('_', ' ').title()} |")
    lines.append("")

    # Models Used
    lines.append("---")
    lines.append("")
    lines.append("## Models Used")
    lines.append("")
    if model_usage:
        lines.append("| Model | Calls | Provider |")
        lines.append("|-------|-------|----------|")
        for model_id, count in sorted(model_usage.items(), key=lambda x: -x[1]):
            provider = _infer_provider(model_id)
            lines.append(f"| {model_id} | {count} | {provider} |")
    else:
        lines.append("*No model usage recorded*")
    lines.append("")

    # Unknown models warning
    unknown_models = model_compliance.get("unknown_models_used", [])
    if unknown_models:
        lines.append("### Unregistered Models")
        lines.append("")
        lines.append("The following models are not in the approved registry:")
        lines.append("")
        for model in unknown_models:
            lines.append(f"- `{model}`")
        lines.append("")

    # Policy Violations
    lines.append("---")
    lines.append("")
    lines.append("## Policy Violations")
    lines.append("")
    if violations:
        lines.append(f"**{len(violations)} violation(s) detected:**")
        lines.append("")
        for i, violation in enumerate(violations[:10], 1):  # Limit to 10
            violation_type = violation.get("type", "unknown")
            model = violation.get("model", "unknown")
            reason = violation.get("reason", "No reason provided")
            lines.append(f"{i}. **{violation_type}** - Model: `{model}`")
            lines.append(f"   - {reason}")
        if len(violations) > 10:
            lines.append(f"   - *... and {len(violations) - 10} more violations*")
        lines.append("")
    else:
        lines.append("**No policy violations detected.**")
        lines.append("")

    # Governance Controls
    lines.append("---")
    lines.append("")
    lines.append("## Governance Controls")
    lines.append("")

    signing = config.get("signing", {}) if isinstance(config, dict) else {}
    wal = config.get("wal", {}) if isinstance(config, dict) else {}
    immutability = config.get("immutability", {}) if isinstance(config, dict) else {}
    ai_act = config.get("ai_act", {}) if isinstance(config, dict) else {}

    lines.append("| Control | Status |")
    lines.append("|---------|--------|")
    lines.append(f"| Event Signing | {'Enabled' if signing.get('enabled') else 'Disabled'} |")
    lines.append(f"| Write-Ahead Log | {'Enabled' if wal.get('enabled') else 'Disabled'} |")
    lines.append(f"| Hash Chain | {'Enabled' if immutability.get('enabled', True) else 'Disabled'} |")
    lines.append(f"| EU AI Act Compliance | {'Enabled' if ai_act.get('enabled') else 'Disabled'} |")
    lines.append("")

    # Data Classifications
    lines.append("---")
    lines.append("")
    lines.append("## Data Classifications")
    lines.append("")
    classifications = _extract_data_classifications(events)
    if classifications:
        lines.append("| Classification | Event Count |")
        lines.append("|----------------|-------------|")
        for classification, count in sorted(classifications.items(), key=lambda x: -x[1]):
            lines.append(f"| {classification} | {count} |")
    else:
        lines.append("*No data classification metadata recorded*")
    lines.append("")

    # Score Breakdown
    lines.append("---")
    lines.append("")
    lines.append("## Score Breakdown")
    lines.append("")
    breakdown = score_data.get("breakdown", {})
    if breakdown:
        lines.append("| Factor | Impact |")
        lines.append("|--------|--------|")
        for factor, impact in sorted(breakdown.items()):
            impact_str = f"+{impact}" if impact > 0 else str(impact)
            lines.append(f"| {factor.replace('_', ' ').title()} | {impact_str} |")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*Generated by Monora AI Governance SDK*")
    lines.append("")

    return "\n".join(lines)


def write_executive_summary(
    report: Dict[str, Any],
    events: List[Dict[str, Any]],
    chain_status: str,
    config: Dict[str, Any],
    output_path: Path,
    trace_id: Optional[str] = None,
) -> Optional[str]:
    """Write executive summary to a file.

    Args:
        report: Compliance report
        events: List of events
        chain_status: Chain verification status
        config: Monora configuration
        output_path: Path to write the summary
        trace_id: Optional trace identifier

    Returns:
        Path to written file, or None on error
    """
    try:
        summary = generate_executive_summary(
            report=report,
            events=events,
            chain_status=chain_status,
            config=config,
            trace_id=trace_id,
        )
        output_path.write_text(summary, encoding="utf-8")
        return str(output_path)
    except Exception:
        return None


def _infer_provider(model_id: str) -> str:
    """Infer provider from model ID."""
    model_lower = model_id.lower()
    if model_lower.startswith("gpt-") or model_lower.startswith("o1"):
        return "OpenAI"
    if model_lower.startswith("claude-"):
        return "Anthropic"
    if model_lower.startswith("deepseek"):
        return "DeepSeek"
    if model_lower.startswith("gemini"):
        return "Google"
    if model_lower.startswith("llama"):
        return "Meta"
    if model_lower.startswith("mistral"):
        return "Mistral"
    return "Unknown"


def _extract_data_classifications(events: List[Dict[str, Any]]) -> Dict[str, int]:
    """Extract data classification counts from events."""
    classifications: Dict[str, int] = {}
    for event in events:
        classification = event.get("data_classification")
        if classification:
            classifications[classification] = classifications.get(classification, 0) + 1
    return classifications
