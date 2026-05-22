.PHONY: all processed components figure renders components_only tikz_only component clean

PYTHON ?= /Users/alexi/miniconda/bin/python

INPUT_RENDER_FILES := $(wildcard inputs/renders/*.png)
TIKZ_FILES := tikz/figure.tex tikz/styles.tex tikz/asset_paths.tex $(wildcard tikz/panels/*.tex)
SCRIPT_FILES := scripts/config.py scripts/01_process_renders.py scripts/02_generate_components.py scripts/03_compile_figure.py

STAMP_DIR := outputs/.stamps
PROCESSED_STAMP := $(STAMP_DIR)/processed.stamp
COMPONENTS_STAMP := $(STAMP_DIR)/components.stamp
FIGURE_STAMP := $(STAMP_DIR)/figure.stamp

all: figure

processed: $(PROCESSED_STAMP)
components: $(COMPONENTS_STAMP)
figure: $(FIGURE_STAMP)

$(PROCESSED_STAMP): scripts/01_process_renders.py scripts/config.py $(INPUT_RENDER_FILES) ; @mkdir -p $(STAMP_DIR) && $(PYTHON) scripts/01_process_renders.py && touch $@

$(COMPONENTS_STAMP): scripts/02_generate_components.py scripts/config.py $(PROCESSED_STAMP) ; @mkdir -p $(STAMP_DIR) && $(PYTHON) scripts/02_generate_components.py && touch $@

$(FIGURE_STAMP): scripts/03_compile_figure.py scripts/config.py $(COMPONENTS_STAMP) $(TIKZ_FILES) ; @mkdir -p $(STAMP_DIR) && $(PYTHON) scripts/03_compile_figure.py && touch $@

renders: ; @$(PYTHON) scripts/01_process_renders.py

components_only: ; @$(PYTHON) scripts/02_generate_components.py

# Rebuild a single component: make component COMPONENT=scorecard
component: ; @$(PYTHON) scripts/02_generate_components.py $(if $(COMPONENT),--only $(COMPONENT),)

tikz_only: ; @$(PYTHON) scripts/03_compile_figure.py --tikz-only

clean: ; @rm -rf outputs/processed outputs/components outputs/figure outputs/.stamps tikz/figure.aux tikz/figure.log tikz/figure.pdf
