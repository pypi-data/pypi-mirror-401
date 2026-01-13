# -*- coding: utf-8 -*-
"""
Katana Meter

Deterministic LUFS & ΔE audio analysis engine.

Public surface:
- Stable API
- CLI & GUI friendly
- UI / backend agnostic

2026 Katana Project
"""

from .api import (
    # Analysis
    analyze_file,
    analyze_samples,
    AnalysisResult,
    DEFAULT_TARGET_LUFS,

    # Convenience helpers
    analyze,
    analyze_raw,

    # Mastering (present in core, optional to use)
    master,
    master_raw,
)

__all__ = [
    # analysis
    "analyze_file",
    "analyze_samples",
    "AnalysisResult",
    "DEFAULT_TARGET_LUFS",

    # helpers
    "analyze",
    "analyze_raw",

    # mastering
    "master",
    "master_raw",
]
