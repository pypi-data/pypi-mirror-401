"""
RaysurferClient - Drop-in replacement for ClaudeSDKClient with code block caching.

This client wraps ClaudeSDKClient to:
1. Pre-fetch relevant code blocks from the Raysurfer backend
2. Download them as files to a sandbox directory
3. Inject file contents into the system prompt
4. Let the agent use standard Bash tool to execute

Uses Anthropic's sandbox runtime for secure execution.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncIterator, Union

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    # Message types (re-exported for convenience)
    Message,
    UserMessage,
    AssistantMessage,
    SystemMessage,
    ResultMessage,
    # Content block types
    TextBlock,
    ThinkingBlock,
    ToolUseBlock,
    ToolResultBlock,
)

from raysurfer.client import AsyncRaySurfer
from raysurfer.sdk_types import CodeFile, GetCodeFilesResponse

# Re-export message types for convenience
__all__ = [
    "RaysurferClient",
    "RaysurferAgentOptions",
    "Message",
    "UserMessage",
    "AssistantMessage",
    "SystemMessage",
    "ResultMessage",
    "TextBlock",
    "ThinkingBlock",
    "ToolUseBlock",
    "ToolResultBlock",
]


DEFAULT_SANDBOX_DIR = Path.home() / ".raysurfer" / "sandbox"


@dataclass
class RaysurferAgentOptions:
    """
    Configuration options for RaysurferClient.

    Extends ClaudeAgentOptions with Raysurfer-specific settings.
    All standard ClaudeAgentOptions fields are passed through to the wrapped client.
    """

    # Raysurfer-specific options
    raysurfer_api_key: str | None = None
    raysurfer_base_url: str = "https://web-production-3d338.up.railway.app"
    prefetch_count: int = 5  # Number of code files to pre-fetch
    min_verdict_score: float = 0.3  # Minimum quality threshold
    prefer_complete: bool = True  # Prefer more complete code blocks
    sandbox_dir: Path = field(default_factory=lambda: DEFAULT_SANDBOX_DIR)

    # Standard ClaudeAgentOptions fields (pass-through)
    # See: https://platform.claude.com/docs/en/agent-sdk/python
    allowed_tools: list[str] | None = None
    disallowed_tools: list[str] | None = None
    permission_mode: str | None = None  # "default", "acceptEdits", "plan", "bypassPermissions"
    system_prompt: str | dict[str, Any] | None = None  # str or SystemPromptPreset
    cwd: str | Path | None = None
    add_dirs: list[str | Path] | None = None
    max_turns: int | None = None
    model: str = "claude-opus-4-5"  # Default to Opus 4.5
    env: dict[str, str] | None = None
    mcp_servers: dict[str, Any] | None = None
    hooks: dict[str, Any] | None = None
    can_use_tool: Any | None = None
    setting_sources: list[str] | None = None
    include_partial_messages: bool = False
    fork_session: bool = False
    continue_conversation: bool = False
    resume: str | None = None
    agents: dict[str, Any] | None = None
    plugins: list[dict[str, Any]] | None = None
    enable_file_checkpointing: bool = False
    output_format: dict[str, Any] | None = None
    sandbox: dict[str, Any] | None = None
    extra_args: dict[str, str | None] | None = None
    max_buffer_size: int | None = None
    stderr: Any | None = None
    user: str | None = None
    settings: str | None = None
    permission_prompt_tool_name: str | None = None


class RaysurferClient:
    """
    Drop-in replacement for ClaudeSDKClient with Raysurfer code block caching.

    Pre-fetches relevant code blocks from the Raysurfer backend, downloads them
    to a sandbox directory, and injects their contents into the system prompt.
    The agent can then use the standard Bash tool to execute the code.

    Usage:
        options = RaysurferAgentOptions(
            raysurfer_api_key="rs_...",
            allowed_tools=["Read", "Write", "Bash"],
            system_prompt="You are a helpful assistant.",
        )

        async with RaysurferClient(options=options) as client:
            await client.query("Fetch data from the GitHub API")
            async for msg in client.receive_response():
                print(msg)
    """

    def __init__(self, options: RaysurferAgentOptions | None = None):
        self.options = options or RaysurferAgentOptions()
        self._raysurfer: AsyncRaySurfer | None = None
        self._claude_client: ClaudeSDKClient | None = None
        self._prefetched_files: list[CodeFile] = []
        self._current_query: str | None = None

    async def __aenter__(self) -> "RaysurferClient":
        """Initialize the Raysurfer client."""
        self._raysurfer = AsyncRaySurfer(
            api_key=self.options.raysurfer_api_key,
            base_url=self.options.raysurfer_base_url,
        )
        await self._raysurfer.__aenter__()

        # Ensure sandbox directory exists
        self.options.sandbox_dir.mkdir(parents=True, exist_ok=True)

        return self

    async def __aexit__(self, *args) -> None:
        """Clean up resources."""
        if self._claude_client:
            await self._claude_client.__aexit__(*args)
        if self._raysurfer:
            await self._raysurfer.__aexit__(*args)

    async def query(self, prompt: str) -> None:
        """
        Send a query to Claude with pre-fetched code files.

        1. Pre-fetches relevant code files from Raysurfer backend
        2. Downloads files to sandbox directory
        3. Injects file contents into system prompt
        4. Delegates to ClaudeSDKClient with sandbox enabled
        """
        self._current_query = prompt

        # Step 1: Pre-fetch relevant code files
        self._prefetched_files = await self._prefetch_code_files(prompt)

        # Step 2: Download files to sandbox directory
        await self._download_files_to_sandbox()

        # Step 3: Build ClaudeAgentOptions with augmented system prompt
        claude_options = self._build_claude_options()

        # Step 4: Initialize and query Claude
        self._claude_client = ClaudeSDKClient(options=claude_options)
        await self._claude_client.__aenter__()
        await self._claude_client.query(prompt)

    async def receive_response(self) -> AsyncIterator[Message]:
        """Receive and yield response messages from Claude."""
        if not self._claude_client:
            raise RuntimeError("Must call query() before receive_response()")

        async for message in self._claude_client.receive_response():
            yield message

    async def _prefetch_code_files(self, task: str) -> list[CodeFile]:
        """Pre-fetch relevant code files for the given task."""
        if not self._raysurfer:
            return []

        try:
            response = await self._raysurfer.get_code_files(
                task=task,
                top_k=self.options.prefetch_count,
                min_verdict_score=self.options.min_verdict_score,
                prefer_complete=self.options.prefer_complete,
            )
            return response.files
        except Exception:
            # Fail silently if backend is unavailable - agent can still work
            return []

    async def _download_files_to_sandbox(self) -> None:
        """Download pre-fetched code files to the sandbox directory."""
        for code_file in self._prefetched_files:
            filepath = self.options.sandbox_dir / code_file.filename
            filepath.write_text(code_file.source)

    def _build_claude_options(self) -> ClaudeAgentOptions:
        """Build ClaudeAgentOptions with sandbox and augmented system prompt."""
        # Build sandbox config (merge with user's sandbox config if provided)
        # Default to enabled unless user explicitly disables it
        sandbox_config: dict[str, Any] = {"enabled": True}
        if self.options.sandbox:
            sandbox_config.update(self.options.sandbox)

        return ClaudeAgentOptions(
            allowed_tools=self.options.allowed_tools or [],
            disallowed_tools=self.options.disallowed_tools or [],
            permission_mode=self.options.permission_mode,
            system_prompt=self._build_system_prompt(),
            cwd=str(self.options.sandbox_dir),  # Set cwd to sandbox dir
            add_dirs=self.options.add_dirs or [],
            max_turns=self.options.max_turns,
            model=self.options.model,
            env=self.options.env or {},
            mcp_servers=self.options.mcp_servers or {},
            hooks=self.options.hooks,
            can_use_tool=self.options.can_use_tool,
            setting_sources=self.options.setting_sources,
            include_partial_messages=self.options.include_partial_messages,
            fork_session=self.options.fork_session,
            continue_conversation=self.options.continue_conversation,
            resume=self.options.resume,
            agents=self.options.agents,
            plugins=self.options.plugins or [],
            enable_file_checkpointing=self.options.enable_file_checkpointing,
            output_format=self.options.output_format,
            sandbox=sandbox_config,
            extra_args=self.options.extra_args or {},
            max_buffer_size=self.options.max_buffer_size,
            stderr=self.options.stderr,
            user=self.options.user,
            settings=self.options.settings,
            permission_prompt_tool_name=self.options.permission_prompt_tool_name,
        )

    def _build_system_prompt(self) -> str | dict[str, Any]:
        """Build system prompt with injected code file contents."""
        base_prompt = self.options.system_prompt

        if not self._prefetched_files:
            return base_prompt or ""

        # If using a preset, append to the preset's append field
        if isinstance(base_prompt, dict) and base_prompt.get("type") == "preset":
            existing_append = base_prompt.get("append", "")
            snippets = self._format_code_snippets()
            return {
                **base_prompt,
                "append": existing_append + snippets,
            }

        # For string prompts, append directly
        base_str = base_prompt if isinstance(base_prompt, str) else ""
        return base_str + self._format_code_snippets()

    def _format_code_snippets(self) -> str:
        """Format pre-fetched code files as markdown for system prompt."""
        snippets = "\n\n## Available Code Snippets\n\n"
        snippets += "The following pre-validated code files are available in your working directory. "
        snippets += "You can execute them directly using the Bash tool.\n\n"

        for f in self._prefetched_files:
            snippets += f"### {f.filename}\n\n"
            snippets += f"**Description**: {f.description}\n\n"
            snippets += f"**Entrypoint**: `{f.entrypoint}`\n\n"
            snippets += f"**Verdict score**: {f.verdict_score:.0%} ({f.thumbs_up} thumbs up)\n\n"

            if f.dependencies:
                snippets += f"**Dependencies**: {', '.join(f.dependencies)}\n\n"

            snippets += f"```{f.language}\n{f.source}\n```\n\n"
            snippets += "---\n\n"

        return snippets

    @property
    def prefetched_files(self) -> list[CodeFile]:
        """Get the list of pre-fetched code files."""
        return self._prefetched_files

    @property
    def sandbox_dir(self) -> Path:
        """Get the sandbox directory path."""
        return self.options.sandbox_dir
