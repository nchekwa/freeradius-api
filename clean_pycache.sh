#!/usr/bin/env bash
set -euo pipefail

# Find and remove all __pycache__ directories recursively
echo "Searching for __pycache__ directories..."

PYCACHE_DIRS=$(find . -type d -name "__pycache__" 2>/dev/null)

if [ -z "$PYCACHE_DIRS" ]; then
    echo "No __pycache__ directories found."
else
    echo "Found the following __pycache__ directories:"
    echo "$PYCACHE_DIRS"
    echo ""
    echo "Removing..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    echo "Done. All __pycache__ directories have been removed."
fi
