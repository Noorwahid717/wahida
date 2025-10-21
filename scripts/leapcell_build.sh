#!/usr/bin/env bash
set -eux

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$PROJECT_ROOT"

if ! command -v poetry >/dev/null 2>&1; then
    pip install --no-cache-dir poetry
fi

cd apps/api
poetry install --no-interaction --no-root
