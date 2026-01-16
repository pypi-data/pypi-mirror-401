from __future__ import annotations

import uuid
import asyncio
import inspect
from typing import Any, TypeVar, Protocol
from datetime import datetime
from contextlib import asynccontextmanager
from collections.abc import Callable, Awaitable, AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request
from pydantic import TypeAdapter, ValidationError
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware

from sb0 import AsyncSb0
from sb0.types.task import Task
from sb0.lib.types.acp import (
    RPC_SYNC_METHODS,
    PARAMS_MODEL_BY_METHOD,
    RPCMethod,
    SendEventParams,
    CancelTaskParams,
    CreateTaskParams,
    SendMessageParams,
)
from sb0.lib.utils.logging import make_logger, ctx_var_request_id
from sb0.lib.sandbox.config import SandboxConfig, get_sandbox_config
from sb0.lib.sandbox.runner import run_handler_sandboxed
from sb0.lib.types.json_rpc import JSONRPCError, JSONRPCRequest, JSONRPCResponse
from sb0.lib.utils.model_utils import BaseModel
from sb0.lib.utils.registration import register_agent
from sb0.lib.sandbox.handler_ref import (
    HandlerRef,
    HandlerValidationError,
    validate_handler_for_sandbox,
)

# from sb0.lib.sdk.fastacp.types import BaseACPConfig
from sb0.lib.environment_variables import EnvironmentVariables, refreshed_environment_variables
from sb0.types.task_message_update import TaskMessageUpdate, StreamTaskMessageFull
from sb0.types.workspace_directory import WorkspaceDirectory
from sb0.lib.adk._modules.workspace import WorkspaceModule
from sb0.types.task_message_content import TaskMessageContent
from sb0.lib.sdk.fastacp.base.constants import (
    FASTACP_HEADER_SKIP_EXACT,
    FASTACP_HEADER_SKIP_PREFIXES,
)

logger = make_logger(__name__)

# Create a TypeAdapter for TaskMessageUpdate validation
task_message_update_adapter = TypeAdapter(TaskMessageUpdate)


class ParamsWithTask(Protocol):
    """Protocol for RPC params that contain a task with workspace_id."""

    task: Task


# TypeVar bound to ParamsWithTask for generic handler wrapping
P = TypeVar("P", bound=ParamsWithTask)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to extract or generate request IDs and add them to logs and response headers"""

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        # Extract request ID from header or generate a new one if there isn't one
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
        # Store request ID in request state for access in handlers
        ctx_var_request_id.set(request_id)
        # Process request
        response = await call_next(request)
        return response


class BaseACPServer(FastAPI):
    """
    AsyncAgentACP provides RPC-style hooks for agent events and commands asynchronously.
    All methods follow JSON-RPC 2.0 format.

    Available methods:
    - event/send → Send a message to a task
    - task/cancel → Cancel a task
    - task/approve → Approve a task
    """

    def __init__(self, sandbox_config: SandboxConfig | None = None):
        super().__init__(lifespan=self.get_lifespan_function())

        self.get("/healthz")(self._healthz)
        self.post("/api")(self._handle_jsonrpc)

        # Method handlers
        # this just adds a request ID to the request and response headers
        self.add_middleware(RequestIDMiddleware)
        self._handlers: dict[RPCMethod, Callable] = {}

        # Handler references for sandboxed execution
        self._handler_refs: dict[RPCMethod, HandlerRef] = {}

        # Sandbox configuration
        self._sandbox_config = sandbox_config or get_sandbox_config()

        # Deployment ID to return in healthz (set during registration)
        self.deployment_id: str | None = None

        # Sb0 client for workspace sync operations (created lazily)
        self._sb0_client: AsyncSb0 | None = None

        # Workspace module for sync operations
        self._workspace_module: WorkspaceModule | None = None

    @classmethod
    def create(cls):
        """Create and initialize BaseACPServer instance"""
        instance = cls()
        instance._setup_handlers()
        return instance

    def _setup_handlers(self):
        """Set up default handlers - override in subclasses"""
        # Base class has no default handlers
        pass

    def get_lifespan_function(self):
        @asynccontextmanager
        async def lifespan_context(app: FastAPI):  # noqa: ARG001
            env_vars = EnvironmentVariables.refresh()
            if env_vars.SB0_BASE_URL:
                await register_agent(env_vars)
                # Store deployment_id for health check responses
                self.deployment_id = env_vars.SB0_DEPLOYMENT_ID
            else:
                logger.warning("SB0_BASE_URL not set, skipping container registration")

            yield

        return lifespan_context

    async def _healthz(self):
        """Health check endpoint - returns deployment_id for platform health monitoring"""
        result = {"status": "healthy"}
        if self.deployment_id:
            result["deployment_id"] = self.deployment_id
        return result

    def _get_sb0_client(self) -> AsyncSb0:
        """Get or create the Sb0 client lazily"""
        if self._sb0_client is None:
            env_vars = EnvironmentVariables.refresh()
            self._sb0_client = AsyncSb0(
                base_url=env_vars.SB0_BASE_URL if env_vars else None,
                api_key=env_vars.AGENT_API_KEY if env_vars else None,
            )
        return self._sb0_client

    def _get_workspace_module(self) -> WorkspaceModule:
        """Get or create the WorkspaceModule lazily"""
        if self._workspace_module is None:
            self._workspace_module = WorkspaceModule(client=self._get_sb0_client())
        return self._workspace_module

    def _wrap_handler(self, fn: Callable[..., Awaitable[Any]]):
        """Wraps handler functions to provide JSON-RPC 2.0 response format"""

        async def wrapper(*args, **kwargs) -> Any:
            return await fn(*args, **kwargs)

        return wrapper

    def _wrap_with_workspace_sync(
        self,
        fn: Callable[[P], Awaitable[Any]],
        handler_name: str,
        sync_up_after: bool = False,
    ) -> Callable[[P], Awaitable[Any]]:
        """
        Wrap a handler with workspace sync operations.

        Args:
            fn: The handler function to wrap (must accept params with a task.workspace_id)
            handler_name: Name for logging (e.g., "on_task_create")
            sync_up_after: If True, also sync_up after handler completes
        """

        async def handler_with_workspace_sync(params: P) -> Any:
            workspace_id = params.task.workspace_id
            if not workspace_id:
                logger.warning(f"[{handler_name}] Task has no workspace_id, skipping workspace sync")
                return await fn(params)

            workspace_module = self._get_workspace_module()

            # Sync down ROOT and DOT_CLAUDE workspaces in parallel before handler runs
            async def sync_down_root():
                try:
                    logger.info(f"[{handler_name}] Syncing down ROOT workspace {workspace_id} before handler")
                    result = await workspace_module.sync_down(
                        workspace_id, workspace_directory="ROOT"
                    )
                    if result.skipped:
                        logger.info(f"[{handler_name}] ROOT sync_down skipped: {result.reason}")
                    else:
                        logger.info(
                            f"[{handler_name}] ROOT sync_down completed: {result.files_extracted} files extracted"
                        )
                except Exception as e:
                    logger.error(f"[{handler_name}] ROOT Workspace sync_down failed: {e}")
                    # Continue with handler even if sync fails - workspace may be empty/new

            async def sync_down_dot_claude():
                try:
                    logger.info(f"[{handler_name}] Syncing down DOT_CLAUDE workspace {workspace_id} before handler")
                    result = await workspace_module.sync_down(
                        workspace_id, workspace_directory="DOT_CLAUDE"
                    )
                    if result.skipped:
                        logger.info(f"[{handler_name}] DOT_CLAUDE sync_down skipped: {result.reason}")
                    else:
                        logger.info(
                            f"[{handler_name}] DOT_CLAUDE sync_down completed: {result.files_extracted} files extracted"
                        )
                except Exception as e:
                    logger.error(f"[{handler_name}] DOT_CLAUDE Workspace sync_down failed: {e}")
                    # Continue with handler even if sync fails - workspace may be empty/new

            # Run both sync_down operations in parallel
            await asyncio.gather(sync_down_root(), sync_down_dot_claude())

            if not sync_up_after:
                return await fn(params)

            # With sync_up_after: run handler then sync up
            try:
                return await fn(params)
            finally:
                # Sync up ROOT and DOT_CLAUDE workspaces in parallel after handler
                async def sync_up_root():
                    try:
                        logger.info(f"[{handler_name}] Syncing up ROOT workspace {workspace_id} after handler")
                        result = await workspace_module.sync_up(
                            workspace_id, workspace_directory="ROOT"
                        )
                        if result.skipped:
                            logger.info(f"[{handler_name}] ROOT sync_up skipped: {result.reason}")
                        else:
                            logger.info(
                                f"[{handler_name}] ROOT sync_up completed: {result.files_uploaded} files uploaded"
                            )
                    except Exception as e:
                        logger.error(f"[{handler_name}] ROOT Workspace sync_up failed: {e}")
                        # Log error but don't raise - handler already completed

                async def sync_up_dot_claude():
                    try:
                        logger.info(f"[{handler_name}] Syncing up DOT_CLAUDE workspace {workspace_id} after handler")
                        result = await workspace_module.sync_up(
                            workspace_id, workspace_directory="DOT_CLAUDE"
                        )
                        if result.skipped:
                            logger.info(f"[{handler_name}] DOT_CLAUDE sync_up skipped: {result.reason}")
                        else:
                            logger.info(
                                f"[{handler_name}] DOT_CLAUDE sync_up completed: {result.files_uploaded} files uploaded"
                            )
                    except Exception as e:
                        logger.error(f"[{handler_name}] DOT_CLAUDE Workspace sync_up failed: {e}")
                        # Log error but don't raise - handler already completed

                # Run both sync_up operations in parallel
                await asyncio.gather(sync_up_root(), sync_up_dot_claude())

        return handler_with_workspace_sync

    def _should_sandbox(self, method: RPCMethod) -> bool:
        """Check if a method should be executed in a sandbox."""
        return self._sandbox_config.enabled and method in self._handler_refs

    def _wrap_with_maybe_sandbox(
        self,
        fn: Callable[[P], Awaitable[Any]],
        method: RPCMethod,
    ) -> Callable[[P], Awaitable[Any]]:
        """Wrap a handler to run sandboxed or in-process based on config."""

        async def maybe_sandboxed(params: P) -> Any:
            if self._should_sandbox(method):
                return await self._run_sandboxed_handler(method, params)
            return await fn(params)

        return maybe_sandboxed

    async def _run_sandboxed_handler(
        self,
        method: RPCMethod,
        params: BaseModel,
    ) -> None:
        """Run a handler in a sandbox."""
        handler_ref = self._handler_refs[method]

        # Extract workspace_id and task_id from params if available
        task = getattr(params, "task", None)
        workspace_id = getattr(task, "workspace_id", None)
        task_id = getattr(task, "id", None)

        logger.info(f"Running handler in sandbox: {handler_ref.module}.{handler_ref.function}")
        if workspace_id:
            logger.info(f"Mounting workspace: /workspaces/{workspace_id}")

        # Map RPCMethod enum to JSON-RPC method string
        method_str = method.value

        result = await run_handler_sandboxed(
            method=method_str,
            handler_ref=handler_ref,
            params=params,
            workspace_id=workspace_id,
            task_id=task_id,
        )

        # Log result
        if result.success:
            logger.info(f"Sandboxed handler completed: {handler_ref.module}.{handler_ref.function}")
            # Log stderr even on success - subprocess errors may be caught by handler
            if result.stderr:
                # Log last 4000 chars to capture Python errors (nsjail INFO fills the start)
                logger.warning(f"Sandbox stderr (handler succeeded but had output, tail): {result.stderr[-4000:]}")
        else:
            logger.error(
                f"Sandboxed handler failed: {handler_ref.module}.{handler_ref.function}, "
                f"exit_code={result.exit_code}, timed_out={result.timed_out}"
            )
            if result.stdout:
                logger.error(f"Sandbox stdout: {result.stdout[:2000]}")
            if result.stderr:
                logger.error(f"Sandbox stderr: {result.stderr[:2000]}")

    async def _handle_jsonrpc(self, request: Request):
        """Main JSON-RPC endpoint handler"""
        rpc_request = None
        logger.info(f"[base_acp_server] received request: {datetime.now()}")
        try:
            data = await request.json()
            rpc_request = JSONRPCRequest(**data)

            # Check if the request is authenticated
            if refreshed_environment_variables and getattr(refreshed_environment_variables, "AGENT_API_KEY", None):
                authorization_header = request.headers.get("x-agent-api-key")
                if authorization_header != refreshed_environment_variables.AGENT_API_KEY:
                    return JSONRPCResponse(
                        id=rpc_request.id,
                        error=JSONRPCError(code=-32601, message="Unauthorized"),
                    )

            # Check if method is valid first
            try:
                method = RPCMethod(rpc_request.method)
            except ValueError:
                logger.error(f"Method {rpc_request.method} was invalid")
                return JSONRPCResponse(
                    id=rpc_request.id,
                    error=JSONRPCError(code=-32601, message=f"Method {rpc_request.method} not found"),
                )

            if method not in self._handlers or self._handlers[method] is None:
                logger.error(f"Method {method} not found on existing ACP server")
                return JSONRPCResponse(
                    id=rpc_request.id,
                    error=JSONRPCError(code=-32601, message=f"Method {method} not found"),
                )

            # Extract application headers using allowlist approach (only x-* headers)
            # Matches gateway's security filtering rules
            # Forward filtered headers via params.request.headers to agent handlers
            custom_headers = {
                key: value
                for key, value in request.headers.items()
                if key.lower().startswith("x-")
                and key.lower() not in FASTACP_HEADER_SKIP_EXACT
                and not any(key.lower().startswith(p) for p in FASTACP_HEADER_SKIP_PREFIXES)
            }

            # Parse params into appropriate model based on method and include headers
            params_model = PARAMS_MODEL_BY_METHOD[method]
            params_data = dict(rpc_request.params) if rpc_request.params else {}

            # Add custom headers to the request structure if any headers were provided
            # Gateway sends filtered headers via HTTP, SDK extracts and populates params.request
            if custom_headers:
                params_data["request"] = {"headers": custom_headers}
            params = params_model.model_validate(params_data)

            if method in RPC_SYNC_METHODS:
                handler = self._handlers[method]
                result = await handler(params)

                if rpc_request.id is None:
                    # Seems like you should return None for notifications
                    return None
                else:
                    # Handle streaming vs non-streaming for MESSAGE_SEND
                    if method == RPCMethod.MESSAGE_SEND and isinstance(result, AsyncGenerator):
                        return await self._handle_streaming_response(rpc_request.id, result)
                    else:
                        if isinstance(result, BaseModel):
                            result = result.model_dump()
                        return JSONRPCResponse(id=rpc_request.id, result=result)
            else:
                # If this is a notification (no request ID), process in background and return immediately
                if rpc_request.id is None:
                    asyncio.create_task(self._process_notification(method, params))
                    return JSONRPCResponse(id=None)

                # For regular requests, start processing in background but return immediately
                asyncio.create_task(self._process_request(rpc_request.id, method, params))

                # Return immediate acknowledgment
                return JSONRPCResponse(id=rpc_request.id, result={"status": "processing"})

        except Exception as e:
            logger.error(f"Error handling JSON-RPC request: {e}", exc_info=True)
            request_id = None
            if rpc_request is not None:
                request_id = rpc_request.id
            return JSONRPCResponse(
                id=request_id,
                error=JSONRPCError(code=-32603, message=str(e)).model_dump(),
            )

    async def _handle_streaming_response(self, request_id: int | str, async_gen: AsyncGenerator):
        """Handle streaming response by formatting TaskMessageUpdate objects as JSON-RPC stream"""

        async def generate_json_rpc_stream():
            try:
                async for chunk in async_gen:
                    # Each chunk should be a TaskMessageUpdate object
                    # Validate using Pydantic's TypeAdapter to ensure it's a proper TaskMessageUpdate
                    try:
                        # This will validate that chunk conforms to the TaskMessageUpdate union type
                        validated_chunk = task_message_update_adapter.validate_python(chunk)
                        # Use mode="json" to properly serialize datetime objects
                        chunk_data = validated_chunk.model_dump(mode="json")
                    except ValidationError as e:
                        raise TypeError(
                            f"Streaming chunks must be TaskMessageUpdate objects. Validation error: {e}"
                        ) from e
                    except Exception as e:
                        raise TypeError(
                            f"Streaming chunks must be TaskMessageUpdate objects, got {type(chunk)}: {e}"
                        ) from e

                    # Wrap in JSON-RPC response format
                    response = JSONRPCResponse(id=request_id, result=chunk_data)
                    # Use model_dump_json() which handles datetime serialization automatically
                    yield f"{response.model_dump_json()}\n"

            except Exception as e:
                logger.error(f"Error in streaming response: {e}", exc_info=True)
                error_response = JSONRPCResponse(
                    id=request_id,
                    error=JSONRPCError(code=-32603, message=str(e)).model_dump(),
                )
                yield f"{error_response.model_dump_json()}\n"

        return StreamingResponse(
            generate_json_rpc_stream(),
            media_type="application/x-ndjson",  # Newline Delimited JSON
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
            },
        )

    async def _process_notification(self, method: RPCMethod, params: Any):
        """Process a notification (request with no ID) in the background"""
        try:
            await self._handlers[method](params)
        except Exception as e:
            logger.error(f"Error processing notification {method}: {e}", exc_info=True)

    async def _process_request(self, request_id: int | str, method: RPCMethod, params: Any):
        """Process a request in the background"""
        try:
            await self._handlers[method](params)
            logger.info(f"Successfully processed request {request_id} for method {method}")
        except Exception as e:
            logger.error(
                f"Error processing request {request_id} for method {method}: {e}",
                exc_info=True,
            )

    """
    Define all possible decorators to be overriden and implemented by each ACP implementation
    Then the users can override the default handlers by implementing their own handlers

    ACP Type: Async
    Decorators:
    - on_task_create
    - on_task_event_send
    - on_task_cancel

    ACP Type: Sync
    Decorators:
    - on_message_send
    """

    # Type: Async
    def on_task_create(self, fn: Callable[[CreateTaskParams], Awaitable[Any]]):
        """Handle task/create method - syncs workspace down before handler runs"""
        # Register for sandboxing
        try:
            handler_ref = validate_handler_for_sandbox(fn)
            self._handler_refs[RPCMethod.TASK_CREATE] = handler_ref
            logger.info(f"Handler registered for sandboxing: {handler_ref.module}.{handler_ref.function}")
        except HandlerValidationError as e:
            logger.warning(f"Handler not suitable for sandboxing, will run in-process: {e}")

        # Wrap: fn → maybe_sandbox → workspace_sync
        maybe_sandboxed = self._wrap_with_maybe_sandbox(fn, RPCMethod.TASK_CREATE)
        handler_with_sync = self._wrap_with_workspace_sync(
            maybe_sandboxed, handler_name="on_task_create", sync_up_after=False
        )
        self._handlers[RPCMethod.TASK_CREATE] = self._wrap_handler(handler_with_sync)
        return fn

    # Type: Async
    def on_task_event_send(self, fn: Callable[[SendEventParams], Awaitable[Any]]):
        """Handle event/send method - syncs workspace down before and up after handler"""
        # Register for sandboxing
        try:
            handler_ref = validate_handler_for_sandbox(fn)
            self._handler_refs[RPCMethod.EVENT_SEND] = handler_ref
            logger.info(f"Handler registered for sandboxing: {handler_ref.module}.{handler_ref.function}")
        except HandlerValidationError as e:
            logger.warning(f"Handler not suitable for sandboxing, will run in-process: {e}")

        # Wrap: fn → maybe_sandbox → workspace_sync
        maybe_sandboxed = self._wrap_with_maybe_sandbox(fn, RPCMethod.EVENT_SEND)
        handler_with_sync = self._wrap_with_workspace_sync(
            maybe_sandboxed, handler_name="on_task_event_send", sync_up_after=True
        )
        self._handlers[RPCMethod.EVENT_SEND] = self._wrap_handler(handler_with_sync)
        return fn

    # Type: Async
    def on_task_cancel(self, fn: Callable[[CancelTaskParams], Awaitable[Any]]):
        """Handle task/cancel method"""
        # Register for sandboxing
        try:
            handler_ref = validate_handler_for_sandbox(fn)
            self._handler_refs[RPCMethod.TASK_CANCEL] = handler_ref
            logger.info(f"Handler registered for sandboxing: {handler_ref.module}.{handler_ref.function}")
        except HandlerValidationError as e:
            logger.warning(f"Handler not suitable for sandboxing, will run in-process: {e}")

        # Wrap: fn → maybe_sandbox (no workspace sync for cancel)
        maybe_sandboxed = self._wrap_with_maybe_sandbox(fn, RPCMethod.TASK_CANCEL)
        self._handlers[RPCMethod.TASK_CANCEL] = self._wrap_handler(maybe_sandboxed)
        return fn

    # Type: Sync
    def on_message_send(
        self,
        fn: Callable[
            [SendMessageParams],
            Awaitable[TaskMessageContent | list[TaskMessageContent] | AsyncGenerator[TaskMessageUpdate, None]],
        ],
    ):
        """Handle message/send method - supports both single and streaming responses

        For non-streaming: return a single TaskMessage
        For streaming: return an AsyncGenerator that yields TaskMessageUpdate objects
        """

        async def message_send_wrapper(params: SendMessageParams):
            """Special wrapper for message_send that handles both regular async functions and async generators"""
            # Check if the function is an async generator function

            # Regardless of whether the Agent developer implemented an Async generator or not, we will always turn the function into an async generator and yield SSE events back tot he Sb0 server so there is only one way for it to process the response. Then, based on the client's desire to stream or not, the Sb0 server will either yield back the async generator objects directly (if streaming) or aggregate the content into a list of TaskMessageContents and to dispatch to the client. This basically gives the Sb0 server the flexibility to handle both cases itself.

            if inspect.isasyncgenfunction(fn):
                # The client wants streaming, an async generator already streams the content, so just return it
                return fn(params)
            else:
                # The client wants streaming, but the function is not an async generator, so we turn it into one and yield each TaskMessageContent as a StreamTaskMessageFull which will be streamed to the client by the Sb0 server.
                task_message_content_response = await fn(params)
                # Handle None returns gracefully - treat as empty list
                if task_message_content_response is None:
                    task_message_content_list = []
                elif isinstance(task_message_content_response, list):
                    # Filter out None values from lists
                    task_message_content_list = [
                        content for content in task_message_content_response if content is not None
                    ]
                else:
                    task_message_content_list = [task_message_content_response]

                async def async_generator(task_message_content_list: list[TaskMessageContent]):
                    for i, task_message_content in enumerate(task_message_content_list):
                        yield StreamTaskMessageFull(type="full", index=i, content=task_message_content)

                return async_generator(task_message_content_list)

        self._handlers[RPCMethod.MESSAGE_SEND] = message_send_wrapper
        return fn

    """
    End of Decorators
    """

    """
    ACP Server Lifecycle Methods
    """

    def run(self, host: str = "0.0.0.0", port: int = 8000, **kwargs):
        """Start the Uvicorn server for async handlers."""
        uvicorn.run(self, host=host, port=port, **kwargs)
