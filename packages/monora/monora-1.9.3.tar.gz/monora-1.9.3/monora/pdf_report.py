"""PDF report generation for Monora compliance reports.

Generates professional, styled PDF reports from compliance data.
Requires optional dependency: pip install weasyprint
"""
from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from monora.logger import logger

# Optional WeasyPrint import
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    HTML = None
    CSS = None


class PDFGenerationError(Exception):
    """Raised when PDF generation fails."""
    pass


# CSS styles for the PDF report
PDF_STYLES = """
@page {
    size: A4;
    margin: 2cm;
    @top-center {
        content: "Monora Compliance Report";
        font-size: 10pt;
        color: #666;
    }
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 10pt;
        color: #666;
    }
}

body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

.header {
    text-align: center;
    border-bottom: 3px solid #2563eb;
    padding-bottom: 20px;
    margin-bottom: 30px;
}

.header h1 {
    color: #1e40af;
    font-size: 28pt;
    margin: 0;
}

.header .subtitle {
    color: #666;
    font-size: 12pt;
    margin-top: 10px;
}

.header .logo {
    font-size: 14pt;
    font-weight: bold;
    color: #2563eb;
    margin-bottom: 10px;
}

.summary-box {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border: 1px solid #93c5fd;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
}

.summary-item {
    text-align: center;
}

.summary-item .value {
    font-size: 24pt;
    font-weight: bold;
    color: #1e40af;
}

.summary-item .label {
    font-size: 10pt;
    color: #666;
    text-transform: uppercase;
}

h2 {
    color: #1e40af;
    border-bottom: 2px solid #dbeafe;
    padding-bottom: 8px;
    margin-top: 30px;
}

h3 {
    color: #3b82f6;
    margin-top: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 10pt;
}

th {
    background: #1e40af;
    color: white;
    padding: 12px 10px;
    text-align: left;
    font-weight: 600;
}

td {
    padding: 10px;
    border-bottom: 1px solid #e5e7eb;
}

tr:nth-child(even) {
    background: #f9fafb;
}

tr:hover {
    background: #eff6ff;
}

.status-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 9pt;
    font-weight: 600;
}

.status-success {
    background: #dcfce7;
    color: #166534;
}

.status-warning {
    background: #fef3c7;
    color: #92400e;
}

.status-error {
    background: #fee2e2;
    color: #991b1b;
}

.risk-minimal { background: #dcfce7; color: #166534; }
.risk-limited { background: #dbeafe; color: #1e40af; }
.risk-high { background: #fef3c7; color: #92400e; }
.risk-unacceptable { background: #fee2e2; color: #991b1b; }

.violation-list {
    background: #fef2f2;
    border-left: 4px solid #ef4444;
    padding: 15px;
    margin: 15px 0;
}

.violation-item {
    margin: 10px 0;
    padding: 10px;
    background: white;
    border-radius: 4px;
}

.footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #e5e7eb;
    text-align: center;
    font-size: 9pt;
    color: #666;
}

.metric-bar {
    height: 20px;
    background: #e5e7eb;
    border-radius: 10px;
    overflow: hidden;
    margin: 5px 0;
}

.metric-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6 0%, #1e40af 100%);
    border-radius: 10px;
}

.two-column {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 15px;
}

.card h4 {
    margin: 0 0 10px 0;
    color: #374151;
}
"""


def _generate_compliance_html(report: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> str:
    """Generate HTML for compliance report."""
    config = config or {}
    org_name = config.get("organization_name", "Organization")

    # Extract data
    total_events = report.get("total_events", 0)
    traces = report.get("traces", 0)
    date_range = report.get("date_range", {})
    by_event_type = report.get("by_event_type", {})
    by_model = report.get("by_model", {})
    violations = report.get("violations", [])
    token_usage = report.get("token_usage", {})
    model_compliance = report.get("model_compliance", {})

    # Format dates
    start_date = date_range.get("start", "N/A")
    end_date = date_range.get("end", "N/A")
    if start_date != "N/A":
        try:
            start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
        except (ValueError, AttributeError):
            pass
    if end_date != "N/A":
        try:
            end_date = datetime.fromisoformat(end_date.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
        except (ValueError, AttributeError):
            pass

    # Build event type rows
    event_type_rows = ""
    for event_type, count in sorted(by_event_type.items(), key=lambda x: -x[1]):
        pct = (count / total_events * 100) if total_events > 0 else 0
        event_type_rows += f"""
        <tr>
            <td>{event_type}</td>
            <td>{count:,}</td>
            <td>
                <div class="metric-bar">
                    <div class="metric-bar-fill" style="width: {pct:.1f}%"></div>
                </div>
            </td>
            <td>{pct:.1f}%</td>
        </tr>
        """

    # Build model usage rows
    model_rows = ""
    for model, count in sorted(by_model.items(), key=lambda x: -x[1]):
        model_rows += f"""
        <tr>
            <td>{model}</td>
            <td>{count:,}</td>
        </tr>
        """

    # Build violations section
    violations_html = ""
    if violations:
        violations_html = '<div class="violation-list"><h4>Policy Violations</h4>'
        for v in violations[:20]:  # Limit to 20
            violations_html += f"""
            <div class="violation-item">
                <strong>{v.get('timestamp', 'N/A')}</strong> -
                Model: <code>{v.get('model', 'N/A')}</code> |
                Policy: {v.get('policy', 'N/A')} |
                {v.get('message', '')}
            </div>
            """
        if len(violations) > 20:
            violations_html += f"<p><em>...and {len(violations) - 20} more violations</em></p>"
        violations_html += "</div>"

    # Token usage section
    total_tokens = token_usage.get("total_tokens", 0)
    prompt_tokens = token_usage.get("total_prompt_tokens", 0)
    completion_tokens = token_usage.get("total_completion_tokens", 0)

    # Model compliance section
    allowed_models = model_compliance.get("allowed_models_used", [])
    forbidden_blocked = model_compliance.get("forbidden_models_blocked", [])
    unknown_models = model_compliance.get("unknown_models_used", [])

    compliance_status = "success" if not violations and not forbidden_blocked else "warning" if len(violations) < 5 else "error"
    compliance_label = "Compliant" if compliance_status == "success" else "Minor Issues" if compliance_status == "warning" else "Non-Compliant"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Monora Compliance Report</title>
    </head>
    <body>
        <div class="header">
            <div class="logo">◆ MONORA</div>
            <h1>Compliance Report</h1>
            <div class="subtitle">{org_name} | {start_date} to {end_date}</div>
        </div>

        <div class="summary-box">
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="value">{total_events:,}</div>
                    <div class="label">Total Events</div>
                </div>
                <div class="summary-item">
                    <div class="value">{traces:,}</div>
                    <div class="label">Traces</div>
                </div>
                <div class="summary-item">
                    <div class="value">{len(by_model):,}</div>
                    <div class="label">Models Used</div>
                </div>
                <div class="summary-item">
                    <div class="value">{len(violations):,}</div>
                    <div class="label">Violations</div>
                </div>
                <div class="summary-item">
                    <div class="value">{total_tokens:,}</div>
                    <div class="label">Total Tokens</div>
                </div>
                <div class="summary-item">
                    <span class="status-badge status-{compliance_status}">{compliance_label}</span>
                    <div class="label">Status</div>
                </div>
            </div>
        </div>

        {violations_html}

        <h2>Event Distribution</h2>
        <table>
            <thead>
                <tr>
                    <th>Event Type</th>
                    <th>Count</th>
                    <th>Distribution</th>
                    <th>Percentage</th>
                </tr>
            </thead>
            <tbody>
                {event_type_rows}
            </tbody>
        </table>

        <div class="two-column">
            <div>
                <h2>Model Usage</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Calls</th>
                        </tr>
                    </thead>
                    <tbody>
                        {model_rows if model_rows else '<tr><td colspan="2">No model usage recorded</td></tr>'}
                    </tbody>
                </table>
            </div>
            <div>
                <h2>Token Usage</h2>
                <div class="card">
                    <h4>Prompt Tokens</h4>
                    <div class="value">{prompt_tokens:,}</div>
                </div>
                <div class="card" style="margin-top: 10px;">
                    <h4>Completion Tokens</h4>
                    <div class="value">{completion_tokens:,}</div>
                </div>
            </div>
        </div>

        <h2>Model Compliance</h2>
        <div class="two-column">
            <div class="card">
                <h4>Allowed Models Used</h4>
                <p>{', '.join(allowed_models) if allowed_models else 'None'}</p>
            </div>
            <div class="card">
                <h4>Unknown Models</h4>
                <p>{', '.join(unknown_models) if unknown_models else 'None'}</p>
            </div>
        </div>

        <div class="footer">
            <p>Generated by Monora SDK | {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p>This report provides an audit trail for AI system governance and compliance.</p>
        </div>
    </body>
    </html>
    """
    return html


def _generate_ai_act_html(report: Dict[str, Any]) -> str:
    """Generate HTML for AI Act transparency report."""
    org_name = report.get("organizationName", "Organization")
    generated_at = report.get("generatedAt", datetime.now().isoformat())
    period_start = report.get("reportingPeriodStart", "N/A")
    period_end = report.get("reportingPeriodEnd", "N/A")

    total_interactions = report.get("totalAiInteractions", 0)
    unique_models = report.get("uniqueModelsUsed", 0)
    unique_traces = report.get("uniqueTraces", 0)
    violations_count = report.get("policyViolationsCount", 0)

    risk_summary = report.get("riskCategorySummary", {})
    models_used = report.get("modelsUsed", [])
    high_risk = report.get("highRiskModels", [])
    unacceptable_risk = report.get("unacceptableRiskModels", [])
    data_classifications = report.get("dataClassificationsUsed", {})
    violations_by_model = report.get("policyViolationsByModel", {})

    # Risk category rows
    risk_rows = ""
    for category in ["minimal", "limited", "high", "unacceptable"]:
        count = risk_summary.get(category, 0)
        risk_rows += f"""
        <tr>
            <td><span class="status-badge risk-{category}">{category.upper()}</span></td>
            <td>{count:,}</td>
        </tr>
        """

    # Models table rows
    model_rows = ""
    for model in models_used:
        risk_cat = model.get("riskCategory", "limited")
        caps = ", ".join(model.get("capabilities", [])[:3]) or "N/A"
        model_rows += f"""
        <tr>
            <td>{model.get('model', 'N/A')}</td>
            <td>{model.get('provider', 'N/A')}</td>
            <td><span class="status-badge risk-{risk_cat}">{risk_cat.upper()}</span></td>
            <td>{model.get('callCount', 0):,}</td>
            <td>{caps}</td>
        </tr>
        """

    # Data classification rows
    classification_rows = ""
    for classification, count in sorted(data_classifications.items(), key=lambda x: -x[1]):
        classification_rows += f"""
        <tr>
            <td>{classification}</td>
            <td>{count:,}</td>
        </tr>
        """

    # Warning section for high/unacceptable risk
    warnings_html = ""
    if high_risk or unacceptable_risk:
        warnings_html = '<div class="violation-list"><h4>⚠️ Risk Warnings</h4>'
        if unacceptable_risk:
            warnings_html += f'<p class="status-badge status-error">UNACCEPTABLE RISK: {", ".join(unacceptable_risk)}</p>'
        if high_risk:
            warnings_html += f'<p class="status-badge status-warning">HIGH RISK: {", ".join(high_risk)}</p>'
        warnings_html += '</div>'

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>EU AI Act Transparency Report</title>
    </head>
    <body>
        <div class="header">
            <div class="logo">◆ MONORA</div>
            <h1>EU AI Act Transparency Report</h1>
            <div class="subtitle">{org_name} | Regulation (EU) 2024/1689</div>
        </div>

        <div class="summary-box">
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="value">{total_interactions:,}</div>
                    <div class="label">AI Interactions</div>
                </div>
                <div class="summary-item">
                    <div class="value">{unique_models:,}</div>
                    <div class="label">Models Used</div>
                </div>
                <div class="summary-item">
                    <div class="value">{unique_traces:,}</div>
                    <div class="label">Unique Traces</div>
                </div>
                <div class="summary-item">
                    <div class="value">{violations_count:,}</div>
                    <div class="label">Violations</div>
                </div>
            </div>
        </div>

        {warnings_html}

        <h2>Risk Category Summary</h2>
        <p>Classification per EU AI Act Article 6 risk categorization:</p>
        <table>
            <thead>
                <tr>
                    <th>Risk Category</th>
                    <th>Model Count</th>
                </tr>
            </thead>
            <tbody>
                {risk_rows}
            </tbody>
        </table>

        <h2>Model Inventory</h2>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Provider</th>
                    <th>Risk Category</th>
                    <th>Call Count</th>
                    <th>Capabilities</th>
                </tr>
            </thead>
            <tbody>
                {model_rows if model_rows else '<tr><td colspan="5">No models used</td></tr>'}
            </tbody>
        </table>

        <h2>Data Classifications</h2>
        <table>
            <thead>
                <tr>
                    <th>Classification</th>
                    <th>Event Count</th>
                </tr>
            </thead>
            <tbody>
                {classification_rows if classification_rows else '<tr><td colspan="2">No data classifications recorded</td></tr>'}
            </tbody>
        </table>

        <div class="footer">
            <p>Generated by Monora SDK | {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p>Report Period: {period_start} to {period_end}</p>
            <p>This transparency report fulfills obligations under EU AI Act (Regulation 2024/1689).</p>
        </div>
    </body>
    </html>
    """
    return html


def generate_compliance_pdf(
    report: Dict[str, Any],
    output_path: str,
    config: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate a PDF compliance report.

    Args:
        report: Compliance report data dictionary.
        output_path: Path to write PDF file.
        config: Optional configuration with organization_name, etc.

    Returns:
        Path to generated PDF file.

    Raises:
        PDFGenerationError: If PDF generation fails.
    """
    if not WEASYPRINT_AVAILABLE:
        raise PDFGenerationError(
            "WeasyPrint is required for PDF generation. "
            "Install with: pip install weasyprint"
        )

    try:
        html_content = _generate_compliance_html(report, config)
        html_doc = HTML(string=html_content)
        css = CSS(string=PDF_STYLES)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        html_doc.write_pdf(str(output_path), stylesheets=[css])
        logger.info("Generated PDF compliance report: %s", output_path)
        return str(output_path)

    except Exception as exc:
        raise PDFGenerationError(f"Failed to generate PDF: {exc}") from exc


def generate_ai_act_pdf(
    report: Dict[str, Any],
    output_path: str,
) -> str:
    """Generate an EU AI Act transparency PDF report.

    Args:
        report: AI Act report data dictionary.
        output_path: Path to write PDF file.

    Returns:
        Path to generated PDF file.

    Raises:
        PDFGenerationError: If PDF generation fails.
    """
    if not WEASYPRINT_AVAILABLE:
        raise PDFGenerationError(
            "WeasyPrint is required for PDF generation. "
            "Install with: pip install weasyprint"
        )

    try:
        html_content = _generate_ai_act_html(report)
        html_doc = HTML(string=html_content)
        css = CSS(string=PDF_STYLES)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        html_doc.write_pdf(str(output_path), stylesheets=[css])
        logger.info("Generated PDF AI Act report: %s", output_path)
        return str(output_path)

    except Exception as exc:
        raise PDFGenerationError(f"Failed to generate AI Act PDF: {exc}") from exc


def compute_pdf_sha256(pdf_path: str) -> str:
    """Compute SHA256 hash of a PDF file.

    Args:
        pdf_path: Path to PDF file.

    Returns:
        SHA256 hash as hex string with 'sha256:' prefix.
    """
    sha256 = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return f"sha256:{sha256.hexdigest()}"


__all__ = [
    "WEASYPRINT_AVAILABLE",
    "PDFGenerationError",
    "generate_compliance_pdf",
    "generate_ai_act_pdf",
    "compute_pdf_sha256",
]
