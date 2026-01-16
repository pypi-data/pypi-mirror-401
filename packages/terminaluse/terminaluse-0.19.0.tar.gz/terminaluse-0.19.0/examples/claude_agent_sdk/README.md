# Claude Agent SDK Integration Example

This example demonstrates how to integrate the **Claude Agent SDK** with Sb0. It shows the seamless message handling where Claude SDK messages are automatically converted to platform types that the UI understands.

## Running

```bash
docker build -f examples/claude_agent_sdk/Dockerfile -t my-agent:latest .

docker run -p 8000:8000 -t \
  -e AGENT_NAME=p2 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e SB0_BASE_URL=http://host.docker.internal:5003 \
  -e ACP_URL="http://host.docker.internal" \
  -e REDIS_URL="redis://host.docker.internal:6379" \
  --cap-add=SYS_ADMIN \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=src/sb0/lib/sandbox/seccomp-profile.json \
  my-agent:latest
```

## Key Concepts

1. **Direct Message Passing**: Claude SDK messages (`AssistantMessage`, `UserMessage`, `StreamEvent`, etc.) are passed directly to `adk.messages.create()` - no manual conversion needed.

2. **Automatic Streaming**: Streaming events are automatically accumulated and displayed in real-time in the UI.

3. **Platform Type Conversion**: Claude messages are converted to platform types the UI expects:
   - `AssistantMessage` with text → `TextContent`
   - `AssistantMessage` with tool_use → `ToolRequestContent`
   - `UserMessage` with tool_result → `ToolResponseContent`
   - `StreamEvent` → Accumulated and streamed in real-time
   - `ResultMessage` → `DataContent` with usage info

## Usage Pattern

```python
from claude_agent_sdk import ClaudeAgentOptions, query
from sb0.lib import adk

# Configure Claude Agent SDK
options = ClaudeAgentOptions(
    # Add tools, MCP servers, etc.
)

# Query Claude and stream messages to the UI
async for message in query(prompt=user_message, options=options):
    # Pass Claude SDK messages directly - automatic conversion!
    await adk.messages.create(task_id=params.task.id, content=message)
```

## Running the Agent

1. Install dependencies:
```bash
sb0 uv sync
```

2. Set your API key:
```bash
export ANTHROPIC_API_KEY=your-key-here
```

3. Run the agent locally:
```bash
export ENVIRONMENT=development
uv run sb0 agents run --manifest manifest.yaml
```

The agent will start on port 8000 and respond to messages using Claude.

## What's Inside

- **`project/acp.py`**: The main agent code demonstrating Claude SDK integration
- **`manifest.yaml`**: Agent configuration and deployment settings
- **`pyproject.toml`**: Dependencies including `claude-agent-sdk`

## Project Structure

```
100_claude_agent_sdk/
├── project/                  # Your agent's code
│   ├── __init__.py
│   └── acp.py               # Claude SDK integration example
├── Dockerfile               # Container definition
├── manifest.yaml            # Deployment config
├── dev.ipynb                # Development notebook for testing
└── pyproject.toml           # Dependencies (uv)
```

## Advanced Usage

### Storing Raw Messages for Analysis

If you need to store the raw Claude messages for downstream analysis:

```python
await adk.messages.create(
    task_id=params.task.id,
    content=message,
    store_raw_claude_message=True  # Also stores ClaudeMessageContent
)
```

### Adding Tools

```python
from claude_agent_sdk import ClaudeAgentOptions, Tool

options = ClaudeAgentOptions(
    tools=[
        Tool(
            name="search",
            description="Search the web",
            input_schema={...}
        )
    ]
)
```

### Adding MCP Servers

```python
from claude_agent_sdk import ClaudeAgentOptions, MCPServer

options = ClaudeAgentOptions(
    mcp_servers=[
        MCPServer(
            name="filesystem",
            command="mcp-server-filesystem",
            args=["/path/to/files"]
        )
    ]
)
```

## Local Development

### 1. Start the Sb0 Backend
```bash
cd sb0
make dev
```

### 2. Setup Your Agent's Environment
```bash
sb0 uv sync
source .venv/bin/activate
```

### 3. Run Your Agent
```bash
export ENVIRONMENT=development
export ANTHROPIC_API_KEY=your-key-here
sb0 agents run --manifest manifest.yaml
```

### 4. Interact with Your Agent

Use the Web UI:
```bash
cd sb0-web
make dev
# Open http://localhost:3000
```

Or use the development notebook (`dev.ipynb`) to test interactively.
