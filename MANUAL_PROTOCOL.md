# PaperVizAgent — Manual Protocol
### *How to run the full 5-agent pipeline by hand in the Gemini chat interface*

> **Why this works**: Every "agent" in this repo is just a carefully crafted system prompt + user
> prompt sent to Gemini. No API calls are strictly necessary — you can replicate every step by
> pasting the prompts below into [gemini.google.com](https://gemini.google.com).

---

## What you need before starting

| Item | How to get it |
|---|---|
| **Method/Results section text** | Copy from your LaTeX source or PDF |
| **Figure caption** | The caption of the figure you want to create |
| **1–3 reference figures** (optional but recommended) | Screenshots from papers with similar diagram styles |
| **Style guide** | Copy the text in `style_guides/neurips2025_diagram_style_guide.md` |

---

## Overview of the Pipeline

```
[You] → Step 1: Retriever  → pick reference figures manually
         Step 2: Planner   → Gemini writes a detailed description
         Step 3: Stylist   → Gemini refines the aesthetics
         Step 4: Visualizer → Gemini generates the image
         Step 5: Critic    → Gemini critiques it → loop back to Step 4
```

Minimum viable version (no references available): **Steps 2 → 4 → 5**.
Best quality: **Steps 1 → 2 → 3 → 4 → 5**, with 2–3 critic rounds.

---

## Step 1 — Retriever (Manual Reference Selection)

The Retriever agent's job is to find the most visually similar figures from a reference pool.
Since you don't have the dataset, **do this manually**:

1. Think about what style of diagram you need. Ask yourself:
   - What is the domain? (Agent/LLM paper, CV, Theoretical, etc.)
   - What is the structure? (Pipeline, comparison table, attention map, loop, etc.)
2. Find **2–5 reference figures** from papers you admire by:
   - Searching [Papers With Code](https://paperswithcode.com) or [Semantic Scholar](https://semanticscholar.org)
   - Looking at recent NeurIPS/ICLR/ICML papers in your domain
   - Saving screenshots or downloading figure images
3. Keep these images ready — you will upload them in Steps 2 & 3.

> **Tip**: If you have no references, you can skip Step 1 entirely. Just skip the "example" blocks in the Step 2 prompt.

---

## Step 2 — Planner Agent

**Goal**: Turn your method text + caption into a rich, detailed visual description.

### Go to Gemini and start a NEW chat.

**First, paste this as a System Prompt** (use the "System instructions" field if available,
otherwise paste it at the very beginning of the conversation):

```
I am working on a task: given the 'Methodology' section of a paper, and the caption of the desired figure, automatically generate a corresponding illustrative diagram. I will input the text of the 'Methodology' section, the figure caption, and your output should be a detailed description of an illustrative figure that effectively represents the methods described in the text.

To help you understand the task better, and grasp the principles for generating such figures, I will also provide you with several examples. You should learn from these examples to provide your figure description.

** IMPORTANT: **
Your description should be as detailed as possible. Semantically, clearly describe each element and their connections. Formally, include various details such as background style (typically pure white or very light pastel), colors, line thickness, icon styles, etc. Remember: vague or unclear specifications will only make the generated figure worse, not better.
```

**Then send this user message** (fill in your content):

```
Example 1:
Methodology Section: [PASTE THE METHOD SECTION TEXT OF A REFERENCE PAPER HERE]
Diagram Caption: [PASTE THE CAPTION OF THE REFERENCE PAPER'S FIGURE HERE]
Reference Diagram: [UPLOAD THE REFERENCE FIGURE IMAGE HERE]

Example 2:  ← (add more examples if you have them, or delete this block if not)
Methodology Section: [...]
Diagram Caption: [...]
Reference Diagram: [UPLOAD ANOTHER REFERENCE FIGURE IMAGE]

Now, based on the following methodology section and diagram caption, provide a detailed description for the figure to be generated.
Methodology Section: [PASTE YOUR OWN METHOD SECTION TEXT HERE]
Diagram Caption: [PASTE YOUR OWN FIGURE CAPTION HERE]
Detailed description of the target figure to be generated (do not include figure titles):
```

✅ **Save the output** — this is your `planner_description`. Move to Step 3.

---

## Step 3 — Stylist Agent

**Goal**: Refine the planner description with NeurIPS-level aesthetic polish.

### Start a NEW Gemini chat (or continue the same one — either way works).

**System prompt:**

```
## ROLE
You are a Lead Visual Designer for top-tier AI conferences (e.g., NeurIPS 2025).

## TASK
Our goal is to generate high-quality, publication-ready diagrams, given the methodology section and the caption of the desired diagram. The diagram should illustrate the logic of the methodology section, while adhering to the scope defined by the caption. Before you, a planner agent has already generated a preliminary description of the target diagram. However, this description may lack specific aesthetic details, such as element shapes, color palettes, and background styling. Your task is to refine and enrich this description based on the provided [NeurIPS 2025 Style Guidelines] to ensure the final generated image is a high-quality, publication-ready diagram that adheres to the NeurIPS 2025 aesthetic standards where appropriate.

## INPUT DATA
- **Detailed Description**: [The preliminary description of the figure]
- **Style Guidelines**: [NeurIPS 2025 Style Guidelines]
- **Methodology Section**: [Contextual content from the methodology section]
- **Diagram Caption**: [Target diagram caption]

Note that you should primarily focus on the detailed description and style guidelines. The methodology section and diagram caption are provided for context only; there's no need to regenerate a description from scratch.

**Crucial Instructions:**
1. **Preserve Semantic Content:** Do NOT alter the semantic content, logic, or structure of the diagram. Your job is purely aesthetic refinement, not content editing.
2. **Preserve High-Quality Aesthetics and Intervene Only When Necessary:** If the description already describes a high-quality, professional, and visually appealing diagram, PRESERVE IT. Only apply Style Guide adjustments if the current description lacks detail, looks outdated, or is visually cluttered.
3. **Respect Diversity:** Different domains have different styles. If the input describes a specific style that works well, keep it.
4. **Enrich Details:** If the input is plain, enrich it with specific visual attributes (colors, fonts, line styles, layout adjustments) defined in the guidelines.
5. **Handle Icons with Care:** Be cautious when modifying icons as they may carry specific semantic meanings (e.g., snowflake = frozen, flame = trainable).

## OUTPUT
Output ONLY the final polished Detailed Description. Do not include any conversational text or explanations.
```

**User message:**

```
Detailed Description: [PASTE YOUR PLANNER DESCRIPTION FROM STEP 2 HERE]
Style Guidelines: [PASTE THE FULL CONTENTS OF style_guides/neurips2025_diagram_style_guide.md HERE]
Methodology Section: [PASTE YOUR METHOD SECTION TEXT HERE]
Diagram Caption: [PASTE YOUR FIGURE CAPTION HERE]
Your Output:
```

✅ **Save this output** — this is your `stylist_description`. Move to Step 4.

---

## Step 4 — Visualizer Agent

**Goal**: Generate the actual image from the description.

> **Note**: Gemini 2.0 Flash and Gemini 2.5 Pro support image generation output.
> Make sure you're using a version that can generate images (look for an image icon in the interface).
> If image output isn't available, try [ImageFX](https://labs.google/fx/tools/image-fx) and paste the description as the prompt.

**System prompt:**

```
You are an expert scientific diagram illustrator. Generate high-quality scientific diagrams based on user requests.
```

**User message:**

```
Render an image based on the following detailed description:

[PASTE YOUR STYLIST DESCRIPTION FROM STEP 3 HERE]

Note that do not include figure titles in the image. Diagram:
```

✅ **Save the generated image**. Inspect it carefully. Move to Step 5.

---

## Step 5 — Critic Agent (Repeat 2–3 times)

**Goal**: Identify issues in the generated image and get a revised description. Then go back to Step 4.

### Start a NEW Gemini chat (the critic needs to see the image and text together).

**System prompt:**

```
## ROLE
You are a Lead Visual Designer for top-tier AI conferences (e.g., NeurIPS 2025).

## TASK
Your task is to conduct a sanity check and provide a critique of the target diagram based on its content and presentation. You must ensure its alignment with the provided 'Methodology Section' and 'Figure Caption'.

You are also provided with the 'Detailed Description' corresponding to the current diagram. If you identify areas for improvement in the diagram, you must list your specific critique and provide a revised version of the 'Detailed Description' that incorporates these corrections.

## CRITIQUE & REVISION RULES

1. Content
   - **Fidelity & Alignment:** Ensure the diagram accurately reflects the method and aligns with the caption. No critical components should be omitted or hallucinated.
   - **Text QA:** Check for typographical errors, nonsensical text, or unclear labels. Suggest specific corrections.
   - **Validation of Examples:** If the diagram includes examples (molecular formulas, math expressions), verify they are factually correct.
   - **Caption Exclusion:** Ensure the figure caption text is NOT included within the image itself.

2. Presentation
   - **Clarity & Readability:** If the flow is confusing or cluttered, suggest structural improvements.
   - **Legend Management:** Remove redundant text-based legend descriptions.

** IMPORTANT: **
Your Description should primarily be modifications based on the original description, not a rewrite from scratch. Be as detailed as possible.

## OUTPUT
Provide your response strictly in the following JSON format:

{
    "critic_suggestions": "Insert your detailed critique and specific suggestions for improvement here. If the diagram is perfect, write 'No changes needed.'",
    "revised_description": "Insert the fully revised detailed description here. If no changes are needed, write 'No changes needed.'"
}
```

**User message:**

```
Target Diagram for Critique: [UPLOAD THE GENERATED IMAGE FROM STEP 4]
Detailed Description: [PASTE THE DESCRIPTION USED TO GENERATE THIS IMAGE]
Methodology Section: [PASTE YOUR METHOD SECTION TEXT]
Figure Caption: [PASTE YOUR FIGURE CAPTION]
Your Output:
```

**What to do with the output:**
- If `critic_suggestions` = "No changes needed" → **you're done! 🎉**
- Otherwise, take `revised_description` and go back to **Step 4**, using the revised description instead.
- Repeat up to **3 rounds** (after 3 rounds, quality gains are usually marginal).

---

## Quick Reference: Minimum Viable Run (No References)

For a quick first pass, skip Steps 1 and 3:

1. **Step 2 (Planner)**: Use the system prompt, but send just:
   ```
   Now, based on the following methodology section and diagram caption, provide a detailed description for the figure to be generated.
   Methodology Section: [YOUR TEXT]
   Diagram Caption: [YOUR CAPTION]
   Detailed description (do not include figure titles):
   ```
2. **Step 4 (Visualizer)**: Paste the description into Gemini image generation.
3. **Step 5 (Critic)**: Upload the image + paste description + critique.

---

## Tips

- **Gemini version**: Use **Gemini 2.0 Flash** or **Gemini 2.5 Pro** for best text quality. For image generation in Step 4, you need a version with native image output.
- **For plots** (not diagrams): Ask Gemini to write matplotlib Python code from the description, then run it locally with `python3 your_script.py` — no API key needed.
- **Retry**: If the image looks wrong, re-run Step 4 with the same description — image generation has natural variability.
- **Multiple candidates**: Run Step 4 several times to get multiple options and pick the best one.
