# -*- coding: utf-8 -*-
"""
Katana Meter – CLI (Analyzer Only)

Command-line interface for Katana Meter analysis engine.
No mastering, no backend, no side effects.

Example:
    katana-meter song.wav
    katana-meter song.wav --target -16
    katana-meter song.wav --json
"""

import argparse
import json
import sys

from .core import analyze_file, DEFAULT_TARGET_LUFS


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="katana-meter",
        description="Katana Meter CLI – Integrated LUFS & ΔE Analyzer",
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="Path to audio file (WAV native, others require ffmpeg)",
    )

    parser.add_argument(
        "--target",
        type=float,
        default=DEFAULT_TARGET_LUFS,
        help=f"Target LUFS reference (default: {DEFAULT_TARGET_LUFS})",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print full analysis result as JSON",
    )

    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        sys.exit(1)

    try:
        result = analyze_file(args.file, target_lufs=args.target)
    except Exception as e:
        print(f"[katana-meter] Error: {e}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    # ---- Human-readable output ----
    print("Katana Meter Analysis")
    print("-" * 24)
    print(f"Integrated LUFS : {result['lufs']}")
    print(f"Target LUFS     : {result['target_lufs']}")
    print(f"Gain to Target  : {result['gain_to_target_db']} dB")
    print(f"Peak (approx)   : {result['peak_dbtp_approx']} dBTP")
    print(f"ΔE              : {result['delta_e']}")

    if result.get("labels"):
        print("\nLabels:")
        for k, v in result["labels"].items():
            print(f"  {k}: {v}")

    if result.get("warnings"):
        print("\nWarnings:")
        for w in result["warnings"]:
            print(f"  - {w}")


if __name__ == "__main__":
    main()
