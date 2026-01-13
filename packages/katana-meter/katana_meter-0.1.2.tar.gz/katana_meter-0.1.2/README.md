# Katana Meter

Katana Meter is a deterministic audio analysis engine designed for
LUFS, True Peak (sample-based approximation), gain calculation,
and ΔE (entropy-change) metrics.

It is intended for research, educational use, and technical evaluation.
The core is dependency-free and focuses on reproducible, transparent results.

---

## Features

- Integrated LUFS (gated, BS.1770-inspired)
- Sample Peak (dBTP approximation)
- Gain calculation to target LUFS
- ΔE entropy-change metric (0.0 – 1.0)
- Deterministic analysis (same input → same output)
- WAV native support
- MP3 / FLAC / AAC / OGG via optional FFmpeg

---

## Installation

```bash
pip install katana-meter
