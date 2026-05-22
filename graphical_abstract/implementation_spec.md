# Implementation Specification: Reference-Convergence Runbook

This document is the iteration-time authority for reproducing the reference figure as a faithful, publication-grade schematic.

- `implementation_spec.md` (this file) = layout contracts, convergence checks, and acceptance gates.

Use this file during every layout iteration.

---

## 1) Scope, goals, and non-goals

### Scope

1. Define deterministic layout contracts for panels (a), (b), and (c).
2. Lock text wrapping, typography hierarchy, arrow routing, and asset usage rules.
3. Define convergence QA gates and an explicit done definition.
4. Align build/dependency expectations with the current workspace state.

### Goal

Recreate the composition and visual hierarchy of `reference/prompt_1_opus_5.png` without undocumented placement decisions during implementation.

### Explicit non-goals

1. No automated pixel-diff threshold tooling in this phase.
2. No re-authoring of protein renders into vector drawings.
3. No expansion of scientific content beyond the reference prompt.

---

## 2) Current workspace baseline (authoritative as of now)

### Files currently present

| Path | Status |
|---|---|
| `graphical_abstract/implementation_plan.md` | Present |
| `graphical_abstract/reference/prompt_1_opus_5.md` | Present |
| `graphical_abstract/reference/prompt_1_opus_5.png` | Present |
| `graphical_abstract/inputs/renders/H1.png` | Present |
| `graphical_abstract/inputs/renders/H2.png` | Present |
| `graphical_abstract/inputs/renders/H3.png` | Present |
| `graphical_abstract/inputs/renders/H4.png` | Present |
| `graphical_abstract/inputs/renders/projected_error.png` | Present |
| `graphical_abstract/inputs/renders/structural_hypothesis.png` | Present |
| `graphical_abstract/inputs/renders/structural_hypothesis_BW.png` | Present |
| `graphical_abstract/inputs/bw_scale.jpg` | Present |
| `graphical_abstract/inputs/gw_scale.jpg` | Present |

### Empty-but-required directories

- `graphical_abstract/scripts/`
- `graphical_abstract/tikz/`
- `graphical_abstract/outputs/`

### Missing implementation artifacts (to create)

- `graphical_abstract/scripts/config.py`
- `graphical_abstract/scripts/01_process_renders.py`
- `graphical_abstract/scripts/02_generate_components.py`
- `graphical_abstract/scripts/03_compile_figure.py`
- `graphical_abstract/tikz/figure.tex`
- `graphical_abstract/tikz/styles.tex`
- `graphical_abstract/tikz/panels/panel_a.tex`
- `graphical_abstract/tikz/panels/panel_b.tex`
- `graphical_abstract/tikz/panels/panel_c.tex`
- `graphical_abstract/tikz/asset_paths.tex` (generated)
- `graphical_abstract/Makefile`

---

## 3) Non-functional requirements (iteration constraints)

1. **Performance:** Full rebuild target < 10 minutes on one local machine.
2. **Determinism:** Same inputs + same config produce byte-stable asset geometry and text layout.
3. **Reliability:** Fail fast on missing assets, missing fonts, or broken anchors.
4. **Security/Privacy:** Local-only processing of figure assets; no external upload dependency.
5. **Maintenance:** One maintainer can rerun and converge from this spec without undocumented tribal knowledge.

---

## 4) Decision log

| ID | Decision | Alternatives considered | Why chosen |
|---|---|---|---|
| D1 | Hybrid layout authority (absolute panel frames + anchor-based internals) | Fully absolute; fully relative | Keeps global composition fixed while allowing maintainable local anchors |
| D2 | Keep convergence spec in separate file | Put all details into `implementation_plan.md` | Reduces per-iteration context load and preserves plan readability |
| D3 | Convergence requires checklist pass + manual overlay approval | Checklist-only; overlay-only | Prevents false positives from either method alone |
| D4 | No automated pixel-diff threshold in this phase | Add pixel-diff gate now | Lower tooling burden while preserving review quality |
| D5 | Protein renders stay raster; generated components are vector-first | Vectorize proteins; raster everything | Matches asset reality and keeps plot/icons publication-sharp |

---

## 5) Layout authority contract

### 5.0 Robust-tuning implementation contract (current code)

The implementation must enforce these rules during every layout edit:

1. **Single geometry authority:** all tunable layout values live in `graphical_abstract/tikz/styles.tex` (canvas, panel positions, insets, content widths, module gaps, title position, chevron Y, flow-lane Y, and panel-A offsets). Do not introduce hard-coded magic numbers in panel files when a shared token is appropriate.
2. **Panel-local anchor framework:** panel internals must be placed from panel-local anchors (e.g., `a_inner_nw`, `b_inner_nw`, `c_inner_nw`) plus shared spacing constants.
3. **Inter-panel flow placement:** chevrons must be derived from panel-gap midpoints and projected onto a shared y-reference (`\InterPanelChevronY`), not manually placed with absolute x-values.
4. **Optional-route lane lock:** the dashed optional path must route through a dedicated global lane (`\FlowLaneY`) below panel B and terminate at `c3_thumb_weightdist`.
5. **Coordinate convention guardrail:** TikZ is rendered with `y=-1cm`; increasing y moves downward. Every vertical offset decision must follow this convention.
6. **Render-safety guardrail:** keep `standalone` border padding on the figure and retain extra `timescale_bar` export padding in `scripts/02_generate_components.py` to prevent top-edge clipping in PNG exports.

## 5.1 Coordinate system and panel frames

- Units: centimeters.
- Origin: top-left of figure canvas.
- +x goes right, +y goes down.

| Token | Value |
|---|---|
| `CANVAS_W` | 28.00 |
| `CANVAS_H` | 13.00 |
| `MARGIN_LEFT` | 0.60 |
| `MARGIN_RIGHT` | 0.70 |
| `TITLE_BAND_H` | 1.05 |
| `PANELS_Y` | 1.60 |
| `PANEL_W` | 8.50 |
| `PANEL_H` | 10.70 |
| `PANEL_GAP` | 0.60 |
| `FLOW_LANE_Y` | 11.85 |

Panel frame rectangles (absolute):

| Panel | x | y | w | h |
|---|---:|---:|---:|---:|
| A | 0.60 | 1.60 | 8.50 | 10.70 |
| B | 9.70 | 1.60 | 8.50 | 10.70 |
| C | 18.80 | 1.60 | 8.50 | 10.70 |

### 5.2 Global spacing and corner tokens

| Token | Value |
|---|---|
| `RADIUS_PANEL` | 8 pt |
| `RADIUS_BOX` | 8 pt |
| `RADIUS_PILL` | 10 pt |
| `GAP_BLOCK` | 0.35 cm |
| `GAP_ROW` | 0.25 cm |
| `GAP_COL` | 0.30 cm |
| `INNER_PAD` | 0.15 cm |
| `LANE_CLEARANCE_MIN` | 0.35 cm |

### 5.3 Typography tokens (enforceable)

| Token | Font family | Size | Weight/shape | Use |
|---|---|---:|---|---|
| `t_figure_title` | Helvetica/Arial (sans) | 16 pt | bold | Global title |
| `t_panel_label` | Helvetica/Arial (sans) | 14 pt | bold | `(a)`, `(b)`, `(c)` |
| `t_panel_header` | Helvetica/Arial (sans) | 14 pt | bold | Panel headers |
| `t_module_title` | Helvetica/Arial (sans) | 12 pt | bold | Module titles |
| `t_step` | Helvetica/Arial (sans) | 9-10 pt | regular | Step labels |
| `t_annotation` | Helvetica/Arial (sans) | 8-9 pt | italic | Small notes |
| `t_math_var` | Helvetica/Arial (sans) | 10 pt | italic | `omega`, `beta`, `L`, subscripts |
| `t_equation_text` | Helvetica/Arial (sans) | 10 pt | regular | Non-math equation words |

**Rule:** all mathematical symbols and text use Helvetica (sans-serif) for visual consistency.

### 5.4 Text-wrap lock policy

1. All multiline labels must use explicit line breaks in source (`\\` in TikZ).
2. No auto-wrap-based reflow is permitted during convergence.
3. Any text change requires:
   - update of the locked-text table in this spec,
   - re-check of Gate B (typography/text fidelity).

Locked strings with required line breaks:

| Text ID | Locked content |
|---|---|
| `title_main` | `jaxENT workflow for ensemble-experiment integration\\and hypothesis testing` |
| `a_required_title` | `Required inputs` |
| `a_optional_title` | `Optional: orthogonal data for\\cross-validation` |
| `b_subtitle` | `compute -> predict -> objective -> optimise` |
| `c_subtitle` | `quantifying robustness` |
| `c_validation_note` | `Prevent overfitting; quantify uncertainty` |

### 5.5 Protected routing lanes

1. `FLOW_LANE_Y` is reserved for the dashed optional-data route.
2. No step-box, badge, or thumbnail may cross into `y >= FLOW_LANE_Y - LANE_CLEARANCE_MIN` in panel B.
3. Cross-panel dashed path must remain orthogonal and stay in this lane until the upward turn in panel C.

---

## 6) Per-panel element manifests (authoritative)

Format:
- `Anchor rule`: deterministic placement relation.
- `Size`: fixed width x height in cm (unless `auto`).
- `Style`: style token from plan/styles.
- `Connector IDs`: outgoing/incoming connectors that must attach to this element.

## 6.1 Panel A manifest

| Element ID | Parent | Anchor rule | Size | Style | Connector IDs |
|---|---|---|---|---|---|
| `a_label` | `panel_A` | `panel_A.nw + (0.20, 0.25)` | auto | `t_panel_label` | - |
| `a_header` | `panel_A` | left baseline at `a_label.e + (0.20, 0.00)` | auto | `t_panel_header` | - |
| `a_required_box` | `panel_A` | top-left `panel_A.nw + (0.35, 0.95)` | 7.80 x 6.80 | `stepbox` | `a_req_to_b_entry` |
| `a_timescale_bar` | `a_required_box` | center at `a_required_box.n + (0.00, 0.55)` | 5.00 x 0.60 | image/plot | - |
| `a_candidate_group` | `a_required_box` | center at `a_required_box.w + (1.65, 3.25)` | 2.20 x 3.20 | mixed (icon + text) | `a_candidate_to_forward` |
| `a_forward_model_box` | `a_required_box` | center at `a_required_box.center + (0.00, 0.20)` | 2.10 x 1.25 | `tealbox` | `a_candidate_to_forward`, `a_forward_to_target`, `a_req_to_b_entry` |
| `a_target_group` | `a_required_box` | center at `a_required_box.e + (-1.65, 3.25)` | 2.35 x 3.20 | mixed (plot + text) | `a_forward_to_target` |
| `a_optional_box` | `panel_A` | top-left `a_required_box.sw + (0.00, 0.40)` | 7.80 x 2.25 | `optbox` | `a_optional_to_c_weightdist` |
| `a_optional_anchor_out` | `a_optional_box` | midpoint on east edge | auto | anchor | `a_optional_to_c_weightdist` |

Panel A content constraints:

1. Three-group required-input layout must remain left/center/right with the forward model exactly centered between candidate and target groups.
2. Candidate and target group centers must be horizontally symmetric around `a_forward_model_box.center.x`.
3. Optional box is below required box; no overlap with required content.

## 6.2 Panel B manifest

| Element ID | Parent | Anchor rule | Size | Style | Connector IDs |
|---|---|---|---|---|---|
| `b_label` | `panel_B` | `panel_B.nw + (0.20, 0.25)` | auto | `t_panel_label` | - |
| `b_header` | `panel_B` | left baseline at `b_label.e + (0.20, 0.00)` | auto | `t_panel_header` | - |
| `b_subtitle_text` | `panel_B` | top-left `panel_B.nw + (0.55, 0.90)` | 7.20 x auto | `t_annotation` | - |
| `b_stack_note` | `b_stack_box` | bottom-center `b_stack_box.n + (0.00, -0.05)` | auto | `t_annotation` | - |
| `b_stack_box` | `panel_B` | top-left `panel_B.nw + (0.35, 1.45)` | 7.80 x 3.20 | invisible container | `b_s1_to_s2`, `b_s2_to_obj` |
| `b_step1` | `b_stack_box` | center at `b_stack_box.n + (0.00, 0.80)` | 7.10 x 1.25 | `tealbox` | `b_s1_to_s2` |
| `b_step2` | `b_stack_box` | center at `b_step1.s + (0.00, 0.95)` | 7.10 x 1.25 | `tealbox` | `b_s2_to_obj` |
| `b_objective_box` | `panel_B` | top-left `b_stack_box.sw + (0.00, 0.35)` | 7.80 x 2.55 | `goldbox` | `b_s2_to_obj`, `b_obj_to_opt` |
| `b_obj_branch_left` | `b_objective_box` | bottom-left `b_objective_box.sw + (0.30, -0.30)` | 3.45 x 0.85 | `stepbox` | - |
| `b_obj_branch_right` | `b_objective_box` | bottom-right `b_objective_box.se + (-0.30, -0.30)` | 3.45 x 0.85 | `stepbox` | - |
| `b_optimise_box` | `panel_B` | top-left `b_objective_box.sw + (0.00, 0.35)` | 7.80 x 2.10 | `coralbox` | `b_obj_to_opt`, `b_to_c_main` |
| `b_badge_row` | `b_optimise_box` | centered at `b_optimise_box.s + (0.00, -0.35)` | 5.10 x 0.45 | `pill` | - |

Panel B constraints:

1. Internal flow is strictly top-to-bottom.
2. Internal arrows are orthogonal/elbow style.
3. Lowest point of `b_optimise_box` content must satisfy `y <= FLOW_LANE_Y - 0.70`.

## 6.3 Panel C manifest

| Element ID | Parent | Anchor rule | Size | Style | Connector IDs |
|---|---|---|---|---|---|
| `c_label` | `panel_C` | `panel_C.nw + (0.20, 0.25)` | auto | `t_panel_label` | - |
| `c_header` | `panel_C` | left baseline at `c_label.e + (0.20, 0.00)` | auto | `t_panel_header` | - |
| `c_subtitle_text` | `panel_C` | top-left `panel_C.nw + (0.55, 0.90)` | 7.20 x auto | `t_annotation` | - |
| `c_validation_box` | `panel_C` | top-left `panel_C.nw + (0.35, 1.45)` | 7.80 x 2.30 | `stepbox` | `c_val_to_score` |
| `c_scoring_box` | `panel_C` | top-left `c_validation_box.sw + (0.00, 0.35)` | 7.80 x 3.30 | `stepbox` | `c_val_to_score`, `c_score_to_best` |
| `c_outputs_box` | `panel_C` | top-left `c_scoring_box.sw + (0.00, 0.35)` | 7.80 x 2.20 | `stepbox` | `c_score_to_best`, `a_optional_to_c_weightdist` |
| `c3_thumb_weightdist` | `c_outputs_box` | center at `c_outputs_box.nw + (1.55, 1.30)` | 2.05 x 1.50 | vector icon | `a_optional_to_c_weightdist` |
| `c3_thumb_params` | `c_outputs_box` | center at `c_outputs_box.nw + (3.90, 1.30)` | 2.05 x 1.50 | vector icon | - |
| `c3_thumb_struct` | `c_outputs_box` | center at `c_outputs_box.nw + (6.25, 1.30)` | 2.05 x 1.50 | raster icon | - |
| `c_best_hypothesis` | `c_scoring_box` | right-side anchor `c_scoring_box.e + (-1.40, 0.20)` | 2.20 x 2.20 | `goldborder` | `c_score_to_best` |

Panel C constraints:

1. Validation -> scoring -> outputs stack remains vertically ordered with fixed block gaps.
2. Dashed optional-data route must terminate at `c3_thumb_weightdist` (not any other thumbnail).
3. Best-hypothesis highlight border color is reserved (`#D4A017`) and not reused for generic boxes.

---

## 7) Connector manifest (routing verification)

| Connector ID | Type | Source anchor | Target anchor | Route contract |
|---|---|---|---|---|
| `a_candidate_to_forward` | internal solid | `a_candidate_group.e` | `a_forward_model_box.w` | straight |
| `a_forward_to_target` | internal solid | `a_forward_model_box.e` | `a_target_group.w` | straight |
| `a_req_to_b_entry` | inter-panel main | `a_required_box.e` | `b_stack_box.w` | thick chevron/short straight |
| `b_s1_to_s2` | internal solid | `b_step1.s` | `b_step2.n` | orthogonal |
| `b_s2_to_obj` | internal solid | `b_step2.s` | `b_objective_box.n` | orthogonal |
| `b_obj_to_opt` | internal solid | `b_objective_box.s` | `b_optimise_box.n` | orthogonal |
| `b_to_c_main` | inter-panel main | `b_optimise_box.e` | `c_validation_box.w` | thick chevron/short straight |
| `c_val_to_score` | internal solid | `c_validation_box.s` | `c_scoring_box.n` | orthogonal |
| `c_score_to_best` | internal solid | `c_scoring_box.center` | `c_best_hypothesis.w` | straight |
| `a_optional_to_c_weightdist` | auxiliary dashed | `a_optional_anchor_out` | `c3_thumb_weightdist.s` | 3 segments: down to `FLOW_LANE_Y`, horizontal in lane, up to target |

Hard checks for `a_optional_to_c_weightdist`:

1. Horizontal segment y-coordinate must equal `FLOW_LANE_Y`.
2. Horizontal segment must remain outside panel B step-box bounding boxes.
3. The arrowhead must visibly touch `c3_thumb_weightdist`.

---

## 8) Asset policy: raster vs vector (locked)

## 8.1 Protein visuals (raster only)

Protein-based visuals remain image assets (PNG workflow):

- Hypothesis proteins (`H1..H4`)
- Ensemble stack render
- Structural mapping thumbnail (`structural_hypothesis*.png`)
- Projected-error thumbnail when sourced from render

Allowed transforms:

1. Background removal to alpha.
2. Uniform crop/pad/canvas normalization.
3. Uniform scaling to fixed target sizes.
4. Controlled tinting and alpha compositing.

Disallowed transforms:

1. Manual vector tracing or re-drawing of protein geometry.
2. Freeform shape edits that alter protein silhouette.
3. Inconsistent per-hypothesis style grammar.

## 8.2 Generated chart/icon components (vector-first)

Matplotlib-generated components must be vector outputs first:

- primary: SVG
- publication inclusion path: PDF export from the same source figure

Required vector-first outputs:

- `timescale_bar`
- `hdx_curves`
- `heatmap_thumb`
- `residue_peptide`
- `weight_dist`
- small algorithmic iconography generated in plotting scripts

---

## 9) Convergence QA gates and acceptance criteria

All gates marked **mandatory** must pass before done.

## Gate A - Structural/layout fidelity (mandatory)

Checklist:

1. Panel frames match Table 5.1 coordinates and dimensions.
2. All major block sizes match manifest values.
3. No overlap between major containers.
4. Inter-panel chevrons attach to declared source/target modules.

Pass condition: all items pass.

## Gate B - Text and typography fidelity (mandatory)

Checklist:

1. Locked text strings match exactly (including line breaks).
2. Typography token assignments match Section 5.3.
3. Math symbols (`omega`, `beta`, `L`, subscripts) are serif italic.
4. No clipping/overflow in boxed text.

Pass condition: all items pass.

## Gate C - Connector and routing fidelity (mandatory)

Checklist:

1. Connector IDs match Section 7 source/target anchors.
2. Panel B internal chain uses orthogonal routing.
3. Dashed cross-panel route stays in protected lane and does not intersect panel B boxes.
4. Dashed route terminates at `c3_thumb_weightdist`.

Pass condition: all items pass.

## Gate D - Readability/accessibility QA (mandatory)

Checklist:

1. Grayscale review preserves hierarchy (not color-only semantics).
2. Colorblind review preserves distinction of active/process/highlight roles.
3. Best-hypothesis emphasis remains legible without relying only on hue.
4. Optional-path semantics remain clear via dashed style even in grayscale.

Pass condition: all items pass.

## Gate E - Overlay convergence review (mandatory)

Procedure:

1. Export candidate figure PNG at final dimensions.
2. Overlay with `reference/prompt_1_opus_5.png` at matched scale.
3. Review composition alignment: panel geometry, major blocks, labels, and route paths.
4. Mark each panel as pass/fail for composition similarity.

Pass condition:

1. Overlay review approved by maintainer.
2. No major composition mismatch in any panel.
3. Mandatory gates A-D already passing.

---

## 10) Done definition

The figure is **done** only when:

1. Gates A-E all pass.
2. Asset policy in Section 8 is respected.
3. No unresolved layout exceptions remain.
4. Build/dependency manifest in Section 11 is satisfied in workspace.

If any mandatory gate fails, convergence is not complete.

---

## 11) Corrected dependency manifest (workspace-aligned)

## 11.1 Input normalization contract

Current input filenames are uppercase (`H1.png`, `H2.png`, `H3.png`, `H4.png`).
Processing scripts must either:

1. accept these names directly, or
2. map them to canonical internal IDs (`h1`, `h2`, `h3`, `h4`) explicitly.

No hidden filename assumptions are allowed.

## 11.2 Stage dependencies

| Stage | Inputs | Outputs | Re-run when |
|---|---|---|---|
| S1 `01_process_renders.py` | `inputs/renders/*.png` proteins + render thumbnails | `outputs/processed/*.png` | render source or tint/crop config changes |
| S2 `02_generate_components.py` | S1 outputs + chart settings | `outputs/components/svg/*.svg` and `outputs/components/pdf/*.pdf` | plot data/style changes |
| S3 `03_compile_figure.py` | S1 + S2 outputs + `tikz/*.tex` | `outputs/figure/jaxent_figure.pdf` (+ optional PNG export) | layout/text/style/asset-path changes |

## 11.3 Iterative rebuild policy

1. Layout-only edits: rerun S3 only.
2. Chart styling/data edits: rerun S2 then S3.
3. Protein render/tint edits: rerun S1 then downstream stages.
4. Full clean rebuild for release candidate: S1 -> S2 -> S3.

---

## 12) Iteration protocol (how to use this spec each cycle)

1. Make one bounded layout/content change set.
2. Rebuild only required stages (Section 11.3).
3. Evaluate Gates A-C first; fix hard layout/routing issues.
4. Evaluate Gate D (grayscale + colorblind checks).
5. Run Gate E overlay review.
6. Record gate outcomes in your change notes before next iteration.

This protocol is mandatory for convergence tracking.
