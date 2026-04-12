#!/bin/bash
set -e

echo "=== Building tools site ==="

echo "Building index page..."
python build_index.py

echo "=== Build complete! ==="
