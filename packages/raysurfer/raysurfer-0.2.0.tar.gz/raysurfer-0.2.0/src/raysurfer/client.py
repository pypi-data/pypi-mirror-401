"""RaySurfer SDK client"""

from typing import Any

import httpx

from raysurfer.exceptions import APIError, AuthenticationError
from raysurfer.types import (
    AgentReview,
    AgentVerdict,
    AlternativeCandidate,
    BestMatch,
    CodeBlock,
    CodeBlockMatch,
    ExecutionIO,
    ExecutionState,
    FewShotExample,
    RetrieveBestResponse,
    RetrieveCodeBlockResponse,
    StoreCodeBlockResponse,
    StoreExecutionResponse,
    TaskPattern,
)
from raysurfer.sdk_types import CodeFile, GetCodeFilesResponse

DEFAULT_BASE_URL = "https://web-production-3d338.up.railway.app"


class AsyncRaySurfer:
    """Async client for RaySurfer API"""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            )
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> "AsyncRaySurfer":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        client = await self._get_client()
        response = await client.request(method, path, **kwargs)

        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        if response.status_code >= 400:
            raise APIError(response.text, status_code=response.status_code)

        return response.json()

    # =========================================================================
    # Store API
    # =========================================================================

    async def store_code_block(
        self,
        name: str,
        source: str,
        entrypoint: str,
        language: str,
        description: str = "",
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        language_version: str | None = None,
        dependencies: list[str] | None = None,
        tags: list[str] | None = None,
        capabilities: list[str] | None = None,
        example_queries: list[str] | None = None,
    ) -> StoreCodeBlockResponse:
        """Store a new code block"""
        data = {
            "name": name,
            "description": description,
            "source": source,
            "entrypoint": entrypoint,
            "language": language,
            "input_schema": input_schema or {},
            "output_schema": output_schema or {},
            "language_version": language_version,
            "dependencies": dependencies or [],
            "tags": tags or [],
            "capabilities": capabilities or [],
            "example_queries": example_queries,
        }
        result = await self._request("POST", "/api/store/code-block", json=data)
        return StoreCodeBlockResponse(**result)

    async def store_execution(
        self,
        code_block_id: str,
        triggering_task: str,
        input_data: dict[str, Any],
        output_data: Any,
        execution_state: ExecutionState = ExecutionState.COMPLETED,
        duration_ms: int = 0,
        error_message: str | None = None,
        error_type: str | None = None,
        verdict: AgentVerdict | None = None,
        review: AgentReview | None = None,
    ) -> StoreExecutionResponse:
        """Store an execution record"""
        io = ExecutionIO(
            input_data=input_data,
            output_data=output_data,
            output_type=type(output_data).__name__,
        )
        data = {
            "code_block_id": code_block_id,
            "triggering_task": triggering_task,
            "io": io.model_dump(),
            "execution_state": execution_state.value,
            "duration_ms": duration_ms,
            "error_message": error_message,
            "error_type": error_type,
            "verdict": verdict.value if verdict else None,
            "review": review.model_dump() if review else None,
        }
        result = await self._request("POST", "/api/store/execution", json=data)
        return StoreExecutionResponse(**result)

    # =========================================================================
    # Retrieve API
    # =========================================================================

    async def retrieve(
        self,
        task: str,
        top_k: int = 10,
        min_verdict_score: float = 0.0,
    ) -> RetrieveCodeBlockResponse:
        """Retrieve code blocks by task description (semantic search)"""
        data = {
            "task": task,
            "top_k": top_k,
            "min_verdict_score": min_verdict_score,
        }
        result = await self._request("POST", "/api/retrieve/code-blocks", json=data)

        code_blocks = [
            CodeBlockMatch(
                code_block=CodeBlock(**cb["code_block"]),
                score=cb["score"],
                verdict_score=cb["verdict_score"],
                thumbs_up=cb["thumbs_up"],
                thumbs_down=cb["thumbs_down"],
                recent_executions=cb.get("recent_executions", []),
            )
            for cb in result["code_blocks"]
        ]
        return RetrieveCodeBlockResponse(
            code_blocks=code_blocks,
            total_found=result["total_found"],
        )

    async def retrieve_best(
        self,
        task: str,
        top_k: int = 10,
        min_verdict_score: float = 0.0,
    ) -> RetrieveBestResponse:
        """Get the single best code block for a task using verdict-aware scoring"""
        data = {
            "task": task,
            "top_k": top_k,
            "min_verdict_score": min_verdict_score,
        }
        result = await self._request("POST", "/api/retrieve/best-for-task", json=data)

        best_match = None
        if result.get("best_match"):
            bm = result["best_match"]
            best_match = BestMatch(
                code_block=CodeBlock(**bm["code_block"]),
                combined_score=bm["combined_score"],
                vector_score=bm["vector_score"],
                verdict_score=bm["verdict_score"],
                error_resilience=bm["error_resilience"],
                thumbs_up=bm["thumbs_up"],
                thumbs_down=bm["thumbs_down"],
            )

        alternatives = [
            AlternativeCandidate(**alt)
            for alt in result.get("alternative_candidates", [])
        ]

        return RetrieveBestResponse(
            best_match=best_match,
            alternative_candidates=alternatives,
            retrieval_confidence=result["retrieval_confidence"],
        )

    async def get_few_shot_examples(
        self,
        task: str,
        k: int = 3,
    ) -> list[FewShotExample]:
        """Retrieve few-shot examples for code generation"""
        data = {"task": task, "k": k}
        result = await self._request("POST", "/api/retrieve/few-shot-examples", json=data)
        return [FewShotExample(**ex) for ex in result["examples"]]

    async def get_task_patterns(
        self,
        task: str | None = None,
        code_block_id: str | None = None,
        min_thumbs_up: int = 0,
        top_k: int = 20,
    ) -> list[TaskPattern]:
        """Retrieve proven task→code mappings"""
        data = {
            "task": task,
            "code_block_id": code_block_id,
            "min_thumbs_up": min_thumbs_up,
            "top_k": top_k,
        }
        result = await self._request("POST", "/api/retrieve/task-patterns", json=data)
        return [TaskPattern(**p) for p in result["patterns"]]

    async def get_code_files(
        self,
        task: str,
        top_k: int = 5,
        min_verdict_score: float = 0.3,
        prefer_complete: bool = True,
    ) -> GetCodeFilesResponse:
        """
        Get code files for a task, ready to download to sandbox.

        Returns code blocks with full source code, optimized for:
        - High verdict scores (proven to work)
        - More complete implementations (prefer longer source)
        - Task relevance (semantic similarity)
        """
        data = {
            "task": task,
            "top_k": top_k,
            "min_verdict_score": min_verdict_score,
            "prefer_complete": prefer_complete,
        }
        result = await self._request("POST", "/api/retrieve/code-files", json=data)
        return GetCodeFilesResponse(
            files=[CodeFile(**f) for f in result["files"]],
            task=result["task"],
            total_found=result["total_found"],
        )


class RaySurfer:
    """Sync client for RaySurfer API"""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.Client | None = None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.Client(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            )
        return self._client

    def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None

    def __enter__(self) -> "RaySurfer":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        client = self._get_client()
        response = client.request(method, path, **kwargs)

        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        if response.status_code >= 400:
            raise APIError(response.text, status_code=response.status_code)

        return response.json()

    # =========================================================================
    # Store API
    # =========================================================================

    def store_code_block(
        self,
        name: str,
        source: str,
        entrypoint: str,
        language: str,
        description: str = "",
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        language_version: str | None = None,
        dependencies: list[str] | None = None,
        tags: list[str] | None = None,
        capabilities: list[str] | None = None,
        example_queries: list[str] | None = None,
    ) -> StoreCodeBlockResponse:
        """Store a new code block"""
        data = {
            "name": name,
            "description": description,
            "source": source,
            "entrypoint": entrypoint,
            "language": language,
            "input_schema": input_schema or {},
            "output_schema": output_schema or {},
            "language_version": language_version,
            "dependencies": dependencies or [],
            "tags": tags or [],
            "capabilities": capabilities or [],
            "example_queries": example_queries,
        }
        result = self._request("POST", "/api/store/code-block", json=data)
        return StoreCodeBlockResponse(**result)

    def store_execution(
        self,
        code_block_id: str,
        triggering_task: str,
        input_data: dict[str, Any],
        output_data: Any,
        execution_state: ExecutionState = ExecutionState.COMPLETED,
        duration_ms: int = 0,
        error_message: str | None = None,
        error_type: str | None = None,
        verdict: AgentVerdict | None = None,
        review: AgentReview | None = None,
    ) -> StoreExecutionResponse:
        """Store an execution record"""
        io = ExecutionIO(
            input_data=input_data,
            output_data=output_data,
            output_type=type(output_data).__name__,
        )
        data = {
            "code_block_id": code_block_id,
            "triggering_task": triggering_task,
            "io": io.model_dump(),
            "execution_state": execution_state.value,
            "duration_ms": duration_ms,
            "error_message": error_message,
            "error_type": error_type,
            "verdict": verdict.value if verdict else None,
            "review": review.model_dump() if review else None,
        }
        result = self._request("POST", "/api/store/execution", json=data)
        return StoreExecutionResponse(**result)

    # =========================================================================
    # Retrieve API
    # =========================================================================

    def retrieve(
        self,
        task: str,
        top_k: int = 10,
        min_verdict_score: float = 0.0,
    ) -> RetrieveCodeBlockResponse:
        """Retrieve code blocks by task description (semantic search)"""
        data = {
            "task": task,
            "top_k": top_k,
            "min_verdict_score": min_verdict_score,
        }
        result = self._request("POST", "/api/retrieve/code-blocks", json=data)

        code_blocks = [
            CodeBlockMatch(
                code_block=CodeBlock(**cb["code_block"]),
                score=cb["score"],
                verdict_score=cb["verdict_score"],
                thumbs_up=cb["thumbs_up"],
                thumbs_down=cb["thumbs_down"],
                recent_executions=cb.get("recent_executions", []),
            )
            for cb in result["code_blocks"]
        ]
        return RetrieveCodeBlockResponse(
            code_blocks=code_blocks,
            total_found=result["total_found"],
        )

    def retrieve_best(
        self,
        task: str,
        top_k: int = 10,
        min_verdict_score: float = 0.0,
    ) -> RetrieveBestResponse:
        """Get the single best code block for a task using verdict-aware scoring"""
        data = {
            "task": task,
            "top_k": top_k,
            "min_verdict_score": min_verdict_score,
        }
        result = self._request("POST", "/api/retrieve/best-for-task", json=data)

        best_match = None
        if result.get("best_match"):
            bm = result["best_match"]
            best_match = BestMatch(
                code_block=CodeBlock(**bm["code_block"]),
                combined_score=bm["combined_score"],
                vector_score=bm["vector_score"],
                verdict_score=bm["verdict_score"],
                error_resilience=bm["error_resilience"],
                thumbs_up=bm["thumbs_up"],
                thumbs_down=bm["thumbs_down"],
            )

        alternatives = [
            AlternativeCandidate(**alt)
            for alt in result.get("alternative_candidates", [])
        ]

        return RetrieveBestResponse(
            best_match=best_match,
            alternative_candidates=alternatives,
            retrieval_confidence=result["retrieval_confidence"],
        )

    def get_few_shot_examples(
        self,
        task: str,
        k: int = 3,
    ) -> list[FewShotExample]:
        """Retrieve few-shot examples for code generation"""
        data = {"task": task, "k": k}
        result = self._request("POST", "/api/retrieve/few-shot-examples", json=data)
        return [FewShotExample(**ex) for ex in result["examples"]]

    def get_task_patterns(
        self,
        task: str | None = None,
        code_block_id: str | None = None,
        min_thumbs_up: int = 0,
        top_k: int = 20,
    ) -> list[TaskPattern]:
        """Retrieve proven task→code mappings"""
        data = {
            "task": task,
            "code_block_id": code_block_id,
            "min_thumbs_up": min_thumbs_up,
            "top_k": top_k,
        }
        result = self._request("POST", "/api/retrieve/task-patterns", json=data)
        return [TaskPattern(**p) for p in result["patterns"]]

    def get_code_files(
        self,
        task: str,
        top_k: int = 5,
        min_verdict_score: float = 0.3,
        prefer_complete: bool = True,
    ) -> GetCodeFilesResponse:
        """
        Get code files for a task, ready to download to sandbox.

        Returns code blocks with full source code, optimized for:
        - High verdict scores (proven to work)
        - More complete implementations (prefer longer source)
        - Task relevance (semantic similarity)
        """
        data = {
            "task": task,
            "top_k": top_k,
            "min_verdict_score": min_verdict_score,
            "prefer_complete": prefer_complete,
        }
        result = self._request("POST", "/api/retrieve/code-files", json=data)
        return GetCodeFilesResponse(
            files=[CodeFile(**f) for f in result["files"]],
            task=result["task"],
            total_found=result["total_found"],
        )
