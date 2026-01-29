# bu-agent-sdk

_An agent is just a for-loop._

![Agent Loop](./static/agent-loop.png)

The simplest possible agent framework. No abstractions. No magic. Just a for-loop of tool calls. The framework powering [BU.app](https://bu.app).

## Install

```bash
uv sync
```

or

```bash
uv add bu-agent-sdk
```

## Quick Start

```python
import asyncio
from bu_agent_sdk import Agent, tool, TaskComplete
from bu_agent_sdk.llm import ChatAnthropic

@tool("Add two numbers")
async def add(a: int, b: int) -> int:
    return a + b

@tool("Signal task completion")
async def done(message: str) -> str:
    raise TaskComplete(message)

agent = Agent(
    llm=ChatAnthropic(model="claude-sonnet-4-20250514"),
    tools=[add, done],
)

async def main():
    result = await agent.query("What is 2 + 3?")
    print(result)

asyncio.run(main())
```

## Philosophy

**The Bitter Lesson:** All the value is in the RL'd model, not your 10,000 lines of abstractions.

Agent frameworks fail not because models are weak, but because their action spaces are incomplete. Give the LLM as much freedom as possible, then vibe-restrict based on evals.

## Features

### Done Tool Pattern

The naive "stop when no tool calls" approach fails. Agents finish prematurely. Force explicit completion:

```python
@tool("Signal completion")
async def done(message: str) -> str:
    raise TaskComplete(message)

agent = Agent(
    llm=llm,
    tools=[..., done],
    require_done_tool=True,  # Autonomous mode
)
```

### Ephemeral Messages

Large tool outputs (browser state, screenshots) blow up context. Keep only the last N:

```python
@tool("Get browser state", ephemeral=3)  # Keep last 3 only
async def get_state() -> str:
    return massive_dom_and_screenshot
```

### Simple LLM Primitives

~300 lines per provider. Same interface. Full control:

```python
from bu_agent_sdk.llm import ChatAnthropic, ChatOpenAI, ChatGoogle

# All implement BaseChatModel
agent = Agent(llm=ChatAnthropic(model="claude-sonnet-4-20250514"), tools=tools)
agent = Agent(llm=ChatOpenAI(model="gpt-4o"), tools=tools)
agent = Agent(llm=ChatGoogle(model="gemini-2.0-flash"), tools=tools)
```

### Context Compaction

Auto-summarize when approaching context limits:

```python
from bu_agent_sdk.agent import CompactionConfig

agent = Agent(
    llm=llm,
    tools=tools,
    compaction=CompactionConfig(threshold_ratio=0.80),
)
```

### Dependency Injection

FastAPI-style, type-safe:

```python
from typing import Annotated
from bu_agent_sdk import Depends

def get_db():
    return Database()

@tool("Query users")
async def get_user(id: int, db: Annotated[Database, Depends(get_db)]) -> str:
    return await db.find(id)
```

### Streaming Events

```python
from bu_agent_sdk.agent import ToolCallEvent, ToolResultEvent, FinalResponseEvent

async for event in agent.query_stream("do something"):
    match event:
        case ToolCallEvent(tool=name, args=args):
            print(f"Calling {name}")
        case ToolResultEvent(tool=name, result=result):
            print(f"{name} -> {result[:50]}")
        case FinalResponseEvent(content=text):
            print(f"Done: {text}")
```

## A CLI in 60 Lines

```python
#!/usr/bin/env python3
import asyncio
from bu_agent_sdk import Agent, tool, TaskComplete
from bu_agent_sdk.llm import ChatAnthropic

@tool("Execute shell command")
async def bash(command: str) -> str:
    proc = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
    )
    stdout, _ = await proc.communicate()
    return stdout.decode()

@tool("Read file")
async def read(path: str) -> str:
    return open(path).read()

@tool("Write file")
async def write(path: str, content: str) -> str:
    open(path, 'w').write(content)
    return f"Wrote {path}"

@tool("Task complete")
async def done(message: str) -> str:
    raise TaskComplete(message)

async def main():
    agent = Agent(
        llm=ChatAnthropic(model="claude-sonnet-4-20250514"),
        tools=[bash, read, write, done],
        system_prompt="You are a coding assistant.",
    )
    print("Agent ready. Ctrl+C to exit.")
    while True:
        try:
            task = input("\n> ")
            async for event in agent.query_stream(task):
                if hasattr(event, 'tool'):
                    print(f"  → {event.tool}")
                elif hasattr(event, 'content') and event.content:
                    print(f"\n{event.content}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    asyncio.run(main())
```

## Examples

See [`examples/`](./examples/) for more:

- `01_hello_world.py` - Simplest possible agent
- `07_minimal_cli.py` - 60-line CLI

## The Bitter Truth

Every abstraction is a liability. Every "helper" is a failure point.

The models got good. Really good. They were RL'd on computer use, coding, browsing. They don't need your guardrails. They need:

- A complete action space
- A for-loop
- An explicit exit
- Context management

**The bitter lesson: The less you build, the more it works.**

## License

MIT

## Credits

Built by [Browser Use](https://browser-use.com). Inspired by reverse-engineering Claude Code and Gemini CLI.
