# WBAL User Guide

WBAL (**W**eights & **B**iases **A**gent **L**ibrary) is a minimal framework for building LLM agents. It provides three core primitives: Agent, Environment, and LM.

## Installation

Install from PyPI:

```bash
pip install wbal
```

For local development from source:

```bash
git clone <this-repo>
cd wbal
uv sync
```

## Quick Start

Requires `OPENAI_API_KEY` in your environment.

```python
import os
import weave
from wbal import OpenAIWBAgent, GPT5MiniTester, weaveTool
from wbal.environments.chat_env import ChatEnv

weave.init(os.getenv("WEAVE_PROJECT", "my-project"))

# Define an environment with tools (and optional persistence)
class MyEnv(ChatEnv):
    env = "You are a helpful assistant."

    @weaveTool
    def greet(self, name: str) -> str:
        """Greet someone by name."""
        return f"Hello, {name}!"

# Create and run an agent (OpenAI Responses API)
env = MyEnv(task="Say hello to Alice, then call exit()", working_directory="./.wbal_state")
agent = OpenAIWBAgent(
    lm=GPT5MiniTester(),
    env=env,
    maxSteps=10,
    system_prompt="Use tools when helpful. Call exit() when you're done.",
)
agent.run()
```

## Core Concepts

### Agent

The `Agent` orchestrates the perceive-invoke-do loop:

1. **perceive()** - Gather observations, update state
2. **invoke()** - Call the LLM with messages and tools
3. **do()** - Execute tool calls from the LLM response

```python
from wbal import Agent, GPT5MiniTester

agent = Agent(
    lm=GPT5MiniTester,      # Language model
    env=MyEnv(),            # Environment with tools
    maxSteps=20,            # Max loop iterations
)
result = agent.run("Your task here")
```

### Environment

The `Environment` provides tools and context:

```python
from wbal import Environment, weaveTool

class MyEnv(Environment):
    env = "You are a helpful assistant."
    include_tools_in_observe = True

    # Instance variables become context
    task: str = "Default task description"

    @weaveTool
    def my_tool(self, query: str) -> str:
        """Tool description (shown to LLM)."""
        return f"Result for: {query}"
```

### Tools

Use `@weaveTool` to expose methods to the LLM:

```python
from wbal import weaveTool

@weaveTool
def search(query: str, limit: int = 10) -> str:
    """Search for information.

    Args:
        query: The search query
        limit: Maximum results to return
    """
    # Implementation
    return results
```

The docstring becomes the tool description. Type hints define the schema.

### Language Models

```python
from wbal import GPT5Large, GPT5MiniTester

# Production model (OpenAI)
agent = OpenAIWBAgent(lm=GPT5Large(), env=env)

# Testing/development model (faster, cheaper)
agent = OpenAIWBAgent(lm=GPT5MiniTester(), env=env)
```

## Stateful Environments

For persistent state across agent runs, WBAL provides two patterns:

1) **Recommended**: `DataEnv` / `ChatEnv` / `PollEnv` (shared notes + observations persisted to `environment_state.json`)
2) **Generic**: `StatefulEnvironment` (a simple JSON-backed state dict)

### DataEnv / ChatEnv / PollEnv (recommended)

```python
from wbal.environments.poll_env import PollEnv

env = PollEnv(task="Monitor something", working_directory="./.wbal_state")
env.store_note("last_status", "ok", category="health")
env.add_observation("poll cycle completed", category="health", severity="INFO")
```

### StatefulEnvironment (generic)

```python
from wbal import StatefulEnvironment

class MyStatefulEnv(StatefulEnvironment):
    observations: list[str] = []

    @weaveTool
    def add_observation(self, obs: str) -> str:
        """Record an observation."""
        self.observations.append(obs)
        self.save_state()  # Persist to disk
        return f"Recorded: {obs}"

# Load from disk (if present)
env = MyStatefulEnv(working_directory="./.wbal_state")
env.load_state()
```

## Exitable Agents

For agents that can decide when to stop, `OpenAIWBAgent` includes an `exit()` tool by default. If you’re building a custom agent on top of the base `Agent`, you can also use `ExitableAgent`.

```python
from wbal import ExitableAgent

class MyAgent(ExitableAgent):
    # Inherits exit() tool automatically
    pass

agent = MyAgent(env=env, maxSteps=50)
result = agent.run("Task that agent can exit from")
```

## Observability

All tool calls are traced with [Weave](https://wandb.ai/site/weave):

```python
import weave
weave.init('my-project')

# Now all agent runs are traced
agent.run("...")
```

View traces at: `https://wandb.ai/<entity>/<project>/weave`

## CLI

```bash
# Run (baseline, non-interactive)
wbal run --project my-project --task "Say hello to Alice, then call exit()" --working-dir ./.wbal_state

# Chat (interactive via tool calls)
wbal chat --project my-project --task "Say hello to Alice" --working-dir ./.wbal_state

# Poll (runs once or on an interval)
wbal poll --project my-project --task "Monitor health" --working-dir ./.wbal_state --interval 300

# Run from a YAML agent manifest
wbal run --project my-project --agent-spec path/to/agent.yaml --task "Do the thing"
```

## YAML Agent Manifests

WBAL can construct agents from YAML:
- prompts live in YAML files (system + optional extra system messages)
- agents declare LM config, max steps, tool modules, and (optionally) subagents
- multi-agent edges are explicit via `delegates` + the `run_agent` tool

See `examples/agents/README.md`.

## Agent Bundles (WandBSwarm-compatible)

WBAL can validate and run WandBSwarm-style “agent bundles” locally:

- `run.sh` (required)
- `install.sh` (optional)

Both scripts run with `cwd=$TASK_DIR` and get the same env vars as WandBSwarm:
`AGENT_DIR`, `TASK_DIR`, `WORKSPACE`, `RUN_ID`, `TASK_ID`, `EXPERIMENT_ID`, `BACKEND`.

```bash
wbal bundle validate --agent-dir path/to/agent
wbal bundle run --agent-dir path/to/agent --task-dir path/to/task --workspace-dir ./workspace
```

## API Reference

### Exports

```python
from wbal import (
    # Core classes
    Agent,
    Environment,
    StatefulEnvironment,
    DataEnv,
    ChatEnv,
    PollEnv,
    OpenAIWBAgent,
    YamlAgent,
    ExitableAgent,
    LM,
    GPT5Large,
    GPT5MiniTester,
    OpenAIResponsesLM,
    ScriptedLM,

    # YAML manifests
    AgentManifest,
    PromptManifest,
    load_agent_manifest,
    load_prompt_manifest,
    build_agent_from_file,

    # Decorators
    weaveTool,
    tool,

    # Helpers
    tool_timeout,
    ToolTimeoutError,
    format_openai_tool_response,
    to_openai_tool,
    to_anthropic_tool,

    # Bundles (WandBSwarm-compatible)
    AgentBundleEntry,
    validate_agent_bundle,
    run_agent_bundle,
    shell_agent_bundle,
)
```

### Agent Methods

| Method | Description |
|--------|-------------|
| `run(task)` | Run the agent loop until completion |
| `step()` | Execute one perceive-invoke-do cycle |
| `perceive()` | Override to customize observation gathering |
| `invoke()` | Override to customize LLM calls |
| `do()` | Override to customize tool execution |

### Environment Methods

| Method | Description |
|--------|-------------|
| `observe()` | Returns string representation of environment state |
| `save()` | (StatefulEnvironment) Persist state to disk |
| `load_or_create(path)` | (StatefulEnvironment) Load or create new instance |
