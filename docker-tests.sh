#!/bin/bash

set -eu

export PYTHONDONTWRITEBYTECODE=1

docker run --rm -it --platform linux/amd64 -it -d \
  --name ffn-basic-docker-api --publish 8889:8889 --expose 8889 \
  --network bridge \
  # -e ES_HOST=http://host.docker.internal:9203 \
  -v "$SCRIPTDIR:/app/FN-Basic-Services/" \
  fn-basic-docker-api:test