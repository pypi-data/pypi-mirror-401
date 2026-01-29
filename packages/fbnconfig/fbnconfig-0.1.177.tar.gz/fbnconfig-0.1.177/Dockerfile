FROM harbor.finbourne.com/external-images/ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies first (better layer caching)
# Note: Avoid BuildKit-only `RUN --mount=...` so this builds with Podman/Buildah too.
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY fbnconfig /app/fbnconfig
COPY server /app/server
COPY public_examples /app/public_examples
COPY pyproject.toml uv.lock readme.md fbnconfig.md /app/

# Install the project
RUN uv sync --frozen --no-dev

# Create non-root user
RUN groupadd -r -g 10100 fbnconfig && \
    useradd --no-log-init -r -m -u 10100 -g fbnconfig fbnconfig && \
    chown -R fbnconfig:fbnconfig /app

# Test stage to validate schema and a simple invoke round-trip
FROM builder AS tester
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
WORKDIR /app

# Ensure the CLI schema stays valid at build time
RUN uv run python -m fbnconfig._smoke.validate_schema

# Smoke test the API server by starting it briefly and testing endpoints
RUN set -eu; \
    port=8000; \
    base="http://127.0.0.1:${port}/api/fbnconfig"; \
    uv run python -m uvicorn server.app:app --host 127.0.0.1 --port "${port}" --timeout-graceful-shutdown 30 & \
    pid="$!"; \
    trap 'kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true' EXIT; \
    SMOKE_BASE="$base" uv run python -m fbnconfig._smoke.api_smoke

# Runtime stage - minimal image
# Use Harbor-mirrored distroless image (pinned by digest)
FROM harbor.finbourne.com/external-images/gcr.io/distroless/python3-debian12:nonroot
# Keep parity with the previous :nonroot base image.
USER 65532:65532

# Copy only what is needed at runtime (smaller surface area)
# Distroless images don't include a shell; avoid relying on a venv whose shebangs
# point at the builder's Python. Copy site-packages and use PYTHONPATH instead.
COPY --from=tester --chown=65532:65532 /app/.venv/lib/python3.11/site-packages /app/site-packages
COPY --from=tester --chown=65532:65532 /app/fbnconfig /app/fbnconfig
COPY --from=tester --chown=65532:65532 /app/server /app/server
COPY --from=tester --chown=65532:65532 /app/public_examples /app/public_examples

WORKDIR /app

# Add venv to PATH
ENV PYTHONPATH="/app/site-packages" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/tmp \
    TMPDIR=/tmp

# Expose API port
EXPOSE 8000

# Note: HEALTHCHECK removed - use Kubernetes probes instead:
# - livenessProbe: /api/fbnconfig/health
# - readinessProbe: /api/fbnconfig/ready

# Start as API server instead of CLI
# --timeout-graceful-shutdown: Allow graceful shutdown for in-flight requests
# --timeout-keep-alive: Timeout idle connections (important for C# sidecar caller)
ENTRYPOINT ["python", "-m", "uvicorn"]
CMD ["server.app:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "30", "--timeout-keep-alive", "10"]
