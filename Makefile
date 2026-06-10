.PHONY: install test lint format clean build upload

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=smartscraper --cov-report=term-missing

lint:
	flake8 smartscraper/ tests/
	black --check smartscraper/ tests/

format:
	black smartscraper/ tests/

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*
