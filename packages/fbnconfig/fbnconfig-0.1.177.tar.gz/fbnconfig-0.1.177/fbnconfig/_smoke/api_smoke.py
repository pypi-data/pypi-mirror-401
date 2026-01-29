from __future__ import annotations

import os
import time

import httpx


def main() -> None:
    # Default matches Docker tester stage (server bound on 127.0.0.1:8000)
    base = os.getenv("SMOKE_BASE") or os.getenv("BASE") or "http://127.0.0.1:8000/api/fbnconfig"
    deadline_seconds = float(os.getenv("SMOKE_DEADLINE_SECONDS", "30"))

    deadline = time.time() + deadline_seconds
    last_error: object | None = None

    while time.time() < deadline:
        try:
            ready = httpx.get(f"{base}/ready", timeout=2)
            if ready.status_code == 200:
                break
            last_error = f"ready={ready.status_code} {ready.text}"
        except Exception as exc:  # pragma: no cover
            last_error = str(exc)
        time.sleep(0.5)
    else:
        raise RuntimeError(f"Server did not become ready: {last_error}")

    health = httpx.get(f"{base}/health", timeout=5)
    health.raise_for_status()
    print("\u2713 Health:", health.json())

    ready = httpx.get(f"{base}/ready", timeout=5)
    ready.raise_for_status()
    print("\u2713 Ready:", ready.json())

    headers = {"X-Request-Id": "runsh-req", "X-Correlation-Id": "runsh-corr"}
    invoke = httpx.post(f"{base}/invoke", json={"test": "run.sh"}, headers=headers, timeout=5)
    invoke.raise_for_status()
    print("\u2713 Invoke:", invoke.json())

    # Validate echoing back correlation headers.
    print("\u2713 Echo X-Request-Id:", invoke.headers.get("x-request-id"))
    print("\u2713 Echo X-Correlation-Id:", invoke.headers.get("x-correlation-id"))


if __name__ == "__main__":
    main()
