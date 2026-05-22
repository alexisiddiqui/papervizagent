#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageEnhance, ImageOps, PngImagePlugin

from config import (
    BEST_HYPOTHESIS_OUTPUT,
    ENSEMBLE_STACK_OUTPUT,
    HYPOTHESIS_CLEAN_OUTPUTS,
    HYPOTHESIS_INPUTS,
    HYPOTHESIS_TINTED_OUTPUTS,
    HYPOTHESIS_TINTS,
    PROJECTED_ERROR_INPUT,
    PROJECTED_ERROR_OUTPUT,
    PROCESSED_DIR,
    RENDERS_DIR,
    SIZES,
    STRUCTURAL_HYPOTHESIS_CANDIDATES,
    STRUCTURAL_HYPOTHESIS_OUTPUT,
    TINT_STRENGTH,
    ensure_output_dirs,
)

STACK_CONFIG: tuple[tuple[str, int, int, float], ...] = (
    ("h4_grey_clean.png", -9, -7, 0.20),
    ("h3_grey_clean.png", -6, -5, 0.30),
    ("h2_grey_clean.png", -3, -3, 0.45),
    ("h1_grey_clean.png", 0, 0, 1.00),
)


def validate_inputs(required_files: Iterable[Path]) -> None:
    missing = [str(path) for path in required_files if not path.exists()]
    if missing:
        missing_list = "\n  - ".join(missing)
        raise FileNotFoundError(f"Missing required render inputs:\n  - {missing_list}")


def remove_background(
    img: Image.Image,
    *,
    white_threshold: int = 245,
    black_threshold: int = 10,
) -> Image.Image:
    rgba = np.asarray(img.convert("RGBA")).copy()
    rgb = rgba[..., :3]
    near_white = (rgb >= white_threshold).all(axis=2)
    near_black = (rgb <= black_threshold).all(axis=2)
    bg_mask = near_white | near_black
    rgba[bg_mask, 3] = 0
    return Image.fromarray(rgba, mode="RGBA")


def auto_crop(img: Image.Image, *, padding: int = 12) -> Image.Image:
    alpha = img.split()[-1]
    bbox = alpha.getbbox()
    if bbox is None:
        return img
    cropped = img.crop(bbox)
    if padding > 0:
        cropped = ImageOps.expand(cropped, border=padding, fill=(0, 0, 0, 0))
    return cropped


def _fit_within(img: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    target_w, target_h = target_size
    src_w, src_h = img.size
    scale = min(target_w / src_w, target_h / src_h)
    new_size = (
        max(1, int(round(src_w * scale))),
        max(1, int(round(src_h * scale))),
    )
    return img.resize(new_size, Image.Resampling.LANCZOS)


def resize_canvas(
    img: Image.Image,
    target_size: tuple[int, int],
    *,
    anchor: str = "center",
) -> Image.Image:
    resized = _fit_within(img, target_size)
    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
    if anchor != "center":
        raise ValueError(f"Unsupported anchor '{anchor}'.")
    x = (target_size[0] - resized.width) // 2
    y = (target_size[1] - resized.height) // 2
    canvas.alpha_composite(resized, dest=(x, y))
    return canvas


def tint_image(
    img: Image.Image,
    rgb_tint: tuple[int, int, int],
    strength: float,
) -> Image.Image:
    strength = max(0.0, min(1.0, strength))
    rgba = np.asarray(img.convert("RGBA")).astype(np.float32)
    rgb = rgba[..., :3] / 255.0
    alpha = rgba[..., 3:4]
    luminance = (
        0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    )[..., None]
    grey_rgb = np.repeat(luminance, 3, axis=2)
    tint = np.array(rgb_tint, dtype=np.float32).reshape((1, 1, 3)) / 255.0
    tinted = grey_rgb * tint
    blended = (1.0 - strength) * grey_rgb + strength * tinted
    out = np.concatenate([np.clip(blended * 255.0, 0, 255), alpha], axis=2)
    return Image.fromarray(out.astype(np.uint8), mode="RGBA")


def save_asset(img: Image.Image, output_path: Path, metadata: dict[str, str]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    png_info = PngImagePlugin.PngInfo()
    for key, value in metadata.items():
        png_info.add_text(key, str(value))
    img.save(output_path, format="PNG", optimize=True, pnginfo=png_info)
    print(f"[processed] {output_path.name}: {img.width}x{img.height}")


def create_ensemble_stack(
    frame_paths_config: Iterable[tuple[str, int, int, float]],
    canvas_size: tuple[int, int],
) -> Image.Image:
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    for source_name, dx, dy, opacity in frame_paths_config:
        frame = Image.open(PROCESSED_DIR / source_name).convert("RGBA")
        alpha = frame.split()[-1]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        frame.putalpha(alpha)
        paste_pos = (
            canvas_size[0] // 2 + dx - frame.width // 2,
            canvas_size[1] // 2 + dy - frame.height // 2,
        )
        canvas.alpha_composite(frame, dest=paste_pos)
    return canvas


def process_render(
    source_path: Path,
    *,
    target_size: tuple[int, int],
    white_threshold: int,
    black_threshold: int,
    padding: int,
) -> Image.Image:
    img = Image.open(source_path).convert("RGBA")
    img = remove_background(
        img, white_threshold=white_threshold, black_threshold=black_threshold
    )
    img = auto_crop(img, padding=padding)
    img = resize_canvas(img, target_size=target_size, anchor="center")
    return img


def _resolve_structural_source() -> Path:
    for name in STRUCTURAL_HYPOTHESIS_CANDIDATES:
        candidate = RENDERS_DIR / name
        if candidate.exists():
            return candidate
    candidates = "\n  - ".join(str(RENDERS_DIR / name) for name in STRUCTURAL_HYPOTHESIS_CANDIDATES)
    raise FileNotFoundError(
        "Missing structural hypothesis render. Checked:\n  - " + candidates
    )


def run(
    *,
    white_threshold: int,
    black_threshold: int,
    padding: int,
) -> None:
    ensure_output_dirs()

    required = [RENDERS_DIR / name for name in HYPOTHESIS_INPUTS.values()]
    required.append(RENDERS_DIR / PROJECTED_ERROR_INPUT)
    validate_inputs(required)
    structural_source = _resolve_structural_source()

    for key, source_name in HYPOTHESIS_INPUTS.items():
        source = RENDERS_DIR / source_name
        clean = process_render(
            source,
            target_size=SIZES["hypothesis_thumb"],
            white_threshold=white_threshold,
            black_threshold=black_threshold,
            padding=padding,
        )
        clean_name = HYPOTHESIS_CLEAN_OUTPUTS[key]
        save_asset(
            clean,
            PROCESSED_DIR / clean_name,
            {
                "source": str(source.name),
                "stage": "clean_hypothesis",
            },
        )

        tinted = tint_image(clean, HYPOTHESIS_TINTS[key], TINT_STRENGTH["hypothesis"])
        save_asset(
            tinted,
            PROCESSED_DIR / HYPOTHESIS_TINTED_OUTPUTS[key],
            {
                "source": str(source.name),
                "stage": "tinted_hypothesis",
                "tint_strength": f"{TINT_STRENGTH['hypothesis']:.2f}",
            },
        )

    # Process "Best Hypothesis" (structural hypothesis render)
    best_hyp = process_render(
        structural_source,
        target_size=SIZES["best_hypothesis"],
        white_threshold=white_threshold,
        black_threshold=black_threshold,
        padding=padding,
    )
    save_asset(
        best_hyp,
        PROCESSED_DIR / BEST_HYPOTHESIS_OUTPUT,
        {"source": structural_source.name, "stage": "best_hypothesis"},
    )

    ensemble = create_ensemble_stack(STACK_CONFIG, SIZES["ensemble_stack"])
    save_asset(
        ensemble,
        PROCESSED_DIR / ENSEMBLE_STACK_OUTPUT,
        {"source": "h1..h4 clean stack", "stage": "ensemble"},
    )

    # Process "Residue Work Done" (projected error render)
    residue_work = process_render(
        RENDERS_DIR / PROJECTED_ERROR_INPUT,
        target_size=SIZES["projected_error"],
        white_threshold=white_threshold,
        black_threshold=black_threshold,
        padding=padding,
    )
    save_asset(
        residue_work,
        PROCESSED_DIR / PROJECTED_ERROR_OUTPUT,
        {"source": PROJECTED_ERROR_INPUT, "stage": "residue_work"},
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Process raw protein renders into normalized pipeline assets."
    )
    parser.add_argument("--white-threshold", type=int, default=245)
    parser.add_argument("--black-threshold", type=int, default=10)
    parser.add_argument("--padding", type=int, default=12)
    args = parser.parse_args()

    run(
        white_threshold=args.white_threshold,
        black_threshold=args.black_threshold,
        padding=args.padding,
    )


if __name__ == "__main__":
    main()
