#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65
#
FROM public.ecr.aws/docker/library/python:3.13-alpine@sha256:070342a0cc1011532c0e69972cce2bbc6cc633eba294bae1d12abea8bd05303b AS uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_FROZEN=true

COPY pyproject.toml uv.lock uv-requirements.txt ./

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apk update && \
    apk add --no-cache --virtual .build-deps \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo

RUN --mount=type=cache,target=/root/.cache/uv \
    pip install --require-hashes --requirement uv-requirements.txt --no-cache-dir && \
    uv sync --python 3.13 --frozen --no-install-project --no-dev --no-editable

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --python 3.13 --frozen --no-dev --no-editable

RUN mkdir -p /root/.local

FROM public.ecr.aws/docker/library/python:3.13-alpine@sha256:070342a0cc1011532c0e69972cce2bbc6cc633eba294bae1d12abea8bd05303b

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

RUN apk update && \
    apk add --no-cache ca-certificates && \
    update-ca-certificates && \
    addgroup -S app && \
    adduser -S app -G app -h /app

COPY --from=uv --chown=app:app /app/.venv /app/.venv

COPY ./docker-healthcheck.sh /usr/local/bin/docker-healthcheck.sh

USER app

HEALTHCHECK --interval=60s --timeout=10s --start-period=10s --retries=3 CMD ["docker-healthcheck.sh"]
ENTRYPOINT ["amazon-bedrock-knowledge-base-mcp"]
