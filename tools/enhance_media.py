#!/usr/bin/env python3
"""Create a gentle, non-destructive enhanced working copy of a journal photo.

The original file is never overwritten. The result is intended for compressed
Messenger/social-media images while the full-resolution originals are awaited.
"""
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import sys

try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
except ImportError as exc:  # pragma: no cover - user-facing dependency message
    raise SystemExit("Pillow is required. Install it with: python -m pip install Pillow") from exc


def enhance(source: Path, output: Path, scale: float = 1.35, quality: int = 91) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    if source.resolve() == output.resolve():
        raise ValueError("Output must be a different file; originals are never overwritten.")

    image = Image.open(source).convert("RGB")
    image = image.filter(ImageFilter.MedianFilter(size=3))
    image = ImageOps.autocontrast(image, cutoff=(0.3, 0.3))
    image = ImageEnhance.Contrast(image).enhance(1.04)
    image = ImageEnhance.Color(image).enhance(1.03)
    image = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    image = image.filter(ImageFilter.UnsharpMask(radius=1.6, percent=115, threshold=3))

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, "JPEG", quality=quality, optimize=True, progressive=True, subsampling=0)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source JPEG/PNG")
    parser.add_argument("output", type=Path, nargs="?", help="Output JPEG")
    parser.add_argument("--scale", type=float, default=1.35, help="Upscale factor (default: 1.35)")
    parser.add_argument("--quality", type=int, default=91, help="JPEG quality (default: 91)")
    args = parser.parse_args()

    output = args.output or args.source.with_name(f"{args.source.stem}-enhanced.jpg")
    enhance(args.source, output, args.scale, args.quality)
    print(f"Enhanced working copy: {output}")
    print(f"Original preserved:     {args.source}")


if __name__ == "__main__":
    main()
