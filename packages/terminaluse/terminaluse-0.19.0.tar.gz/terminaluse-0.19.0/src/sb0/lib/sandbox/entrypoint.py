"""
Jailed handler entrypoint - runs inside nsjail.

Protocol:
  stdin:  JSON object with keys: method, handler, params
  stdout: Small status object as JSON (optional)
  exit 0: success
  exit 1: failure
"""

from __future__ import annotations

import sys
import json
import asyncio
import importlib
from typing import Any, Callable


def _get_params_class(method: str):
    """Get the appropriate params class for a method."""
    # Import here to ensure it works in the jail
    from sb0.lib.types.acp import (
        SendEventParams,
        CancelTaskParams,
        CreateTaskParams,
    )

    method_to_class = {
        "task/create": CreateTaskParams,
        "event/send": SendEventParams,
        "task/cancel": CancelTaskParams,
    }

    cls = method_to_class.get(method)
    if cls is None:
        raise ValueError(f"Unsupported method: {method}")
    return cls


def _load_params(method: str, data: dict[str, Any]):
    """Load and validate params for the given method."""
    params_data = data.get("params", {})
    params_class = _get_params_class(method)
    return params_class.model_validate(params_data)


def _load_handler(handler_ref: dict[str, str]) -> Callable[..., Any]:
    """
    Load a user handler by import path.

    The handler must be importable inside the jail and accept exactly one argument:
    the parsed params model (CreateTaskParams, SendEventParams, or CancelTaskParams).
    """
    module_name = handler_ref.get("module")
    function_name = handler_ref.get("function")

    if not module_name or not function_name:
        raise ValueError("handler.module and handler.function are required")

    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise ValueError(f"Could not import handler module: {module_name}") from e

    fn = getattr(module, function_name, None)
    if fn is None:
        raise ValueError(f"Handler not found: {module_name}.{function_name}")

    if not callable(fn):
        raise ValueError(f"Handler is not callable: {module_name}.{function_name}")

    return fn


def main() -> int:
    """Main entrypoint for jailed handler execution."""
    try:
        # Read payload from stdin
        raw = sys.stdin.read()
        if not raw:
            raise ValueError("No input received on stdin")

        payload = json.loads(raw)

        # Extract and validate
        method = payload.get("method")
        if not method:
            raise ValueError("Missing 'method' in payload")

        handler_ref = payload.get("handler", {})
        if not handler_ref:
            raise ValueError("Missing 'handler' in payload")

        # Load params and handler
        params = _load_params(method, payload)
        fn = _load_handler(handler_ref)

        # Execute the handler
        # Handlers are typically async, but support sync too
        if asyncio.iscoroutinefunction(fn):
            asyncio.run(fn(params))
        else:
            fn(params)

        # Success - write status to stdout
        out = {"status": "ok"}
        sys.stdout.write(json.dumps(out))
        return 0

    except Exception as exc:
        # Log error to stderr
        print(f"ERROR in sandboxed handler: {exc}", file=sys.stderr)

        # Try to write error status to stdout (ACP wrapper may use this)
        try:
            error_out = {"status": "error", "error": str(exc)}
            sys.stdout.write(json.dumps(error_out))
        except Exception:
            pass

        return 1


if __name__ == "__main__":
    raise SystemExit(main())
