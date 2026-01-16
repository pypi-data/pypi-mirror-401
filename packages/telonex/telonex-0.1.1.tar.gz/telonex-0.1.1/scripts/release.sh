#!/bin/bash
set -e

echo "Running build first..."
./scripts/build.sh

echo "Uploading to PyPI..."
twine upload dist/*

echo "Release complete!"
