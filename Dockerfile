#syntax=docker/dockerfile:1.9

ARG PYTHON_VERSION="3.12"
FROM ghcr.io/astral-sh/uv:0.3.1 AS uv
FROM python:${PYTHON_VERSION}-slim-bookworm

ENV FLYTE_SDK_RICH_TRACEBACKS=0 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/root \
    PATH="/opt/venv/bin:$PATH"

RUN id -u flytekit || useradd --create-home --shell /bin/bash flytekit
RUN chown -R flytekit /root && chown -R flytekit /home

RUN --mount=type=cache,sharing=locked,mode=0777,target=/root/.cache/uv,id=uv \
    --mount=from=uv,source=/uv,target=/usr/bin/uv \
    uv venv /opt/venv && \
    uv pip install --prefix /opt/venv union kubernetes

WORKDIR /root
USER flytekit
