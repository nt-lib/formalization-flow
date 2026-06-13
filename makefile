VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
PLASTEX := $(VENV)/bin/plastex

.PHONY: venv install test clean example

venv:
	python3 -m venv $(VENV)
	$(PIP) install -e ".[dev]"

install:
	$(PIP) install -e ".[dev]"

test:
	$(PYTEST) tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dist/ build/ *.egg-info

example:
	cd examples && TEXINPUTS="../sty/:" pdflatex unit_hom.tex
	cd examples && TEXINPUTS="../sty/:" $(PLASTEX) unit_hom.tex
	cd examples && TEXINPUTS="../sty/:" $(PLASTEX) --renderer lean4 unit_hom.tex
