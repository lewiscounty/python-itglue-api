.PHONY: deps lint test test-full venv

deps:
	pip install --upgrade pip
	pip install -e ".[dev]"
	pre-commit install

lint:
	pre-commit run --all-files

test:
	mypy --strict -p itglue
	coverage run -m unittest discover
	coverage report -m

test-full:
	nox

venv:
	rm -rf .venv
	python -m venv .venv
