This repo extends paperbanana to be usable by anyone to generate publication-quality figures.

Requirements:
- Draft figure caption (can be iterated during developmet)
- Methodology description (fixed. written by you) 
- Latex renderer and python packages (matplotlib, etc depending on your requirements)



Step 1:
We first decompose paperbanana into a set of prompts that can be fed into LLMs for generation of figures via image generation.
- This is useful as you can mix and match models and prompts to tune the output.

This step generates a recipe that describes how to make the figure via nanobanana (or other image generation tool). 

The paperbanana method defults to using the Review and Critic agents to iteratively improve the figure. This is expensive and slow. So instead of doing this, we recommend using the generated image to guide the generation of a tikz version of the figure. 

Step 2:
To generate the editable tikz version, we use an existing tikz skeleton which describes the layout and structure of the figure in a programmatic way. Since we want to generate as many of the components in a vector format as possible, we can ask a model to identify which components are diagrammatic (i.e. can be described by tikz/matplotlib code) and others which must be provided separately as raster images (e.g. images, PyMOL renders, etc). 

This step is comprised of 3 stages:
1. Process raster components (PyMOl renders etc.), including sharpening and tinting.
2. Generate the composite components 
3. Compile the tikz files describing the layout, which is generated from the config file.

The makefile describes commands to generate each stage as well as clear intermediate files between runs.