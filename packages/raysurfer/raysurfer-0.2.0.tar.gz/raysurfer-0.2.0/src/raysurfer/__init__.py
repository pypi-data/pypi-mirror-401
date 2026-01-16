"""
RaySurfer Python SDK

Store and retrieve code blocks for AI agents with semantic search
and verdict-aware scoring.

Includes Claude Agent SDK integration via RaysurferClient.
"""

from raysurfer.client import RaySurfer, AsyncRaySurfer
from raysurfer.sdk_client import RaysurferClient, RaysurferAgentOptions
from raysurfer.types import (
    AgentReview,
    AgentVerdict,
    BestMatch,
    CodeBlock,
    ExecutionIO,
    ExecutionRecord,
    ExecutionState,
    FewShotExample,
    TaskPattern,
)
from raysurfer.sdk_types import CodeFile, GetCodeFilesResponse
from raysurfer.exceptions import RaySurferError, APIError, AuthenticationError

__version__ = "0.2.0"

__all__ = [
    # Clients
    "RaySurfer",
    "AsyncRaySurfer",
    # Claude Agent SDK integration
    "RaysurferClient",
    "RaysurferAgentOptions",
    # Types
    "AgentReview",
    "AgentVerdict",
    "BestMatch",
    "CodeBlock",
    "CodeFile",
    "ExecutionIO",
    "ExecutionRecord",
    "ExecutionState",
    "FewShotExample",
    "GetCodeFilesResponse",
    "TaskPattern",
    # Exceptions
    "RaySurferError",
    "APIError",
    "AuthenticationError",
]
