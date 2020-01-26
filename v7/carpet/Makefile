THIS_MAKEFILE_PATH := $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
THIS_DIR := $(shell cd $(dir $(THIS_MAKEFILE_PATH));pwd)
FONTAWSSOME_DIR := $(THIS_DIR)/lib/fontawesome
DIST_DIR := $(THIS_DIR)/assets

NPM ?= $(NODE) $(shell which npm)

# Build
build:
	@$(NPM) run build
	@cp -R $(FONTAWSSOME_DIR)/css $(DIST_DIR)
	@cp -R $(FONTAWSSOME_DIR)/fonts $(DIST_DIR)

# NPM
install:
	@$(NPM) install

.PHONY: run test
