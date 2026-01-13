"""Report rendering (text and JSON)."""

from __future__ import annotations

from typo_shield.report.render_json import (
    parse_json_report,
    render_json_report,
    render_json_summary,
    validate_json_report,
)
from typo_shield.report.render_text import render_result_line, render_text_report

__all__ = [
    "render_text_report",
    "render_result_line",
    "render_json_report",
    "render_json_summary",
    "parse_json_report",
    "validate_json_report",
]

