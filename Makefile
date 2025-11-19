.PHONY: install build clean run validate help dev test-local

help:
	@echo "Loja Online TP1 - Build Commands"
	@echo "================================"
	@echo "  install      - Install build dependencies"
	@echo "  validate     - Validate Python syntax" 
	@echo "  build        - Build package"
	@echo "  clean        - Clean build artifacts"
	@echo "  run          - Run the application"
	@echo "  dev          - Setup development environment"
	@echo "  test-local   - Run local build test"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

validate:
	@echo "Validating Python syntax..."
	python3 -m py_compile src/loja_online/*.py
	@echo "Syntax validation completed"

build: 
	@echo "Building package..."
	python3 -m build
	@echo "Package build completed"
	@ls -la dist/

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	@echo "Build artifacts cleaned"

run:
	@echo "Running application..."
	PYTHONPATH=src python3 -m loja_online.main

dev:
	@echo "Setting up development environment..."
	pip install -e .
	@echo "Development environment ready!"

test-local:
	@echo "Running local build test..."
	./scripts/build.sh
