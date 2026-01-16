"""Multi-Agent Demo: Sales Forecaster & Inventory Order Agents.

This example demonstrates how to create multiple agent types within one service:
1. Sales Forecaster Agent - Simple agent with system prompt, no tools
2. Inventory Order Agent - Agent with order_inventory tool
3. Sales Forecast + Order Inventory Agent - Combined agent that creates child tasks

The agent type is determined by the 'agent_type' parameter passed during task creation.
"""

from __future__ import annotations

from typing import Any

from claude_agent_sdk import ClaudeAgentOptions, tool, query, create_sdk_mcp_server
from claude_agent_sdk.types import ResultMessage

from sb0.lib import adk
from sb0.lib.types.acp import SendEventParams, CancelTaskParams, CreateTaskParams
from sb0.lib.utils.logging import make_logger
from sb0.types.data_content import DataContent
from sb0.types.text_content import TextContent
from sb0.lib.sdk.agent_server import AgentServer

logger = make_logger(__name__)

# Create an agent server
server = AgentServer()


# ============================================================================
# Agent Type Constants
# ============================================================================
AGENT_TYPE_SALES_FORECASTER = "sales_forecaster"
AGENT_TYPE_INVENTORY_ORDER = "inventory_order"


# ============================================================================
# Custom Tool: Order Inventory
# ============================================================================
@tool(
    "order_inventory", "Place an inventory order for a specific month and number of units", {"month": str, "units": int}
)
async def order_inventory(args: dict[str, Any]) -> dict[str, Any]:
    """Dummy tool that always returns success."""
    month = args["month"]
    units = args["units"]
    logger.info(f"Order inventory called: month={month}, units={units}")
    return {
        "content": [{"type": "text", "text": f"Inventory order successfully submitted for {units} units in {month}"}]
    }


# Create MCP server with the inventory tool
inventory_tools_server = create_sdk_mcp_server(name="inventory-tools", version="1.0.0", tools=[order_inventory])


def get_agent_config(agent_type: str | None) -> dict:
    """Get configuration based on agent type."""
    if agent_type == AGENT_TYPE_INVENTORY_ORDER:
        return {
            "mcp_servers": {"inventory-tools": inventory_tools_server},
            "allowed_tools": ["Read", "Glob", "Grep", "Write", "Bash", "mcp__inventory-tools__order_inventory"],
            "welcome_message": "I'm the Inventory Order Agent. I can help you place inventory orders. Just tell me what month and how many units you'd like to order.",
        }
    else:  # Default to sales forecaster
        return {
            "mcp_servers": None,
            "allowed_tools": ["Read", "Glob", "Grep", "Write", "Bash"],
            "welcome_message": "I'm the Sales Forecasting Agent. I can analyze sales data and provide forecasts. Share your historical data or ask me about projected sales.",
        }


@server.on_task_create
async def handle_task_create(params: CreateTaskParams):
    """Handle task creation.

    Initialize any state or resources needed for the task.
    Determine agent type from params and send appropriate welcome message.
    """
    logger.info(f"Task created: {params.task.id}")

    # Get agent type from params (default to sales_forecaster)
    agent_type = params.params.get("agent_type") if params.params else None
    system_prompt = params.params.get("system_prompt") if params.params else None

    logger.info(f"Agent type: {agent_type or 'sales_forecaster (default)'}")

    # Send welcome message based on agent type
    # await adk.messages.create(
    #     task_id=params.task.id,
    #     content=TextContent(
    #         author="agent",
    #         content=config["welcome_message"],
    #     ),
    # )

    # Initialize state with agent type for later use
    await adk.state.create(
        task_id=params.task.id,
        agent_id=params.agent.id,
        state={
            "agent_type": agent_type,
            "system_prompt": system_prompt,
        },
    )


@server.on_task_event_send
async def handle_task_event_send(params: SendEventParams):
    """Handle incoming messages from users.

    Routes to appropriate agent behavior based on agent type.
    """
    logger.info(f"Received event for task {params.task.id}: {params.event.id}")

    try:
        # Parse user message
        if isinstance(params.event.content, TextContent):
            user_message = params.event.content
        elif isinstance(params.event.content, DataContent):
            user_message = TextContent(
                author="user",
                content=f"Received data event: {params.event.content.data}",
            )
        else:
            raise ValueError("Got an unsupported message type. Only text or data messages are supported.")

        # Get agent type and configuration
        state = await adk.state.get_by_task_and_agent(task_id=params.task.id, agent_id=params.agent.id)
        agent_type = state.state.get("agent_type") if state and state.state else None
        system_prompt = state.state.get("system_prompt") if state and state.state else None
        session_id = state.state.get("session_id") if state and state.state else None

        logger.info(f"Using Claude session ID {session_id}")

        config = get_agent_config(agent_type)

        # Log stderr for debugging
        def log_stderr(line: str) -> None:
            logger.warning(f"Claude stderr: {line}")

        # Configure Claude Agent SDK options based on agent type
        options = ClaudeAgentOptions(
            include_partial_messages=True,
            permission_mode="bypassPermissions",
            cwd="/workspace",
            system_prompt="always do your work in /workspace" + (system_prompt or ""),
            mcp_servers=config["mcp_servers"],
            allowed_tools=config["allowed_tools"],  # Allow all tools from MCP servers
            resume=session_id,
            stderr=log_stderr,
            model="claude-haiku-4-5",
        )

        # MCP servers require streaming mode (bidirectional communication)
        # Wrap the prompt in an async generator to enable streaming
        async def prompt_stream():
            yield {
                "type": "user",
                "message": {"role": "user", "content": user_message.content},
            }

        async for message in query(prompt=prompt_stream(), options=options):
            await adk.messages.create(task_id=params.task.id, content=message)

            if isinstance(message, ResultMessage):
                session_id = message.session_id
                await adk.state.update(
                    state_id=state.id,
                    task_id=params.task.id,
                    agent_id=params.agent.id,
                    state={
                        **state.state,  # Preserve existing state (agent_type, system_prompt, etc.)
                        "session_id": session_id,
                    },
                )

    except Exception as e:
        # Extract underlying errors from ExceptionGroup/TaskGroup
        error_msg = str(e)
        if hasattr(e, "exceptions"):  # ExceptionGroup
            error_details = [f"  - {type(sub).__name__}: {sub}" for sub in e.exceptions]
            error_msg = f"{e}\nUnderlying errors:\n" + "\n".join(error_details)

        logger.error(f"Error querying Claude: {error_msg}")
        await adk.messages.create(
            task_id=params.task.id,
            content=TextContent(
                author="agent",
                content=f"Sorry, I encountered an error: {error_msg}",
            ),
        )


@server.on_task_cancel
async def handle_task_cancel(params: CancelTaskParams):
    """Handle task cancellation.

    Clean up any resources or state when a task is cancelled.
    """
    logger.info(f"Task cancelled: {params.task.id}")
