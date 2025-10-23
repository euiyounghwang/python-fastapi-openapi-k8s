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

# --
# Waitng for ES
# ./wait_for_es.sh $ES_HOST

echo "Runinng"
# poetry run uvicorn main:app --host=0.0.0.0 --port=8888 --workers 4
gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8888 --workers 4