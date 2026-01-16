#!/bin/bash
set -e

echo "Running linting..."
ruff check telonex/ tests/

echo "Running type checking..."
mypy telonex/

echo "Running tests..."
pytest tests/ -v

echo "Cleaning old builds..."
rm -rf dist/ build/ *.egg-info

echo "Building package..."
python -m build

echo "Build complete! Files in dist/"
ls -la dist/
