#!/usr/bin/env bash
set -eux

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$PROJECT_ROOT"

if ! command -v poetry >/dev/null 2>&1; then
    pip install --no-cache-dir poetry
fi

# Adjust working directory when repo root is mounted; Leapcell may already set root to apps/api
if [ -d "apps/api" ]; then
    cd apps/api
elif [ -f "pyproject.toml" ]; then
    : "already at project root"
else
    echo "pyproject.toml not found; aborting" >&2
    exit 1
fi

poetry install --no-interaction --no-root
