#!/bin/bash
set -ex

# sleep 60

export PYTHONDONTWRITEBYTECODE=1

echo "entrypoints.sh"

# --
# Poetry v.
# --
source /app/poetry-venv/bin/activate
cd /app/FN-Basic-Services

# py.test -v tests
# py.test -v ./tests --cov-report term-missing --cov
poetry run py.test -sv ./tests --disable-warnings --cov-report term-missing --cov
