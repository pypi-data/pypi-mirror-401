# WBAL Project Status

Last updated: 2026-01-08

## Current State: 80% Complete

The core agent framework is solid and functional. Main gaps are CLI ergonomics and a few bugs.

---

## What Works Well

### CLI Entrypoints (`wbal`)

| Command | Description |
|---------|-------------|
| `wbal chat` | Interactive chat agent with user input |
| `wbal poll` | Polling agent (can run on interval) |
| `wbal run` | Non-interactive baseline agent |
| `wbal bundle validate` | Validate WandBSwarm bundle |
| `wbal bundle run` | Run a bundle locally |
| `wbal bundle shell` | Shell with bundle env vars |

All commands support:
- `--agent-spec <path.yaml>` - Load agent from YAML manifest
- `--task <string>` - Set the task
- `--max-steps <int>` - Limit steps (default: 20)
- `--working-dir <path>` - State persistence directory
- `--project <name>` - Project name (required)
- `--org <name>` - Organization name (optional)

### YAML Manifests

Full `AgentManifest` schema:

```yaml
name: "my-agent"
description: "What this agent does"

# Prompt configuration
prompt: "./prompts/system.yaml"  # or inline:
system_prompt: "You are a helpful assistant..."
system_messages:
  - "Additional context message 1"
  - "Additional context message 2"

# Language model
lm:
  kind: openai_responses  # or: gpt5_large, gpt5_mini, scripted
  model: "gpt-5-mini"
  temperature: 0.7  # optional
  reasoning:
    effort: "minimal"
  include:
    - "reasoning.encrypted_content"

# Environment
env:
  kind: data  # or: basic, chat, poll
  task: "Default task if not provided via CLI"
  env: "Environment description and context"
  working_directory: "./workspace"
  include_working_directory_listing: true
  include_tools_in_observe: false

# Tools
tools:
  agent:
    - "mymodule:my_tool_function"
  env:
    - "wbal.tools.bash:bash"

# Execution settings
max_steps: 50
maxSteps: 50  # alias
tool_timeout: 60
parallel_tool_calls: false
max_concurrent_tool_calls: 4

# Multi-agent delegation
delegates:
  worker: "./agents/worker.agent.yaml"
  researcher: "./agents/researcher.agent.yaml"
share_working_directory: true
```

### Environment Flavors

| Kind | Class | Features |
|------|-------|----------|
| `basic` | `ConfiguredEnvironment` | Minimal, just task/env/tools |
| `data` | `ConfiguredDataEnv` | Persistent state, notes, observations |
| `poll` | `ConfiguredPollEnv` | `store_note`, `delete_note` tools |
| `chat` | `ConfiguredChatEnv` | Interactive `chat()` tool, user input |

### Multi-Agent Delegation

YamlAgent has built-in tools:
- `list_agents()` - List available subagents
- `run_agent(agent, task, max_steps)` - Call a delegate

Delegates are defined in the manifest and resolved relative to the manifest path.

### Tool Loading

Tools can be loaded from import specs:
```yaml
tools:
  agent:
    - "mypackage.tools:search"      # function
    - "mypackage.tools:MyToolClass" # class with @tool methods
  env:
    - "wbal.tools.bash:bash"
```

### LM Options

| Kind | Class | Notes |
|------|-------|-------|
| `openai_responses` | `OpenAIResponsesLM` | Generic, any model string |
| `gpt5_large` | `GPT5Large` | GPT-5 with reasoning.encrypted_content |
| `gpt5_mini` | `GPT5MiniTester` | GPT-5-mini with minimal reasoning |
| `scripted` | `ScriptedLM` | Deterministic for tests |

### Bundle Support

WandBSwarm-compatible bundles:
```
agent-bundle/
├── run.sh       # Required - main entry point
├── install.sh   # Optional - dependency installation
└── agent.yaml   # Your agent manifest
```

---

## Known Bugs

### 1. Temperature Always Set in `build_lm()` (manifests.py)

**Problem**: `build_lm()` always sets `inst.temperature = lm.temperature`, even when it should be None. This breaks reasoning models that reject the temperature parameter.

**Location**: `wbal/manifests.py:71-85`

**Fix**:
```python
# Change LMManifest default
temperature: float | None = None  # was: float = 1.0

# In build_lm(), only set if specified:
if lm.kind == "gpt5_mini":
    inst = GPT5MiniTester()
    if lm.temperature is not None:
        inst.temperature = lm.temperature
    # ...
```

### 2. Duplicate Import in yaml_agent.py

**Location**: `wbal/agents/yaml_agent.py:168-175`

The `run_agent` method has duplicate import statements and duplicate code block.

---

## Missing Features

### High Priority

| Feature | Description | Effort |
|---------|-------------|--------|
| `--weave-project` CLI flag | Enable weave tracking from CLI | Small |
| Fix temperature bug | Propagate Optional[float] fix to manifests | Small |
| `wbal init` command | Scaffold new agent.yaml templates | Medium |

### Medium Priority

| Feature | Description | Effort |
|---------|-------------|--------|
| `--model` CLI override | Override LM model from command line | Small |
| `wbal list` command | List agents in a directory | Small |
| Better error messages | More helpful errors for manifest issues | Medium |
| Async agent support | async perceive/invoke/do loop | Large |

### Low Priority

| Feature | Description | Effort |
|---------|-------------|--------|
| `wbal validate` command | Validate a manifest without running | Small |
| Agent composition docs | Examples of multi-agent patterns | Medium |
| Provider abstraction | Support Anthropic, etc. beyond OpenAI | Large |

---

## Testing Status

| Area | Coverage | Notes |
|------|----------|-------|
| Agent loop | Good | `test_agent.py` |
| Helper/tools | Good | `test_helper.py` |
| LM classes | Basic | `test_lm.py` |
| Bundles | Good | `test_bundle.py` |
| CLI | Basic | `test_cli_run.py` |
| YAML manifests | Partial | Needs more edge cases |
| Multi-agent | Minimal | Needs delegation tests |

---

## File Structure

```
wbal/
├── wbal/
│   ├── __init__.py          # Public exports
│   ├── agent.py              # Base Agent class
│   ├── environment.py        # Base Environment classes
│   ├── lm.py                 # LM classes (OpenAI, GPT5, Scripted)
│   ├── helper.py             # @tool decorator, schema extraction
│   ├── object.py             # WBALObject base
│   ├── manifests.py          # YAML manifest loading
│   ├── cli.py                # CLI entrypoint
│   ├── bundle.py             # WandBSwarm bundle support
│   ├── tool_imports.py       # Dynamic tool loading
│   ├── agents/
│   │   ├── openai_agent.py   # OpenAIWBAgent
│   │   └── yaml_agent.py     # YamlAgent (manifest-driven)
│   ├── environments/
│   │   ├── data_env.py       # DataEnv (persistent state)
│   │   ├── poll_env.py       # PollEnv (store/delete notes)
│   │   ├── chat_env.py       # ChatEnv (interactive)
│   │   └── configured_env.py # Tool-loadable env variants
│   └── tools/
│       └── bash.py           # Bash tool implementation
├── examples/
│   ├── simple_example.py
│   ├── zagent_v1.py
│   └── agents/               # Example YAML agents
├── tests/
└── docs/
    ├── README.md
    ├── USER.md
    ├── DEVELOPER.md
    └── Agent_Instructions.md
```

---

## Next Steps

1. **Fix temperature bug** - Update `LMManifest` and `build_lm()` 
2. **Add `--weave-project`** - Wire weave.init() into CLI commands
3. **Add `wbal init`** - Scaffold command for new agents
4. **Clean up yaml_agent.py** - Remove duplicate code block
5. **Add more tests** - Especially for multi-agent delegation
