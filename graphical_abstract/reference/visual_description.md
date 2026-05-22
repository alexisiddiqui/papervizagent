# Verified & Updated TikZ Specification — jaxENT Workflow Figure

I cross-checked the spec against the image. The original is ~90% accurate but has several inaccuracies and omissions. Below is a corrected, reproduction-ready version. Notable corrections are flagged with **[FIX]** and additions with **[ADD]**.

---

## 0. Errors and oddities to reproduce *verbatim* from the source

The source figure contains spelling inconsistencies. These are to be fixed in the final output.

- Panel (b) bold subtitle: **"modular loses"** (should be "losses")
- Panel (b) step 1 header: **"Compute forward-model fatures per frame"** (should be "features")
- Panel (b) step 1 inline text: **"Residues,frames (x H-onds, contacts) →"** (should be "H-bonds"; also note comma-no-space and the trailing arrow inside the text)
- Panel (b) step 2 sublabel: **"(residue → peptide aggregation + correcion)"** (should be "correction")
- Panel (c) hypothesis testing left column: the word **"Candidate ensembles"** wraps awkwardly under the H-icons; "Cand**ʇ**date" appears slightly broken by an overlapping element in the source — render as plain "Candidate ensembles".

---

## 1. Overall composition

Wide landscape diagram, white background, strong left-to-right narrative.

- Canvas aspect ratio ≈ **2.23 : 1** (confirmed)
- Title block: top-left, **two lines**, occupies top ~10–12% of height, left-aligned to panel (a)'s left edge
- Three rounded panel containers fill the remaining ~80% height, all with **identical top and bottom edges**
- Two large dark chevrons between panels, vertically centered on panel mid-height
- One **dashed grey path** exits the bottom of panel (a), drops below the baseline of panel (b), rises into the **left edge of panel (c)** at roughly the vertical level *between* the Hypothesis-testing and Outputs cards **[FIX — original said it terminates at the weight-distribution thumbnail; in the source it enters the left side of (c) and does not visibly attach to a specific thumbnail]**

Horizontal width split (measured from source):
- Panel (a): ~38%
- Chevron 1: ~2.5%
- Panel (b): ~28%
- Chevron 2: ~2.5%
- Panel (c): ~27%
- Outer left/right margins: ~1.5%

---

## 2. Color palette (sampled from source)

| Element | Approx. hex |
|---|---|
| Panel (a) fill | very pale blue `#E8F0F7` |
| Panel (b) fill | pale lavender/pink `#EFE0EA` |
| Panel (c) fill | pale mint `#DCEAE0` |
| Internal cards | white `#FFFFFF` with thin charcoal border `#2A2A2A`, ~0.6pt |
| Step boxes (panel b) | white fill, **teal** border `#3FA9A2` |
| Objective box | white fill, **gold/amber** border `#E0B84A`, faint cream tint `#FBF3DC` |
| Optimise box | white fill, **coral** border `#E07A5F`, faint peach tint `#FBE7DE` |
| Chevrons | dark navy/charcoal `#1F2A37` |
| Candidate accent (teal) | `#2C8C84` |
| Target accent (coral) | `#E07A5F` |
| Dashed-optional border | medium grey `#7A7A7A`, dash pattern ~3pt on / 2pt off |
| Gradient bar | linear: teal `#2C8C84` → coral `#E07A5F` |

All Greek symbols (ω, β, ℒ) are **serif italic** in their accent color (coral for ω/β in the optimise box; gold for ℒ in the objective box).

---

## 3. Title

Two-line, bold sans-serif, dark navy `#1F2A37`, ~28pt, line-height ~1.1, left-aligned to panel (a)'s left edge:

> **jaxENT workflow for ensemble–experiment**
> **integration and hypothesis testing**

Note the **en-dash** in "ensemble–experiment", not a hyphen.

---

## 4. Panel (a) — Inputs

### 4.1 Header strip
- "(a)" bold, upper-left, ~14pt
- *timescale gap* centered italic grey, above the gradient bar
- **Gradient bar**: rounded rectangle, ~85% of panel width, height ~22pt, teal→coral horizontal gradient
  - Left text inside bar (white): **Candidate** (bold) " (fs–ns)" (regular)
  - Right text inside bar (white): **Target** (bold) " (ms–hours/days)" (regular)
- Below bar, centered italic grey: *Integration acts as a statistical connector*

### 4.2 "Required inputs" card

White rounded card occupying ~62% of panel height, centered.

Header centered at top: **Required inputs** (bold).

**Three-column horizontal layout inside:**

**Left column (Candidate side)**
- Label **Candidate** in teal, bold, ~14pt
- Below: protein ensemble icon (multiple overlapping translucent grey ribbon silhouettes — supplied externally)
- Below icon, bold: **Structural ensembles**
- Sublabel grey: "(e.g., MD, AF2 subsampling)"
- Bullet list (no bullets, plain stacked lines, slightly indented):
  - Molecular Dynamics
  - AlphaFold2 + MSA subsampling
  - Enhanced sampling / clustering

**Center column (bridge)**
- Small rounded rectangle, white fill, **teal border** ~0.8pt, slightly taller than wide
- Contents stacked, centered:
  - **Forward model** (bold)
  - **BV (β_h, β_c, ω)** — β and ω serif italic, subscripts serif italic
  - "(Best–Vendruscolo)" small grey, en-dash
- **Two short black arrows** at the column's vertical mid-line: one entering from the left (from ensemble icon), one exiting right (to plot). Arrows are thin with small filled arrowheads.

**Right column (Target side)**
- Label **Target** in coral, bold, ~14pt
- Below: small Cartesian plot
  - y-axis label rotated 90°: "HDX uptake"
  - x-axis label: "time"
  - 4–5 smooth monotone-rising curves in distinct colors (teal, coral, gold, lavender, olive)
  - No axis ticks/numbers
- Below plot, bold: **Experimental data**
- Sublabel grey: "(e.g., HDX-MS uptake curves)"
- Then on separate stacked lines:
  - "or"
  - "or NMR Protection Factors"
  
  **[ADD — both lines literally begin with "or" in the source; this is unusual but should be reproduced]**

### 4.3 Optional dashed box
- Wide shallow rounded rectangle, ~85% panel width, height ~32pt
- Dashed medium-grey border, no fill (or very faint cream-grey)
- Centered text: **Optional**: orthogonal data for cross-validation ("Optional:" bold)
- A **dashed grey arrow** exits the right edge, drops a small amount, then runs horizontally rightward (see §7)

---

## 5. Panel (b) — jaxENT engine

### 5.1 Header
- "(b)" bold upper-left
- Centered subtitle, regular weight: **compute → predict → objective → optimise** (the arrows are literal "→" glyphs)
- Centered bold below: **autodiff + JIT + modular losses** [sic]

### 5.2 Step 1 — Compute features (teal-bordered white box)
- Header bold left-aligned: **Compute forward-model features per frame** [sic]
- Inside body: small **heatmap mosaic** (irregular grid of teal/blue cells, ~6×3, varying saturation) at left
- To the right of heatmap, regular text: "Residues,frames (x H-bonds, contacts) →" [sic]
- Downward thin arrow exits bottom-center

### 5.3 Step 2 — Predict uptake curves (teal-bordered white box)
- Header bold left-aligned: **Predict uptake curves**
- Sublabel grey beneath header: "(residue → peptide aggregation + correction)" [sic]
- Right-side mini schematic:
  - Word "residue" with a small smooth coral/teal line beneath it
  - Word "peptide" with a slightly rougher aggregated coral line beneath it
  - A small curved arrow connecting residue → peptide
- Downward arrow exits bottom-center

### 5.4 Step 3 — Define Objective (gold-bordered, faint cream-tinted box)
- Header bold left-aligned: **Define Objective**
- Centered formula, with proper spacing and visual emphasis on terms:

  **ℒ = Target Reconstruction (Error)  +  MaxEnt (Work)  +  Priors/Constraints**
  
  - ℒ in **gold serif italic**, slightly larger
  - "MaxEnt (Work)" sits inside a **subtle pale-gold rounded pill highlight**
  - "Priors/Constraints" appears as plain text aligned with the icon cluster on the right
- Beneath formula, italic grey, left-aligned under "MaxEnt": *Regularisation*
- **Upper-right icon cluster** [ADD — the original spec was vague]:
  - Three small text labels in a row: "error", "work", "cons" (truncated)
  - Below them, a small **funnel/triangle graphic** (lines converging downward)
  - To the right of the funnel, a **dark grey gear/cog icon**
  - These represent the three loss terms being combined
- **Two small variant boxes side-by-side** at the bottom of the objective block:
  - Left: white, thin border — **Error + Work** (bold) / "(baseline)" (grey small)
  - Right: white, thin border — **Error + Constraints + Work** (bold) / "(physics/knowledge)" (grey small)
- Downward arrow exits bottom-center

### 5.5 Step 4 — optimise (coral-bordered, faint peach-tinted box)
- Header bold lowercase left-aligned: **optimise**
- Two horizontal symbol-text groups, evenly spaced:

  **Left group:**
  - Large coral serif italic **ω**
  - Tiny coral 3-bar chart icon immediately right of ω
  - Label right of icon: **frame weights** (bold, two lines if needed)

  **Right group:**
  - Large coral serif italic **β**
  - Tiny 2-track slider icon (horizontal lines with circular knobs) right of β
  - Label right of icon: **forward-model parameters** (bold)

- Below both groups, centered italic grey: *Simultaneous fitting of weights and parameters*
- At the **bottom of the box**, three rounded pill badges centered horizontally with equal spacing:
  - **autodiff** — pale teal fill, teal border, dark text
  - **JIT** — pale teal fill, teal border, dark text
  - **Extensible** — pale teal fill, teal border, dark text
  
  All three pills have the same height; "Extensible" is naturally wider.

---

## 6. Panel (c) — Validation, scoring, outputs

### 6.1 Header
- "(c)" bold upper-left
- Centered subtitle: **quantifying robustness**

### 6.2 Validation card (top)
- White rounded card
- Header centered bold: **Validation (built-in)**
- One row of three sub-boxes, evenly spaced:
  1. Solid thin border: "Split types / Replicates" (two lines)
  2. Solid thin border: "Robust success metrics" (two lines)
  3. **Dashed border**: "Cross-validation (orthogonal data)" (two lines)
- Below row, centered italic grey: *Prevent overfitting; quantify uncertainty*

### 6.3 Hypothesis testing card (middle, slightly tallest)
- White rounded card
- Header centered bold: **Hypothesis testing & model selection**

Three-column internal layout:

**Left — Candidate hypotheses**
- Three small protein-silhouette thumbnails stacked vertically:
  - Top: teal-tinted, label right: **H₁ (0%)**
  - Middle: coral-tinted, label right: **H₂ (85%)**
  - Bottom: lavender-tinted, label right: **H₃ (15%)**
- Subscripts are serif italic numerals
- Below the stack, plain text: "Candidate ensembles"

**Center — Scorecard**
- Bordered table, **pale lavender internal tint**, header bar at top
- Title in header bar, lowercase italic-feeling: **scorecard**
- Four rows, left-aligned text:
  1. Work_{KLD}
  2. Work_{Scale..}  (note the trailing two dots — truncation in source)
  3. held-out error
  4. Replicate Uncertainty
- Subscripts on "Work" are serif italic

**Right — Best hypothesis**
- Single larger protein silhouette inside a rounded box with **thick gold border** (~1.5pt) and very faint gold tint
- Below or beside the protein, bold: **Best hypothesis**

**Connectors:** thin black arrow from candidate-stack region → scorecard; thin black arrow from scorecard → best hypothesis box.

### 6.4 Outputs card (bottom)
- White rounded card
- Header centered bold: **Outputs** (bold) followed by "(interpretable)" (regular weight, same size)
- Three evenly-spaced thumbnail columns:

  **Left — weight distribution**
  - Symbol above (centered): **ω** (coral serif italic)
  - Mini chart: teal histogram bars with overlaid smooth teal density curve
  - Label below (bold): **weight distribution**

  **Middle — fitted parameters**
  - Symbol above: **β, ω** (coral serif italic, comma-separated)
  - Mini graphic: 2–3 horizontal coral slider tracks with circular knobs at varying positions
  - Label below (bold): **fitted parameters**

  **Right — residue-level Work done**
  - No symbol above (or a small implicit one)
  - Graphic: protein cartoon silhouette with grayscale-mapped surface regions
  - Narrow vertical black-to-white gradient strip immediately to the right of the protein (colorbar)
  - Label below: **residue-level *Work* done** ("Work" in italic)

---

## 7. Chevrons and the dashed optional path

### 7.1 Chevrons
- Two large filled chevrons (`>` shape), dark navy `#1F2A37`
- Height ≈ 35% of panel height
- Vertically centered on the panel mid-line
- Sit in the gaps between (a)|(b) and (b)|(c)

### 7.2 Dashed optional path **[FIX — corrected routing]**
- Origin: **right edge of the Optional dashed box** in panel (a), at its vertical midline
- Path: short rightward segment → drops down ~15pt → long horizontal segment running **below the bottom edge of panel (b)** (entirely outside (b)) → rises back up → enters **left edge of panel (c)** at a height roughly **between the Hypothesis-testing card and the Outputs card** (i.e., not at any specific thumbnail)
- Style: medium grey, dashed (~3pt on / 2pt off), thin filled arrowhead at terminus
- Crosses *under* chevron 2 visually but is drawn behind chevrons (z-order matters)

---

## 8. Drawing order (z-order, back to front)

1. White background
2. Three outer panel containers (rounded rects with colored fills)
3. Title text
4. Panel labels (a), (b), (c) and centered subtitles
5. Gradient bar in panel (a) and its associated italic captions
6. Large white internal cards (Required inputs, Validation, Hypothesis testing, Outputs)
7. Step boxes inside panel (b) — Compute, Predict, Objective, Optimise
8. **Dashed optional path** (drawn before chevrons so chevrons sit on top)
9. Two chevrons between panels
10. Internal mini-graphics (heatmap, plot, sliders, histograms, gear, funnel, scorecard table, protein silhouettes/colorbar)
11. All text labels (headers, sublabels, formulas, list items)
12. Pill badges (autodiff / JIT / Extensible) and gold-border emphasis on Best hypothesis
13. Internal arrows (process arrows last so they sit cleanly on top of borders)

---

## 9. Primitive inventory for TikZ

Define these as reusable styles/macros:

| Primitive | Style key |
|---|---|
| `panelA`, `panelB`, `panelC` | rounded rect, ~12pt corner radius, thin charcoal border, tinted fill |
| `whiteCard` | white fill, charcoal border 0.6pt, 8pt corner |
| `tealStep` | white fill, teal border 0.8pt, 6pt corner |
| `goldObjective` | cream tint, gold border 1.0pt, 8pt corner |
| `coralOptimise` | peach tint, coral border 1.0pt, 8pt corner |
| `dashedBox` | no fill, grey dashed border, 6pt corner |
| `chevron` | filled path `(0,0) -- (1,0.5) -- (0,1) -- (0.3,0.5) -- cycle` scaled, navy fill |
| `procArrow` | `-{Latex[length=4pt]}`, thin |
| `dashedArrow` | grey, dashed, `-{Latex[length=4pt]}` |
| `pill` | rounded rect, 50% corner, teal stroke, pale-teal fill |
| `gradBar` | rounded rect with `\shade` left=teal, right=coral |
| `miniPlot`, `miniHist`, `miniSliders`, `miniHeatmap`, `miniScorecard`, `miniGear`, `miniFunnel` | TikZ subpictures |
| Protein silhouettes | external `\includegraphics` placeholders (supplied separately) |

---

## 10. Summary of corrections from original spec

1. **Dashed-path terminus** — corrected: enters left edge of panel (c) between cards, not the weight-distribution thumbnail.
2. **Source typos preserved** — added explicit list (loses, fatures, H-onds, correcion).
3. **"or NMR Protection Factors" double "or"** — clarified it really is two stacked lines both starting with "or" in the source.
4. **Objective icon cluster** — clarified as funnel + gear with three labels (error/work/cons), not "arrows converging into a blue gear" (gear is dark grey, not blue).
5. **Color palette** — added concrete hex sample values.
6. **Z-order** — clarified dashed path goes behind chevrons.
7. **Scorecard "Work_Scale.."** — kept the literal trailing dots from the source.
8. **Title em-dash vs hyphen** — flagged en-dash explicitly.
9. **Chevron geometry & size** — quantified.
10. **"optimise" lowercase header** — preserved British spelling and lowercase as in source.

This should be sufficient to render a faithful TikZ reproduction once protein silhouettes are dropped in as `\includegraphics` placeholders.