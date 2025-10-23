

FROM --platform=linux/amd64 python:3.9-slim-buster as environment
ARG DEBIAN_FRONTEND=noninteractive

# Configure Poetry
ENV POETRY_VERSION=1.3.2
ENV POETRY_HOME=/app/poetry
ENV POETRY_VENV=/app/poetry-venv
ENV PATH="/app/poetry-venv/bin:$PATH"
ENV POETRY_CACHE_DIR=/app/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy Dependencies
COPY poetry.lock pyproject.toml ./

RUN /bin/bash -c 'source $POETRY_VENV/bin/activate && \
    poetry install --no-root'


FROM --platform=linux/amd64 python:3.9-slim-buster as test

WORKDIR /app
#COPY --from=indexing_environment $POETRY_VENV $POETRY_VENV
COPY --from=environment /app .
COPY . FN-Basic-Services

# RUN chmod +x /app/FN-Basic-Services/*.sh

ENTRYPOINT ["/app/FN-Basic-Services/docker-run-tests.sh"]


FROM --platform=linux/amd64 python:3.9-slim-buster as runtime

WORKDIR /app

#COPY --from=indexing_environment $POETRY_VENV $POETRY_VENV
COPY --from=environment /app .
COPY . FN-Basic-Services

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Enable venv
ENV PATH="/app/poetry-venv/bin:$PATH"

# ENTRYPOINT ["/app/FN-Basic-Services/docker-run-entrypoints.sh"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8888", "main:app"]

# Command to run Gunicorn with Uvicorn workers
CMD ["gunicorn", "-w", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8888", "-t", "30", "--pythonpath", "/app/FN-Basic-Services", "main:app"]
