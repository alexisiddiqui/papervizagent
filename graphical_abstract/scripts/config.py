from __future__ import annotations

from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parents[1]
INPUTS_DIR = ROOT / "inputs"
RENDERS_DIR = INPUTS_DIR / "renders"
OUTPUTS_DIR = ROOT / "outputs"
PROCESSED_DIR = OUTPUTS_DIR / "processed"
COMPONENTS_DIR = OUTPUTS_DIR / "components"
COMPONENTS_SVG_DIR = COMPONENTS_DIR / "svg"
COMPONENTS_PDF_DIR = COMPONENTS_DIR / "pdf"
FIGURE_OUT_DIR = OUTPUTS_DIR / "figure"
STAMPS_DIR = OUTPUTS_DIR / ".stamps"
TIKZ_DIR = ROOT / "tikz"
PANELS_DIR = TIKZ_DIR / "panels"


# Palette
COLORS: dict[str, tuple[int, int, int]] = {
    "teal": (31, 157, 138),  # #1F9D8A
    "purple": (144, 164, 174), # #90A4AE
    "apple_green": (152, 208, 163),  # #98D0A3
    "coral": (210, 100, 63),  # #D2643F
    "gold": (210, 100, 63),  # #D2643F
    "gold_bright": (210, 100, 63),  # #D2643F
    "lilac": (204, 204, 255), #CCCCFF
    "slate": (107, 114, 128),  # #6B7280
    "navy": (17, 24, 39),  # #111827
    "grey_mid": (107, 107, 107),  # #6B7280
    "charcoal": (199, 205, 212),  # #C7CDD4
    "slate_light": (144, 164, 174), # #90A4AE
    "silver": (207, 216, 220), # #CFD8DC
    "lavender": (59, 91, 165),  # #3B5BA5
    "zone_a": (248, 250, 252),  # #F8FAFC
    "zone_b": (248, 250, 252),  # #F8FAFC
    "zone_c": (248, 250, 252),  # #F8FAFC
    "teal_light": (232, 246, 243),  # #E8F6F3
    "coral_light": (251, 237, 231),  # #FBEDE7
    "lavender_light": (238, 242, 251),  # #EEF2FB
    "cream": (248, 250, 252),  # #F8FAFC
    "white": (255, 255, 255),
}

HYPOTHESIS_TINTS: dict[str, tuple[int, int, int]] = {
    "h1": COLORS["navy"],
    "h2": COLORS["grey_mid"],
    "h3": COLORS["lavender"],
    "h4": COLORS["slate"],
}

TINT_STRENGTH: dict[str, float] = {
    "hypothesis": 1.0,
    "ensemble_front": 0.35,
    "ensemble_back": 0.15,
}


# Sizes in px at 300 dpi
SIZES: dict[str, tuple[int, int]] = {
    "hypothesis_thumb": (180, 180),
    "best_hypothesis": (220, 220),
    "ensemble_stack": (280, 280),
    "projected_error": (200, 200),
    "structural_hyp": (200, 200),
    "hdx_curves": (280, 200),
    "heatmap_thumb": (220, 140),
    "residue_peptide": (260, 130),
    "weight_dist": (200, 150),
    "timescale_bar": (500, 60),
    "scorecard": (400, 650),
    "tiny_bar_chart": (80, 80),
    "tiny_sliders": (100, 80),
}

DPI = 300
FONT_FAMILY = "Helvetica"
FONT_FALLBACK = "DejaVu Sans"


# Input files currently present in workspace
HYPOTHESIS_INPUTS: dict[str, str] = {
    "h1": "H1.png",
    "h2": "H2.png",
    "h3": "H3.png",
    "h4": "H4.png",
}

PROJECTED_ERROR_INPUT = "projected_error_BW.png"
STRUCTURAL_HYPOTHESIS_CANDIDATES: tuple[str, ...] = (
    "structural_hypothesis.png",
    "structural_hypothesis_BW.png",
)


# Processed outputs
HYPOTHESIS_TINTED_OUTPUTS: dict[str, str] = {
    "h1": "h1_teal.png",
    "h2": "h2_coral.png",
    "h3": "h3_lavender.png",
    "h4": "h4_slate.png",
}

HYPOTHESIS_CLEAN_OUTPUTS: dict[str, str] = {
    "h1": "h1_grey_clean.png",
    "h2": "h2_grey_clean.png",
    "h3": "h3_grey_clean.png",
    "h4": "h4_grey_clean.png",
}

BEST_HYPOTHESIS_OUTPUT = "best_hypothesis.png"
ENSEMBLE_STACK_OUTPUT = "ensemble_stack.png"
PROJECTED_ERROR_OUTPUT = "residue_work.png"
STRUCTURAL_HYPOTHESIS_OUTPUT = "best_hypothesis.png"

REQUIRED_PROCESSED_FOR_COMPILE: tuple[str, ...] = (
    "h1_teal.png",
    "h2_coral.png",
    "h3_lavender.png",
    "h4_slate.png",
    "best_hypothesis.png",
    "ensemble_stack.png",
    "residue_work.png",
)


# TikZ files expected by compiler
REQUIRED_TIKZ_FILES: tuple[Path, ...] = (
    TIKZ_DIR / "figure.tex",
    TIKZ_DIR / "styles.tex",
    PANELS_DIR / "panel_a.tex",
    PANELS_DIR / "panel_b.tex",
    PANELS_DIR / "panel_c.tex",
)


# TikZ color name mapping (Python key → LaTeX \definecolor name).
# "white" is excluded — it is a LaTeX built-in and must not be redefined.
TIKZ_COLOR_MAP: dict[str, str] = {
    "teal":        "cTeal",
    "lilac":       "cLilac",
    "coral":       "cCoral",
    "gold":        "cGold",
    "gold_bright": "cGoldBright",
    "slate":       "cSlate",
    "slate_light": "cSlateLight",
    "navy":        "cNavy",
    "grey_mid":    "cGreyMid",
    "charcoal":    "cCharcoal",
    "lavender":    "cLavender",
    "zone_a":      "cZoneA",
    "zone_b":      "cZoneB",
    "zone_c":      "cZoneC",
    "teal_light":  "cTealLight",
    "coral_light": "cCoralLight",
    "lavender_light": "cLavenderLight",
    "cream":       "cCream",
}

# TikZ figure layout constants.
# Values containing a "cm" suffix are used as TikZ dimension arguments
# (minimum width, minimum height, text width).  Bare floats are coordinate
# values in the y=-1cm canvas coordinate system.


def _even_y_positions(
    panel_h: float,
    subtitle_area: float,
    card_heights: list[float],
) -> list[float]:
    """Return evenly-spaced card start Y-positions (relative to panel NW).

    The available vertical space is ``panel_h - subtitle_area`` (everything
    below the subtitle).  Cards are placed so that the gaps between adjacent
    cards—and the margins above the first card and below the last card—are
    all equal.

    Args:
        panel_h:       total panel height in cm.
        subtitle_area: height reserved for label + subtitle above the first
                       card (i.e. the minimum first-card Y-offset).
        card_heights:  estimated rendered heights of each card in cm.

    Returns:
        List of Y-offsets (from panel NW) for each card's north anchor.
    """
    n = len(card_heights)
    available = panel_h - subtitle_area
    total_card_h = sum(card_heights)
    # n+1 equal gaps: above first, between each pair, below last
    gap = (available - total_card_h) / (n + 1)
    positions: list[float] = []
    y = subtitle_area + gap
    for h in card_heights:
        positions.append(round(y, 2))
        y += h + gap
    return positions


def _y_positions_fixed_gap(
    subtitle_area: float,
    card_heights: list[float],
    gap: float,
) -> list[float]:
    """Place cards with a fixed inter-subpanel gap (above first and between each).

    Args:
        subtitle_area: Y-offset to the top of the first card (cm).
        card_heights:  rendered height of each card (cm).
        gap:           fixed gap before the first card and between cards (cm).

    Returns:
        List of Y-offsets (from panel NW) for each card's north anchor.
    """
    y = subtitle_area + gap
    positions: list[float] = []
    for h in card_heights:
        positions.append(round(y, 2))
        y += h + gap
    return positions


# ── Tier 1: Hand-authored atomic values ───────────────────────────────────
# Card height estimates (cm) — adjust if rendered heights change.
# These drive the automatic even-spacing calculation.
_PANEL_H = 14.50
_SUBTITLE_AREA = 1.40   # space reserved above first card (label + subtitle)

# Shared inter-subpanel gap (cm) — used identically in panels A, B, and C.
_GAP = 0.35

# Panel B card heights: [Map Structures, Define Objective, Fit to Target]
# Last card height includes the pills row (~0.6 cm) that sits below the box.
_B_CARD_H = [3.20, 4.50, 4.10]
_B_Y = _y_positions_fixed_gap(_SUBTITLE_AREA, _B_CARD_H, _GAP)

# Panel C: merged Validation+HypTesting card + Outputs card
# Heights must stay in sync with panel_c.tex minimum height values.
_C_COMBINED_H = 6.25   # merged C1 card (Validation & Hypothesis Testing)
_C_OUT_H      = 3.20   # C2 card (Outputs)
_c_stack      = _C_COMBINED_H + _GAP + _C_OUT_H          # 9.80 cm
_c_margin     = (_PANEL_H - _SUBTITLE_AREA - _c_stack) / 2  # 1.65 cm
_C_COMBINED_Y = _SUBTITLE_AREA + _c_margin               # = 3.05 cm
# Legacy alias kept so nothing outside panel_c.tex breaks on import
_C_CARD_H = [_C_COMBINED_H, _C_OUT_H]
_C_Y      = [_C_COMBINED_Y, _C_COMBINED_Y + _C_COMBINED_H + _GAP]

ATOMIC_LAYOUT: dict[str, float | str] = {
    # Canvas
    "canvas_w":      31.70,
    "canvas_h":      17.50,
    # Top margin (figure title)
    "title_x":        0.60,
    "title_y":        0.70,
    # Panels top edge
    "panels_y":       2.00,
    "panel_margin_x": 0.60,   # left edge of Panel A (and right margin)
    "panel_gap":      0.60,    # gap between panels
    # Panel sizes
    "panel_a_w":     10.20,
    "panel_w":        9.00,   # Panel B width
    "panel_c_w":     10.20,   # Panel C width (matching A)
    "panel_h":       _PANEL_H,
    # Inner padding (from panel NW corner to content)
    "panel_pad_x":    0.35,
    "panel_pad_y":    1.40,
    "card_inner_sep": 0.20,   # ~6pt
    # Header offsets (from panel NW)
    "header_off_x":   0.20,
    "header_off_y":   0.25,
    "subtitle_off_x": 0.55,
    "subtitle_off_y": 0.60,
    # Card spacing — kept in sync with _GAP so chained boxes have equal gaps
    "card_gap":       _GAP,
    # Column layout fractions (of inner content width)
    "a_col_left_frac":  0.20,
    "a_col_right_frac": 0.80,
    "b_col_left_frac":  0.25,
    "b_col_mid_frac":   0.50,
    "b_col_right_frac": 0.75,
    "c_col_left_frac":  0.20,
    "c_col_mid_frac":   0.50,
    "c_col_right_frac": 0.80,
    # Panel A Card Y-positions (relative to panel NW)
    "a_req_y":        3.25,   # top of the big white box
    # Optional box top = a_req_y + box_height + _GAP = 3.25 + 8.0 + 0.35
    "a_optional_y":   3.25 + 8.0 + _GAP,
    # Panel B Card Y-positions — auto-computed for even spacing
    "b_feats_y":      _B_Y[0],
    "b_obj_y":        _B_Y[1],
    "b_opt_y":        _B_Y[2],
    # ── Panel C Card Y-positions ─────────────────────────────────────────
    "c_combined_y":  _C_COMBINED_Y,
    "c_out_y":       _C_Y[1],
    # Inter-panel features
    "flow_lane_y":   16.70,
    "inter_panel_arrow_y_ref": 9.25,
    "chevron_y":      9.25,

    "chevron_size":   15,
}


def get_derived_layout() -> dict[str, str]:
    """Return a flat dict of every TikZ \\def value, derived from ATOMIC_LAYOUT."""
    a = ATOMIC_LAYOUT          # shorthand alias

    # ── Panel x-positions (auto-derived) ─────────────────────────────────
    panel_a_x = a["panel_margin_x"]
    panel_b_x = panel_a_x + a["panel_a_w"] + a["panel_gap"]
    panel_c_x = panel_b_x + a["panel_w"]   + a["panel_gap"]

    # ── Content widths (panel width minus 2× horizontal padding) ─────────
    panel_a_content_w = a["panel_a_w"] - 2 * a["panel_pad_x"]
    panel_b_content_w = a["panel_w"]   - 2 * a["panel_pad_x"]
    panel_c_content_w = a["panel_c_w"] - 2 * a["panel_pad_x"]

    # ── Column centred x-offsets (from panel NW) ─────────────────────────
    a_col_l_x =  a["panel_pad_x"] + panel_a_content_w  * a["a_col_left_frac"]
    a_col_r_x =  a["panel_pad_x"] + panel_a_content_w  * a["a_col_right_frac"]
    
    b_col_l_x =  a["panel_pad_x"] + panel_b_content_w * a["b_col_left_frac"]
    b_col_m_x =  a["panel_pad_x"] + panel_b_content_w * a["b_col_mid_frac"]
    b_col_r_x =  a["panel_pad_x"] + panel_b_content_w * a["b_col_right_frac"]

    c_col_l_x =  a["panel_pad_x"] + panel_c_content_w * a["c_col_left_frac"]
    c_col_m_x =  a["panel_pad_x"] + panel_c_content_w * a["c_col_mid_frac"]
    c_col_r_x =  a["panel_pad_x"] + panel_c_content_w * a["c_col_right_frac"]

    def fmt(v: float) -> str:
        return f"{v:.2f}"

    return {
        # ── Canvas ───────────────────────────────────────────────────────
        "CanvasW":              fmt(a["canvas_w"]),
        "CanvasH":              fmt(a["canvas_h"]),
        # ── Figure title ─────────────────────────────────────────────────
        "FigureTitleX":         fmt(a["title_x"]),
        "FigureTitleY":         fmt(a["title_y"]),
        # ── Panels geometry ───────────────────────────────────────────────
        "PanelsY":              fmt(a["panels_y"]),
        "PanelW":               fmt(a["panel_w"]),
        "PanelAW":              fmt(a["panel_a_w"]),
        "PanelCW":              fmt(a["panel_c_w"]),
        "PanelH":               fmt(a["panel_h"]),
        "PanelAx":              fmt(panel_a_x),
        "PanelBx":              fmt(panel_b_x),
        "PanelCx":              fmt(panel_c_x),
        # ── Interior padding ─────────────────────────────────────────────
        "PanelPadX":            fmt(a["panel_pad_x"]),
        "PanelPadY":            fmt(a["panel_pad_y"]),
        # ── Standard header offsets ───────────────────────────────────────
        "PanelHeaderX":         fmt(a["header_off_x"]),
        "PanelHeaderY":         fmt(a["header_off_y"]),
        "PanelSubtitleX":       fmt(a["subtitle_off_x"]),
        "PanelSubtitleY":       fmt(a["subtitle_off_y"]),
        # ── Interior card padding ────────────────────────────────────────
        "CardInnerSep":         fmt(a["card_inner_sep"]),
        # ── Content constraints (for \node text width= arguments) ─────────
        "PanelAContentW":       f"{panel_a_content_w:.2f}cm",
        "PanelAContentInnerW":  f"{panel_a_content_w - 2 * a['card_inner_sep']:.2f}cm",
        "PanelBContentW":       f"{panel_b_content_w:.2f}cm",
        "PanelBContentInnerW":  f"{panel_b_content_w - 2 * a['card_inner_sep']:.2f}cm",
        "PanelCContentW":       f"{panel_c_content_w:.2f}cm",
        "PanelCContentInnerW":  f"{panel_c_content_w - 2 * a['card_inner_sep']:.2f}cm",
        # Legacy aliases kept for backward compatibility
        "PanelContentW":        f"{panel_b_content_w:.2f}cm",
        "PanelContentInnerW":   f"{panel_b_content_w - 2 * a['card_inner_sep']:.2f}cm",
        # ── Card spacing ──────────────────────────────────────────────────
        "CardGap":              fmt(a["card_gap"]),
        # ── Card minimum heights (from _*_CARD_H, used for chained placement) ──
        "PanelBObjH":          f"{_B_CARD_H[1]:.2f}cm",
        "PanelCCombinedH":     f"{_C_COMBINED_H:.2f}cm",
        "PanelCHypH":          f"{_C_COMBINED_H:.2f}cm",   # compat alias
        "PanelCOutH":          f"{_C_OUT_H:.2f}cm",
        # ── Internal Slots (Y) ───────────────────────────────────────────
        "PanelAReqY":           fmt(a["a_req_y"]),
        "PanelAOptY":           fmt(a["a_optional_y"]),
        "PanelBFeatsY":         fmt(a["b_feats_y"]),
        "PanelBObjY":           fmt(a["b_obj_y"]),
        "PanelBOptY":           fmt(a["b_opt_y"]),
        "PanelCValY":           fmt(a["c_combined_y"]),   # kept for compat
        "PanelCCombinedY":      fmt(a["c_combined_y"]),
        "PanelCCombinedH":      f"{_C_COMBINED_H:.2f}cm",
        "PanelCOutY":           fmt(a["c_out_y"]),
        # ── Column slots (x-offsets from panel NW) ────────────────────────
        "PanelAColLeftX":       fmt(a_col_l_x),
        "PanelAColRightX":      fmt(a_col_r_x),
        "PanelBColLeftX":       fmt(b_col_l_x),
        "PanelBColMidX":        fmt(b_col_m_x),
        "PanelBColRightX":      fmt(b_col_r_x),
        "PanelCColLeftX":       fmt(c_col_l_x),
        "PanelCColMidX":        fmt(c_col_m_x),
        "PanelCColRightX":      fmt(c_col_r_x),
        # ── Column x-offsets relative to card NW (= ColX - PanelPadX) ────────
        "PanelBColLeftXRel":    fmt(b_col_l_x - a["panel_pad_x"]),
        "PanelBColMidXRel":     fmt(b_col_m_x - a["panel_pad_x"]),
        "PanelBColRightXRel":   fmt(b_col_r_x - a["panel_pad_x"]),
        "PanelCColLeftXRel":    fmt(c_col_l_x - a["panel_pad_x"]),
        "PanelCColMidXRel":     fmt(c_col_m_x - a["panel_pad_x"]),
        "PanelCColRightXRel":   fmt(c_col_r_x - a["panel_pad_x"]),
        # ── Routing ───────────────────────────────────────────────────────
        "FlowLaneY":            fmt(a["flow_lane_y"]),
        "InterPanelChevronY":   fmt(a["chevron_y"]),
        "InterPanelChevronSize": str(int(a["chevron_size"])),
    }


COMPONENT_MANIFEST: list[dict] = [
    {"name": "hdx_curves"},
    {"name": "heatmap_thumb"},
    {"name": "residue_peptide"},
    {"name": "weight_dist"},
    {"name": "timescale_bar"},
    {"name": "scorecard"},
    {"name": "tiny_bar_chart"},
    {"name": "tiny_sliders"},
]

COMPONENT_BASENAMES: tuple[str, ...] = tuple(c["name"] for c in COMPONENT_MANIFEST)


def ensure_output_dirs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    COMPONENTS_SVG_DIR.mkdir(parents=True, exist_ok=True)
    COMPONENTS_PDF_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_OUT_DIR.mkdir(parents=True, exist_ok=True)
    STAMPS_DIR.mkdir(parents=True, exist_ok=True)


def rgb01(color_name: str) -> tuple[float, float, float]:
    rgb = COLORS[color_name]
    return tuple(channel / 255.0 for channel in rgb)
