from __future__ import annotations

import argparse
import time

from wbal.agents.openai_agent import OpenAIWBAgent
from wbal.bundle import run_agent_bundle, shell_agent_bundle, validate_agent_bundle
from wbal.environments.chat_env import ChatEnv
from wbal.environments.data_env import DataEnv
from wbal.environments.poll_env import PollEnv
from wbal.manifests import build_agent_from_file


def _parse_env(pairs: list[str] | None) -> dict[str, str]:
    env: dict[str, str] = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise ValueError(f"Invalid --env value (expected KEY=VALUE): {pair!r}")
        key, value = pair.split("=", 1)
        env[key] = value
    return env


def _cmd_chat(args: argparse.Namespace) -> int:
    env_description = f"Org: {args.org}\nProject: {args.project}"
    if args.agent_spec:
        agent = build_agent_from_file(
            args.agent_spec,
            task=args.task or None,
            max_steps=args.max_steps,
            working_directory=args.working_dir,
            env_kind="chat",
            env_description=env_description,
        )
        agent.run(task=args.task, max_steps=args.max_steps)
        return 0

    env = ChatEnv(task=args.task or "", working_directory=args.working_dir)
    env.env = env_description
    OpenAIWBAgent(env=env).run(task=args.task, max_steps=args.max_steps)
    return 0


def _cmd_poll(args: argparse.Namespace) -> int:
    def run_once() -> None:
        env_description = f"Org: {args.org}\nProject: {args.project}"
        if args.agent_spec:
            agent = build_agent_from_file(
                args.agent_spec,
                task=args.task or None,
                max_steps=args.max_steps,
                working_directory=args.working_dir,
                env_kind="poll",
                env_description=env_description,
            )
            agent.run(task=args.task, max_steps=args.max_steps)
            return

        env = PollEnv(task=args.task or "", working_directory=args.working_dir)
        env.env = env_description
        OpenAIWBAgent(env=env).run(task=args.task, max_steps=args.max_steps)

    if args.interval:
        while True:
            run_once()
            time.sleep(args.interval)
    else:
        run_once()

    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    env_description = f"Org: {args.org}\nProject: {args.project}"
    if args.agent_spec:
        agent = build_agent_from_file(
            args.agent_spec,
            task=args.task or None,
            max_steps=args.max_steps,
            working_directory=args.working_dir,
            env_description=env_description,
        )
        agent.run(task=args.task, max_steps=args.max_steps)
        return 0

    env = DataEnv(task=args.task or "", working_directory=args.working_dir)
    env.env = env_description
    OpenAIWBAgent(env=env).run(task=args.task, max_steps=args.max_steps)
    return 0


def _cmd_bundle_validate(args: argparse.Namespace) -> int:
    validate_agent_bundle(args.agent_dir)
    return 0


def _cmd_bundle_run(args: argparse.Namespace) -> int:
    extra_env = _parse_env(args.env)
    return run_agent_bundle(
        agent_dir=args.agent_dir,
        task_dir=args.task_dir,
        workspace_dir=args.workspace_dir,
        install=not args.skip_install,
        run_id=args.run_id,
        task_id=args.task_id,
        experiment_id=args.experiment_id,
        backend=args.backend,
        extra_env=extra_env or None,
    )


def _cmd_bundle_shell(args: argparse.Namespace) -> int:
    extra_env = _parse_env(args.env)
    return shell_agent_bundle(
        agent_dir=args.agent_dir,
        task_dir=args.task_dir,
        workspace_dir=args.workspace_dir,
        run_id=args.run_id,
        task_id=args.task_id,
        experiment_id=args.experiment_id,
        backend=args.backend,
        extra_env=extra_env or None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wbal", description="WBAL CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    chat_p = sub.add_parser("chat", help="Run an interactive chat agent")
    chat_p.add_argument(
        "--agent-spec",
        type=str,
        default=None,
        help="Path to an agent YAML manifest (optional).",
    )
    chat_p.add_argument("--task", type=str, default="", help="Task for the agent")
    chat_p.add_argument(
        "--working-dir", type=str, default=None, help="Directory for state persistence"
    )
    chat_p.add_argument(
        "--max-steps",
        type=int,
        default=20,
        help="Max steps before stopping (default: 20)",
    )
    chat_p.add_argument(
        "--org", type=str, default="", help="Organization name (optional)"
    )
    chat_p.add_argument(
        "--project", type=str, required=True, help="Project name (required)"
    )
    chat_p.set_defaults(func=_cmd_chat)

    poll_p = sub.add_parser("poll", help="Run a polling agent")
    poll_p.add_argument(
        "--agent-spec",
        type=str,
        default=None,
        help="Path to an agent YAML manifest (optional).",
    )
    poll_p.add_argument("--task", type=str, default="", help="Task for the agent")
    poll_p.add_argument(
        "--working-dir", type=str, default=None, help="Directory for state persistence"
    )
    poll_p.add_argument(
        "--max-steps", type=int, default=20, help="Max steps per run (default: 20)"
    )
    poll_p.add_argument(
        "--interval",
        type=int,
        default=None,
        help="Seconds to sleep between runs (if provided)",
    )
    poll_p.add_argument(
        "--org", type=str, default="", help="Organization name (optional)"
    )
    poll_p.add_argument(
        "--project", type=str, required=True, help="Project name (required)"
    )
    poll_p.set_defaults(func=_cmd_poll)

    run_p = sub.add_parser("run", help="Run a baseline (non-interactive) agent")
    run_p.add_argument(
        "--agent-spec",
        type=str,
        default=None,
        help="Path to an agent YAML manifest (optional).",
    )
    run_p.add_argument("--task", type=str, default="", help="Task for the agent")
    run_p.add_argument(
        "--working-dir", type=str, default=None, help="Directory for state persistence"
    )
    run_p.add_argument(
        "--max-steps",
        type=int,
        default=20,
        help="Max steps before stopping (default: 20)",
    )
    run_p.add_argument(
        "--org", type=str, default="", help="Organization name (optional)"
    )
    run_p.add_argument(
        "--project", type=str, required=True, help="Project name (required)"
    )
    run_p.set_defaults(func=_cmd_run)

    bundle_p = sub.add_parser(
        "bundle", help="Run/validate WandBSwarm-compatible agent bundles"
    )
    bundle_sub = bundle_p.add_subparsers(dest="bundle_command", required=True)

    validate_p = bundle_sub.add_parser(
        "validate", help="Validate an agent bundle directory"
    )
    validate_p.add_argument(
        "--agent-dir", required=True, help="Path to agent bundle directory"
    )
    validate_p.set_defaults(func=_cmd_bundle_validate)

    bundle_run_p = bundle_sub.add_parser("run", help="Run an agent bundle locally")
    bundle_run_p.add_argument(
        "--agent-dir", required=True, help="Path to agent bundle directory"
    )
    bundle_run_p.add_argument(
        "--task-dir", required=True, help="Path to task directory (cwd for scripts)"
    )
    bundle_run_p.add_argument(
        "--workspace-dir", required=True, help="Workspace directory for agent outputs"
    )
    bundle_run_p.add_argument(
        "--skip-install", action="store_true", help="Skip install.sh even if present"
    )
    bundle_run_p.add_argument("--run-id", default="local", help="RUN_ID env var")
    bundle_run_p.add_argument("--task-id", default="local", help="TASK_ID env var")
    bundle_run_p.add_argument(
        "--experiment-id", default="local", help="EXPERIMENT_ID env var"
    )
    bundle_run_p.add_argument("--backend", default="local", help="BACKEND env var")
    bundle_run_p.add_argument(
        "--env",
        action="append",
        default=[],
        help="Extra env var (KEY=VALUE). Can repeat.",
    )
    bundle_run_p.set_defaults(func=_cmd_bundle_run)

    shell_p = bundle_sub.add_parser(
        "shell", help="Open a shell with bundle env vars set"
    )
    shell_p.add_argument(
        "--agent-dir", required=True, help="Path to agent bundle directory"
    )
    shell_p.add_argument(
        "--task-dir", required=True, help="Path to task directory (cwd for shell)"
    )
    shell_p.add_argument(
        "--workspace-dir", required=True, help="Workspace directory for agent outputs"
    )
    shell_p.add_argument("--run-id", default="local", help="RUN_ID env var")
    shell_p.add_argument("--task-id", default="local", help="TASK_ID env var")
    shell_p.add_argument(
        "--experiment-id", default="local", help="EXPERIMENT_ID env var"
    )
    shell_p.add_argument("--backend", default="local", help="BACKEND env var")
    shell_p.add_argument(
        "--env",
        action="append",
        default=[],
        help="Extra env var (KEY=VALUE). Can repeat.",
    )
    shell_p.set_defaults(func=_cmd_bundle_shell)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
