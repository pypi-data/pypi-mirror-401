# Dockerfile for running sandbox isolation tests
#
# This container provides:
# - Linux environment with nsjail
# - Python 3.12 with pytest
# - sb0 package installed in editable mode
#
# Build:
#   docker build -t sb0-sandbox-tests -f tests/sandbox/Dockerfile .
#
# Run tests:
#   docker run --rm \
#     --cap-add=SYS_ADMIN \
#     --cap-add=SYS_PTRACE \
#     --security-opt seccomp=src/sb0/lib/sandbox/seccomp-profile.json \
#     sb0-sandbox-tests
#
FROM python:3.12-slim

# Install system dependencies and nsjail build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    # Runtime dependencies
    libprotobuf32 \
    libnl-route-3-200 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Build and install nsjail (pinned to v3.4)
RUN git clone --branch 3.4 --depth 1 https://github.com/google/nsjail.git /tmp/nsjail \
    && cd /tmp/nsjail \
    && make \
    && cp nsjail /usr/local/bin/ \
    && rm -rf /tmp/nsjail \
    # Remove build dependencies to reduce image size
    && apt-get purge -y --auto-remove \
        autoconf automake bison flex g++ git libtool make pkg-config

# Create workspace directories that sandboxes will use
RUN mkdir -p /workspaces /dot_claudes \
    && chmod 777 /workspaces /dot_claudes

# Install pip and test dependencies
RUN pip install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy just pyproject.toml first for dependency caching
COPY pyproject.toml README.md ./

# Install the package in editable mode with test dependencies
# We copy minimal files first to leverage Docker layer caching
COPY src/ ./src/

# Install the package and test dependencies
# Note: dev deps are in [tool.rye], not pip extras, so install pytest explicitly
RUN pip install --no-cache-dir -e . pytest pytest-asyncio pytest-xdist

# Copy test files
COPY tests/ ./tests/

# Set environment for sandbox testing
ENV SB0_SANDBOX_ENABLED=true
ENV SB0_NSJAIL_PATH=/usr/local/bin/nsjail
ENV PYTHONPATH=/app/src

# Required by EnvironmentVariables (used by runner to pass env to sandbox)
ENV AGENT_NAME=sandbox-test-agent
ENV ACP_URL=http://localhost:8000

# Default command runs sandbox tests
CMD ["python", "-m", "pytest", "tests/sandbox/", "-v", "--tb=short"]
