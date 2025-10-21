#!/bin/bash

set -eu

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

docker run --rm -it --platform linux/amd64 -it -d \
  --name ffn-basic-docker-api --publish 8889:8889 --expose 8889 \
  --network bridge \
  # -e ES_HOST=http://host.docker.internal:9203 \
  -v "$SCRIPTDIR:/app/FN-Basic-Services/" \
  fn-basic-docker-api:test