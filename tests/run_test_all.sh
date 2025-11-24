#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

python3 -m pytest -vv tests/test_api_*.py tests/test_repositories.py tests/test_services.py "$@"
