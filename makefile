.PHONY: install test clean example

install:
	pip install -e .

test:
	pytest tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dist/ build/ *.egg-info

example:
	cd examples && pdflatex main.tex
	cd examples && plastex main.tex
	cd examples && plastex --renderer=lean4 main.tex
