# -*- coding: utf-8 -*-
"""
Katana Meter – Public API

Stable, import-friendly public interface for:
- Scripts
- Plugins
- AI / DSP pipelines
- Desktop / backend tools (without framework dependency)

The internal core engine may evolve,
but this API MUST remain backward-compatible.
"""

from typing import Dict, List, Any, Tuple

from .core import (
    # Analysis
    analyze_file,
    analyze_samples,
    AnalysisResult,
    DEFAULT_TARGET_LUFS,

    # Mastering
    master_file,
    master_audio_samples,
)

__all__ = [
    # analysis
    "analyze_file",
    "analyze_samples",
    "AnalysisResult",
    "DEFAULT_TARGET_LUFS",

    # mastering
    "master_file",
    "master_audio_samples",

    # helpers
    "analyze",
    "analyze_raw",
    "master",
    "master_raw",
]

# ------------------------------------------------------------------
# Analysis helpers (thin wrappers)
# ------------------------------------------------------------------

def analyze(
    path: str,
    target_lufs: float = DEFAULT_TARGET_LUFS
) -> Dict[str, Any]:
    """
    Convenience wrapper around analyze_file().

    Example:
        from katana_meter.api import analyze
        result = analyze("song.wav")
    """
    return analyze_file(path, target_lufs=target_lufs)


def analyze_raw(
    audio: List[List[float]],
    sr: int,
    target_lufs: float = DEFAULT_TARGET_LUFS
) -> AnalysisResult:
    """
    Analyze already-decoded audio samples.

    Example:
        result = analyze_raw(samples, sr)
    """
    return analyze_samples(audio, sr, target_lufs=target_lufs)

# ------------------------------------------------------------------
# Mastering helpers (thin wrappers)
# ------------------------------------------------------------------

def master(
    input_path: str,
    output_path: str,
    mode: str = "youtube",
) -> Dict[str, Any]:
    """
    File-based mastering helper.

    Modes:
        - youtube
        - spotify
        - apple
        - broadcast
        - ai_natural

    Example:
        from katana_meter.api import master
        meta = master("song.wav", "song_master.wav", mode="ai_natural")
    """
    return master_file(
        input_path=input_path,
        output_path=output_path,
        mode=mode,
    )


def master_raw(
    audio: List[List[float]],
    sr: int,
    mode: str = "youtube",
) -> Tuple[List[List[float]], Dict[str, Any]]:
    """
    Sample-level mastering helper.

    Useful when Katana Meter is embedded into:
    - DAW-style pipelines
    - AI mastering engines
    - Real-time or offline DSP graphs

    Returns:
        (mastered_audio_samples, metadata)

    Example:
        out, info = master_raw(samples, sr, mode="spotify")
    """
    return master_audio_samples(audio, sr, mode=mode)
