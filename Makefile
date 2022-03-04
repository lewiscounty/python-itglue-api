.PHONY: deps lint test test-ci venv

deps:
	pip install --upgrade pip
	pip install -e ".[dev]"
	pre-commit install

lint:
	pre-commit run --all-files

test:
	nox --sessions test

test-ci:
	mypy --strict -p itglue
	coverage run -m unittest discover
	coverage report -m

venv:
	rm -rf .venv
	python -m venv .venv
