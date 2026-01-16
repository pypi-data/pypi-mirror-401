#!/usr/bin/env bash
#
# Run sandbox isolation tests in a Docker container.
#
# This script builds a container with nsjail and runs the sandbox tests.
# Use this on macOS or any system without nsjail installed.
#
# Usage:
#   ./tests/sandbox/run_tests.sh              # Run all sandbox tests
#   ./tests/sandbox/run_tests.sh -k "file"    # Run tests matching "file"
#   ./tests/sandbox/run_tests.sh --build      # Force rebuild the container
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

IMAGE_NAME="sb0-sandbox-tests"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"
SECCOMP_PROFILE="$REPO_ROOT/src/sb0/lib/sandbox/seccomp-profile.json"

# Parse arguments
FORCE_BUILD=false
PYTEST_ARGS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        --build)
            FORCE_BUILD=true
            shift
            ;;
        *)
            PYTEST_ARGS+=("$1")
            shift
            ;;
    esac
done

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

# Build the container if needed
if [[ "$FORCE_BUILD" == "true" ]] || ! docker image inspect "$IMAGE_NAME" &> /dev/null; then
    echo "Building sandbox test container..."
    docker build -t "$IMAGE_NAME" -f "$DOCKERFILE" "$REPO_ROOT"
fi

# Run the tests
echo "Running sandbox tests in container..."
echo ""

# Construct the command
CMD=("python" "-m" "pytest" "tests/sandbox/" "-v" "--tb=short")
if [[ ${#PYTEST_ARGS[@]} -gt 0 ]]; then
    CMD+=("${PYTEST_ARGS[@]}")
fi

# Run with --privileged for nsjail namespace operations
# This is required because nsjail needs to make root mounts private
# which requires more privileges than just SYS_ADMIN capability
docker run --rm \
    --privileged \
    "$IMAGE_NAME" \
    "${CMD[@]}"
