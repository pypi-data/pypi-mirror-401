# -*- coding: utf-8 -*-
# Katana Meter
# Copyright (C) 2026 Katana Project
# Licensed under the GNU General Public License v3.0
#
# Deterministic audio analysis + mastering core:
# - Integrated LUFS (gated, BS.1770-inspired)
# - Sample Peak (dBFS approx)
# - Gain to target LUFS
# - ΔE entropy-change metric (0..1 scaled)
#
# No external Python dependencies.
# WAV native I/O. MP3/FLAC/AAC/OGG decode/encode require optional ffmpeg.

from __future__ import annotations

import os
import math
import wave
import struct
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

# ------------------------------------------------------------------
# Settings
# ------------------------------------------------------------------

DEFAULT_TARGET_LUFS = -14.0

DEFAULT_DECODE_SR = 48000
DEFAULT_DECODE_CH = 2

SILENCE_EPS = 1e-9
MIN_DURATION_FOR_LUFS_SEC = 0.40  # 400ms

# Mastering defaults (safety)
DEFAULT_TRUE_PEAK_LIMIT_DB = -1.0  # sample-peak approx clamp
DEFAULT_AI_NATURAL_TARGET_LUFS = -14.0

# ------------------------------------------------------------------
# Utils
# ------------------------------------------------------------------

def has_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def guess_format(path: str) -> str:
    _, ext = os.path.splitext(path)
    return (ext.lower().lstrip(".") or "unknown").strip()


def safe_remove(path: str) -> None:
    try:
        os.remove(path)
    except Exception:
        pass


def db20(x: float) -> float:
    return 20.0 * math.log10(max(x, 1e-12))


def db10(x: float) -> float:
    return 10.0 * math.log10(max(x, 1e-18))


def lin_from_db(db: float) -> float:
    return 10.0 ** (db / 20.0)

# ------------------------------------------------------------------
# Decode / Read / Write
# ------------------------------------------------------------------

def decode_to_wav_if_needed(
    path: str,
    target_sr: int = DEFAULT_DECODE_SR,
    target_ch: int = DEFAULT_DECODE_CH,
) -> Tuple[str, Optional[str], Dict[str, Any]]:
    """
    Returns (wav_path, tmp_path_or_none, decode_info).
    WAV input -> returns original path, tmp=None.
    Non-WAV -> uses ffmpeg to decode to temp WAV.
    """
    src_format = guess_format(path)

    if path.lower().endswith(".wav"):
        return path, None, {
            "decoder": "wav-native",
            "src_format": src_format,
            "dst_sr": None,
            "dst_ch": None,
        }

    if not has_ffmpeg():
        raise RuntimeError("Non-WAV input requires ffmpeg in PATH")

    tmp = "_katana_tmp_decode.wav"

    cmd = [
        "ffmpeg", "-y",
        "-i", path,
        "-ac", str(target_ch),
        "-ar", str(target_sr),
        "-f", "wav",
        tmp,
    ]

    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        err = (r.stderr or b"").decode(errors="ignore")
        raise RuntimeError(f"ffmpeg decode failed: {err[-400:]}")

    return tmp, tmp, {
        "decoder": "ffmpeg",
        "src_format": src_format,
        "dst_sr": target_sr,
        "dst_ch": target_ch,
    }


def read_wav_float(path: str) -> Tuple[List[List[float]], int]:
    """
    Reads PCM WAV into float channels in [-1, 1).
    Supports 16-bit, 24-bit, 32-bit PCM.
    """
    with wave.open(path, "rb") as wf:
        ch = wf.getnchannels()
        sr = wf.getframerate()
        sw = wf.getsampwidth()
        raw = wf.readframes(wf.getnframes())

    audio: List[List[float]] = [[] for _ in range(ch)]

    if sw == 2:
        data = struct.unpack("<" + "h" * (len(raw) // 2), raw)
        for i, s in enumerate(data):
            audio[i % ch].append(s / 32768.0)

    elif sw == 3:
        for i in range(0, len(raw), 3):
            v = raw[i] | (raw[i + 1] << 8) | (raw[i + 2] << 16)
            if v & 0x800000:
                v -= 0x1000000
            audio[(i // 3) % ch].append(v / 8388608.0)

    elif sw == 4:
        data = struct.unpack("<" + "i" * (len(raw) // 4), raw)
        for i, s in enumerate(data):
            audio[i % ch].append(s / 2147483648.0)

    else:
        raise RuntimeError("Unsupported WAV format")

    return audio, sr


def write_wav_16bit(path: str, audio: List[List[float]], sr: int) -> None:
    """
    Writes float audio [-1,1] to 16-bit PCM WAV.
    Interleaves channels.
    """
    if not audio or not audio[0]:
        raise ValueError("Empty audio")

    ch = len(audio)
    n = min(len(c) for c in audio)

    frames: List[int] = []
    for i in range(n):
        for c in range(ch):
            v = float(audio[c][i])
            v = max(-1.0, min(1.0, v))
            s = int(round(v * 32767.0))
            frames.append(s)

    raw = struct.pack("<" + "h" * len(frames), *frames)

    with wave.open(path, "wb") as wf:
        wf.setnchannels(ch)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(raw)


def export_mastered_like_input(
    input_path: str,
    output_path: str,
    mastered_audio: List[List[float]],
    sr: int,
) -> Dict[str, Any]:
    """
    Keeps output format based on output_path extension.
    - .wav : writes 16-bit PCM WAV
    - other: writes temp WAV then ffmpeg encodes to output ext (requires ffmpeg)
    """
    out_ext = guess_format(output_path)

    if out_ext == "wav":
        write_wav_16bit(output_path, mastered_audio, sr)
        return {"encoder": "wav-16bit", "format": "wav"}

    if not has_ffmpeg():
        raise RuntimeError("Non-WAV export requires ffmpeg in PATH")

    tmp_wav = "_katana_tmp_export.wav"
    try:
        write_wav_16bit(tmp_wav, mastered_audio, sr)

        cmd = ["ffmpeg", "-y", "-i", tmp_wav, output_path]
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if r.returncode != 0:
            err = (r.stderr or b"").decode(errors="ignore")
            raise RuntimeError(f"ffmpeg encode failed: {err[-400:]}")

        return {"encoder": "ffmpeg", "format": out_ext}
    finally:
        safe_remove(tmp_wav)

# ------------------------------------------------------------------
# Labels / Warnings (analysis)
# ------------------------------------------------------------------

def label_loudness(lufs: float) -> str:
    if lufs > -11.0:
        return "very loud"
    if lufs > -14.0:
        return "loud"
    if lufs > -18.0:
        return "balanced"
    return "dynamic"


def label_peak_risk(peak_db: float) -> str:
    if peak_db >= 0.0:
        return "clipping risk"
    if peak_db >= -1.0:
        return "encode risk"
    return "safe"


def label_gain_action(gain_db: float) -> str:
    if gain_db > 2.0:
        return "needs lift"
    if gain_db < -2.0:
        return "needs trim"
    return "near target"


def build_warnings(lufs: float, peak_db: float) -> List[str]:
    warns: List[str] = []
    if peak_db >= 0.0:
        warns.append("Peak >= 0 dBFS: clipping / encode overflow risk")
    elif peak_db >= -1.0:
        warns.append("Peak near -1 dBFS: encode overflow possible")
    if lufs > -11.0:
        warns.append("Very loud content: platforms will normalize aggressively")
    return warns

# ------------------------------------------------------------------
# DSP Metrics (analysis) — DO NOT BREAK
# ------------------------------------------------------------------

def dc_remove(ch: List[float]) -> List[float]:
    if not ch:
        return ch
    m = sum(ch) / len(ch)
    return [v - m for v in ch]


def is_silent(audio: List[List[float]]) -> bool:
    for ch in audio:
        for v in ch[:50000]:
            if abs(v) > SILENCE_EPS:
                return False
    return True


def sample_peak_db(audio: List[List[float]]) -> float:
    peak = 0.0
    for ch in audio:
        for v in ch:
            av = abs(v)
            if av > peak:
                peak = av
    return db20(peak)


def integrated_lufs(audio: List[List[float]], sr: int) -> float:
    """
    Simple gated integrated loudness (BS.1770-inspired),
    block 400ms / step 100ms, absolute gate -70 LUFS, relative -10 LU.
    """
    block = int(sr * 0.400)
    step = int(sr * 0.100)

    if len(audio[0]) < block:
        raise RuntimeError("Audio too short for LUFS")

    def ms_to_lufs(ms: float) -> float:
        return -0.691 + db10(ms)

    blocks: List[float] = []
    for i in range(0, len(audio[0]) - block + 1, step):
        ms = 0.0
        for ch in audio:
            seg = ch[i:i + block]
            ms += sum(v * v for v in seg) / block
        blocks.append(ms / len(audio))

    gated = [b for b in blocks if ms_to_lufs(b) > -70]
    mean = sum(gated) / len(gated)
    gate = ms_to_lufs(mean) - 10
    final = [b for b in gated if ms_to_lufs(b) > gate]

    return ms_to_lufs(sum(final) / len(final))


def delta_e(audio: List[List[float]], sr: int) -> float:
    mono = audio[0] if len(audio) == 1 else [
        (audio[0][i] + audio[1][i]) * 0.5 for i in range(len(audio[0]))
    ]

    size = max(int(sr * 0.100), 16)
    diffs: List[float] = []
    prev: Optional[float] = None

    for i in range(0, len(mono) - size, size):
        blk = mono[i:i + size]
        mags = [abs(v) for v in blk]
        mx = max(mags)

        if mx < 1e-12:
            h = 0.0
        else:
            hist = [0] * 32
            for m in mags:
                idx = int((m / mx) * 31)
                if idx < 0:
                    idx = 0
                elif idx > 31:
                    idx = 31
                hist[idx] += 1
            h = 0.0
            for c in hist:
                if c:
                    p = c / len(mags)
                    h -= p * math.log(p, 2)

        if prev is not None:
            diffs.append(abs(h - prev))
        prev = h

    return min(sum(diffs) / len(diffs), 1.0) if diffs else 0.0

# ------------------------------------------------------------------
# Public API (analysis)
# ------------------------------------------------------------------

@dataclass
class AnalysisResult:
    lufs: float
    peak_dbtp_approx: float
    gain_to_target_db: float
    delta_e: float
    target_lufs: float
    labels: Dict[str, str]
    warnings: List[str]
    info: Dict[str, Any]


def analyze_samples(
    audio: List[List[float]],
    sr: int,
    target_lufs: float = DEFAULT_TARGET_LUFS
) -> AnalysisResult:
    if not audio or not audio[0]:
        raise ValueError("Empty audio")

    if len(audio) == 1:
        audio = [audio[0], audio[0][:]]

    if is_silent(audio):
        raise ValueError("Audio is silent")

    audio = [dc_remove(ch) for ch in audio]

    if len(audio[0]) < int(sr * MIN_DURATION_FOR_LUFS_SEC):
        raise ValueError("Audio too short")

    lufs = integrated_lufs(audio, sr)
    peak = sample_peak_db(audio)
    gain = target_lufs - lufs
    de = delta_e(audio, sr)

    return AnalysisResult(
        lufs=lufs,
        peak_dbtp_approx=peak,
        gain_to_target_db=gain,
        delta_e=de,
        target_lufs=target_lufs,
        labels={
            "loudness": label_loudness(lufs),
            "peak_risk": label_peak_risk(peak),
            "gain_action": label_gain_action(gain),
        },
        warnings=build_warnings(lufs, peak),
        info={
            "sr": sr,
            "channels": len(audio),
            "peak_kind": "sample-peak (approx)",
            "lufs_kind": "integrated gated",
            "delta_e_kind": "entropy-change",
        },
    )


def analyze_file(path: str, target_lufs: float = DEFAULT_TARGET_LUFS) -> Dict[str, Any]:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    tmp = None
    try:
        wav, tmp, decode_info = decode_to_wav_if_needed(path)
        audio, sr = read_wav_float(wav)
        res = analyze_samples(audio, sr, target_lufs)

        return {
            "lufs": round(res.lufs, 3),
            "peak_dbtp_approx": round(res.peak_dbtp_approx, 3),
            "gain_to_target_db": round(res.gain_to_target_db, 3),
            "delta_e": round(res.delta_e, 5),
            "target_lufs": target_lufs,
            "labels": res.labels,
            "warnings": res.warnings,
            "info": {**res.info, **decode_info},
        }
    finally:
        if tmp:
            safe_remove(tmp)

# ------------------------------------------------------------------
# Mastering DSP (no external deps)
# ------------------------------------------------------------------

def apply_gain(audio: List[List[float]], gain_db: float) -> List[List[float]]:
    g = lin_from_db(gain_db)
    return [[v * g for v in ch] for ch in audio]


def clamp_sample_peak(audio: List[List[float]], peak_limit_db: float = DEFAULT_TRUE_PEAK_LIMIT_DB) -> List[List[float]]:
    """
    Sample-peak clamp (approx true-peak).
    If audio peak exceeds limit, applies a global trim.
    """
    peak = 0.0
    for ch in audio:
        for v in ch:
            av = abs(v)
            if av > peak:
                peak = av

    if peak <= 0.0:
        return audio

    peak_db = db20(peak)
    if peak_db <= peak_limit_db:
        return audio

    trim_db = peak_limit_db - peak_db
    return apply_gain(audio, trim_db)


def soft_clip(audio: List[List[float]], drive: float = 1.0) -> List[List[float]]:
    out: List[List[float]] = []
    for ch in audio:
        o: List[float] = []
        for v in ch:
            o.append(math.tanh(v * drive))
        out.append(o)
    return out


def simple_one_pole_hp(ch: List[float], sr: int, cutoff_hz: float) -> List[float]:
    if cutoff_hz <= 0:
        return ch
    rc = 1.0 / (2.0 * math.pi * cutoff_hz)
    dt = 1.0 / float(sr)
    alpha = rc / (rc + dt)

    y_prev = 0.0
    x_prev = 0.0
    out: List[float] = []
    for x in ch:
        y = alpha * (y_prev + x - x_prev)
        out.append(y)
        y_prev = y
        x_prev = x
    return out


def simple_one_pole_lp(ch: List[float], sr: int, cutoff_hz: float) -> List[float]:
    if cutoff_hz <= 0:
        return ch
    rc = 1.0 / (2.0 * math.pi * cutoff_hz)
    dt = 1.0 / float(sr)
    alpha = dt / (rc + dt)

    y_prev = 0.0
    out: List[float] = []
    for x in ch:
        y_prev = y_prev + alpha * (x - y_prev)
        out.append(y_prev)
    return out


def light_compress(ch: List[float], threshold_db: float = -18.0, ratio: float = 1.2) -> List[float]:
    th = lin_from_db(threshold_db)
    out: List[float] = []
    for x in ch:
        s = -1.0 if x < 0 else 1.0
        a = abs(x)
        if a <= th:
            out.append(x)
        else:
            over = a / th
            comp = th * (over ** (1.0 / ratio))
            out.append(s * comp)
    return out


def normalize_to_lufs_samples(
    audio: List[List[float]],
    sr: int,
    target_lufs: float,
    peak_limit_db: float = DEFAULT_TRUE_PEAK_LIMIT_DB,
) -> Tuple[List[List[float]], Dict[str, float]]:
    lufs = integrated_lufs(audio, sr)
    gain_db = target_lufs - lufs

    out = apply_gain(audio, gain_db)
    out = clamp_sample_peak(out, peak_limit_db)

    peak_db = sample_peak_db(out)
    return out, {
        "input_lufs": float(lufs),
        "applied_gain_db": float(gain_db),
        "post_peak_db": float(peak_db),
        "target_lufs": float(target_lufs),
        "peak_limit_db": float(peak_limit_db),
    }


def ai_natural_mastering_samples(
    audio: List[List[float]],
    sr: int,
) -> Tuple[List[List[float]], Dict[str, Any]]:
    """
    AI Natural Balance (dependency-free):
    - Normalize to -14 LUFS, peak clamp -1 dBFS
    - Use ΔE to decide gentle HP/LP shaping + light compression
    - Soft clip for safety
    """
    out, norm_info = normalize_to_lufs_samples(
        audio, sr,
        DEFAULT_AI_NATURAL_TARGET_LUFS,
        DEFAULT_TRUE_PEAK_LIMIT_DB
    )

    de = delta_e(out, sr)
    delta_norm = min(max(de, 0.0), 1.0)

    LOW = 0.42
    HIGH = 0.65
    shape_info: Dict[str, Any] = {"delta_e": float(de), "delta_norm": float(delta_norm)}

    if delta_norm < LOW:
        shape_info["mode"] = "lift_presence"
        for c in range(len(out)):
            out[c] = simple_one_pole_hp(out[c], sr, 60.0)

    elif delta_norm > HIGH:
        shape_info["mode"] = "soften_highs"
        cutoff = 18000.0 - ((delta_norm - HIGH) * 2000.0)
        if cutoff < 12000.0:
            cutoff = 12000.0
        for c in range(len(out)):
            out[c] = simple_one_pole_lp(out[c], sr, cutoff)
        shape_info["lp_cutoff_hz"] = float(cutoff)

    else:
        shape_info["mode"] = "neutral"

    for c in range(len(out)):
        out[c] = light_compress(out[c], threshold_db=-22.0, ratio=1.1)

    out = soft_clip(out, drive=1.05)
    out = clamp_sample_peak(out, DEFAULT_TRUE_PEAK_LIMIT_DB)

    info = {"normalize": norm_info, "shape": shape_info, "peak_db": float(sample_peak_db(out))}
    return out, info


def master_audio_samples(
    audio: List[List[float]],
    sr: int,
    mode: str = "none",
) -> Tuple[List[List[float]], Dict[str, Any]]:
    """
    Mastering entry point.
    mode:
      - none
      - youtube / spotify (-14 LUFS, -1 dB)
      - apple (-16 LUFS, -1 dB)
      - broadcast (-23 LUFS, -1 dB)
      - ai_natural (AI Natural Balance)
    """
    mode_key = (mode or "none").strip().lower()

    if not audio or not audio[0]:
        raise ValueError("Empty audio")

    if len(audio) == 1:
        audio = [audio[0], audio[0][:]]

    presets = {
        "youtube": (-14.0, -1.0),
        "spotify": (-14.0, -1.0),
        "apple": (-16.0, -1.0),
        "broadcast": (-23.0, -1.0),
    }

    if mode_key in presets:
        t_lufs, t_peak = presets[mode_key]
        out, norm_info = normalize_to_lufs_samples(audio, sr, t_lufs, t_peak)
        return out, {"mode": mode_key, "normalize": norm_info}

    if mode_key == "ai_natural":
        out, info = ai_natural_mastering_samples(audio, sr)
        info["mode"] = "ai_natural"
        return out, info

    return audio, {"mode": "none"}


def master_file(
    input_path: str,
    output_path: str,
    mode: str = "youtube",
    target_sr: int = DEFAULT_DECODE_SR,
    target_ch: int = DEFAULT_DECODE_CH,
) -> Dict[str, Any]:
    """
    Full pipeline:
    - decode to wav if needed (ffmpeg optional)
    - read float
    - master (mode)
    - export keeping output extension (wav native, others require ffmpeg)
    Returns metadata.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(input_path)

    tmp = None
    try:
        wav, tmp, decode_info = decode_to_wav_if_needed(input_path, target_sr=target_sr, target_ch=target_ch)
        audio, sr = read_wav_float(wav)

        # pre analysis
        pre = analyze_samples(audio, sr, target_lufs=DEFAULT_TARGET_LUFS)

        mastered, m_info = master_audio_samples(audio, sr, mode=mode)
        mastered = clamp_sample_peak(mastered, DEFAULT_TRUE_PEAK_LIMIT_DB)

        enc_info = export_mastered_like_input(input_path, output_path, mastered, sr)

        post = analyze_samples(mastered, sr, target_lufs=DEFAULT_TARGET_LUFS)

        return {
            "ok": True,
            "mode": m_info.get("mode", mode),
            "decode": decode_info,
            "encode": enc_info,
            "output_path": output_path,
            "pre": {
                "lufs": round(float(pre.lufs), 3),
                "peak_dbtp_approx": round(float(pre.peak_dbtp_approx), 3),
                "delta_e": round(float(pre.delta_e), 5),
            },
            "post": {
                "lufs": round(float(post.lufs), 3),
                "peak_dbtp_approx": round(float(post.peak_dbtp_approx), 3),
                "delta_e": round(float(post.delta_e), 5),
            },
            "master_info": m_info,
        }
    finally:
        if tmp:
            safe_remove(tmp)


__all__ = [
    # analysis
    "analyze_file",
    "analyze_samples",
    "AnalysisResult",
    "DEFAULT_TARGET_LUFS",
    # mastering
    "master_audio_samples",
    "master_file",
]
