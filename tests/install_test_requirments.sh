#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQ_FILE="$PROJECT_ROOT/requirements-dev.txt"

if [[ ! -f "$REQ_FILE" ]]; then
  echo "Could not find requirements file at $REQ_FILE" >&2
  exit 1
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r "$REQ_FILE"
