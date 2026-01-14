# WBAL YAML-First Runner Plan (Agents)

Goal: make “specify everything in YAML, then run it” the default WBAL workflow by moving the runner pattern (currently reimplemented per-agent in `factory`, e.g. `factory/src/factory/f1/runner.py`) into `wbal`. This should work for *any* YAML-authored agent, while keeping WBAL’s existing convenience entrypoints (`run`, `chat`, `poll`) as thin wrappers.

## Target UX
- Run a spec by path: `wbal agents run --spec path/to/agent.yaml --task "..."`.
- Run an installed/registered agent by name: `wbal agents run f1 --task "..." --model kimi`.
- Pass templating vars: `--var KEY=VALUE` (repeatable).
- Pass overrides without custom wrappers: `--set lm.model=gpt-5-mini --set agent.tool_timeout=1800`.
- Enable tracing: `--weave-project wandb/<project>` (sets `WEAVE_PROJECT` + calls `weave.init`).
- Inject env vars for providers: `--env WANDB_API_KEY=... --env OPENAI_API_KEY=...` (repeatable).
- Optional standardized run metadata: `--metadata-out run.json`.

## Principle: YAML Is the Source of Truth
- Provider selection is explicit via YAML (primarily `lm.import_path`), not by guessing from model strings.
- Defaults live in YAML (LM class, model id, max steps, tool timeout, env kind, prompt files, tool modules).
- CLI flags are primarily *execution wiring* (task text, vars, trace project, metadata output, env injection).
- `--set` exists for ad-hoc experiments, but should not be required for normal use.

## CLI Shape (Proposed)
- New command group to avoid breaking existing `wbal run/chat/poll`:
  - `wbal agents run [NAME] [--spec PATH] ...`
  - `wbal agents list` (lists registered names + spec locations)
  - `wbal agents validate --spec PATH` (schema + importability checks; no run)

### Keep Existing Entry Points (But Make Them Thin)
- `wbal run/chat/poll` remain “easy buttons” for quick usage and demos.
- Internally, they should call the same runner primitive as `wbal agents run`, with a default `env.kind` override (or default spec), rather than duplicating behavior.

## Runner API (wbal-owned)
Add a small library entrypoint so “wrapper CLIs” (like `factory-f1`) don’t reimplement behavior:
- `wbal.runner.run_agent_spec(...)`:
  - Loads YAML via `build_agent_from_file(..., template_vars=...)`.
  - Applies runtime overrides (model/temperature/reasoning, tool timeout, max steps, agent-specific fields).
  - Handles `--weave-project` and optional `--metadata-out`.
  - Supports env injection (`--env KEY=VALUE`) without relying on the shell.

## Provider / LM Selection Rules
Avoid the “Kimi model id accidentally sent to OpenAI” failure mode:
- `--model` means “model id for the current LM instance”.
- Provider switching happens via either:
  - explicit spec choice (`lm.import_path: wbal.lm:KimiK2LM`), or
  - explicit CLI override (`--lm wbal.lm:KimiK2LM`), or
  - (optional convenience) a safe alias layer: `--model kimi` implies `--lm wbal.lm:KimiK2LM` *only* when `--lm` / `lm.import_path` is not set.

## Tracing Policy (Weave)
Make tracing deterministic:
- Preferred: the runner owns tracing (`--weave-project` => `weave.init(...)`) and sets `WEAVE_PROJECT` for downstream code.
- LMs should avoid calling `weave.init(...)` as a side-effect (today `KimiK2LM` does this). If kept for backwards compat, deprecate it and document that runner-level tracing is the supported path.

## Registry for “Run By Name”
Start simple, then harden:
1) MVP: `wbal agents list --dir ./agents` + `wbal agents run --spec ./agents/<name>.yaml`.
2) Installed agents: add a Python entrypoint group (e.g. `wbal.agent_specs`) mapping `name -> spec_path` for packaged agents.
3) Optional: allow local overrides via env var (e.g. `WBAL_AGENT_PATHS=...`) for dev.

## Migration Plan (Factory → WBAL)
- Keep `factory-f1` as a thin shim that delegates to `wbal.runner.run_agent_spec(...)` (or shells out to `wbal agents run ...`) with F1 defaults.
- Keep Harbor wrappers (`factory/src/factory/f1/harbor_agent.py`) calling the shim (or directly `wbal` CLI) so containers stay simple.
- Move all “generic runner flags” to `wbal` (weave, metadata, env injection, overrides).

## Consolidate the Agent Run Loop
Reduce duplicated run-loop implementations (today there’s a base loop in `wbal/agent.py` and an OpenAI-specific loop in `wbal/agents/openai_agent.py`):
- Pick one “canonical” loop implementation for YAML-driven agents (likely `OpenAIWBAgent`/`YamlAgent`).
- Ensure all non-trivial features (parallel tool calls, tool timeout, output routing, usage tracking) exist in one place.
- Keep the other implementation either removed, deprecated, or minimized to avoid divergence.

## Incremental Implementation Steps
1) Add `wbal/runner.py` with `run_agent_spec(...)` and shared helper functions (vars parsing, overrides parsing, metadata writer).
2) Add `wbal agents run` CLI command that calls `run_agent_spec(...)` (and exposes `--var/--set/--env/--weave-project/--metadata-out`).
3) Add tests for:
   - template var substitution (`--var`)
   - dotted overrides (`--set`)
   - LM/provider switching behavior (Kimi vs OpenAI)
4) Add `wbal agents validate` and `wbal agents list` (MVP local dir mode).
5) Update docs (`wbal/README.md`, `wbal/USER.md`) with the new workflow.
6) Refactor `wbal run/chat/poll` to call the runner primitive (no duplicated wiring / weaving / overrides parsing).
7) Deprecate LM-level `weave.init(...)` side-effects (or gate them behind an explicit opt-in).

## Open Questions
- Do we want `--model kimi` to auto-select `KimiK2LM` (convenience) or require explicit `--lm` / spec selection (safety)?
- Where should provider-specific flags live (e.g. OpenAI `--reasoning-effort`): generic `--set` only, or convenience flags too?
- Should `weave.init` live exclusively in the runner (recommended) vs also inside certain LMs (current `KimiK2LM` behavior)?
