# syntax=docker/dockerfile:1.3
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.6.4 /uv /uvx /bin/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    htop \
    vim \
    curl \
    tar \
    python3-dev \
    postgresql-client \
    build-essential \
    libpq-dev \
    gcc \
    cmake \
    netcat-openbsd \
    nodejs \
    npm \
    # nsjail build dependencies
    autoconf \
    automake \
    bison \
    flex \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Build and install nsjail for handler sandboxing
RUN git clone https://github.com/google/nsjail.git /tmp/nsjail \
    && cd /tmp/nsjail \
    && make \
    && cp nsjail /usr/local/bin/ \
    && rm -rf /tmp/nsjail

RUN uv pip install --system --upgrade pip setuptools wheel

ENV UV_HTTP_TIMEOUT=1000

# Copy sb0 package to /app (so ../.. from examples/claude_agent_sdk resolves to /app)
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
COPY README.md /app/README.md

# Copy the claude_agent_sdk project files (path must match ../.. reference in tool.uv.sources)
COPY examples/claude_agent_sdk/pyproject.toml /app/examples/claude_agent_sdk/pyproject.toml
COPY examples/claude_agent_sdk/project /app/examples/claude_agent_sdk/project

WORKDIR /app/examples/claude_agent_sdk

# Install the claude_agent_sdk package and its dependencies (including sb0 from ../.. = /app)
RUN uv pip install --system .

# Set environment variables
ENV PYTHONPATH=/app

# Run the agent using uvicorn
CMD ["uvicorn", "project.acp:server", "--host", "0.0.0.0", "--port", "8000"]
