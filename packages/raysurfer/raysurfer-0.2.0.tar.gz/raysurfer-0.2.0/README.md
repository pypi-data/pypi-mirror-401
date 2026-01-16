# RaySurfer Python SDK

Store and retrieve code blocks for AI agents with semantic search and verdict-aware scoring.

## Install

```bash
pip install raysurfer
```

## Quick Start

```python
from raysurfer import RaySurfer

rs = RaySurfer(api_key="your-api-key")

# Store a code block
result = rs.store_code_block(
    name="fetch_weather",
    source="""
def fetch_weather(city: str) -> dict:
    import requests
    resp = requests.get(f"https://api.weather.com/{city}")
    return resp.json()
""",
    entrypoint="fetch_weather",
    language="python",
    description="Fetches weather data for a city",
    tags=["api", "weather"],
)
print(f"Stored: {result.code_block_id}")

# Retrieve code blocks by task
results = rs.retrieve("get weather data for a location")
for match in results.code_blocks:
    print(f"{match.code_block.name}: {match.score}")

# Get the single best match with verdict-aware scoring
best = rs.retrieve_best("fetch current temperature")
if best.best_match:
    print(f"Best: {best.best_match.code_block.name}")
    print(f"Confidence: {best.retrieval_confidence}")
```

## Async Usage

```python
from raysurfer import AsyncRaySurfer

async def main():
    async with AsyncRaySurfer(api_key="your-api-key") as rs:
        results = await rs.retrieve("parse JSON data")
        print(results.code_blocks)
```

## Store Execution Records

Track how code blocks perform to improve future retrieval:

```python
from raysurfer import RaySurfer, ExecutionState, AgentVerdict

rs = RaySurfer(api_key="your-api-key")

# After running a code block
rs.store_execution(
    code_block_id="cb_xxx",
    triggering_task="get weather for NYC",
    input_data={"city": "NYC"},
    output_data={"temp": 72, "conditions": "sunny"},
    execution_state=ExecutionState.COMPLETED,
    duration_ms=150,
    verdict=AgentVerdict.THUMBS_UP,
)
```

## API Reference

### `RaySurfer` / `AsyncRaySurfer`

**Store methods:**
- `store_code_block(...)` - Store a new code block
- `store_execution(...)` - Store an execution record with optional verdict

**Retrieve methods:**
- `retrieve(task)` - Semantic search for code blocks
- `retrieve_best(task)` - Get the single best match with scoring
- `get_few_shot_examples(task)` - Get examples for code generation
- `get_task_patterns(...)` - Get proven task→code mappings

## Verdict System

RaySurfer uses thumbs up/down verdicts that are **independent** of execution state:
- A technical error can be thumbs up (correct validation behavior)
- A successful execution can be thumbs down (useless output)

This allows the system to learn which code blocks are actually *useful*, not just which ones run without errors.
