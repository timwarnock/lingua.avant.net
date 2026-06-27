# Makefile for lingua.avant.net
# Zensical site lives in ora/ (special preview at /ora/site/)
#
# Default: build
# Run `make serve` in a separate terminal for the dev server on :7007

.DEFAULT_GOAL := build

.PHONY: build serve kill restart help

help:
	@echo "ora/ (Zensical) targets:"
	@echo "  make        - build the site (default)"
	@echo "  make build  - build ora/site/"
	@echo "  make serve  - start dev server on localhost:7007"
	@echo "  make kill   - kill running zensical dev server (pkill)"
	@echo "  make restart - kill then restart dev server"
	@echo ""
	@echo "Run 'make serve' (or 'make restart') in a separate window while editing."

build:
	cd ora && uvx zensical build

deploy:
	git add . && git commit -am updates && git push && ssh avant 'cd lingua.avant.net; git pull'

serve:
	cd ora && uvx zensical serve -a localhost:7007

kill:
	pkill -f 'zensical serve' || true

restart: kill serve
