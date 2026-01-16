# Raysurfer Python SDK

Python SDK for Raysurfer - code block caching and retrieval for AI agents with Claude Agent SDK integration.

## Installation

```bash
pip install raysurfer
```

## Quick Start

### Basic Client (Store/Retrieve Code Blocks)

```python
from raysurfer import AsyncRaySurfer

async with AsyncRaySurfer(api_key="rs_...") as client:
    # Store a code block
    result = await client.store_code_block(
        name="GitHub User Fetcher",
        source="def fetch_user(username): ...",
        entrypoint="fetch_user",
        language="python",
    )

    # Retrieve code blocks for a task
    response = await client.retrieve(task="Fetch GitHub user data")
    for match in response.code_blocks:
        print(match.code_block.name, match.verdict_score)
```

### Claude Agent SDK Integration

```python
from raysurfer import RaysurferClient, RaysurferAgentOptions

options = RaysurferAgentOptions(
    raysurfer_api_key="rs_...",
    allowed_tools=["Read", "Write", "Bash"],
    system_prompt="You are a helpful assistant.",
    model="claude-opus-4-5",  # Default
)

async with RaysurferClient(options=options) as client:
    # Pre-fetches code files, downloads to sandbox, injects into prompt
    await client.query("Fetch user data from GitHub API")

    # Agent sees code files in system prompt and can execute with Bash
    async for msg in client.receive_response():
        print(msg)
```

## RaysurferAgentOptions

Drop-in replacement options for `ClaudeAgentOptions` with Raysurfer-specific settings:

```python
@dataclass
class RaysurferAgentOptions:
    # Raysurfer-specific
    raysurfer_api_key: str | None = None
    raysurfer_base_url: str = "https://api.raysurfer.com"
    prefetch_count: int = 5
    min_verdict_score: float = 0.3
    prefer_complete: bool = True
    sandbox_dir: Path = ~/.raysurfer/sandbox

    # Standard ClaudeAgentOptions (all passed through)
    allowed_tools: list[str] | None = None
    model: str = "claude-opus-4-5"
    system_prompt: str | dict | None = None
    sandbox: dict | None = None
    # ... all other ClaudeAgentOptions fields
```

## How It Works

1. **On `query()`**: RaysurferClient calls the backend to get relevant code files
2. **Downloads to sandbox**: Files are written to `~/.raysurfer/sandbox/`
3. **Injects into prompt**: Code snippets are added to the system prompt
4. **Agent executes**: Agent can run the code using the Bash tool within the sandbox

---

# Claude Agent SDK Python Reference

## Core Classes

### `ClaudeSDKClient`

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("Hello Claude")
    async for message in client.receive_response():
        print(message)
```

### `ClaudeAgentOptions`

```python
ClaudeAgentOptions(
    allowed_tools=["Read", "Write", "Bash"],
    disallowed_tools=[],
    permission_mode="acceptEdits",  # or "default", "plan", "bypassPermissions"
    system_prompt="You are helpful.",
    model="claude-opus-4-5",
    cwd="/path/to/project",
    sandbox={"enabled": True},
    max_turns=10,
    # ... more options
)
```

Key parameters:
- `allowed_tools`: Tools the agent can use
- `permission_mode`: How permissions are handled
- `model`: Claude model to use
- `sandbox`: Enable sandboxed execution
- `setting_sources`: `["user", "project", "local"]` to load CLAUDE.md files

### `SandboxSettings`

```python
sandbox={
    "enabled": True,
    "autoAllowBashIfSandboxed": True,
    "excludedCommands": ["docker"],
    "network": {
        "allowLocalBinding": True,
    }
}
```

## Message Types

```python
from claude_agent_sdk import (
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)

async for message in client.receive_response():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
            elif isinstance(block, ToolUseBlock):
                print(f"Using tool: {block.name}")
    elif isinstance(message, ResultMessage):
        print(f"Done! Cost: ${message.total_cost_usd}")
```

## Custom Tools

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("greet", "Greet a user", {"name": str})
async def greet(args):
    return {"content": [{"type": "text", "text": f"Hello, {args['name']}!"}]}

server = create_sdk_mcp_server("my-tools", tools=[greet])

options = ClaudeAgentOptions(
    mcp_servers={"tools": server},
    allowed_tools=["mcp__tools__greet"],
)
```

## Error Handling

```python
from claude_agent_sdk import (
    CLINotFoundError,
    ProcessError,
    CLIConnectionError,
)

try:
    async for message in query(prompt="Hello"):
        print(message)
except CLINotFoundError:
    print("Install Claude Code: npm install -g @anthropic-ai/claude-code")
except ProcessError as e:
    print(f"Process failed: {e.exit_code}")
```
