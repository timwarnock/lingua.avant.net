# Makefile for lingua.avant.net
# Zensical site lives in ora/ (special preview at /ora/site/)
#
# Default: build
# Run `make serve` in a separate terminal for the dev server on :7007

.DEFAULT_GOAL := build

.PHONY: build serve help

help:
	@echo "ora/ (Zensical) targets:"
	@echo "  make        - build the site (default)"
	@echo "  make build  - build ora/site/"
	@echo "  make serve  - start dev server on localhost:7007"
	@echo ""
	@echo "Run 'make serve' in a separate window while editing."

build:
	cd ora && uvx zensical build

serve:
	cd ora && uvx zensical serve -a localhost:7007
