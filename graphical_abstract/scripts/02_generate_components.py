#!/usr/bin/env python3
from __future__ import annotations

import argparse

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

from config import (
    COLORS,
    COMPONENT_MANIFEST,
    COMPONENTS_PDF_DIR,
    COMPONENTS_SVG_DIR,
    COMPONENT_BASENAMES,
    DPI,
    FONT_FALLBACK,
    FONT_FAMILY,
    SIZES,
    ensure_output_dirs,
    rgb01,
)


def px_to_inches(size: tuple[int, int]) -> tuple[float, float]:
    return size[0] / DPI, size[1] / DPI


def save_vector_figure(fig: plt.Figure, basename: str) -> None:
    COMPONENTS_SVG_DIR.mkdir(parents=True, exist_ok=True)
    COMPONENTS_PDF_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = COMPONENTS_SVG_DIR / f"{basename}.svg"
    pdf_path = COMPONENTS_PDF_DIR / f"{basename}.pdf"
    # Keep tight boxes for most assets. Increase padding for HDX curves to avoid crowding.
    if basename == "timescale_bar":
        pad_inches = 0.04
    elif basename == "hdx_curves":
        pad_inches = 0.20
    else:
        pad_inches = 0.02
    save_kwargs = {"transparent": True, "bbox_inches": "tight", "pad_inches": pad_inches}
    fig.savefig(svg_path, format="svg", **save_kwargs)
    fig.savefig(pdf_path, format="pdf", **save_kwargs)
    plt.close(fig)
    print(f"[components] {basename}.svg, {basename}.pdf")


def gaussian_smooth(values: np.ndarray, sigma: float = 2.0) -> np.ndarray:
    radius = max(1, int(round(3 * sigma)))
    x = np.arange(-radius, radius + 1, dtype=float)
    kernel = np.exp(-(x**2) / (2 * sigma**2))
    kernel /= kernel.sum()
    return np.convolve(values, kernel, mode="same")


def generate_hdx_curves() -> None:
    fig, ax = plt.subplots(figsize=px_to_inches(SIZES["hdx_curves"]))
    t = np.linspace(0.0, 10.0, 200)
    # Use a sequence of greys for the target experimental data
    curve_colors = [
        rgb01("slate"), 
        rgb01("charcoal"), 
        rgb01("slate_light"),
        rgb01("silver")
    ]
    
    # Each curve: sum of two exponential phases with different rate constants
    curve_params = [
        (0.72, 0.12, 0.28, 0.04),   # (A1, k1, A2, k2)
        (0.82, 0.25, 0.18, 0.06),
        (0.55, 0.06, 0.45, 0.02),
        (0.90, 0.50, 0.10, 0.08),
    ]
    
    for i, (a1, k1, a2, k2) in enumerate(curve_params):
        y = a1 * (1.0 - np.exp(-k1 * t)) + a2 * (1.0 - np.exp(-k2 * t))
        ax.plot(
            t,
            y,
            color=curve_colors[i],
            linewidth=1.5,
            solid_capstyle="round",
        )
    ax.set_xlim(0, 10)
    ax.set_ylim(0.0, 1.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines[["top", "right"]].set_visible(False)
    save_vector_figure(fig, "hdx_curves")


def generate_heatmap_thumb() -> None:
    rng = np.random.default_rng(seed=42)
    n_residues, n_frames = 18, 12
    base = np.zeros((n_residues, n_frames))
    base[4:14, :] = 0.6
    noise = rng.uniform(0.0, 0.4, (n_residues, n_frames))
    data = np.clip(base + noise, 0.0, 1.0)

    fig, ax = plt.subplots(figsize=px_to_inches(SIZES["heatmap_thumb"]))
    teal_cmap = LinearSegmentedColormap.from_list("teal_map", ["#FFFFFF", "#4CA6A8"])
    ax.imshow(data, cmap=teal_cmap, aspect="auto", interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor(rgb01("charcoal"))
        spine.set_linewidth(0.8)
    save_vector_figure(fig, "heatmap_thumb")


def generate_residue_peptide() -> None:
    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=px_to_inches(SIZES["residue_peptide"]),
        gridspec_kw={"wspace": 0.45},
    )

    # --- Left: residue–peptide sparse coverage map ---
    # Y-axis = residue position; each column is one peptide bar spanning its range.
    rng = np.random.default_rng(seed=17)
    n_residues = 30
    n_peptides = 8
    starts = rng.integers(0, n_residues - 6, size=n_peptides)
    lengths = rng.integers(6, 15, size=n_peptides)
    peptides = [(int(s), int(min(s + l, n_residues))) for s, l in zip(starts, lengths)]
    pep_colors = [rgb01("teal"), rgb01("coral")]

    for i, (start, end) in enumerate(peptides):
        ax1.add_patch(
            plt.Rectangle(
                (i - 0.35, start), 0.7, end - start,
                facecolor=pep_colors[i % 2], alpha=0.75, linewidth=0,
            )
        )

    ax1.set_xlim(-0.5, n_peptides - 0.5)
    ax1.set_ylim(-0.5, n_residues + 0.5)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.spines[["left", "bottom"]].set_color(rgb01("charcoal"))
    ax1.spines[["left", "bottom"]].set_linewidth(0.7)

    # --- Right: peptide-level uptake curve (unchanged) ---
    t = np.linspace(0.0, 10.0, 100)
    peptide = (1.0 - np.exp(-0.3 * t)) * 0.7 + (1.0 - np.exp(-0.8 * t)) * 0.3
    ax2.plot(t, peptide, color=rgb01("coral"), linewidth=1.5)
    ax2.set_ylim(0.0, 1.1)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.spines[["left", "bottom"]].set_color(rgb01("charcoal"))
    ax2.spines[["left", "bottom"]].set_linewidth(0.7)

    # Straight connection arrow: coverage map → uptake curve.
    from matplotlib.patches import ConnectionPatch
    arrow = ConnectionPatch(
        xyA=(1.0, 0.5), xyB=(0.0, 0.5),
        coordsA="axes fraction", coordsB="axes fraction",
        axesA=ax1, axesB=ax2,
        arrowstyle="-|>", color=rgb01("grey_mid"),
        lw=1.0, mutation_scale=8,
        connectionstyle="arc3,rad=0.0",
    )
    fig.add_artist(arrow)

    save_vector_figure(fig, "residue_peptide")


def generate_weight_dist() -> None:
    rng = np.random.default_rng(seed=7)
    n_frames = 16
    raw = rng.exponential(0.3, n_frames)
    weights = np.sort(raw / raw.sum())[::-1]
    x = np.arange(n_frames)

    fig, ax = plt.subplots(figsize=px_to_inches(SIZES["weight_dist"]))
    ax.bar(x, weights, color=rgb01("teal"), alpha=0.85, width=0.8)

    # Reference distribution: a centered Gaussian curve to represent the prior/orthogonal distribution
    x_fine = np.linspace(0, n_frames - 1, 100)
    mu, sigma = n_frames / 2.5, n_frames / 4.0
    reference_curve = np.exp(-((x_fine - mu) ** 2) / (2 * sigma**2))
    reference_curve = reference_curve * (weights.max() * 0.9 / reference_curve.max())
    
    ax.plot(
        x_fine,
        reference_curve,
        color=rgb01("slate"),
        linewidth=1.5,
        linestyle="--",
        alpha=0.9,
        zorder=5,
    )

    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    save_vector_figure(fig, "weight_dist")


def generate_timescale_bar() -> None:
    fig, ax = plt.subplots(figsize=px_to_inches(SIZES["timescale_bar"]))
    width_px = 1000
    gradient = np.linspace(0.0, 1.0, width_px)[None, :]
    cmap = LinearSegmentedColormap.from_list("teal_to_coral", ["#4CA6A8", "#E8735A"])
    ax.imshow(
        gradient,
        cmap=cmap,
        aspect="auto",
        interpolation="bicubic",
        extent=[0.0, 1.0, 0.0, 1.0],
    )
    ax.axis("off")
    save_vector_figure(fig, "timescale_bar")


def generate_scorecard() -> None:
    """
    Generates the evaluation scorecard table as a vector graphic.
    Refined as a clean mini-table with alternating row fills.
    """
    fig, ax = plt.subplots(figsize=px_to_inches(SIZES["scorecard"]))
    
    # Define table data
    header = "Scorecard"
    rows = [
        "$Work_{Scale}$",
        "$Work_{KLD}$",
        "Held-out Error",
        "Replicate Uncertainty"
    ]

    text_row_colors = [rgb01("navy"), rgb01("slate"), rgb01("slate"), rgb01("slate")]
    
    n_rows = len(rows)
    row_spacing = 1.2  # Increase vertical units per row
    # Background colors
    colors = ["#FFFFFF", "#F9F5FC"] # White and faint lavender
    
    # Set axis limits for table layout
    ax.set_xlim(0, 1)
    ax.set_ylim(0, (n_rows + 1) * row_spacing)
    
    # Draw header
    header_y = n_rows * row_spacing
    ax.add_patch(plt.Rectangle((0, header_y), 1, row_spacing, color=rgb01("charcoal"), alpha=0.1))
    ax.text(0.5, header_y + (row_spacing * 0.45), header, fontsize=8, weight="bold", ha="center", va="center", color=rgb01("navy"))
    
    # Draw rows
    for i, label in enumerate(rows):
        y = (n_rows - 1 - i) * row_spacing
        bg_color = colors[i % 2]
        ax.add_patch(plt.Rectangle((0, y), 1, row_spacing, facecolor=bg_color, edgecolor=rgb01("charcoal"), linewidth=0.5))
        # Left-aligned row label (moved even higher)
        ax.text(0.05, y + (row_spacing * 0.72), label, fontsize=7, ha="left", va="center", color=text_row_colors[i])
        
        # Add three score bars below the text: Teal, Lilac, Grey
        # Systematic ranks: 
        #   Row 0: Lilac #1, Teal #2, Grey #3
        #   Others: Teal/Lilac variable, Grey always #3
        
        all_scores = [
            {"lilac": 0.88, "teal": 0.65, "slate": 0.35}, # Work_Scale
            {"teal": 0.82, "lilac": 0.60, "slate": 0.25}, # Work_KLD
            {"lilac": 0.75, "teal": 0.55, "slate": 0.30}, # Held-out
            {"teal": 0.70, "lilac": 0.45, "slate": 0.20}, # Uncertainty
        ]
        scores = all_scores[i]
        
        # Draw bars with more vertical separation
        bar_height = 0.09  # Slightly thinner
        # Position bars within the lower part of the row
        bar_y_starts = {
            "teal":  y + (row_spacing * 0.44), 
            "lilac": y + (row_spacing * 0.27), 
            "slate": y + (row_spacing * 0.10)
        }
        
        for color_name in ["teal", "lilac", "slate"]:
            val = scores[color_name]
            ax.add_patch(plt.Rectangle(
                (0.05, bar_y_starts[color_name]), 
                val * 0.8, 
                bar_height, 
                color=rgb01(color_name), 
                alpha=1.0
            ))

    # Outer border
    ax.add_patch(plt.Rectangle((0, 0), 1, (n_rows + 1) * row_spacing, fill=False, edgecolor=rgb01("charcoal"), lw=1.0))

    ax.axis("off")
    save_vector_figure(fig, "scorecard")


def generate_tiny_bar_chart() -> None:
    fig, ax = plt.subplots(figsize=px_to_inches(SIZES["tiny_bar_chart"]))
    x = np.arange(5)
    y = [0.4, 0.7, 0.3, 0.8, 0.5]
    ax.bar(x, y, color=rgb01("lilac"), width=0.7)
    ax.axis("off")
    save_vector_figure(fig, "tiny_bar_chart")


def generate_tiny_sliders() -> None:
    fig, ax = plt.subplots(figsize=px_to_inches(SIZES["tiny_sliders"]))
    # Slider 1
    ax.plot([0.1, 0.9], [0.7, 0.7], color=rgb01("grey_mid"), lw=1.5)
    ax.plot(0.4, 0.7, "o", color=rgb01("lilac"), markersize=4)
    # Slider 2
    ax.plot([0.1, 0.9], [0.3, 0.3], color=rgb01("grey_mid"), lw=1.5)
    ax.plot(0.7, 0.3, "o", color=rgb01("lilac"), markersize=4)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    save_vector_figure(fig, "tiny_sliders")


def configure_plot_defaults() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [FONT_FAMILY, FONT_FALLBACK],
            "axes.facecolor": "none",
            "savefig.facecolor": "none",
            "axes.edgecolor": tuple(channel / 255 for channel in COLORS["charcoal"]),
            "text.color": tuple(channel / 255 for channel in COLORS["navy"]),
        }
    )


def run(only: set[str] | None = None) -> None:
    ensure_output_dirs()
    configure_plot_defaults()
    generators = {c["name"]: globals()[f"generate_{c['name']}"] for c in COMPONENT_MANIFEST}
    selected = only if only else set(generators.keys())
    unknown = selected.difference(generators.keys())
    if unknown:
        valid = ", ".join(sorted(generators))
        bad = ", ".join(sorted(unknown))
        raise ValueError(f"Unknown component(s): {bad}. Valid choices: {valid}")
    for name in sorted(selected):
        if name in generators:
            generators[name]()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate vector-first component graphics for the figure."
    )
    parser.add_argument(
        "--only",
        nargs="+",
        choices=COMPONENT_BASENAMES,
        help="Generate only the listed components.",
    )
    args = parser.parse_args()
    run(only=set(args.only) if args.only else None)


if __name__ == "__main__":
    main()
