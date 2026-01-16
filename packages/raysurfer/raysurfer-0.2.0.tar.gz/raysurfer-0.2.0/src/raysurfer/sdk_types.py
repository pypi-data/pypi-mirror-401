"""Types for Claude Agent SDK integration"""

from typing import Any

from pydantic import BaseModel, Field


class CodeFile(BaseModel):
    """A code file ready to be written to sandbox"""

    code_block_id: str
    filename: str  # e.g., "github_fetcher.py"
    source: str  # Full source code
    entrypoint: str  # Function to call
    description: str
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    language: str
    dependencies: list[str] = Field(default_factory=list)
    verdict_score: float
    thumbs_up: int
    thumbs_down: int


class GetCodeFilesResponse(BaseModel):
    """Response with code files for a task"""

    files: list[CodeFile]
    task: str
    total_found: int
