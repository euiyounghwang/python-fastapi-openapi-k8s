#!/bin/bash

set -eu

#docker build --no-cache \


docker build \
  -f "$(dirname "$0")/Dockerfile" \
  -t fn-basic-docker-api:es \
  --target runtime \
  "$(dirname "$0")/."


# docker build \
#   -f "$(dirname "$0")/Dockerfile" \
#   -t fn-basic-docker-api:test \
#   --target test \
#   "$(dirname "$0")/."


# docker build \
#   -f "$(dirname "$0")/Dockerfile" \
#   -t fn-basic-docker-api:omni_es \
#   --target omni_es \
#   "$(dirname "$0")/."