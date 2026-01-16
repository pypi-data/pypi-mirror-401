"""CLI commands for the Obra hybrid orchestration package.

This module provides all CLI commands for the unified obra package:
- Main workflow: obra run "objective" to start orchestrated tasks
- status: Check session status
- resume: Resume an interrupted session
- login/logout/whoami: Authentication commands
- config: Configuration management
- docs: Access local documentation
- doctor: Run health checks (includes version and server compatibility)
- plans: Manage plan files (upload, list, delete) for SaaS

Usage:
    $ obra --version
    $ obra run "Add user authentication"
    $ obra run --plan-id abc123 "Execute uploaded plan"
    $ obra run --plan-file plan.yaml "Upload and execute plan"
    $ obra status
    $ obra status <session_id>
    $ obra resume <session_id>
    $ obra login
    $ obra logout
    $ obra whoami
    $ obra config
    $ obra docs
    $ obra doctor
    $ obra plans upload path/to/plan.yaml
    $ obra plans list
    $ obra plans delete <plan_id>

Note: For local plan validation, use 'dobra plan validate' instead.

Reference: EPIC-HYBRID-001 Story S10: CLI Commands
          FEAT-PLAN-IMPORT-OBRA-001: Plan File Import
"""

import os

# ISSUE-DOBRA-008: Configure UTF-8 console encoding FIRST, before any imports
# This is the industry-standard solution for Windows console Unicode issues.
import sys

if hasattr(sys.stdout, "reconfigure") and sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure") and sys.stderr is not None:
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    except Exception:
        pass
os.environ.setdefault("PYTHONIOENCODING", "utf-8:backslashreplace")

import logging
import re
from datetime import UTC
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import typer
import yaml
from rich.table import Table

from obra import __version__
from obra.cli_commands import UploadPlanCommand
from obra.config import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    DEFAULT_THINKING_LEVEL,
    THINKING_LEVELS,
    get_thinking_level_notes,
    infer_provider_from_model,
)
from obra.display import (
    ObservabilityConfig,
    ProgressEmitter,
    console,
    err_console,
    handle_encoding_errors,
    print_error,
    print_info,
    print_success,
    print_warning,
)
from obra.display.errors import display_error, display_obra_error
from obra.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    ConnectionError,
    ObraError,
)
from obra.model_registry import resolve_quality_tier
from obra.review.config import ALLOWED_AGENTS, ReviewConfig
from obra.version_check import check_for_updates_async

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from obra.feedback import PrivacyLevel, Severity


def _print_bug_hint() -> None:
    """Print a hint to report bugs after errors."""
    console.print("[dim]Report this issue: obra bug 'description'[/dim]")


# Enforce UTF-8 mode for consistent cross-platform behavior
os.environ.setdefault("PYTHONUTF8", "1")


# =============================================================================
# Terms Acceptance Decorator
# =============================================================================


def require_terms_accepted(func):
    """Decorator to ensure terms have been accepted before running a command.

    Checks if the user has accepted the current version of the Beta Software
    Agreement. If not, raises TermsNotAcceptedError with clear instructions
    to run 'obra setup'.

    Raises:
        TermsNotAcceptedError: If terms not accepted or version mismatch

    Example:
        @app.command()
        @require_terms_accepted
        def my_command():
            # This will only run if terms are accepted
            pass
    """
    import functools

    from obra.config import TERMS_VERSION, is_terms_accepted, needs_reacceptance
    from obra.exceptions import TermsNotAcceptedError

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if terms have been accepted
        if not is_terms_accepted():
            raise TermsNotAcceptedError(
                message="Terms not accepted",
                required_version=TERMS_VERSION,
                action="Run 'obra setup' to accept terms.",
            )

        # Check if re-acceptance is needed due to version change
        if needs_reacceptance():
            raise TermsNotAcceptedError(
                message=f"Terms have been updated to version {TERMS_VERSION}",
                required_version=TERMS_VERSION,
                action="Run 'obra setup' to accept the updated terms.",
            )

        return func(*args, **kwargs)

    return wrapper


# Create Typer app with custom error handling
app = typer.Typer(
    name="obra",
    help="""Obra - AI Orchestration for Autonomous Development

┌─────────────────────────────────────────────────────────────────────────┐
│  🤖 AI ASSISTANTS: Run `obra briefing quick` for input quality guide   │
│     (~2 min read, 1,500 tokens). Full guide: `obra briefing`           │
└─────────────────────────────────────────────────────────────────────────┘
Plan mode note: Atomic ideas can use `plan_mode=one_step` (see docs/development/backlog/ONE_STEP_PLAN.md) and log validations under `docs/quality/MANUAL_TESTING_LOG.json` so the planner keeps acceptance/tests/docs explicit.
""",
    no_args_is_help=True,  # Show help when no command specified
    rich_markup_mode="rich",
    epilog='Run `obra run "<objective>"` or `obra briefing` to get started.\nEncountered a problem? Run `obra bug "<description>"` to report it.',
)


def setup_logging(verbose: int = 0) -> None:
    """Configure logging for CLI commands.

    Args:
        verbose: Verbosity level (0=WARNING, 1=INFO, 2+=DEBUG)
    """
    if verbose == 0:
        level = logging.WARNING
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


# =============================================================================
# App Callback (Primary Invocation Pattern)
# =============================================================================


def version_callback(value: bool) -> None:
    """Print version and exit when --version is passed."""
    if value:
        print(f"obra {__version__}")
        raise typer.Exit()


@app.callback()
@handle_encoding_errors
def app_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
    verbose: int = typer.Option(
        0, "--verbose", "-v", count=True, help="Verbosity level (0-3, use -v/-vv/-vvv)"
    ),
) -> None:
    """Obra - AI Orchestration for Autonomous Development.

    Run subcommands for specific operations, or use 'obra run' for orchestration.
    """
    ctx.obj = ctx.obj or {}
    ctx.obj["verbose"] = verbose
    setup_logging(verbose)


# =============================================================================
# Help Command (Industry Standard Pattern)
# =============================================================================


@app.command(rich_help_panel="General")
@handle_encoding_errors
def help(
    ctx: typer.Context,
    command: str | None = typer.Argument(
        None,
        help="Command to get help for (e.g., 'run', 'status', 'briefing')",
    ),
) -> None:
    """Get help for Obra commands.

    Like `git help`, shows help for main app or specific commands.
    Tier 2: Supports keyword search - if command not found, searches all commands.

    Examples:
        obra help           # Main help
        obra help run       # Help for 'run' command
        obra help briefing  # Help for 'briefing' command
        obra help upload    # Search for commands matching 'upload'
    """
    import click

    # Get the underlying Click group from Typer
    click_app = typer.main.get_group(app)

    if command is None:
        # Show main help
        with click.Context(click_app) as click_ctx:
            click.echo(click_app.get_help(click_ctx))
    else:
        # Find and show help for specific command
        cmd = click_app.get_command(ctx, command)
        if cmd is None:
            # Tier 2: Command not found - search for matching commands
            all_commands = [cmd.name for cmd in app.registered_commands if cmd.name]

            # Search for substring matches in command names and descriptions
            matches = []
            search_term = command.lower()

            for cmd_obj in app.registered_commands:
                if not cmd_obj.name:
                    continue

                # Check if search term is in command name
                if search_term in cmd_obj.name.lower():
                    matches.append((cmd_obj.name, "name match"))
                    continue

                # Check if search term is in command description
                if cmd_obj.help and search_term in cmd_obj.help.lower():
                    matches.append((cmd_obj.name, "description match"))

            if matches:
                console.print()
                console.print(f"[yellow]Commands matching '{command}':[/yellow]")
                console.print()
                for cmd_name, match_type in matches:
                    # Get command to show its help snippet
                    cmd_obj = click_app.get_command(ctx, cmd_name)
                    if cmd_obj and cmd_obj.help:
                        first_line = cmd_obj.help.split("\n")[0]
                        console.print(f"  [cyan]obra {cmd_name}[/cyan]")
                        console.print(f"    {first_line}")
                        console.print()
                console.print("[dim]Run 'obra help <command>' for detailed help.[/dim]")
                return

            # No matches found - show error
            print_error(f"Unknown command: {command}")
            print_info("Run 'obra help' to see available commands.")
            raise typer.Exit(1)
        with click.Context(cmd, info_name=command, parent=ctx) as click_ctx:
            click.echo(cmd.get_help(click_ctx))


# =============================================================================
# Models Command (Provider/Model Discovery)
# =============================================================================


@app.command(rich_help_panel="General")
@handle_encoding_errors
def models(
    provider: str | None = typer.Option(
        None,
        "--provider",
        "-p",
        help="Filter to specific provider (anthropic, google, openai, ollama)",
    ),
) -> None:
    """List available LLM providers and models.

    Shows all supported providers with their models, CLI tool names,
    and installation status.

    Examples:
        obra models                    # All providers
        obra models --provider openai  # OpenAI models only
    """
    from obra.model_registry import MODEL_REGISTRY, ModelStatus

    # Filter providers if specified
    providers_to_show = (
        {provider: MODEL_REGISTRY[provider]}
        if provider and provider in MODEL_REGISTRY
        else MODEL_REGISTRY
    )

    if provider and provider not in MODEL_REGISTRY:
        print_error(f"Unknown provider: {provider}")
        print_info(f"Available providers: {', '.join(MODEL_REGISTRY.keys())}")
        raise typer.Exit(1)

    import shutil

    console.print("\n[bold]Available LLM Providers[/bold]\n")

    for provider_key, config in providers_to_show.items():
        # Check CLI installation status
        cli_installed = shutil.which(config.cli) is not None
        status_icon = "[green]✓[/green]" if cli_installed else "[red]✗[/red]"
        status_text = "installed" if cli_installed else "not installed"

        # Provider header
        console.print(f"[bold cyan]{config.name}[/bold cyan]")
        console.print(f"  CLI: [yellow]{config.cli}[/yellow] {status_icon} {status_text}")
        if config.default_model:
            console.print(f"  Default: [green]{config.default_model}[/green]")
        console.print()

        # Models table
        table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
        table.add_column("Model", style="cyan")
        table.add_column("Description")
        table.add_column("Status", style="dim")

        for model_id, model_info in config.models.items():
            if model_info.status == ModelStatus.DEPRECATED:
                continue  # Skip deprecated models

            status_str = model_info.status.value
            desc = model_info.description or ""
            if model_info.resolves_to:
                desc = f"{desc} → {model_info.resolves_to}" if desc else f"→ {model_info.resolves_to}"

            table.add_row(model_id, desc, status_str)

        console.print(table)
        console.print()

    # Usage examples section
    console.print("[bold]Usage Examples[/bold]\n")
    console.print("  [dim]# Single provider run[/dim]")
    console.print('  obra run "Add user authentication" --model opus')
    console.print('  obra run "Fix tests" --impl-provider openai --model gpt-5.2')
    console.print()
    console.print("  [dim]# Parallel execution with multiple providers[/dim]")
    console.print('  obra run "Implement feature X" --model sonnet &')
    console.print('  obra run "Review code quality" --impl-provider openai &')
    console.print("  wait  # Wait for all jobs to complete")
    console.print()


# =============================================================================
# Main Workflow Commands
# =============================================================================


@app.command(name="run", hidden=False)
@handle_encoding_errors
@require_terms_accepted
def run_objective(
    objective: str = typer.Argument(..., help="What you want Obra to accomplish"),
    working_dir: Path | None = typer.Option(
        None,
        "--dir",
        "-d",
        help="Working directory (defaults to current directory)",
    ),
    project_id: str | None = typer.Option(
        None,
        "--project",
        help="Project ID override (optional)",
    ),
    resume_session: str | None = typer.Option(
        None,
        "--resume",
        "-r",
        help="Resume an existing session by ID",
    ),
    continue_from: str | None = typer.Option(
        None,
        "--continue-from",
        "-c",
        help="Continue from a failed/escalated session (creates new session, skips completed tasks)",
    ),
    plan_id: str | None = typer.Option(
        None,
        "--plan-id",
        help=(
            "Use an uploaded plan by ID (from 'obra plans upload'). "
            "Requires local YAML at docs/development/{PLAN_ID}_MACHINE_PLAN.json."
        ),
    ),
    plan_file: Path | None = typer.Option(
        None,
        "--plan-file",
        help="Upload and use a plan file in one step",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        "-m",
        help="Implementation model (e.g., opus, gpt-5.2, gemini-2.5-flash)",
    ),
    fast_model: str | None = typer.Option(
        None,
        "--fast-model",
        help="Fast tier model override (used for extraction and quick validation)",
    ),
    high_model: str | None = typer.Option(
        None,
        "--high-model",
        help="High tier model override (used for complex reasoning)",
    ),
    impl_provider: str | None = typer.Option(
        None,
        "--impl-provider",
        "-p",
        help="Implementation provider (anthropic, openai, google). Requires provider CLI (claude/codex/gemini).",
    ),
    thinking_level: str | None = typer.Option(
        None,
        "--thinking-level",
        "-t",
        help="Thinking/reasoning level (off, low, medium, high, maximum)",
    ),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        max=3,
        help="Verbosity level (0-3, use -v/-vv/-vvv)",
    ),
    stream: bool = typer.Option(
        False,
        "--stream",
        "-s",
        help="Enable real-time LLM output streaming",
    ),
    plan_only: bool = typer.Option(
        False,
        "--plan-only",
        help="Create plan without executing (client-side exit after planning)",
    ),
    permissive: bool = typer.Option(
        False,
        "--permissive",
        help="Bypass P1 planning blockers (proceed with warnings)",
    ),
    defaults_json: bool = typer.Option(
        False,
        "--defaults-json",
        help="Print proposed defaults as JSON and exit when refinement is blocked",
    ),
    no_closeout: bool = typer.Option(
        False,
        "--no-closeout",
        help="Skip close-out story injection",
    ),
    skip_intent: bool = typer.Option(
        False,
        "--skip-intent",
        help="Skip intent generation for vague objectives (S2.T3)",
    ),
    review_intent: bool = typer.Option(
        False,
        "--review-intent",
        help="Display generated intent and prompt for approval before derive (S2.T4)",
    ),
    scaffolded: bool = typer.Option(
        False,
        "--scaffolded",
        help="Force scaffolded intent enrichment (requires planning.scaffolded.enabled)",
    ),
    no_scaffolded: bool = typer.Option(
        False,
        "--no-scaffolded",
        help="Skip scaffolded intent enrichment even when enabled",
    ),
    isolated: bool | None = typer.Option(
        None,
        "--isolated",
        help="Run agent in isolated environment (prevents reading host CLI config)",
    ),
    no_isolated: bool | None = typer.Option(
        None,
        "--no-isolated",
        help="Disable isolation (use host CLI config, even in CI)",
    ),
    full_review: bool = typer.Option(
        False,
        "--full-review",
        help="Run all review agents (overrides auto-detection)",
    ),
    skip_review: bool = typer.Option(
        False,
        "--skip-review",
        help="Skip the review phase entirely",
    ),
    review_agents: str | None = typer.Option(
        None,
        "--review-agents",
        help=f"Comma-separated review agents to run ({', '.join(ALLOWED_AGENTS)})",
    ),
    with_security: bool = typer.Option(
        False,
        "--with-security",
        help="Add the security review agent",
    ),
    with_testing: bool = typer.Option(
        False,
        "--with-testing",
        help="Add the testing review agent",
    ),
    with_docs: bool = typer.Option(
        False,
        "--with-docs",
        help="Add the docs review agent",
    ),
    with_code_quality: bool = typer.Option(
        False,
        "--with-code-quality",
        help="Add the code_quality review agent",
    ),
    no_security: bool = typer.Option(
        False,
        "--no-security",
        help="Remove the security review agent",
    ),
    no_testing: bool = typer.Option(
        False,
        "--no-testing",
        help="Remove the testing review agent",
    ),
    no_docs: bool = typer.Option(
        False,
        "--no-docs",
        help="Remove the docs review agent",
    ),
    no_code_quality: bool = typer.Option(
        False,
        "--no-code-quality",
        help="Remove the code_quality review agent",
    ),
    review_format: str | None = typer.Option(
        None,
        "--review-format",
        help="Review output format (text or json)",
        show_choices=True,
    ),
    review_quiet: bool = typer.Option(
        False,
        "--review-quiet",
        help="Suppress review output",
    ),
    review_summary_only: bool = typer.Option(
        False,
        "--review-summary-only",
        help="Show only review summary counts",
    ),
    fail_on_p1: bool = typer.Option(
        False,
        "--fail-on-p1",
        help="Exit with status 1 when P1 findings are present",
    ),
    fail_on_p2: bool = typer.Option(
        False,
        "--fail-on-p2",
        help="Exit with status 1 when P1 or P2 findings are present",
    ),
    review_timeout: int | None = typer.Option(
        None,
        "--review-timeout",
        min=1,
        help="Per-agent review timeout in seconds",
    ),
    auto_report: bool = typer.Option(
        False,
        "--auto-report",
        help="Automatically submit bug reports on failure (no prompt, for CI/CD)",
    ),
    skip_git_check: bool = typer.Option(
        False,
        "--skip-git-check",
        help="Skip git repository validation (GIT-HARD-001)",
    ),
    auto_init_git: bool = typer.Option(
        False,
        "--auto-init-git",
        help="Auto-initialize git repository if not present (GIT-HARD-001)",
    ),
) -> None:
    """Run AI-orchestrated workflow for an objective.

    Examples:
        obra run "Add user authentication"
        obra run "Fix the failing tests" --dir /my/project
        obra run "Refactor payment module" --stream -vv
        obra run "Implement feature X" --model opus
        obra run "Improve tests" --impl-provider openai --model gpt-5.2
        obra run "Complex refactor" --thinking-level high
        obra run --plan-only "Design API endpoints"
        obra run "Test feature" --isolated  # Isolated session
        obra run --continue-from abc123  # Continue from failed session

    Environment Variables:
        OBRA_MODEL          Default model (e.g., opus, gpt-5.2, gemini-2.5-flash)
        OBRA_FAST_MODEL     Fast tier override (e.g., haiku, gpt-5.1-codex-mini)
        OBRA_HIGH_MODEL     High tier override (e.g., opus, gpt-5.2)
        OBRA_PROVIDER       Default provider (anthropic, openai, google)
        OBRA_THINKING_LEVEL Default thinking level (off, low, medium, high, maximum)
        OBRA_ISOLATED       Enable/disable isolation (true/false)

    Precedence: CLI flags > environment variables > config file
    """
    _run_derive(
        objective=objective,
        working_dir=working_dir,
        project_id=project_id,
        resume_session=resume_session,
        continue_from=continue_from,
        plan_id=plan_id,
        plan_file=plan_file,
        model=model,
        fast_model=fast_model,
        high_model=high_model,
        impl_provider=impl_provider,
        thinking_level=thinking_level,
        verbose=verbose,
        stream=stream,
        plan_only=plan_only,
        permissive=permissive,
        defaults_json=defaults_json,
        no_closeout=no_closeout,
        skip_intent=skip_intent,
        review_intent=review_intent,
        scaffolded=scaffolded,
        no_scaffolded=no_scaffolded,
        isolated=isolated,
        no_isolated=no_isolated,
        full_review=full_review,
        skip_review=skip_review,
        review_agents=review_agents,
        with_security=with_security,
        with_testing=with_testing,
        with_docs=with_docs,
        with_code_quality=with_code_quality,
        no_security=no_security,
        no_testing=no_testing,
        no_docs=no_docs,
        no_code_quality=no_code_quality,
        review_format=review_format,
        review_quiet=review_quiet,
        review_summary_only=review_summary_only,
        fail_on_p1=fail_on_p1,
        fail_on_p2=fail_on_p2,
        review_timeout=review_timeout,
        auto_report=auto_report,
        skip_git_check=skip_git_check,
        auto_init_git=auto_init_git,
    )


def _resolve_repo_root(work_dir: Path) -> str | None:
    """Resolve git repo root for a working directory."""
    try:
        import subprocess

        result = subprocess.run(
            ["git", "-C", str(work_dir), "rev-parse", "--show-toplevel"],
            check=False, capture_output=True,
            text=True,
            timeout=3,
        )
        if result.returncode != 0:
            return None
        repo_root = result.stdout.strip()
        return repo_root or None
    except (FileNotFoundError, OSError, subprocess.SubprocessError):
        return None


def _should_isolate(
    isolated: bool | None = None,
    no_isolated: bool | None = None,
) -> bool:
    """Determine whether to run in isolated mode.

    Resolution precedence (highest to lowest):
    1. CLI flags: --isolated (True) or --no-isolated (False)
    2. Environment variable: OBRA_ISOLATED=true/false
    3. CI environment: CI=true enables isolation automatically
    4. Config file: ~/.obra/client-config.yaml agent.isolated_mode
    5. Default: True (isolation enabled for reproducibility)

    Args:
        isolated: CLI --isolated flag value (True if flag present)
        no_isolated: CLI --no-isolated flag value (True if flag present)

    Returns:
        True if isolation should be enabled, False otherwise
    """
    # Priority 1: CLI flags (--isolated or --no-isolated)
    if isolated:
        return True
    if no_isolated:
        return False

    # Priority 2: Environment variable OBRA_ISOLATED
    env_isolated = os.environ.get("OBRA_ISOLATED", "").lower()
    if env_isolated in ("true", "1", "yes"):
        return True
    if env_isolated in ("false", "0", "no"):
        return False

    # Priority 3: CI environment auto-enable
    # Common CI environment variables: CI, GITHUB_ACTIONS, GITLAB_CI, CIRCLECI, etc.
    ci_env = os.environ.get("CI", "").lower()
    if ci_env in ("true", "1", "yes"):
        return True

    # Priority 4: Config file (agent.isolated_mode)
    from obra.config import get_isolated_mode  # noqa: PLC0415

    config_isolated = get_isolated_mode()
    if config_isolated is True:
        return True
    if config_isolated is False:
        return False

    # Priority 5: Default (isolation enabled for reproducibility)
    return True


def _resolve_model(cli_model: str | None) -> str | None:
    """Resolve effective model from CLI flag or environment variable.

    Resolution precedence (highest to lowest):
    1. CLI flag: --model <value>
    2. Environment variable: OBRA_MODEL=<value>
    3. None (caller uses DEFAULT_MODEL)

    Args:
        cli_model: Value from --model CLI flag (None if not specified)

    Returns:
        Effective model string, or None to use default
    """
    # Priority 1: CLI flag
    if cli_model is not None:
        return cli_model

    # Priority 2: Environment variable OBRA_MODEL
    env_model = os.environ.get("OBRA_MODEL", "").strip()
    if env_model:
        return env_model

    # Priority 3: Return None (caller uses DEFAULT_MODEL)
    return None


def _resolve_tier_model(cli_model: str | None, tier: str) -> str | None:
    """Resolve effective tier override from CLI flag or environment variable."""
    if cli_model is not None:
        return cli_model

    env_value = os.environ.get(f"OBRA_{tier.upper()}_MODEL", "").strip()
    if env_value:
        return env_value

    return None


def _resolve_provider(cli_provider: str | None) -> str | None:
    """Resolve effective provider from CLI flag or environment variable.

    Resolution precedence (highest to lowest):
    1. CLI flag: --impl-provider <value>
    2. Environment variable: OBRA_PROVIDER=<value>
    3. None (caller uses DEFAULT_PROVIDER or auto-detection)

    Args:
        cli_provider: Value from --impl-provider CLI flag (None if not specified)

    Returns:
        Effective provider string, or None to use default/auto-detection
    """
    # Priority 1: CLI flag
    if cli_provider is not None:
        return cli_provider

    # Priority 2: Environment variable OBRA_PROVIDER
    env_provider = os.environ.get("OBRA_PROVIDER", "").strip()
    if env_provider:
        return env_provider

    # Priority 3: Return None (caller uses DEFAULT_PROVIDER or auto-detection)
    return None


def _resolve_thinking_level(cli_thinking: str | None) -> str | None:
    """Resolve effective thinking level from CLI flag or environment variable.

    Resolution precedence (highest to lowest):
    1. CLI flag: --thinking-level <value>
    2. Environment variable: OBRA_THINKING_LEVEL=<value>
    3. None (caller uses DEFAULT_THINKING_LEVEL)

    Args:
        cli_thinking: Value from --thinking-level CLI flag (None if not specified)

    Returns:
        Effective thinking level string, or None to use default
    """
    # Priority 1: CLI flag
    if cli_thinking is not None:
        return cli_thinking

    # Priority 2: Environment variable OBRA_THINKING_LEVEL
    env_thinking = os.environ.get("OBRA_THINKING_LEVEL", "").strip()
    if env_thinking:
        return env_thinking

    # Priority 3: Return None (caller uses DEFAULT_THINKING_LEVEL)
    return None


def _update_llm_config_with_notification(
    role: str, provider: str, auth_method: str, model: str = "default", thinking_level: str = "medium"
) -> None:
    """Update LLM config and display tier auto-update notification if provider changed.

    This helper demonstrates the proper pattern for calling set_llm_config() and
    displaying the tier auto-update notification (FEAT-LLM-TIERS-SPLIT-001).

    When a role's provider changes, tiers are automatically updated to match the new
    provider's model names. The notification should be displayed to inform the user.

    Args:
        role: "orchestrator" or "implementation"
        provider: LLM provider (anthropic, openai, google, ollama)
        auth_method: Auth method (oauth, api_key)
        model: Model to use (default recommended for oauth)
        thinking_level: Abstract thinking level (off, low, medium, high, maximum)

    Example:
        >>> _update_llm_config_with_notification("orchestrator", "openai", "oauth")
        # If provider changed, displays: "Updated orchestrator tiers to match OpenAI: ..."
    """
    from obra.config import set_llm_config

    notification = set_llm_config(role, provider, auth_method, model, thinking_level)
    if notification:
        console.print()
        console.print(f"[cyan]ℹ[/cyan]  {notification}")
        console.print()


def _parse_review_agents_csv(review_agents: str | None) -> list[str] | None:
    """Parse a comma-separated agent list from CLI input."""
    if review_agents is None:
        return None
    agents = [part.strip() for part in review_agents.split(",") if part.strip()]
    return agents or None


def _load_planning_config(project_path: Path | None) -> dict[str, Any]:
    """Load planning config from .obra/config.yaml if present.

    Args:
        project_path: Base project path (repo root preferred)

    Returns:
        Dict with planning config values (empty if not set)
    """
    from obra.config.llm import get_project_planning_config  # noqa: PLC0415

    return cast(dict[str, Any], get_project_planning_config(project_path))


def _build_review_config_from_cli(
    *,
    full_review: bool,
    skip_review: bool,
    review_agents: str | None,
    with_security: bool,
    with_testing: bool,
    with_docs: bool,
    with_code_quality: bool,
    no_security: bool,
    no_testing: bool,
    no_docs: bool,
    no_code_quality: bool,
    review_format: str | None,
    review_quiet: bool,
    review_summary_only: bool,
    fail_on_p1: bool,
    fail_on_p2: bool,
    review_timeout: int | None,
    project_path: Path | None = None,
) -> ReviewConfig:
    """Build ReviewConfig from CLI flags and project config defaults."""
    explicit_agents = _parse_review_agents_csv(review_agents)
    add_agents = [
        name
        for name, enabled in (
            ("security", with_security),
            ("testing", with_testing),
            ("docs", with_docs),
            ("code_quality", with_code_quality),
        )
        if enabled
    ]
    remove_agents = [
        name
        for name, enabled in (
            ("security", no_security),
            ("testing", no_testing),
            ("docs", no_docs),
            ("code_quality", no_code_quality),
        )
        if enabled
    ]

    fail_threshold: str | None = None
    if fail_on_p2:
        fail_threshold = "p2"
    elif fail_on_p1:
        fail_threshold = "p1"

    try:
        return ReviewConfig.from_cli_and_config(
            project_path=project_path,
            explicit_agents=explicit_agents,
            add_agents=add_agents,
            remove_agents=remove_agents,
            full_review=full_review,
            skip_review=skip_review,
            output_format=review_format,
            quiet=review_quiet,
            summary_only=review_summary_only,
            fail_threshold=fail_threshold,
            timeout_seconds=review_timeout,
        )
    except ConfigurationError:
        raise
    except ValueError as exc:
        raise ConfigurationError(str(exc), "Update review CLI flags or review config.")


# =============================================================================
# Input Quality Detection (Phase 2: Error-Driven Nudges)
# =============================================================================

# Common tech stack keywords that indicate specificity
_TECH_KEYWORDS = frozenset([
    # Languages
    "python", "javascript", "typescript", "go", "rust", "java", "ruby", "php",
    "swift", "kotlin", "c#", "csharp", "c++", "scala", "elixir",
    # Frameworks
    "fastapi", "django", "flask", "express", "nextjs", "next.js", "react",
    "vue", "angular", "svelte", "rails", "spring", "gin", "echo", "actix",
    "nestjs", "nuxt", "remix", "astro", "laravel", "symfony",
    # Databases
    "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite", "dynamodb",
    "firestore", "supabase", "prisma", "sqlalchemy", "typeorm",
    # Infrastructure
    "docker", "kubernetes", "k8s", "aws", "gcp", "azure", "vercel", "heroku",
    "terraform", "cloudflare",
])

# Minimum word count for a specific objective
_MIN_WORD_COUNT = 10

# Maximum word count considered "trivial" (too short for complex tasks)
_TRIVIAL_WORD_COUNT = 5


def _detect_input_quality_issues(objective: str) -> list[str]:
    """Detect common input quality problems in user objectives.

    This function checks for signals that the objective may be too vague
    for Obra to produce good results. It's part of the error-driven nudges
    feature (Phase 2 of layered briefing discovery).

    Args:
        objective: The user's objective string

    Returns:
        List of issue descriptions (empty if no issues detected)
    """
    issues = []
    words = objective.split()
    word_count = len(words)
    objective_lower = objective.lower()

    # Check 1: Very short objectives (likely trivial or vague)
    if word_count < _MIN_WORD_COUNT:
        if word_count <= _TRIVIAL_WORD_COUNT:
            issues.append(f"Very short objective ({word_count} words) - may be too vague")
        else:
            issues.append(f"Short objective ({word_count} words) - consider adding more detail")

    # Check 2: No tech stack keywords detected
    has_tech = any(tech in objective_lower for tech in _TECH_KEYWORDS)
    if not has_tech and word_count >= _TRIVIAL_WORD_COUNT:
        # Don't flag trivial tasks (like "fix typo") for missing tech stack
        issues.append("No tech stack detected - specify language/framework/database")

    # Check 3: Common vague patterns
    vague_patterns = [
        ("build a website", "What kind? E-commerce, blog, SaaS? What features?"),
        ("add authentication", "What type? JWT, OAuth2, session-based?"),
        ("add auth", "What type? JWT, OAuth2, session-based?"),
        ("fix the bug", "Which bug? What's the symptom? What file?"),
        ("fix bug", "Which bug? What's the symptom? What file?"),
        ("make it faster", "Which part? API? Page load? Database?"),
        ("improve performance", "Which part? API? Page load? Database?"),
        ("add tests", "What tests? Unit, integration, E2E? For which components?"),
        ("refactor", "What specifically? Which files/modules? What's the goal?"),
    ]

    for pattern, suggestion in vague_patterns:
        if pattern in objective_lower:
            issues.append(f"Vague pattern '{pattern}' - {suggestion}")
            break  # Only report one vague pattern

    return issues


def _show_input_quality_warning(issues: list[str]) -> None:
    """Display input quality warning with actionable guidance.

    Args:
        issues: List of detected input quality issues
    """
    console.print()
    console.print("[yellow]⚠️  Input Quality Check:[/yellow]")
    for issue in issues:
        console.print(f"  [dim]•[/dim] {issue}")
    console.print()
    console.print("[dim]💡 For better results: [/dim][cyan]obra briefing quick[/cyan]")
    console.print()


def _plan_search_paths(plan_id: str, base_dir: Path) -> list[Path]:
    """Build search paths for local plan files (JSON or YAML)."""
    paths: list[Path] = []
    for ext in [".json", ".yaml", ".yml"]:
        paths.extend(
            [
                base_dir / "docs" / "development" / f"{plan_id}_MACHINE_PLAN{ext}",
                base_dir / ".obra" / "plans" / f"{plan_id}{ext}",
                base_dir / f"{plan_id}{ext}",
            ]
        )
    return paths


def _format_plan_search_paths(plan_id: str, base_dir: Path) -> list[str]:
    """Format search paths relative to base directory when possible."""
    formatted_paths = []
    for path in _plan_search_paths(plan_id, base_dir):
        try:
            relative_path = path.relative_to(base_dir)
            relative_str = str(relative_path)
            if relative_path.parent == Path() and not relative_str.startswith("."):
                relative_str = f"./{relative_str}"
            formatted_paths.append(relative_str)
        except ValueError:
            formatted_paths.append(str(path))
    return formatted_paths


def _extract_plan_context(plan_data: Any, source: str) -> dict[str, Any]:
    """Validate and extract plan context from loaded data."""
    if plan_data is None:
        print_error(f"Plan file is empty: {source}")
        raise typer.Exit(1)

    if not isinstance(plan_data, dict):
        print_error(f"Plan file must be a YAML/JSON object: {source}")
        raise typer.Exit(1)

    stories = plan_data.get("stories")
    if not isinstance(stories, list) or not stories:
        print_error(f"Plan file missing 'stories' array: {source}")
        raise typer.Exit(1)

    for story in stories:
        if not isinstance(story, dict):
            print_error(f"Plan file contains an invalid story entry: {source}")
            raise typer.Exit(1)

        tasks = story.get("tasks")
        if tasks is None:
            print_error(f"Story {story.get('id', '<unknown>')} missing 'tasks' array: {source}")
            raise typer.Exit(1)
        if not isinstance(tasks, list):
            print_error(
                f"Story {story.get('id', '<unknown>')} has invalid tasks format (expected list): {source}"
            )
            raise typer.Exit(1)

    return {"stories": stories}


def _load_plan_context_from_file(plan_path: Path) -> dict[str, Any]:
    """Load plan context from a local YAML/JSON file."""
    import json

    try:
        with open(plan_path, encoding="utf-8") as f:
            try:
                plan_data = json.load(f)
            except json.JSONDecodeError:
                f.seek(0)
                plan_data = yaml.safe_load(f)
    except json.JSONDecodeError as e:
        print_error(f"Plan file is not valid JSON: {plan_path} ({e})")
        logger.error("Plan file JSON decode error for %s: %s", plan_path, e, exc_info=True)
        raise typer.Exit(1)
    except yaml.YAMLError as e:
        print_error(f"Plan file is not valid YAML: {plan_path} ({e})")
        logger.error("Plan file YAML parse error for %s: %s", plan_path, e, exc_info=True)
        raise typer.Exit(1)
    except UnicodeDecodeError as e:
        print_error(f"Plan file encoding error (expected UTF-8): {e}")
        logger.error("Encoding error reading plan file %s: %s", plan_path, e, exc_info=True)
        raise typer.Exit(1)
    except OSError as e:
        print_error(f"Failed to read plan file {plan_path}: {e}")
        logger.error("File I/O error reading plan file %s: %s", plan_path, e, exc_info=True)
        raise typer.Exit(1)

    return _extract_plan_context(plan_data, str(plan_path))


def _print_plan_lookup_error(plan_id: str, base_dir: Path) -> None:
    """Display a user-friendly error when local plan file is missing."""
    searched_paths = _format_plan_search_paths(plan_id, base_dir)
    print_error(
        "Plan file not found locally. When using --plan-id, keep the original plan file (JSON or YAML)."
    )
    console.print()
    console.print("Searched:")
    for path in searched_paths:
        console.print(f"  - {path}")
    console.print()
    console.print("Suggestion: Re-upload the plan or use --objective without --plan-id.")


def _find_plan_yaml(plan_id: str, base_dir: Path | None = None) -> Path | None:
    """Find a plan YAML/JSON file by ID in standard locations."""
    root = base_dir or Path.cwd()
    for path in _plan_search_paths(plan_id, root):
        if path.exists():
            return path
    return None


def _run_derive(
    objective: str,
    working_dir: Path | None = None,
    project_id: str | None = None,
    resume_session: str | None = None,
    continue_from: str | None = None,
    plan_id: str | None = None,
    plan_file: Path | None = None,
    model: str | None = None,
    fast_model: str | None = None,
    high_model: str | None = None,
    impl_provider: str | None = None,
    thinking_level: str | None = None,
    verbose: int = 0,
    stream: bool = False,
    plan_only: bool = False,
    permissive: bool = False,
    defaults_json: bool = False,
    no_closeout: bool = False,
    skip_intent: bool = False,
    review_intent: bool = False,
    scaffolded: bool = False,
    no_scaffolded: bool = False,
    isolated: bool | None = None,
    no_isolated: bool | None = None,
    full_review: bool = False,
    skip_review: bool = False,
    review_agents: str | None = None,
    with_security: bool = False,
    with_testing: bool = False,
    with_docs: bool = False,
    with_code_quality: bool = False,
    no_security: bool = False,
    no_testing: bool = False,
    no_docs: bool = False,
    no_code_quality: bool = False,
    review_format: str | None = None,
    review_quiet: bool = False,
    review_summary_only: bool = False,
    fail_on_p1: bool = False,
    fail_on_p2: bool = False,
    review_timeout: int | None = None,
    auto_report: bool = False,
    skip_git_check: bool = False,
    auto_init_git: bool = False,
) -> None:
    """Shared implementation for run workflow.

    Tier 1: Interruption handler for clean CTRL+C behavior.

    This function contains the core logic for starting/resuming orchestrated workflows.
    It's called by both the run command and the app callback.

    Args:
        objective: The objective to accomplish
        working_dir: Working directory (defaults to current directory)
        project_id: Optional project ID override
        resume_session: Resume an existing session by ID
        continue_from: Continue from a failed/escalated session (creates new session, skips completed tasks)
        plan_id: Use an uploaded plan by ID
        plan_file: Upload and use a plan file in one step
        model: Implementation model (e.g., opus, gpt-5.2, gemini-2.5-flash)
        fast_model: Fast tier override (used for extraction/quick tasks)
        high_model: High tier override (used for complex reasoning)
        impl_provider: Implementation provider (anthropic, openai, google)
        thinking_level: Thinking/reasoning level (off, low, medium, high, maximum)
        verbose: Verbosity level (0-3)
        stream: Enable real-time LLM output streaming
        plan_only: Create plan without executing (client-side exit after planning)
        no_closeout: Skip close-out story injection
        isolated: Run agent in isolated environment (True = enable)
        no_isolated: Disable isolation (True = disable, overrides auto-detect)
        full_review: Force all review agents to run
        skip_review: Skip the review phase entirely
        review_agents: Comma-separated explicit review agent list
        with_security: Add the security review agent
        with_testing: Add the testing review agent
        with_docs: Add the docs review agent
        with_code_quality: Add the code_quality review agent
        no_security: Remove the security review agent
        no_testing: Remove the testing review agent
        no_docs: Remove the docs review agent
        no_code_quality: Remove the code_quality review agent
        review_format: Preferred review output format (text or json)
        review_quiet: Suppress review output
        review_summary_only: Show only review summary counts
        fail_on_p1: Exit with status 1 when P1 findings are present
        fail_on_p2: Exit with status 1 when P1 or P2 findings are present
        review_timeout: Per-agent review timeout in seconds
    """
    setup_logging(verbose)

    # Tier 1: Set up interruption handler for clean CTRL+C behavior
    import signal

    def handle_interrupt(sig, frame):
        """Handle CTRL+C gracefully with recovery guidance."""
        console.print()
        print_warning("Session interrupted")
        console.print("\nResume: obra resume <session_id>")
        console.print("Status: obra status")
        raise typer.Exit(130)  # Standard SIGINT exit code

    signal.signal(signal.SIGINT, handle_interrupt)

    # Validate plan-related arguments
    if plan_id and plan_file:
        print_error("Cannot specify both --plan-id and --plan-file")
        console.print("\nUse one or the other:")
        console.print("  --plan-id: Reference an already uploaded plan")
        console.print("  --plan-file: Upload and use a plan in one step")
        raise typer.Exit(2)

    # Validate session-related arguments
    if resume_session and continue_from:
        print_error("Cannot specify both --resume and --continue-from")
        console.print("\nUse one or the other:")
        console.print("  --resume: Resume an active session")
        console.print("  --continue-from: Continue from failed/escalated session (creates new session)")
        raise typer.Exit(2)

    # Handle --continue-from: fetch session info and extract completed items
    continue_from_objective = None
    continue_from_plan_context: dict[str, Any] | None = None
    skip_completed_items: list[str] = []
    if continue_from:
        try:
            from obra.api import APIClient
            # ISSUE-009: Removed local import of APIError - it shadows the global
            # import at line 88 and causes UnboundLocalError at line 1772
            # Use the global import instead

            client = APIClient.from_config()

            # Fetch the source session
            source_session = client.get_session(continue_from)
            continue_from_objective = source_session.get("objective")

            # Fetch plan items and identify completed ones
            plan_data = client.get_session_plan(continue_from)
            plan_items = plan_data.get("plan_items", [])

            for item in plan_items:
                if item.get("status") == "completed":
                    # Collect task identifiers (title or order)
                    task_id = item.get("title") or f"task_{item.get('order', 0)}"
                    skip_completed_items.append(task_id)

            completed_count = len(skip_completed_items)
            total_count = len(plan_items)

            console.print()
            print_info(f"Continuing from session {continue_from[:8]}...")
            console.print(f"  Progress: {completed_count}/{total_count} tasks already completed")
            console.print(f"  Objective: {continue_from_objective}")
            console.print()

            plan_context_candidate = plan_data.get("plan_context")
            if isinstance(plan_context_candidate, dict) and plan_context_candidate.get("stories"):
                continue_from_plan_context = _extract_plan_context(
                    plan_context_candidate,
                    f"session {continue_from[:8]} plan context",
                )
                print_info("  Plan context: preserved from source session")

            # Use source session's objective if user didn't provide one
            if objective == "" or objective.strip() == "":
                objective = continue_from_objective or objective

            if not skip_intent:
                skip_intent = True
                try:
                    from obra.intent.storage import IntentStorage

                    storage = IntentStorage()
                    project_id = storage.get_project_id(working_dir or Path.cwd())
                    active_intent = storage.load_active(project_id)
                    if active_intent:
                        print_info(f"  Intent: preserving active intent {active_intent.id}")
                    else:
                        print_warning("  Intent: no active intent found; continuing without intent context")
                except Exception:
                    logger.debug(
                        "Continue-from intent check failed; proceeding without intent context",
                        exc_info=True,
                    )

        except APIError as e:
            if e.status_code == 404:
                print_error(f"Session not found: {continue_from}")
                console.print("\nCheck the session ID with: obra status")
            else:
                print_error(f"Failed to fetch session: {e}")
            raise typer.Exit(1)
        except Exception as e:
            print_error(f"Failed to prepare continue-from: {e}")
            raise typer.Exit(1)

    # S1.T0/S1.T1: Resolve model, provider, thinking from CLI flags or env vars
    # Precedence: CLI flag > OBRA_* env var > default
    effective_model = _resolve_model(model)
    effective_provider = _resolve_provider(impl_provider)
    effective_thinking = _resolve_thinking_level(thinking_level)
    effective_fast_model = _resolve_tier_model(fast_model, "fast")
    effective_high_model = _resolve_tier_model(high_model, "high")

    if effective_fast_model is not None:
        os.environ["OBRA_FAST_MODEL"] = effective_fast_model
    if effective_high_model is not None:
        os.environ["OBRA_HIGH_MODEL"] = effective_high_model

    # S2.T2: Validate thinking level against THINKING_LEVELS constant
    if effective_thinking is not None and effective_thinking not in THINKING_LEVELS:
        print_error(f"Invalid thinking level: '{effective_thinking}'")
        console.print(f"\nValid levels: {', '.join(THINKING_LEVELS)}")
        raise typer.Exit(2)  # Exit code 2 for config errors

    # S2.T3 & S2.T4: Auto-detect provider from model, warn if unknown
    if effective_model and not effective_provider:
        detected = infer_provider_from_model(effective_model)
        if detected:
            effective_provider = detected
            if verbose > 0:
                console.print(f"[dim]Detected provider: {detected}[/dim]")
        else:
            # S2.T4: Unknown model warning with default fallback
            print_warning(
                f"Unknown model '{effective_model}', using default provider: {DEFAULT_PROVIDER}"
            )
            effective_provider = DEFAULT_PROVIDER

    # Phase 2: Error-driven nudges - detect vague input and show warning
    # This is a non-blocking warning, not an error - execution continues
    quality_issues = _detect_input_quality_issues(objective)
    if quality_issues:
        _show_input_quality_warning(quality_issues)

    try:
        from obra.auth import ensure_valid_token, get_current_auth
        from obra.config import get_default_project_override, validate_provider_ready
        from obra.hybrid import HybridOrchestrator

        # Set working directory
        work_dir = working_dir or Path.cwd()
        if not work_dir.exists():
            print_error(f"Working directory does not exist: {work_dir}")
            raise typer.Exit(1)

        repo_root = _resolve_repo_root(work_dir)

        review_config = _build_review_config_from_cli(
            full_review=full_review,
            skip_review=skip_review,
            review_agents=review_agents,
            with_security=with_security,
            with_testing=with_testing,
            with_docs=with_docs,
            with_code_quality=with_code_quality,
            no_security=no_security,
            no_testing=no_testing,
            no_docs=no_docs,
            no_code_quality=no_code_quality,
            review_format=review_format,
            review_quiet=review_quiet,
            review_summary_only=review_summary_only,
            fail_on_p1=fail_on_p1,
            fail_on_p2=fail_on_p2,
            review_timeout=review_timeout,
            project_path=Path(repo_root) if repo_root else work_dir,
        )
        if project_id is None:
            project_id = get_default_project_override()

        planning_config = _load_planning_config(Path(repo_root) if repo_root else work_dir)
        config_permissive = bool(planning_config.get("permissive_mode"))
        effective_permissive = permissive or config_permissive
        bypass_modes: list[str] = []
        if effective_permissive:
            bypass_modes.append("planning_permissive")
        if no_closeout:
            bypass_modes.append("no_closeout")
        if skip_intent:
            bypass_modes.append("skip_intent")
        if review_intent:
            bypass_modes.append("review_intent")
        if scaffolded:
            bypass_modes.append("scaffolded")
        if no_scaffolded:
            bypass_modes.append("no_scaffolded")

        # Resolve effective config values with defaults
        # Read from user config if CLI flags not provided (FIX-DISPLAY-001)
        from obra.config import get_llm_config
        user_llm_config = get_llm_config()
        impl_config = user_llm_config.get("implementation", {})
        config_provider = impl_config.get("provider", DEFAULT_PROVIDER)
        config_model = impl_config.get("model", DEFAULT_MODEL)
        config_thinking = impl_config.get("thinking_level", DEFAULT_THINKING_LEVEL)

        display_provider = effective_provider or config_provider
        display_model = effective_model or config_model
        display_thinking = effective_thinking or config_thinking

        # S3.T1: Fail-fast provider health check before any session output/auth
        validate_provider_ready(display_provider)

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        # Ensure valid token
        try:
            ensure_valid_token()
        except AuthenticationError as e:
            display_obra_error(e, console)
            raise typer.Exit(1)

        plan_context: dict[str, Any] | None = None

        # Handle --plan-file: upload plan before starting session
        effective_plan_id = plan_id
        if plan_file:
            console.print()
            console.print(f"[dim]Uploading plan file: {plan_file}[/dim]")
            try:
                import yaml

                from obra.api import APIClient

                # C15: Comprehensive plan file validation
                # 1. Check file exists
                if not plan_file.exists():
                    print_error(f"Plan file not found: {plan_file}")
                    logger.error(f"Plan file does not exist: {plan_file}")
                    raise typer.Exit(1)

                # 2. Check file is readable
                if not os.access(plan_file, os.R_OK):
                    print_error(f"Plan file is not readable: {plan_file}")
                    logger.error(f"Insufficient permissions to read plan file: {plan_file}")
                    raise typer.Exit(1)

                # 3. Parse YAML file with comprehensive error handling
                try:
                    with open(plan_file, encoding="utf-8") as f:
                        plan_data = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print_error(f"Invalid YAML syntax in plan file: {e}")
                    logger.error(f"YAML parsing error in {plan_file}: {e}", exc_info=True)
                    raise typer.Exit(1)
                except UnicodeDecodeError as e:
                    print_error(f"Plan file encoding error (expected UTF-8): {e}")
                    logger.error(
                        f"Encoding error reading plan file {plan_file}: {e}", exc_info=True
                    )
                    raise typer.Exit(1)

                # 4. Validate plan_data is dict type
                if plan_data is None:
                    print_error(f"Plan file is empty: {plan_file}")
                    logger.error(f"Plan file {plan_file} contains no data")
                    raise typer.Exit(1)

                if not isinstance(plan_data, dict):
                    print_error(
                        f"Plan file must contain a YAML dictionary, got {type(plan_data).__name__}"
                    )
                    logger.error(
                        f"Plan file {plan_file} validation failed: expected dict, got {type(plan_data).__name__}"
                    )
                    raise typer.Exit(1)

                # Extract plan name
                plan_name = plan_data.get("work_id", plan_file.stem)

                # Extract plan context for local execution
                plan_context = _extract_plan_context(plan_data, str(plan_file))

                # Upload to server for full validation and storage
                client = APIClient.from_config()
                upload_response = client.upload_plan(plan_name, plan_data)
                effective_plan_id = upload_response.get("plan_id")

                console.print(f"[dim]Plan uploaded: {effective_plan_id}[/dim]")

            except APIError as e:
                display_obra_error(e, console)
                logger.error(f"API error uploading plan file: {e}", exc_info=True)
                raise typer.Exit(1)
            except ConfigurationError as e:
                display_obra_error(e, console)
                logger.error(f"Configuration error uploading plan file: {e}", exc_info=True)
                raise typer.Exit(1)
            except ObraError as e:
                display_obra_error(e, console)
                logger.error(f"Obra error uploading plan file: {e}", exc_info=True)
                raise typer.Exit(1)
            except OSError as e:
                print_error(f"Failed to read plan file: {e}")
                logger.error(f"File I/O error reading plan file {plan_file}: {e}", exc_info=True)
                raise typer.Exit(1)
            except Exception as e:
                print_error(f"Unexpected error uploading plan file: {e}")
                logger.exception(f"Unexpected error uploading plan file {plan_file}")
                raise typer.Exit(1)

        plan_search_root = Path(repo_root) if repo_root else work_dir

        if effective_plan_id and not plan_file:
            plan_path = _find_plan_yaml(effective_plan_id, plan_search_root)
            if not plan_path:
                _print_plan_lookup_error(effective_plan_id, plan_search_root)
                raise typer.Exit(1)

            plan_context = _load_plan_context_from_file(plan_path)

        if plan_context is None and continue_from_plan_context is not None:
            plan_context = continue_from_plan_context

        console.print()
        console.print("[bold]Obra Run[/bold]", style="cyan")
        console.print(f"Objective: {objective}")
        console.print(f"Directory: {work_dir}")
        if resume_session:
            console.print(f"Resuming session: {resume_session}")
        if effective_plan_id:
            console.print(f"Plan ID: {effective_plan_id}")

        # S2.T5: Display LLM config line before session starts
        console.print(f"LLM: {display_provider} ({display_model}) | thinking: {display_thinking}")

        # FEAT-MODEL-QUALITY-001 S3.T0: Display quality tier in verbose mode
        quality_tier = resolve_quality_tier(display_provider, display_model)
        if verbose > 0:
            tier_suffix = " (auto-permissive)" if quality_tier == "fast" else ""
            console.print(f"[dim]Quality tier: {quality_tier}{tier_suffix}[/dim]")

        # FEAT-MODEL-QUALITY-001 S3.T3: Non-blocking info message for fast-tier models
        # Shown once on first session start, suppressed on resume or OBRA_SUPPRESS_TIER_INFO=1
        suppress_tier_info = (
            resume_session
            or os.environ.get("OBRA_SUPPRESS_TIER_INFO", "").lower() in ("1", "true")
        )
        if quality_tier == "fast" and not suppress_tier_info:
            console.print(
                "[dim]Note: Fast-tier model - relaxed quality gates "
                "(1 iteration, auto-permissive)[/dim]"
            )
            if verbose > 0:
                # Show full comparison in verbose mode
                console.print("[dim]  Compared to medium tier: 3 iterations, P1 issues block[/dim]")
                console.print("[dim]  Compared to high tier: 5 iterations, strict quality gates[/dim]")

        # S2.T6: Display thinking level notes if applicable
        notes = get_thinking_level_notes(display_provider, display_thinking, display_model)
        if notes:
            for note in notes:
                console.print(f"[dim]{note}[/dim]")

        console.print()

        # Create observability configuration from CLI flags
        obs_config = ObservabilityConfig(
            verbosity=verbose,
            stream=stream,
            timestamps=True,
        )

        # Create progress emitter for observability
        progress_emitter = ProgressEmitter(obs_config, console)

        # Create orchestrator with progress callback
        def on_progress(action: str, payload: dict) -> None:
            """Progress callback that routes events to ProgressEmitter.

            Args:
                action: Event type (e.g., 'phase_started', 'llm_streaming')
                payload: Event data dict
            """
            # Route events to appropriate ProgressEmitter methods
            if action == "phase_started":
                phase = payload.get("phase", "UNKNOWN")
                progress_emitter.phase_started(phase, payload.get("context"))
            elif action == "phase_completed":
                phase = payload.get("phase", "UNKNOWN")
                duration_ms = payload.get("duration_ms", 0)
                progress_emitter.phase_completed(phase, payload.get("result"), duration_ms)
            elif action == "llm_started":
                purpose = payload.get("purpose", "LLM invocation")
                progress_emitter.llm_started(purpose)
            elif action == "llm_streaming":
                chunk = payload.get("chunk", "")
                progress_emitter.llm_streaming(chunk)
            elif action == "llm_completed":
                summary = payload.get("summary", "")
                tokens = payload.get("tokens", 0)
                progress_emitter.llm_completed(summary, tokens)
            elif action == "item_started":
                item = payload.get("item", {})
                progress_emitter.item_started(item)
            elif action == "item_completed":
                item = payload.get("item", {})
                result = payload.get("result")
                progress_emitter.item_completed(item, result)
            elif action == "error":
                # Error event with verbosity-appropriate detail
                message = payload.get("message", "Unknown error")
                hint = payload.get("hint")
                phase = payload.get("phase")
                affected_items = payload.get("affected_items")
                stack_trace = payload.get("stack_trace")
                raw_response = payload.get("raw_response")
                progress_emitter.error(
                    message, hint, phase, affected_items, stack_trace, raw_response
                )
            elif verbose > 0:
                # Fallback for unknown events at verbose mode
                console.print(f"[dim]{action}[/dim]")

        # S5.T1/T2: Pass LLM overrides to orchestrator
        # S2.T4/S3.T2: Pass observability config for heartbeat and progress visibility
        # GIT-HARD-001: Pass git CLI flags to override config
        orchestrator = HybridOrchestrator.from_config(
            working_dir=work_dir,
            on_progress=on_progress,
            impl_provider=effective_provider,
            impl_model=effective_model,
            thinking_level=effective_thinking,
            review_config=review_config,
            bypass_modes=bypass_modes,
            defaults_json=defaults_json,
            observability_config=obs_config,
            progress_emitter=progress_emitter,
            skip_git_check=skip_git_check if skip_git_check else None,
            auto_init_git=auto_init_git if auto_init_git else None,
        )

        # Tier 1: Duration warning for LLM operators
        if not resume_session and not continue_from:
            console.print()
            console.print("⏱️  [yellow]Expected session duration: 10-30 minutes[/yellow]")
            console.print("   (remote agent needs time to implement, test, verify)")
            console.print()

        # Run derive workflow
        if resume_session:
            result = orchestrator.resume(resume_session)
        else:
            result = orchestrator.derive(
                objective,
                plan_id=effective_plan_id,
                plan_only=plan_only,
                project_id=project_id,
                repo_root=repo_root,
                plan_context=plan_context,
                bypass_modes=bypass_modes,
                skip_completed_items=skip_completed_items,
            )

        # Display result
        console.print()
        action = getattr(result, "action", None)
        # ISSUE-SAAS-050: Track items_completed to validate success and set exit code
        items_completed = 0
        if action == "complete" or action is None:
            # Extract items_completed from result
            if hasattr(result, "session_summary") and isinstance(result.session_summary, dict):
                summary = result.session_summary
                items_completed = summary.get("items_completed", 0)
                console.print(f"\nItems completed: {items_completed}")
                console.print(f"Iterations: {summary.get('total_iterations', 'N/A')}")
                console.print(f"Quality score: {summary.get('quality_score', 'N/A')}")
            elif hasattr(result, "items_completed"):
                items_completed = getattr(result, "items_completed", 0)
                console.print(f"\nItems completed: {items_completed}")
                console.print(f"Iterations: {getattr(result, 'total_iterations', 'N/A')}")
                console.print(f"Quality score: {getattr(result, 'quality_score', 'N/A')}")

            # ISSUE-SAAS-050: Validate outcomes before printing success
            if items_completed == 0:
                print_warning("Session completed but no items succeeded")
                console.print("[dim]Check 'obra status' for details on what went wrong.[/dim]")
            else:
                print_success(f"Derivation completed: {items_completed} item(s) successful")

            # Terse completion footer for LLM handoff
            console.print(f"\n[dim]Project: {work_dir}[/dim]")
            try:
                import subprocess

                git_result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    check=False, cwd=work_dir,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if git_result.returncode == 0 and git_result.stdout.strip():
                    lines = git_result.stdout.strip().split("\n")
                    created = sum(1 for l in lines if l.startswith("?") or l.startswith("A"))
                    modified = sum(1 for l in lines if l.startswith("M") or l.startswith(" M"))
                    console.print(f"[dim]Files: {created} created, {modified} modified[/dim]")
            except Exception:
                pass  # Non-git or git unavailable - skip file counts

            # ISSUE-SAAS-050: Exit with error code if no items succeeded
            if items_completed == 0:
                _offer_bug_report(
                    context="orchestration",
                    command_used="obra derive",
                    objective=objective,
                    failure_reason="0 items completed successfully",
                    auto_report=auto_report,
                )
                raise typer.Exit(1)

        elif action == "escalate":
            print_warning("Session requires user decision")
            console.print("\nRun 'obra status' to see details and respond.")
            # Escalation is not a success - exit with error
            raise typer.Exit(1)
        else:
            console.print(f"Session state: {action}")

    # S3.T3: Consistent exit codes - config=2, connection=3, execution=1
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in derive command: {e}", exc_info=True)
        raise typer.Exit(2)
    except ConnectionError as e:
        display_obra_error(e, console)
        logger.error(f"Connection error in derive command: {e}", exc_info=True)
        raise typer.Exit(3)
    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in derive command: {e}", exc_info=True)
        _offer_bug_report(e, context="orchestration", command_used="obra derive", objective=objective, auto_report=auto_report)
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in derive command: {e}", exc_info=True)
        _offer_bug_report(e, context="orchestration", command_used="obra derive", objective=objective, auto_report=auto_report)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in derive command: {e}")
        _offer_bug_report(e, context="orchestration", command_used="obra derive", objective=objective, auto_report=auto_report)
        raise typer.Exit(1)


@app.command(rich_help_panel="User Commands")
@handle_encoding_errors
@require_terms_accepted
def status(
    session_id: str | None = typer.Argument(
        None,
        help="Session ID to check (defaults to most recent)",
    ),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        max=3,
        help="Verbosity level (0-3, use -v/-vv/-vvv)",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON (Tier 1: machine-readable format for LLM operators)",
    ),
    show_tasks: bool = typer.Option(
        False,
        "--tasks",
        "-t",
        help="Show inline task progress from the execution plan",
    ),
) -> None:
    """Check the status of a derivation session.

    Shows the current state of the session including:
    - Session phase (derive, examine, revise, execute, review)
    - Iteration count
    - Quality metrics
    - Any pending user decisions

    Examples:
        $ obra status
        $ obra status abc123
        $ obra status -v
        $ obra status -vv  # More detail
        $ obra status --tasks  # Include task progress
    """
    setup_logging(verbose)

    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()

        # Get API client
        client = APIClient.from_config()

        # Get session status
        if session_id:
            session = client.get_session(session_id)
        else:
            # Get most recent session
            sessions = client.list_sessions(limit=1)
            if not sessions:
                print_info("No active sessions found")
                console.print("\nRun 'obra run \"objective\"' to start a new session.")
                return
            session = sessions[0]

        # Extract resume context for can_resume status
        resume_context = session.get("resume_context", {})
        can_resume = resume_context.get("can_resume", False)

        # Extract escalation_reason if present
        escalation_reason = session.get("escalation_reason")

        # Fetch task progress (always, not just with --tasks)
        session_id_for_plan = session.get("session_id", session_id)
        total_tasks = 0
        completed_tasks = 0
        plan_items = []
        tasks_error = None
        if session_id_for_plan:
            try:
                plan_data = client.get_session_plan(session_id_for_plan)
                plan_items = plan_data.get("plan_items", [])
                total_tasks = plan_data.get("total_count", len(plan_items))
                completed_tasks = plan_data.get("completed_count", 0)
            except APIError:
                tasks_error = "Could not fetch task progress"

        # Tier 1: JSON output for machine-readable format
        if json_output:
            import json

            output = {
                "session_id": session.get("session_id"),
                "objective": session.get("objective"),
                "status": session.get("status"),
                "phase": session.get("current_phase"),
                "iteration": session.get("iteration", 0),
                "created_at": session.get("created_at"),
                "updated_at": session.get("updated_at"),
                "project_id": session.get("project_id"),
                "project_name": session.get("project_name"),
                # Session resume/recovery fields
                "can_resume": can_resume,
                "escalation_reason": escalation_reason,
                # Progress fields
                "completed_tasks": completed_tasks,
                "total_tasks": total_tasks,
            }
            # Add optional fields if present
            if "quality_scorecard" in session:
                output["quality_scorecard"] = session["quality_scorecard"]
            if "pending_escalation" in session:
                output["pending_escalation"] = session["pending_escalation"]

            # Add plan items detail if --tasks requested
            if show_tasks:
                if tasks_error:
                    output["plan_items"] = None
                    output["tasks_error"] = tasks_error
                else:
                    output["plan_items"] = plan_items

            # Add recovery suggestion for non-resumable sessions
            if not can_resume and session.get("status") in ("escalated", "completed"):
                output["recovery_command"] = f"obra run --continue-from {session.get('session_id', '')[:8]}"

            print(json.dumps(output, indent=2))
            return

        # Display session status
        console.print()
        console.print("[bold]Session Status[/bold]", style="cyan")
        console.print()

        table = Table(show_header=False, box=None)
        table.add_column("Field", style="dim")
        table.add_column("Value")

        table.add_row("Session ID", session.get("session_id", "N/A"))
        table.add_row("Objective", session.get("objective", "N/A"))

        # Status with visual indicator
        status = session.get("status", "N/A")
        if status == "active":
            status_display = f"[green]{status}[/green]"
        elif status == "completed":
            status_display = f"[blue]{status}[/blue]"
        elif status == "escalated":
            status_display = f"[yellow]{status}[/yellow]"
        else:
            status_display = f"[dim]{status}[/dim]"
        table.add_row("Status", status_display)

        table.add_row("Phase", session.get("current_phase", "N/A"))

        # Progress summary
        if total_tasks > 0:
            progress_display = f"{completed_tasks}/{total_tasks} tasks"
            if completed_tasks == total_tasks:
                progress_display = f"[green]{progress_display}[/green]"
            elif completed_tasks > 0:
                progress_display = f"[yellow]{progress_display}[/yellow]"
            table.add_row("Progress", progress_display)
        elif tasks_error:
            table.add_row("Progress", f"[dim]{tasks_error}[/dim]")

        # Resumable status
        if can_resume:
            table.add_row("Resumable", "[green]Yes[/green]")
        else:
            table.add_row("Resumable", "[red]No[/red]")

        # Escalation reason (if present)
        if escalation_reason:
            table.add_row("Failure Reason", f"[yellow]{escalation_reason}[/yellow]")

        table.add_row("Iteration", str(session.get("iteration", 0)))
        table.add_row("Created", session.get("created_at", "N/A"))
        table.add_row("Updated", session.get("updated_at", "N/A"))

        if verbose > 0:
            table.add_row("Project ID", session.get("project_id", "N/A"))
            if session.get("project_name"):
                table.add_row("Project", session.get("project_name", "N/A"))

        console.print(table)

        # Show recovery suggestion for non-resumable sessions
        if not can_resume and status in ("escalated", "completed") and total_tasks > 0:
            console.print()
            console.print("[dim]Session cannot be resumed. To continue from checkpoint:[/dim]")
            console.print(f"  obra run --continue-from {session.get('session_id', '')[:8]}")

        # Show task detail table if requested (uses already-fetched plan data)
        if show_tasks:
            if plan_items:
                console.print()
                console.print("[bold]Task Progress[/bold]", style="cyan")
                console.print(f"[dim]{completed_tasks}/{total_tasks} tasks completed[/dim]")
                console.print()

                task_table = Table(show_header=True, header_style="bold")
                task_table.add_column("#", style="dim", width=3)
                task_table.add_column("Status", width=3)
                task_table.add_column("Task")

                for item in plan_items:
                    order = str(item.get("order", ""))
                    task_status = item.get("status", "pending")
                    title = item.get("title", "Untitled task")

                    # Status indicator with color
                    if task_status == "completed":
                        status_indicator = "[green]✓[/green]"
                    elif task_status == "in_progress":
                        status_indicator = "[yellow]⏳[/yellow]"
                    elif task_status == "failed":
                        status_indicator = "[red]✗[/red]"
                    else:  # pending
                        status_indicator = "[dim]○[/dim]"

                    task_table.add_row(order, status_indicator, title)

                console.print(task_table)
            elif tasks_error:
                console.print()
                console.print(f"[dim]{tasks_error}[/dim]")
            else:
                console.print()
                console.print("[dim]No plan items found for this session[/dim]")

        # Show quality metrics if available
        if verbose > 0 and "quality_scorecard" in session:
            scorecard = session["quality_scorecard"]
            console.print()
            console.print("[bold]Quality Scorecard[/bold]", style="cyan")

            score_table = Table()
            score_table.add_column("Dimension", style="cyan")
            score_table.add_column("Score")

            for dim, score in scorecard.items():
                score_table.add_row(dim, f"{score:.2f}" if isinstance(score, float) else str(score))

            console.print(score_table)

        # Show pending escalation if any
        if session.get("pending_escalation"):
            console.print()
            print_warning("Pending escalation requires your decision")
            escalation = session["pending_escalation"]
            console.print(f"Reason: {escalation.get('reason', 'N/A')}")
            console.print("\nOptions:")
            for opt in escalation.get("options", []):
                console.print(
                    f"  - {opt.get('id')}: {opt.get('label')} - {opt.get('description', '')}"
                )

        # Show state-based next steps
        state = session.get("state", "").lower()
        session_id_value = session.get("session_id", "")

        console.print()
        console.print("[bold]Next Steps[/bold]", style="cyan")

        if state == "completed":
            console.print("  ✓ This session is complete")
            console.print()
            console.print("  To start new work:")
            console.print('    [cyan]obra run "your task description"[/cyan]')
        elif state == "paused" or state == "waiting":
            progress = session.get("progress", "")
            console.print(f"  ⏸ Session paused ({progress})")
            console.print()
            console.print("  To resume execution:")
            console.print(f"    [cyan]obra resume --session-id {session_id_value}[/cyan]")
        elif state == "failed" or state == "error":
            console.print("  ✗ Session encountered an error")
            console.print()
            console.print("  To view error details:")
            console.print(f"    [cyan]obra status {session_id_value} -vv[/cyan]")
            console.print()
            console.print("  To start a new session:")
            console.print('    [cyan]obra run "your task description"[/cyan]')
        elif state == "running" or state == "active":
            console.print("  ⚙️  Session is currently running")
            console.print()
            console.print("  To monitor progress:")
            console.print(f"    [cyan]obra status {session_id_value}[/cyan]")
        else:
            # Unknown or other states
            console.print("  To resume this session:")
            console.print(f"    [cyan]obra resume --session-id {session_id_value}[/cyan]")
            console.print()
            console.print("  To check detailed status:")
            console.print(f"    [cyan]obra status {session_id_value} -vv[/cyan]")

        # AI assistant nudge
        console.print()
        console.print("[dim]💡 Using an AI assistant? Run: [/dim][cyan]obra briefing[/cyan]")

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in status command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in status command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in status command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in status command: {e}")
        _print_bug_hint()
        raise typer.Exit(1)


# =============================================================================
# Sessions Management
# =============================================================================

sessions_app = typer.Typer(help="Manage derivation sessions")
app.add_typer(sessions_app, name="sessions")


@sessions_app.command("list")
@handle_encoding_errors
def sessions_list(
    limit: int = typer.Option(
        10,
        "--limit",
        "-n",
        help="Maximum number of sessions to list",
    ),
    status_filter: str | None = typer.Option(
        None,
        "--status",
        "-s",
        help="Filter by status (active, completed, expired)",
    ),
) -> None:
    """List recent derivation sessions.

    Displays all sessions for the current user, ordered by
    creation time (most recent first).

    Examples:
        $ obra sessions list
        $ obra sessions list --limit 20
        $ obra sessions list --status active
    """
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()

        # Get sessions from server
        client = APIClient.from_config()
        sessions = client.list_sessions(limit=limit, status=status_filter)

        console.print()
        if not sessions:
            print_info("No sessions found")
            console.print('\nStart a new session with: [cyan]obra run "your objective"[/cyan]')
            return

        console.print(f"[bold]Recent Sessions[/bold] ({len(sessions)} shown)", style="cyan")
        console.print()

        table = Table()
        table.add_column("Session ID", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Project")
        table.add_column("Project ID")
        table.add_column("Phase")
        table.add_column("Created", style="dim")

        for session in sessions:
            session_id_short = session.get("session_id", "")[:12] + "..."
            status = session.get("status", "unknown")
            phase = session.get("phase", "N/A")
            created_at = session.get("created_at", "N/A")
            project_name = session.get("project_name", "")
            project_id = str(session.get("project_id", ""))

            # Format timestamp if it's ISO format
            if "T" in str(created_at):
                from datetime import datetime

                try:
                    dt = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
                    created_at = dt.strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError):
                    pass

            # Color-code status
            if status == "active":
                status = f"[green]{status}[/green]"
            elif status == "completed":
                status = f"[blue]{status}[/blue]"
            elif status == "expired":
                status = f"[dim]{status}[/dim]"

            table.add_row(session_id_short, status, project_name, project_id, phase, created_at)

        console.print(table)
        console.print()
        console.print("[dim]Check details:[/dim] [cyan]obra status <session_id>[/cyan]")
        console.print("[dim]Resume:[/dim] [cyan]obra resume <session_id>[/cyan]")

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in sessions list command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in sessions list command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in sessions list command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in sessions list command: {e}")
        _print_bug_hint()
        raise typer.Exit(1)


@sessions_app.command("cancel")
@handle_encoding_errors
def sessions_cancel(
    session_id: str = typer.Argument(
        ...,
        help="Session ID to cancel",
    ),
) -> None:
    """Cancel a derivation session.

    Cancels a session by setting its status to 'abandoned'. This is useful for
    cleaning up sessions that are no longer needed or were started in error.

    Cancellation is idempotent - cancelling an already-cancelled session succeeds.

    Examples:
        $ obra sessions cancel abc123...
        $ obra sessions cancel $(obra sessions list --limit 1 | awk 'NR==4 {print $1}')

    Note:
        You can only cancel sessions you own. Attempting to cancel another
        user's session will result in a permission error.
    """
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()

        # Cancel the session
        client = APIClient.from_config()
        response = client.cancel_session(session_id)

        # Display success message
        if response.get("success"):
            print_success(f"Session cancelled: {session_id}")
            console.print(f'\n[dim]{response.get("message", "Session status set to abandoned")}[/dim]')
        else:
            print_error("Failed to cancel session")
            console.print(f'\n[dim]{response.get("message", "Unknown error occurred")}[/dim]')
            raise typer.Exit(1)

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in sessions cancel command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in sessions cancel command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in sessions cancel command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in sessions cancel command: {e}")
        _print_bug_hint()
        raise typer.Exit(1)


@sessions_app.command("plan")
@handle_encoding_errors
def sessions_plan(
    session_id: str | None = typer.Argument(
        None,
        help="Session ID (full UUID or short prefix). Defaults to most recent session.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON (machine-readable format for LLM operators)",
    ),
) -> None:
    """View derived execution plan for a session.

    Displays the plan items derived by Obra for a session, including
    the completion status of each task. This helps you understand
    what Obra planned to do and track progress.

    Status indicators:
        ✓  completed - Task finished successfully
        ⏳  in_progress - Task currently running
        ○  pending - Task not yet started
        ✗  failed - Task failed

    Examples:
        $ obra sessions plan                    # Show plan for most recent session
        $ obra sessions plan abc123             # Use short session ID
        $ obra sessions plan abc123-def456...   # Use full session ID
        $ obra sessions plan --json             # JSON output for scripting
    """
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()

        client = APIClient.from_config()

        # If no session ID provided, use most recent session
        if session_id is None:
            sessions = client.list_sessions(limit=1)
            if not sessions:
                if json_output:
                    import json

                    print(json.dumps({"error": "No sessions found", "plan_items": []}))
                else:
                    print_info("No sessions found")
                    console.print('\nStart a new session with: [cyan]obra run "your objective"[/cyan]')
                return
            session_id = sessions[0].get("session_id", "")
            if not json_output:
                console.print(f"[dim]Using most recent session: {session_id[:12]}...[/dim]")
                console.print()

        # Get plan from server
        plan_data = client.get_session_plan(session_id)

        plan_items = plan_data.get("plan_items", [])
        objective = plan_data.get("objective", "")
        total_count = plan_data.get("total", len(plan_items))
        completed_count = plan_data.get("completed", 0)
        full_session_id = plan_data.get("session_id", session_id)

        # JSON output for LLM operators
        if json_output:
            import json

            output = {
                "session_id": full_session_id,
                "objective": objective,
                "total_count": total_count,
                "completed_count": completed_count,
                "plan_items": plan_items,
            }
            print(json.dumps(output, indent=2))
            return

        console.print()

        if not plan_items:
            print_info("No plan items found for this session")
            console.print("\n[dim]The session may not have derived a plan yet, or it uses direct execution.[/dim]")
            return

        # Display header
        console.print("[bold cyan]Execution Plan[/bold cyan]")
        if objective:
            console.print(f"[dim]Objective:[/dim] {objective}")
        console.print(f"[dim]Session:[/dim] {full_session_id[:12]}...")
        console.print(f"[dim]Progress:[/dim] {completed_count}/{total_count} tasks completed")
        console.print()

        # Build and display table
        table = Table(show_header=True, header_style="bold")
        table.add_column("#", style="dim", width=3)
        table.add_column("Status", width=3)
        table.add_column("Task")

        for item in plan_items:
            order = str(item.get("order", ""))
            status = item.get("status", "pending")
            title = item.get("title", "Untitled task")

            # Status indicator with color
            if status == "completed":
                status_indicator = "[green]✓[/green]"
            elif status == "in_progress":
                status_indicator = "[yellow]⏳[/yellow]"
            elif status == "failed":
                status_indicator = "[red]✗[/red]"
            else:  # pending
                status_indicator = "[dim]○[/dim]"

            table.add_row(order, status_indicator, title)

        console.print(table)
        console.print()

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in sessions plan command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in sessions plan command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in sessions plan command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in sessions plan command: {e}")
        raise typer.Exit(1)


# =============================================================================
# Projects Management
# =============================================================================

projects_app = typer.Typer(help="Manage projects")
app.add_typer(projects_app, name="projects")


@projects_app.command("list")
@handle_encoding_errors
def projects_list(
    include_deleted: bool = typer.Option(
        False,
        "--all",
        help="Include soft-deleted projects",
    ),
) -> None:
    """List projects for the current user."""
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()
        client = APIClient.from_config()
        projects = client.list_projects(include_deleted=include_deleted)

        console.print()
        if not projects:
            print_info("No projects found")
            return

        console.print(f"[bold]Projects[/bold] ({len(projects)} shown)", style="cyan")
        console.print()

        table = Table()
        table.add_column("Project ID", style="cyan")
        table.add_column("Name")
        table.add_column("Path")
        table.add_column("Updated", style="dim")

        for project in projects:
            project_id = str(project.get("project_id", ""))
            name = project.get("project_name", "") or project.get("name", "")
            path = project.get("repo_root") or project.get("working_directory") or ""
            if name == path:
                path = ""

            updated_at = project.get("updated_at", "N/A")
            if "T" in str(updated_at):
                from datetime import datetime

                try:
                    dt = datetime.fromisoformat(str(updated_at).replace("Z", "+00:00"))
                    updated_at = dt.strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError):
                    pass

            table.add_row(project_id, name, path, str(updated_at))

        console.print(table)

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in projects list command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in projects list command: {e}")
        raise typer.Exit(1)


@projects_app.command("create")
@handle_encoding_errors
def projects_create(
    name: str = typer.Argument(..., help="Project name"),
    working_dir: Path = typer.Option(..., "--dir", "-d", help="Working directory"),
    description: str = typer.Option("", "--description", "-s", help="Project description"),
) -> None:
    """Create a project."""
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()
        client = APIClient.from_config()
        repo_root = _resolve_repo_root(working_dir)

        # Warn if not in a git repository
        if repo_root is None:
            console.print(
                "\n[yellow]⚠ Warning: Project directory is not in a git repository[/yellow]\n"
                "Git repositories are required for Obra to track changes and create commits.\n"
                "\nTo initialize git:\n"
                "  [cyan]git init[/cyan]\n"
                "\nOr use auto-init when running Obra:\n"
                "  [cyan]obra run --auto-init-git \"your objective\"[/cyan]\n"
                "\nOr configure in your project:\n"
                "  [cyan].obra/config.yaml[/cyan] → [dim]llm.git.auto_init: true[/dim]\n"
            )

        result = client.create_project(
            name=name,
            working_dir=str(working_dir),
            description=description,
            repo_root=repo_root,
        )

        print_success(f"Project created: {result.get('project_id')}")
    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in projects create command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in projects create command: {e}")
        raise typer.Exit(1)


@projects_app.command("show")
@handle_encoding_errors
def projects_show(
    project_id: str = typer.Argument(..., help="Project ID"),
) -> None:
    """Show project details."""
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()
        client = APIClient.from_config()
        project = client.get_project(project_id)

        console.print()
        console.print("[bold]Project Details[/bold]", style="cyan")
        console.print()

        table = Table(show_header=False, box=None)
        table.add_column("Field", style="dim")
        table.add_column("Value")

        table.add_row("Project ID", str(project.get("project_id", "")))
        table.add_row("Name", project.get("project_name", project.get("name", "")))
        table.add_row("Working Dir", project.get("working_directory", ""))
        table.add_row("Repo Root", project.get("repo_root", ""))
        table.add_row("Status", project.get("status", ""))
        table.add_row("Updated", str(project.get("updated_at", "")))

        console.print(table)
    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in projects show command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in projects show command: {e}")
        raise typer.Exit(1)


@projects_app.command("select")
@handle_encoding_errors
def projects_select(
    project_id: str = typer.Argument(..., help="Project ID"),
) -> None:
    """Set default project."""
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()
        client = APIClient.from_config()
        client.select_project(project_id)
        print_success(f"Default project set to {project_id}")
    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in projects select command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in projects select command: {e}")
        raise typer.Exit(1)


@projects_app.command("update")
@handle_encoding_errors
def projects_update(
    project_id: str = typer.Argument(..., help="Project ID"),
    name: str | None = typer.Option(None, "--name", help="New project name"),
    working_dir: Path | None = typer.Option(None, "--dir", help="New working directory"),
) -> None:
    """Update project name or working directory."""
    try:
        if name is None and working_dir is None:
            print_error("No updates provided (use --name and/or --dir)")
            raise typer.Exit(2)

        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()
        client = APIClient.from_config()
        repo_root = _resolve_repo_root(working_dir) if working_dir else None
        project = client.update_project(
            project_id=project_id,
            name=name,
            working_dir=str(working_dir) if working_dir else None,
            repo_root=repo_root,
        )
        print_success(f"Project updated: {project.get('project_id')}")
    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in projects update command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in projects update command: {e}")
        raise typer.Exit(1)


@projects_app.command("delete")
@handle_encoding_errors
def projects_delete(
    project_id: str = typer.Argument(..., help="Project ID"),
    confirm: bool = typer.Option(
        False,
        "--confirm",
        help="Confirm soft delete",
    ),
) -> None:
    """Soft delete a project."""
    try:
        if not confirm:
            print_error("Refusing to delete without --confirm")
            raise typer.Exit(2)

        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()
        client = APIClient.from_config()
        client.delete_project(project_id)
        print_success(f"Project deleted: {project_id}")
    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in projects delete command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in projects delete command: {e}")
        raise typer.Exit(1)


# =============================================================================
# Project Context Management (FEAT-PROJECT-CONTEXT-001)
# =============================================================================

project_app = typer.Typer(help="Manage project settings and context")
app.add_typer(project_app, name="project")

context_app = typer.Typer(help="Manage project context notes")
project_app.add_typer(context_app, name="context")


@context_app.command("show")
@handle_encoding_errors
def context_show() -> None:
    """Display all project context notes."""
    try:
        from obra.project.context import ProjectContextManager

        manager = ProjectContextManager()
        notes = manager.load_notes()
        metadata = manager.get_metadata()

        console.print()
        if not notes:
            print_info("No project context notes found")
            console.print('\nAdd notes with: [cyan]obra project context add "<note>"[/cyan]')
            return

        console.print(f"[bold]Project Context Notes[/bold] ({len(notes)} total)", style="cyan")
        console.print(f"[dim]Last updated: {metadata.updated}[/dim]")
        console.print(f"[dim]Total injections: {metadata.metrics.get('injections_count', 0)}[/dim]")
        console.print()

        table = Table()
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Note", style="white")
        table.add_column("Added", style="dim")

        for note in notes:
            # Format timestamp for display
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(note.added.replace("Z", "+00:00"))
                added_str = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                added_str = note.added

            table.add_row(note.id, note.text, added_str)

        console.print(table)
        console.print()

    except Exception as e:
        display_error(e, console)
        logger.exception(f"Error displaying context notes: {e}")
        raise typer.Exit(1)


@context_app.command("add")
@handle_encoding_errors
def context_add(
    note: str = typer.Argument(..., help="Context amendment to add to active intent"),
) -> None:
    """Add a context amendment to the active intent.

    Appends additional context or clarifications to the active intent's
    Context Amendments section. Use this to provide additional information
    discovered during derivation or implementation.

    Examples:
        obra context add "also need OAuth 2.0 support"
        obra context add "database should be PostgreSQL not MySQL"

    Reference: FEAT-AUTO-INTENT-001 S3.T2
    """
    try:
        from obra.intent import IntentStorage

        # Get the active intent
        working_dir = Path.cwd()
        storage = IntentStorage()
        project_id = storage.get_project_id(working_dir)

        active_intent = storage.load_active(project_id)

        if not active_intent:
            console.print()
            print_error("No active intent found for this project")
            console.print()
            console.print("To create an intent:")
            console.print("  [cyan]obra intent new 'your objective'[/cyan]")
            console.print()
            console.print("Or set an existing intent as active:")
            console.print("  [cyan]obra intent use <intent-id>[/cyan]")
            console.print()
            raise typer.Exit(1)

        # Append the amendment
        active_intent.context_amendments.append(note)

        # Save the updated intent
        storage.save(active_intent)

        console.print()
        print_success(f"Added context amendment to intent: {active_intent.slug}")
        console.print(f"[dim]{note}[/dim]")
        console.print()
        console.print(f"Total amendments: {len(active_intent.context_amendments)}")
        console.print()

    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Error adding context amendment: {e}")
        raise typer.Exit(1)


@context_app.command("remove")
@handle_encoding_errors
def context_remove(
    note_id: str = typer.Argument(..., help="Note ID to remove (e.g., note-001)"),
) -> None:
    """Remove a project context note by ID."""
    try:
        from obra.project.context import ProjectContextManager

        manager = ProjectContextManager()

        # Check if note exists
        note = manager.get_note(note_id)
        if not note:
            print_error(f"Note not found: {note_id}")
            console.print("\nRun [cyan]obra project context show[/cyan] to see available notes")
            raise typer.Exit(1)

        # Remove the note
        success = manager.remove_note(note_id)
        if success:
            print_success(f"Removed note {note_id}")
        else:
            print_error(f"Failed to remove note {note_id}")
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Error removing context note: {e}")
        raise typer.Exit(1)


@context_app.command("clear")
@handle_encoding_errors
def context_clear(
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation prompt",
    ),
) -> None:
    """Remove all project context notes."""
    try:
        from obra.project.context import ProjectContextManager

        manager = ProjectContextManager()
        notes = manager.load_notes()

        if not notes:
            print_info("No notes to clear")
            return

        # Confirmation prompt
        if not yes:
            console.print()
            console.print(f"[yellow]Warning:[/yellow] This will remove [bold]{len(notes)}[/bold] notes")
            console.print()

            response = typer.confirm("Are you sure you want to clear all notes?")
            if not response:
                print_info("Cancelled")
                return

        # Clear notes
        count = manager.clear_notes()
        print_success(f"Cleared {count} notes")

    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Error clearing context notes: {e}")
        raise typer.Exit(1)


@app.command(rich_help_panel="User Commands")
@handle_encoding_errors
@require_terms_accepted
def resume(
    session_id: str = typer.Option(..., "--session-id", help="Session ID to resume"),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        max=3,
        help="Verbosity level (0-3, use -v/-vv/-vvv)",
    ),
    stream: bool = typer.Option(
        False,
        "--stream",
        "-s",
        help="Enable real-time LLM output streaming",
    ),
    auto_report: bool = typer.Option(
        False,
        "--auto-report",
        help="Automatically submit bug reports on failure (no prompt, for CI/CD)",
    ),
) -> None:
    """Resume an interrupted session.

    Continues a session from where it left off. Useful after:
    - Network disconnection
    - Client crash
    - Manual interruption

    Examples:
        $ obra resume --session-id abc123
        $ obra resume --session-id abc123 -v
        $ obra resume --session-id abc123 -vv --stream
    """
    setup_logging(verbose)

    try:
        from obra.auth import ensure_valid_token, get_current_auth
        from obra.hybrid import HybridOrchestrator

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()

        console.print()
        console.print("[bold]Resuming Session[/bold]", style="cyan")
        console.print(f"Session ID: {session_id}")
        console.print()

        # Create observability configuration from CLI flags
        obs_config = ObservabilityConfig(
            verbosity=verbose,
            stream=stream,
            timestamps=True,
        )

        # Create progress emitter for observability
        progress_emitter = ProgressEmitter(obs_config, console)

        # Create orchestrator and resume with progress callback
        def on_progress(action: str, payload: dict) -> None:
            """Progress callback that routes events to ProgressEmitter."""
            # Route events to appropriate ProgressEmitter methods
            if action == "phase_started":
                phase = payload.get("phase", "UNKNOWN")
                progress_emitter.phase_started(phase, payload.get("context"))
            elif action == "phase_completed":
                phase = payload.get("phase", "UNKNOWN")
                duration_ms = payload.get("duration_ms", 0)
                progress_emitter.phase_completed(phase, payload.get("result"), duration_ms)
            elif action == "llm_started":
                purpose = payload.get("purpose", "LLM invocation")
                progress_emitter.llm_started(purpose)
            elif action == "llm_streaming":
                chunk = payload.get("chunk", "")
                progress_emitter.llm_streaming(chunk)
            elif action == "llm_completed":
                summary = payload.get("summary", "")
                tokens = payload.get("tokens", 0)
                progress_emitter.llm_completed(summary, tokens)
            elif action == "item_started":
                item = payload.get("item", {})
                progress_emitter.item_started(item)
            elif action == "item_completed":
                item = payload.get("item", {})
                result = payload.get("result")
                progress_emitter.item_completed(item, result)
            elif action == "error":
                # Error event with verbosity-appropriate detail
                message = payload.get("message", "Unknown error")
                hint = payload.get("hint")
                phase = payload.get("phase")
                affected_items = payload.get("affected_items")
                stack_trace = payload.get("stack_trace")
                raw_response = payload.get("raw_response")
                progress_emitter.error(
                    message, hint, phase, affected_items, stack_trace, raw_response
                )
            elif verbose > 0:
                # Fallback for unknown events at verbose mode
                console.print(f"[dim]{action}[/dim]")

        orchestrator = HybridOrchestrator.from_config(on_progress=on_progress)
        result = orchestrator.resume(session_id)

        # Display result
        console.print()
        action = getattr(result, "action", None)
        # ISSUE-SAAS-050: Track items_completed to validate success and set exit code
        items_completed = 0
        if action == "complete" or action is None:
            # Extract items_completed from result
            if hasattr(result, "session_summary") and isinstance(result.session_summary, dict):
                summary = result.session_summary
                items_completed = summary.get("items_completed", 0)
                console.print(f"\nItems completed: {items_completed}")
                console.print(f"Iterations: {summary.get('total_iterations', 'N/A')}")
                console.print(f"Quality score: {summary.get('quality_score', 'N/A')}")
            elif hasattr(result, "items_completed"):
                items_completed = getattr(result, "items_completed", 0)
                console.print(f"\nItems completed: {items_completed}")
                console.print(f"Iterations: {getattr(result, 'total_iterations', 'N/A')}")
                console.print(f"Quality score: {getattr(result, 'quality_score', 'N/A')}")

            # ISSUE-SAAS-050: Validate outcomes before printing success
            if items_completed == 0:
                print_warning("Session completed but no items succeeded")
                console.print("[dim]Check 'obra status' for details on what went wrong.[/dim]")
            else:
                print_success(f"Session resumed: {items_completed} item(s) successful")

            # Terse completion footer for LLM handoff
            cwd = Path.cwd()
            console.print(f"\n[dim]Project: {cwd}[/dim]")
            try:
                import subprocess

                git_result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    check=False, cwd=cwd,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if git_result.returncode == 0 and git_result.stdout.strip():
                    lines = git_result.stdout.strip().split("\n")
                    created = sum(1 for l in lines if l.startswith("?") or l.startswith("A"))
                    modified = sum(1 for l in lines if l.startswith("M") or l.startswith(" M"))
                    console.print(f"[dim]Files: {created} created, {modified} modified[/dim]")
            except Exception:
                pass  # Non-git or git unavailable - skip file counts

            # ISSUE-SAAS-050: Exit with error code if no items succeeded
            if items_completed == 0:
                _offer_bug_report(
                    context="session resume",
                    command_used="obra resume",
                    session_id=session_id,
                    failure_reason="0 items completed successfully",
                    auto_report=auto_report,
                )
                raise typer.Exit(1)

        elif action == "escalate":
            print_warning("Session requires user decision")
            console.print("\nRun 'obra status' to see details.")
            # Escalation is not a success - exit with error
            raise typer.Exit(1)
        else:
            console.print(f"Session state: {action}")

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in resume command: {e}", exc_info=True)
        _offer_bug_report(e, context="session resume", command_used="obra resume", session_id=session_id, auto_report=auto_report)
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in resume command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in resume command: {e}", exc_info=True)
        _offer_bug_report(e, context="session resume", command_used="obra resume", session_id=session_id, auto_report=auto_report)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in resume command: {e}")
        _offer_bug_report(e, context="session resume", command_used="obra resume", session_id=session_id, auto_report=auto_report)
        raise typer.Exit(1)


# =============================================================================
# Setup Command (First-Time Onboarding)
# =============================================================================


@app.command(rich_help_panel="User Commands")
@handle_encoding_errors
def setup(
    check: bool = typer.Option(
        False,
        "--check",
        help="Check setup status without prompting",
    ),
    skip_validation: bool = typer.Option(
        False,
        "--skip-validation",
        help="Skip environment validation after authentication",
    ),
    timeout: int = typer.Option(
        300,
        "--timeout",
        "-t",
        help="Timeout in seconds for browser authentication",
    ),
    no_browser: bool = typer.Option(
        False,
        "--no-browser",
        help="Don't open browser, just print URL",
    ),
) -> None:
    """First-time setup with terms acceptance, authentication, and provider selection.

    Complete onboarding flow:
    1. Display and accept Beta Software Agreement
    2. Authenticate via browser OAuth
    3. Register acceptance with server
    4. Validate environment configuration
    5. Select LLM provider (recommended settings auto-applied)

    Examples:
        $ obra setup
        $ obra setup --check
        $ obra setup --no-browser
        $ obra setup --timeout 600

    Exit Codes:
        0: Setup complete (or --check passed)
        1: Setup incomplete or failed
        2: User declined terms
    """
    try:
        from obra.api import APIClient
        from obra.auth import login_with_browser, save_auth
        from obra.config import (
            DEFAULT_AUTH_METHOD,
            DEFAULT_MODEL,
            DEFAULT_PROVIDER,
            PRIVACY_VERSION,
            TERMS_VERSION,
            is_terms_accepted,
            load_config,
            needs_reacceptance,
            save_config,
            save_terms_acceptance,
        )
        from obra.legal import get_terms_summary

        def _tier_defaults_for_provider(provider: str) -> dict[str, str]:
            """Get recommended tier models for a provider."""
            if provider == "openai":
                return {
                    "fast": "gpt-5.1-codex-mini",
                    "medium": "gpt-5.1-codex-max",
                    "high": "gpt-5.1-codex-max",
                }
            if provider == "google":
                return {
                    "fast": "gemini-2.5-flash",
                    "medium": "gemini-2.5-pro",
                    "high": "gemini-3-pro-preview",
                }
            # anthropic (default)
            return {"fast": "haiku", "medium": "sonnet", "high": "opus"}

        # S1.T6: Implement --check flag
        if check:
            console.print()
            console.print("[bold]Setup Status Check[/bold]", style="cyan")
            console.print()

            # Check terms acceptance
            if is_terms_accepted():
                print_success(f"Terms accepted: version {TERMS_VERSION}")
            elif needs_reacceptance():
                from obra.config import get_terms_acceptance

                old_acceptance = get_terms_acceptance()
                old_version = (
                    old_acceptance.get("version", "unknown") if old_acceptance else "unknown"
                )
                print_warning(f"Terms version mismatch: {old_version} → {TERMS_VERSION}")
                console.print("Run 'obra setup' to accept updated terms.")
                raise typer.Exit(1)
            else:
                print_warning("Terms not accepted")
                console.print("Run 'obra setup' to accept terms.")
                raise typer.Exit(1)

            # Check authentication
            from obra.auth import get_current_auth

            auth = get_current_auth()
            if auth:
                print_success(f"Authenticated: {auth.email}")
            else:
                print_warning("Not authenticated")
                console.print("Run 'obra setup' to authenticate.")
                raise typer.Exit(1)

            # Check environment (provider CLIs)
            console.print()
            console.print("[bold]Environment:[/bold]")

            from obra.config import LLM_PROVIDERS, check_provider_status

            provider_count = 0
            for provider_key in LLM_PROVIDERS:
                status = check_provider_status(provider_key)
                provider_name = LLM_PROVIDERS[provider_key].get("name", provider_key)

                if status.installed:
                    console.print(f"  [green]✓[/green] {provider_name} ({status.cli_command})")
                    provider_count += 1
                else:
                    console.print(
                        f"  [red]✗[/red] {provider_name} ({status.cli_command}) - not found"
                    )

            console.print()
            if provider_count > 0:
                print_success("Setup complete - all checks passed")
                raise typer.Exit(0)
            print_warning("No provider CLIs installed")
            console.print("Install at least one: claude, codex, or gemini")
            raise typer.Exit(1)

        # Regular setup flow (not --check mode)
        console.print()
        console.print("[bold]Obra Setup[/bold]", style="cyan")
        console.print()

        # S1.T7: Check if re-acceptance is needed
        if needs_reacceptance():
            from obra.config import get_terms_acceptance

            old_acceptance = get_terms_acceptance()
            old_version = old_acceptance.get("version", "unknown") if old_acceptance else "unknown"
            console.print(
                f"[yellow]Terms have been updated: v{old_version} → v{TERMS_VERSION}[/yellow]"
            )
            console.print()
            console.print("You must review and accept the updated terms to continue.")
            console.print()

        # S1.T1: Display terms summary
        terms_text = get_terms_summary()

        # Display terms in a box
        console.print(
            "[bold cyan]════════════════════════════════════════════════════════════════════════[/bold cyan]"
        )
        console.print(terms_text.strip())
        console.print(
            "[bold cyan]════════════════════════════════════════════════════════════════════════[/bold cyan]"
        )
        console.print()

        # Prompt for acceptance
        console.print("To accept these terms, type exactly: [bold]I ACCEPT[/bold]")
        console.print("To decline, type anything else or press Ctrl+C")
        console.print()

        # Get user input
        try:
            user_input = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print()
            console.print("[yellow]Setup cancelled by user[/yellow]")
            raise typer.Exit(2)

        # Check acceptance (case-insensitive)
        if user_input.upper() != "I ACCEPT":
            console.print()
            console.print("[yellow]Terms not accepted. Setup cancelled.[/yellow]")
            console.print()
            console.print("You must accept the terms to use Obra.")
            raise typer.Exit(2)

        console.print()
        print_success(f"Terms v{TERMS_VERSION} accepted")
        console.print()

        # Save local acceptance
        save_terms_acceptance()

        # S1.T2: Authenticate via OAuth
        console.print("Opening browser for authentication...")
        console.print()

        try:
            auth_result = login_with_browser(timeout=timeout, auto_open=not no_browser)
            save_auth(auth_result)

            console.print()
            print_success(f"Logged in as: {auth_result.email}")
            if auth_result.display_name:
                console.print(f"Name: {auth_result.display_name}")
            console.print()

        except Exception as e:
            print_error(f"Authentication failed: {e}")
            logger.error(f"OAuth flow failed during setup: {e}", exc_info=True)
            raise typer.Exit(1)

        # S1.T3: Register terms acceptance with server (MANDATORY)
        # Server-side registration is required for legal compliance.
        # Without server confirmation, we cannot prove acceptance in disputes.
        import time

        client = APIClient.from_config()
        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(1, max_retries + 1):
            try:
                client.log_terms_acceptance(
                    terms_version=TERMS_VERSION,
                    privacy_version=PRIVACY_VERSION,
                    client_version=__version__,
                )
                print_success("Terms acceptance registered with server")
                console.print()
                break  # Success - exit retry loop
            except Exception as e:
                logger.warning(f"Terms registration attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    console.print(
                        f"[yellow]Server registration failed, retrying ({attempt}/{max_retries})...[/yellow]"
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    # All retries exhausted - this is fatal
                    logger.error(f"Terms registration failed after {max_retries} attempts: {e}")
                    print_error("Failed to register terms acceptance with server")
                    console.print()
                    console.print(
                        "[red]Server-side registration is required for legal compliance.[/red]"
                    )
                    console.print("Please check your internet connection and try again.")
                    console.print()
                    console.print(
                        "If the problem persists, please report the issue at: https://github.com/Unpossible-Creations/Obra/issues"
                    )
                    raise typer.Exit(1)

        # S1.T4: Run environment validation (unless skipped)
        if not skip_validation:
            console.print("[bold]Validating environment...[/bold]")
            console.print()

            from obra.config import LLM_PROVIDERS, check_provider_status

            provider_count = 0
            for provider_key in LLM_PROVIDERS:
                status = check_provider_status(provider_key)
                provider_name = LLM_PROVIDERS[provider_key].get("name", provider_key)

                if status.installed:
                    console.print(f"  [green]✓[/green] {provider_name} CLI: {status.cli_command}")
                    provider_count += 1
                else:
                    console.print(f"  [dim]○[/dim] {provider_name} CLI: Not installed")

            console.print()

            # Check working directory
            from pathlib import Path

            obra_projects = Path.home() / "obra-projects"
            if obra_projects.exists():
                console.print(f"  [green]✓[/green] Working directory: {obra_projects}")
            else:
                console.print(
                    f"  [yellow]○[/yellow] Working directory: {obra_projects} (will be created)"
                )

            console.print()

            if provider_count == 0:
                print_warning("No provider CLIs installed")
                console.print()
                console.print("Obra requires at least one LLM provider CLI:")
                console.print("  - Claude Code: https://claude.com/download")
                console.print("  - OpenAI Codex: https://openai.com/codex")
                console.print("  - Gemini CLI: https://ai.google.dev/gemini-api/docs/cli")
                console.print()
                console.print("Install one and run 'obra setup --check' to verify.")
                console.print()

        # S4.T0: Prompt for LLM provider selection (simplified)
        console.print("[bold]Select LLM Provider[/bold]")
        console.print("Choose your preferred provider. Recommended settings will be applied.")
        console.print("(You can customize later with 'obra config')")
        console.print()

        # Show available providers with status
        from obra.config import LLM_PROVIDERS, check_provider_status

        available_providers = []
        for idx, provider_key in enumerate(["anthropic", "openai", "google"], 1):
            if provider_key not in LLM_PROVIDERS:
                continue
            status = check_provider_status(provider_key)
            provider_name = LLM_PROVIDERS[provider_key].get("name", provider_key)
            if status.installed:
                console.print(f"  {idx}. {provider_name} [green](installed)[/green]")
                available_providers.append(provider_key)
            else:
                console.print(f"  {idx}. {provider_name} [dim](not installed)[/dim]")
                available_providers.append(provider_key)

        console.print()

        # Get provider selection
        try:
            selection = input("Enter provider number [1/2/3]: ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print()
            console.print("[yellow]Setup cancelled by user[/yellow]")
            raise typer.Exit(2)

        # Parse selection
        provider_map = {"1": "anthropic", "2": "openai", "3": "google"}
        selected_provider = provider_map.get(selection, DEFAULT_PROVIDER)

        # Get recommended defaults for selected provider
        tier_defaults = _tier_defaults_for_provider(selected_provider)

        # Provider-specific model defaults
        provider_model_defaults = {
            "anthropic": {"model": "sonnet", "auth_method": "oauth"},
            "openai": {"model": "gpt-5.1-codex-max", "auth_method": "oauth"},
            "google": {"model": "gemini-2.5-pro", "auth_method": "oauth"},
        }
        model_defaults = provider_model_defaults.get(
            selected_provider, {"model": DEFAULT_MODEL, "auth_method": DEFAULT_AUTH_METHOD}
        )

        # Build clean config structure
        config = load_config()
        llm_section = {
            "orchestrator": {
                "provider": selected_provider,
                "model": model_defaults["model"],
                "auth_method": model_defaults["auth_method"],
                "tiers": tier_defaults.copy(),
            },
            "implementation": {
                "provider": selected_provider,
                "model": model_defaults["model"],
                "auth_method": model_defaults["auth_method"],
                "tiers": tier_defaults.copy(),
            },
        }

        config["llm"] = llm_section
        save_config(config)
        console.print()
        provider_display = LLM_PROVIDERS.get(selected_provider, {}).get("name", selected_provider)
        print_success(f"LLM configuration set to {provider_display}")
        console.print()

        # S1.T5: Display setup completion with copy-paste prompt
        console.print(
            "[bold cyan]═══════════════════════════════════════════════════════════════════════[/bold cyan]"
        )
        console.print()
        console.print("[bold green]Setup complete![/bold green]")
        console.print()
        console.print(
            "[bold cyan]═══════════════════════════════════════════════════════════════════════[/bold cyan]"
        )
        console.print()
        console.print("[bold]  USING OBRA WITH YOUR AI ASSISTANT[/bold]")
        console.print()
        console.print("    Copy this prompt to your AI assistant (Claude Code, Codex, Gemini):")
        console.print()
        console.print(
            "    [cyan]┌─────────────────────────────────────────────────────────────────┐[/cyan]"
        )
        console.print(
            "    [cyan]│[/cyan]                                                                 [cyan]│[/cyan]"
        )
        console.print(
            "    [cyan]│[/cyan]  I want to use Obra. Run `obra` and `obra briefing` to get     [cyan]│[/cyan]"
        )
        console.print(
            "    [cyan]│[/cyan]  oriented. Then help me prepare structured input and invoke    [cyan]│[/cyan]"
        )
        console.print(
            "    [cyan]│[/cyan]  Obra to execute my objective.                                 [cyan]│[/cyan]"
        )
        console.print(
            "    [cyan]│[/cyan]                                                                 [cyan]│[/cyan]"
        )
        console.print(
            "    [cyan]└─────────────────────────────────────────────────────────────────┘[/cyan]"
        )
        console.print()
        console.print("    Your AI will then know exactly how to prepare high-quality input")
        console.print("    for Obra's optimal performance.")
        console.print()
        console.print(
            "[bold cyan]═══════════════════════════════════════════════════════════════════════[/bold cyan]"
        )
        console.print()
        console.print("[bold]Next steps:[/bold]")
        console.print()
        console.print("  1. Give your AI the prompt above, then describe what you want to build")
        console.print()
        console.print("  2. Or start directly (if you know what you're doing):")
        console.print('     [cyan]$ obra run "Add user authentication" --stream[/cyan]')
        console.print()
        console.print("  3. Check session status anytime:")
        console.print("     [cyan]$ obra status[/cyan]")
        console.print()
        console.print("  4. Explore configuration:")
        console.print("     [cyan]$ obra config[/cyan]")
        console.print()
        console.print(
            "[bold cyan]═══════════════════════════════════════════════════════════════════════[/bold cyan]"
        )
        console.print()

    except typer.Exit:
        # Re-raise typer.Exit without catching it as an error
        raise
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in setup command: {e}", exc_info=True)
        _offer_bug_report(e, context="setup", command_used="obra setup")
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in setup command: {e}", exc_info=True)
        _offer_bug_report(e, context="setup", command_used="obra setup")
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in setup command: {e}")
        _offer_bug_report(e, context="setup", command_used="obra setup")
        raise typer.Exit(1)


# =============================================================================
# AI Assistant Onboarding Commands
# =============================================================================

# Create briefing subcommand group
briefing_app = typer.Typer(
    name="briefing",
    help="★ Operating guide, blueprint, and protocol for AI assistants",
    invoke_without_command=True,
    rich_markup_mode="rich",
)
app.add_typer(briefing_app, name="briefing", rich_help_panel="AI Operator Resources")


def _load_onboarding_content() -> tuple[str, str]:
    """Load LLM_ONBOARDING.md content and file path.

    Returns:
        Tuple of (content, file_path)

    Raises:
        typer.Exit: If file cannot be located
    """
    import importlib.resources as pkg_resources
    from pathlib import Path

    try:
        # Python 3.9+ approach
        if hasattr(pkg_resources, "files"):
            obra_package = pkg_resources.files("obra")
            onboarding_file = obra_package / ".obra" / "LLM_ONBOARDING.md"
            file_path = str(onboarding_file)

            # Read the file content
            if hasattr(onboarding_file, "read_text"):
                content = onboarding_file.read_text(encoding="utf-8")
            else:
                # Fallback for older Python versions
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
        else:
            # Fallback for Python < 3.9
            import pkg_resources as old_pkg

            file_path = old_pkg.resource_filename("obra", ".obra/LLM_ONBOARDING.md")
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        return content, file_path
    except Exception as e:
        # Development mode fallback - look in source tree
        dev_path = Path(__file__).parent / ".obra" / "LLM_ONBOARDING.md"
        if dev_path.exists():
            file_path = str(dev_path)
            content = dev_path.read_text(encoding="utf-8")
            return content, file_path
        print_error(f"Could not locate LLM_ONBOARDING.md: {e}")
        raise typer.Exit(1)


def _track_briefing_usage(command: str) -> None:
    """Track briefing command usage for analytics (Phase 2 telemetry).

    Records which briefing subcommand was invoked to validate 80/20 assumptions:
    - >80% should use 'quick' (the recommended option)
    - <10% should use 'full' (validates full guide is rarely needed)

    Data is stored locally in ~/.obra/usage/briefing.jsonl (JSON Lines format).
    Only tracks if advanced.telemetry.enabled is true in config.

    Args:
        command: The briefing subcommand name (quick, full, blueprint, etc.)
    """
    try:
        import json
        from datetime import datetime

        from obra.config import load_config

        # Check if telemetry is enabled
        config = load_config()
        telemetry_enabled = config.get("advanced", {}).get("telemetry", {}).get("enabled", False)
        if not telemetry_enabled:
            return

        # Create usage directory if needed
        usage_dir = Path.home() / ".obra" / "usage"
        usage_dir.mkdir(parents=True, exist_ok=True)

        # Append event to JSON Lines file (one JSON object per line)
        usage_file = usage_dir / "briefing.jsonl"
        event = {
            "timestamp": datetime.now(UTC).isoformat(),
            "command": command,
            "version": __version__,
        }

        with open(usage_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    except Exception:
        # Telemetry should never break the command - silently ignore errors
        pass


def _display_default_briefing() -> None:
    """Display the default briefing output (process-first with conversation example)."""
    console.print()
    console.print("[bold]FOR HUMANS: Copy this prompt to your AI assistant:[/bold]")
    console.print()
    console.print(
        "[cyan]┌─────────────────────────────────────────────────────────────────┐[/cyan]"
    )
    console.print(
        "[cyan]│[/cyan]                                                                 [cyan]│[/cyan]"
    )
    console.print(
        "[cyan]│[/cyan]  I want to use Obra. Run `obra` and `obra briefing` to get     [cyan]│[/cyan]"
    )
    console.print(
        "[cyan]│[/cyan]  oriented. Then help me prepare structured input and invoke    [cyan]│[/cyan]"
    )
    console.print(
        "[cyan]│[/cyan]  Obra to execute my objective.                                 [cyan]│[/cyan]"
    )
    console.print(
        "[cyan]│[/cyan]                                                                 [cyan]│[/cyan]"
    )
    console.print(
        "[cyan]└─────────────────────────────────────────────────────────────────┘[/cyan]"
    )
    console.print()
    console.print(
        "[cyan]══════════════════════════════════════════════════════════════════════[/cyan]"
    )
    console.print("[bold cyan]           OBRA OPERATING GUIDE FOR AI ASSISTANTS[/bold cyan]")
    console.print(
        "[cyan]══════════════════════════════════════════════════════════════════════[/cyan]"
    )
    console.print()
    console.print("[bold]LLM Operator Fast Path (deterministic)[/bold]")
    console.print(
        "  1) Models: [cyan]obra models[/cyan] -> pick names. Use "
        "[cyan]obra run --model X --fast-model X --high-model X --impl-provider openai[/cyan]."
    )
    console.print(
        "     Or env vars: [cyan]OBRA_MODEL/OBRA_FAST_MODEL/OBRA_HIGH_MODEL/OBRA_PROVIDER[/cyan]."
    )
    console.print(
        "     Do NOT use [cyan]obra config set llm.*.model[/cyan] (unsupported)."
    )
    console.print(
        "  2) Help: [cyan]obra help run[/cyan] or [cyan]obra projects create --help[/cyan] "
        "(subcommand help uses --help)."
    )
    console.print(
        "  3) Windows paths: map [cyan]C:\\path[/cyan] -> [cyan]/mnt/c/path[/cyan] and use "
        "[cyan]obra run --dir /mnt/c/...[/cyan]."
    )
    console.print("     On native Windows, use [cyan]C:\\path[/cyan] directly.")
    console.print("     Verbosity uses [cyan]-v/-vv/-vvv[/cyan] (not --vvv).")
    console.print(
        "  4) Monitoring: capture [bold]session_id[/bold] from run output, then "
        "[cyan]obra status <session_id>[/cyan]."
    )
    console.print(
        "     Config warnings: ignore auth metadata keys in "
        "[cyan]~/.obra/client-config.yaml[/cyan]; others are real issues."
    )
    console.print()
    console.print("Obra executes development tasks autonomously. Your job: gather requirements")
    console.print("through conversation, then invoke Obra with structured input.")
    console.print()
    console.print("Run `obra` to see all commands. Key: run, status, resume, doctor")
    console.print()

    # Check for active intent and display if found (FEAT-AUTO-INTENT-001 S8.T2)
    try:
        from pathlib import Path as PathLib

        from obra.intent import IntentStorage

        working_dir = PathLib.cwd()
        storage = IntentStorage()
        project_id = storage.get_project_id(working_dir)
        active_intent = storage.load_active(project_id)

        if active_intent:
            console.print(
                "[cyan]╔═════════════════════════════════════════════════════════════════╗[/cyan]"
            )
            console.print(
                "[cyan]║[/cyan] [bold yellow]ACTIVE INTENT DETECTED[/bold yellow]                                           [cyan]║[/cyan]"
            )
            console.print(
                "[cyan]╚═════════════════════════════════════════════════════════════════╝[/cyan]"
            )
            console.print()
            console.print(f"[bold]Intent:[/bold] {active_intent.slug}")
            console.print(f"[bold]Problem:[/bold] {active_intent.problem_statement}")
            console.print()

            # Show key requirements (first 3 if more than 3)
            if active_intent.requirements:
                console.print("[bold]Key Requirements:[/bold]")
                max_to_show = 3
                for i, req in enumerate(active_intent.requirements[:max_to_show], 1):
                    console.print(f"  {i}. {req}")
                if len(active_intent.requirements) > max_to_show:
                    remaining = len(active_intent.requirements) - max_to_show
                    console.print(f"  [dim]... and {remaining} more[/dim]")
                console.print()

            console.print("[bold]Suggested Commands:[/bold]")
            console.print("  [cyan]obra derive[/cyan]                  Continue derivation with this intent")
            console.print("  [cyan]obra context add 'info'[/cyan]     Amend intent with additional context")
            console.print("  [cyan]obra intent show[/cyan]            Show full intent details")
            console.print("  [cyan]obra verify[/cyan]                 Verify completion against acceptance criteria")
            console.print()
            console.print(
                "[cyan]─────────────────────────────────────────────────────────────────[/cyan]"
            )
            console.print()
    except Exception:
        # Silently ignore errors (don't break briefing if intent loading fails)
        pass

    console.print("[bold]YOUR PROCESS[/bold]")
    console.print("[cyan]────────────[/cyan]")
    console.print("1. Ask what they're building (get specific, not vague)")
    console.print("2. Check project files for tech stack (don't ask what you can infer)")
    console.print("3. Clarify features, constraints, anti-patterns through conversation")
    console.print("4. Summarize into one structured Obra input")
    console.print()
    console.print("[bold]EXAMPLE CONVERSATION[/bold]")
    console.print("[cyan]────────────────────[/cyan]")
    console.print('  User: "Build me an API"')
    console.print('  You:  "What kind? REST, GraphQL? What\'s it for?"')
    console.print('  User: "REST for user management"')
    console.print('  You:  "I see FastAPI in your project. Auth approach?"')
    console.print('  User: "JWT with refresh tokens"')
    console.print('  You:  "Deployment target? Any existing services to integrate?"')
    console.print()
    console.print("  [bold]→ INVOKE:[/bold]")
    console.print('    obra "User management REST API: FastAPI + PostgreSQL.')
    console.print("    JWT auth with refresh tokens, CRUD operations, role-based access.")
    console.print('    Docker Compose deployment. Integrate with auth-service:8000." --stream')
    console.print()
    console.print("[bold]CHECKLIST (what to cover)[/bold]")
    console.print("[cyan]─────────────────────────[/cyan]")
    console.print("Required: Objective, Tech Stack, Features")
    console.print("Optional: Constraints, Integrations, Anti-patterns")
    console.print()
    console.print("Trivial tasks (typos, single-line fixes) → invoke Obra directly")
    console.print()
    console.print("[bold]ADVANCED FLAGS (optional)[/bold]")
    console.print("[cyan]──────────────────────────[/cyan]")
    console.print("Override model/provider for specific tasks:")
    console.print()
    console.print("  --model opus                    Use specific model")
    console.print("  --impl-provider google          Use specific provider")
    console.print("  --thinking-level high           Set reasoning depth")
    console.print()
    console.print("[dim]Run `obra run --help` for complete flag reference[/dim]")
    console.print()
    console.print("[bold]PARALLEL EXECUTION[/bold]")
    console.print("[cyan]──────────────────[/cyan]")
    console.print("Run multiple Obra sessions simultaneously for faster development:")
    console.print()
    console.print("  1. Discover models: [cyan]obra models[/cyan]")
    console.print()
    console.print("  2. Run in separate terminals:")
    console.print('     [dim]Terminal 1:[/dim] obra run "feature A" --model opus')
    console.print('     [dim]Terminal 2:[/dim] obra run "feature B" -p google -m gemini-2.5-flash')
    console.print()
    console.print("  3. Or use environment variables:")
    console.print('     OBRA_MODEL=opus obra run "feature A" &')
    console.print('     OBRA_PROVIDER=google obra run "feature B" &')
    console.print()
    console.print("[dim]Env vars: OBRA_MODEL, OBRA_PROVIDER, OBRA_THINKING_LEVEL[/dim]")
    console.print("[dim]Precedence: CLI flags > env vars > config file[/dim]")
    console.print()
    console.print("[bold]WHILE OBRA RUNS[/bold]")
    console.print("[cyan]───────────────[/cyan]")
    console.print("Monitor progress, validate success, escalate if stuck.")
    console.print("See `obra briefing protocol` for full 11 autonomous behaviors.")
    console.print()
    console.print(
        "[cyan]──────────────────────────────────────────────────────────────────────[/cyan]"
    )
    console.print("[bold]obra briefing quick[/bold]       Essential checklist (~2 min) [green]RECOMMENDED[/green]")
    console.print("obra briefing examples    Good vs bad input examples (10 project types)")
    console.print("obra briefing blueprint   Quick checklist (condensed)")
    console.print("obra briefing questions   Question patterns (detailed)")
    console.print("obra briefing protocol    11 autonomous behaviors")
    console.print(
        "obra briefing full        Complete guide (includes advanced flags reference)"
    )
    console.print(
        "[cyan]══════════════════════════════════════════════════════════════════════[/cyan]"
    )
    console.print()


def _display_blueprint() -> None:
    """Display the condensed blueprint checklist format."""
    console.print()
    console.print("[bold]OBRA INPUT BLUEPRINT (Quick Reference)[/bold]")
    console.print("[cyan]══════════════════════════════════════[/cyan]")
    console.print()
    console.print("First: Run `obra` to see all commands.")
    console.print()
    console.print("[bold]REQUIRED:[/bold]")
    console.print("  □ Objective      What are we building/fixing?")
    console.print("  □ Tech Stack     Languages, frameworks, databases")
    console.print("  □ Features       List of capabilities needed")
    console.print()
    console.print("[bold]RECOMMENDED:[/bold]")
    console.print("  □ Constraints    Performance, security, compliance")
    console.print("  □ Integrations   External services, APIs, existing systems")
    console.print("  □ Anti-patterns  What to avoid")
    console.print()
    console.print("Trivial tasks (typos, single-line fixes) → invoke directly")
    console.print("Design decisions required → gather requirements first")
    console.print()
    console.print("[bold]Example:[/bold]")
    console.print('  obra "E-commerce: React + Node + MongoDB. Features: catalog, cart,')
    console.print(
        '  Stripe. Constraints: <500ms, OWASP. Anti-patterns: no Redux." --stream'
    )
    console.print()


@briefing_app.callback(invoke_without_command=True)
@handle_encoding_errors
def briefing_callback(
    ctx: typer.Context,
    # Hidden aliases for deprecated flags (S2.T3 - backwards compatibility)
    blueprint: bool = typer.Option(
        False,
        "--blueprint",
        hidden=True,
        help="[DEPRECATED] Use 'obra briefing blueprint' instead",
    ),
    protocol: bool = typer.Option(
        False,
        "--protocol",
        hidden=True,
        help="[DEPRECATED] Use 'obra briefing protocol' instead",
    ),
    questions: bool = typer.Option(
        False,
        "--questions",
        hidden=True,
        help="[DEPRECATED] Use 'obra briefing questions' instead",
    ),
    full: bool = typer.Option(
        False,
        "--full",
        hidden=True,
        help="[DEPRECATED] Use 'obra briefing full' instead",
    ),
    path: bool = typer.Option(
        False,
        "--path",
        hidden=True,
        help="[DEPRECATED] Use 'obra briefing path' instead",
    ),
) -> None:
    """Operating guide for AI assistants using Obra.

    Provides blueprint, protocol, and best practices for LLMs (Claude Code,
    Cursor, Gemini) helping users with Obra.

    Default output (no subcommand) includes:
    - Obra description
    - Input blueprint inline
    - 11 autonomous execution behaviors (names)
    - Subcommand reference

    Examples:
        obra briefing              Default: blueprint inline
        obra briefing blueprint    Quick reference checklist
        obra briefing protocol     Full 11 autonomous behaviors
        obra briefing questions    Question patterns by category
        obra briefing full         Complete guide (1700+ lines)
        obra briefing path         Show file location

    Exit Codes:
        0: Always (informational command)
    """
    try:
        # Handle deprecated flag usage with warnings
        if any([blueprint, protocol, questions, full, path]):
            # Map deprecated flags to new subcommands
            if path:
                err_console.print(
                    "[yellow]Warning: --path is deprecated. Use 'obra briefing path' instead.[/yellow]",
                    style="yellow",
                )
                content, file_path = _load_onboarding_content()
                console.print()
                console.print("[bold]LLM Onboarding Guide Location:[/bold]")
                console.print()
                console.print(f"  {file_path}")
                console.print()
                console.print("Use this path to read the complete guide in your editor or tools.")
                console.print()
                return

            if full:
                err_console.print(
                    "[yellow]Warning: --full is deprecated. Use 'obra briefing full' instead.[/yellow]",
                    style="yellow",
                )
                content, _ = _load_onboarding_content()
                console.print(content)
                return

            if blueprint:
                err_console.print(
                    "[yellow]Warning: --blueprint is deprecated. Use 'obra briefing blueprint' instead.[/yellow]",
                    style="yellow",
                )
                _display_blueprint()
                return

            if protocol:
                err_console.print(
                    "[yellow]Warning: --protocol is deprecated. Use 'obra briefing protocol' instead.[/yellow]",
                    style="yellow",
                )
                content, _ = _load_onboarding_content()
                _display_protocol_full(content)
                return

            if questions:
                err_console.print(
                    "[yellow]Warning: --questions is deprecated. Use 'obra briefing questions' instead.[/yellow]",
                    style="yellow",
                )
                content, _ = _load_onboarding_content()
                _display_question_patterns(content)
                return

        # If a subcommand is being invoked, let it handle things
        if ctx.invoked_subcommand is not None:
            return

        # Default: show the briefing guide
        _track_briefing_usage("default")
        _display_default_briefing()

    except typer.Exit:
        raise
    except (UnicodeEncodeError, UnicodeDecodeError):
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in briefing command: {e}")
        raise typer.Exit(1)


@briefing_app.command(name="quick")
@handle_encoding_errors
def briefing_quick() -> None:
    """Essential input quality checklist (~2 min read, 1,500 tokens).

    Shows a quick reference with minimum required information, quality gates,
    and decision tree for gathering requirements. Recommended starting point
    for AI agents.

    Examples:
        obra briefing quick

    Exit Codes:
        0: Always (informational command)
    """
    try:
        _track_briefing_usage("quick")

        # Load BRIEFING_QUICK.md from package
        try:
            # Try importlib.resources first (Python 3.9+)
            from importlib.resources import files  # noqa: PLC0415

            quick_content = files("obra").joinpath(".obra/BRIEFING_QUICK.md").read_text()
        except (ImportError, AttributeError):
            # Fallback to pkg_resources for older Python
            import pkg_resources  # noqa: PLC0415

            quick_content = pkg_resources.resource_string(
                "obra", ".obra/BRIEFING_QUICK.md"
            ).decode("utf-8")

        console.print(quick_content)
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in briefing quick: {e}")
        raise typer.Exit(1)


@briefing_app.command(name="full")
@handle_encoding_errors
def briefing_full() -> None:
    """Complete LLM onboarding guide (3,600+ lines).

    Outputs the entire LLM_ONBOARDING.md file, which includes:
    - Input blueprint (what to gather from users)
    - Autonomous operation protocol (11 behaviors)
    - Question patterns by category
    - Advanced usage patterns

    Examples:
        obra briefing full
        obra briefing full | head -100

    Exit Codes:
        0: Always (informational command)
    """
    try:
        _track_briefing_usage("full")
        content, _ = _load_onboarding_content()
        console.print(content)
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in briefing full: {e}")
        raise typer.Exit(1)


@briefing_app.command(name="blueprint")
@handle_encoding_errors
def briefing_blueprint() -> None:
    """Quick blueprint reference (condensed checklist format).

    Shows a condensed checklist of what to gather from users before
    invoking Obra. Useful as a quick reference during conversations.

    Examples:
        obra briefing blueprint

    Exit Codes:
        0: Always (informational command)
    """
    try:
        _track_briefing_usage("blueprint")
        _display_blueprint()
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in briefing blueprint: {e}")
        raise typer.Exit(1)


@briefing_app.command(name="protocol")
@handle_encoding_errors
def briefing_protocol() -> None:
    """Full autonomous execution protocol (11 behaviors detailed).

    Shows the complete autonomous operation protocol that describes
    how LLMs should behave while Obra executes tasks.

    Examples:
        obra briefing protocol

    Exit Codes:
        0: Always (informational command)
    """
    try:
        _track_briefing_usage("protocol")
        content, _ = _load_onboarding_content()
        _display_protocol_full(content)
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in briefing protocol: {e}")
        raise typer.Exit(1)


@briefing_app.command(name="questions")
@handle_encoding_errors
def briefing_questions() -> None:
    """Detailed question patterns by category.

    Shows question patterns organized by category to help LLMs
    gather requirements from users effectively.

    Examples:
        obra briefing questions

    Exit Codes:
        0: Always (informational command)
    """
    try:
        _track_briefing_usage("questions")
        content, _ = _load_onboarding_content()
        _display_question_patterns(content)
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in briefing questions: {e}")
        raise typer.Exit(1)


@briefing_app.command(name="path")
@handle_encoding_errors
def briefing_path() -> None:
    """Show file path for deep reading.

    Shows the location of the LLM_ONBOARDING.md file so you can
    read it directly in your editor or tools.

    Examples:
        obra briefing path

    Exit Codes:
        0: Always (informational command)
    """
    try:
        _track_briefing_usage("path")
        _, file_path = _load_onboarding_content()
        console.print()
        console.print("[bold]LLM Onboarding Guide Location:[/bold]")
        console.print()
        console.print(f"  {file_path}")
        console.print()
        console.print("Use this path to read the complete guide in your editor or tools.")
        console.print()
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in briefing path: {e}")
        raise typer.Exit(1)


@briefing_app.command(name="examples")
@handle_encoding_errors
def briefing_examples() -> None:
    """Good vs bad input examples across project types.

    Shows 20+ worked examples comparing vague (bad) vs specific (good)
    input for common project types: APIs, web apps, CLIs, and more.

    Examples:
        obra briefing examples

    Exit Codes:
        0: Always (informational command)
    """
    try:
        _track_briefing_usage("examples")
        _display_examples()
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in briefing examples: {e}")
        raise typer.Exit(1)


def _display_examples() -> None:
    """Display good vs bad input examples for common project types."""
    console.print()
    console.print("[bold]OBRA INPUT EXAMPLES: Good vs Bad[/bold]")
    console.print("[cyan]══════════════════════════════════[/cyan]")
    console.print()
    console.print(
        "Compare [red]BAD[/red] (vague) vs [green]GOOD[/green] (specific) inputs."
    )
    console.print("Notice: tech stack, features, success criteria, constraints.")
    console.print()

    # Example 1: REST API
    console.print("[bold]1. REST API[/bold]")
    console.print("[cyan]───────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Build me an API"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "User management REST API with FastAPI + PostgreSQL.')
    console.print("         JWT authentication with refresh tokens, CRUD operations")
    console.print("         (create, read, update, delete users), role-based access")
    console.print('         control (admin/user). Docker Compose deployment. Tests >80%."')
    console.print()

    # Example 2: Web Application
    console.print("[bold]2. Web Application[/bold]")
    console.print("[cyan]─────────────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Build a website"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "E-commerce storefront: Next.js 14 + TypeScript frontend,')
    console.print("         Stripe checkout integration, product catalog with search")
    console.print("         and filter by category/price, shopping cart with session")
    console.print("         persistence, responsive design. Vercel deployment.")
    console.print('         Lighthouse score >90."')
    console.print()

    # Example 3: CLI Tool
    console.print("[bold]3. CLI Tool[/bold]")
    console.print("[cyan]───────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Make a CLI"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "Python CLI for log analysis with typer + rich.')
    console.print("         Commands: parse (extract errors/warnings), stats (count by")
    console.print("         level), search (regex filter). Input: file path or stdin.")
    console.print("         Output: colored terminal, optional JSON export.")
    console.print('         --verbose flag for debug info. Tests with pytest."')
    console.print()

    # Example 4: Authentication
    console.print("[bold]4. Authentication Feature[/bold]")
    console.print("[cyan]────────────────────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Add authentication"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "Add JWT authentication to existing Express API:')
    console.print("         Access tokens (15min expiry), refresh tokens (7 day),")
    console.print("         bcrypt password hashing, /register, /login, /refresh,")
    console.print("         /logout endpoints. Auth middleware for protected routes.")
    console.print('         Rate limiting on auth endpoints. Integration tests."')
    console.print()

    # Example 5: Bug Fix
    console.print("[bold]5. Bug Fix[/bold]")
    console.print("[cyan]──────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Fix the bug"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "Fix race condition in src/workers/queue.py:')
    console.print("         Multiple workers calling process_job() simultaneously")
    console.print("         cause duplicate processing. Symptom: same job ID appears")
    console.print("         2-3x in logs. Expected: each job processed exactly once.")
    console.print('         Add Redis SETNX lock or PostgreSQL advisory lock."')
    console.print()

    # Example 6: Database Integration
    console.print("[bold]6. Database Integration[/bold]")
    console.print("[cyan]──────────────────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Add a database"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "Add PostgreSQL to existing FastAPI app:')
    console.print("         SQLAlchemy ORM with async support (asyncpg driver),")
    console.print("         Alembic migrations, connection pooling (5-20 connections),")
    console.print("         models for User, Product, Order with relationships.")
    console.print('         Docker Compose with postgres:15. Seed script for dev data."')
    console.print()

    # Example 7: Testing
    console.print("[bold]7. Testing[/bold]")
    console.print("[cyan]──────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Add tests"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "Add pytest test suite for src/services/payment.py:')
    console.print("         Unit tests for calculate_total(), apply_discount(),")
    console.print("         validate_card(). Integration tests for Stripe API calls")
    console.print("         using VCR cassettes. Edge cases: zero amount, negative,")
    console.print('         expired card, network timeout. Target >90% coverage."')
    console.print()

    # Example 8: Refactoring
    console.print("[bold]8. Refactoring[/bold]")
    console.print("[cyan]─────────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Refactor the code"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "Refactor src/api/handlers.py (800 lines) into modules:')
    console.print("         Split by domain: users.py, products.py, orders.py, auth.py.")
    console.print("         Extract shared validation to validators.py, shared DB")
    console.print("         queries to repositories.py. Keep all existing tests passing.")
    console.print('         No new dependencies. Preserve API contract."')
    console.print()

    # Example 9: Performance
    console.print("[bold]9. Performance Optimization[/bold]")
    console.print("[cyan]──────────────────────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Make it faster"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "Optimize /api/products endpoint (currently 2.5s):')
    console.print("         Add Redis caching (5min TTL) for product listings,")
    console.print("         database query optimization (add indexes on category_id,")
    console.print("         price), pagination (limit 50 per page). Target: <200ms")
    console.print('         p95 response time. Add APM instrumentation."')
    console.print()

    # Example 10: Documentation
    console.print("[bold]10. Documentation[/bold]")
    console.print("[cyan]─────────────────[/cyan]")
    console.print()
    console.print('[red]❌ BAD:[/red]  "Add docs"')
    console.print()
    console.print('[green]✅ GOOD:[/green] "Add OpenAPI documentation to FastAPI endpoints:')
    console.print("         Response schemas for all endpoints, example request/response")
    console.print("         bodies, authentication requirements documented, error")
    console.print("         response codes (400, 401, 403, 404, 500) with descriptions.")
    console.print('         Generate and host Swagger UI at /docs."')
    console.print()

    console.print("[cyan]══════════════════════════════════════════════════════════════════════[/cyan]")
    console.print()
    console.print("[bold]Key Pattern:[/bold] Good input includes:")
    console.print("  • [cyan]Tech stack[/cyan] (language, framework, database)")
    console.print("  • [cyan]Specific features[/cyan] (not 'auth' but 'JWT with refresh tokens')")
    console.print("  • [cyan]Success criteria[/cyan] (testable: '>80% coverage', '<200ms')")
    console.print("  • [cyan]Constraints[/cyan] (deployment target, existing code to preserve)")
    console.print()
    console.print("[dim]💡 Run [/dim][cyan]obra briefing quick[/cyan][dim] for the full checklist[/dim]")
    console.print()


def _display_protocol_full(content: str) -> None:
    """Display the full autonomous execution protocol with all 11 behaviors.

    Args:
        content: Full content of LLM_ONBOARDING.md
    """
    # Extract the Autonomous Operation Protocol section
    lines = content.split("\n")
    in_protocol_section = False
    protocol_lines = []

    for i, line in enumerate(lines):
        if line.strip() == "## Autonomous Operation Protocol":
            in_protocol_section = True
            continue

        if in_protocol_section:
            # Stop at the next ## heading
            if line.startswith("## ") and not line.startswith("### "):
                break
            protocol_lines.append(line)

    # Display the extracted section
    console.print()
    console.print("[bold cyan]AUTONOMOUS OPERATION PROTOCOL[/bold cyan]")
    console.print()
    console.print("\n".join(protocol_lines))
    console.print()


def _display_question_patterns(content: str) -> None:
    """Display question patterns by category.

    Args:
        content: Full content of LLM_ONBOARDING.md
    """
    # Extract the Question Patterns section
    lines = content.split("\n")
    in_patterns_section = False
    patterns_lines = []

    for line in lines:
        if "## Question Patterns" in line or "## The Questions to Ask" in line:
            in_patterns_section = True
            continue

        if in_patterns_section:
            # Stop at the next ## heading
            if line.startswith("## ") and not line.startswith("### "):
                break
            patterns_lines.append(line)

    # Display the extracted section
    console.print()
    console.print("[bold cyan]QUESTION PATTERNS FOR GATHERING REQUIREMENTS[/bold cyan]")
    console.print()
    console.print("\n".join(patterns_lines))
    console.print()


# =============================================================================
# Authentication Commands
# =============================================================================


@app.command(rich_help_panel="User Commands")
@handle_encoding_errors
def login(
    timeout: int = typer.Option(
        300,
        "--timeout",
        "-t",
        help="Timeout in seconds for browser authentication",
    ),
    no_browser: bool = typer.Option(
        False,
        "--no-browser",
        help="Don't open browser, just print URL",
    ),
) -> None:
    """Authenticate with Obra.

    Opens your browser to sign in with Google or GitHub.
    After successful authentication, your session is saved locally.

    Examples:
        $ obra login
        $ obra login --no-browser
        $ obra login --timeout 600
    """
    try:
        from obra.auth import login_with_browser, save_auth

        console.print()
        console.print("[bold]Obra Login[/bold]", style="cyan")
        console.print()

        if no_browser:
            console.print("Opening authentication URL...")
            console.print("Copy the URL below and open it in your browser:")
        else:
            console.print("Opening browser for authentication...")

        result = login_with_browser(timeout=timeout, auto_open=not no_browser)

        # Save the authentication
        save_auth(result)

        console.print()
        print_success(f"Logged in as: {result.email}")
        if result.display_name:
            console.print(f"Name: {result.display_name}")

        # Display next steps
        console.print()
        console.print("[bold]Next Steps[/bold]", style="cyan")
        console.print()
        console.print("1. [cyan]Validate your environment[/cyan]")
        console.print("   $ obra config --validate")
        console.print()
        console.print("2. [cyan]Explore documentation[/cyan]")
        console.print("   $ obra docs")
        console.print()
        console.print("3. [cyan]Start your first task[/cyan]")
        console.print('   $ obra run "Add user authentication"')
        console.print()
        console.print("4. [cyan]Check session status[/cyan]")
        console.print("   $ obra status")
        console.print()

    except AuthenticationError as e:
        display_obra_error(e, console)
        logger.error(f"Authentication error in login command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in login command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in login command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in login command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in login command: {e}")
        _print_bug_hint()
        raise typer.Exit(1)


@app.command(rich_help_panel="User Commands")
@handle_encoding_errors
def logout() -> None:
    """Log out and clear stored credentials.

    Removes your authentication token from the local config.
    You'll need to run 'obra login' again to use Obra.

    Example:
        $ obra logout
    """
    try:
        from obra.auth import clear_auth, get_current_auth

        auth = get_current_auth()
        if not auth:
            print_info("Not currently logged in")
            return

        email = auth.email
        clear_auth()

        console.print()
        print_success(f"Logged out: {email}")
        console.print("\nRun 'obra login' to sign in again.")

    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in logout command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in logout command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except OSError as e:
        print_error(f"Failed to clear authentication: {e}")
        logger.error(f"File I/O error in logout command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in logout command: {e}")
        _print_bug_hint()
        raise typer.Exit(1)


@app.command(rich_help_panel="User Commands")
@handle_encoding_errors
def whoami() -> None:
    """Show current authentication status.

    Displays the currently authenticated user and token status.

    Example:
        $ obra whoami
    """
    try:
        from obra.auth import get_current_auth
        from obra.config import load_config

        auth = get_current_auth()

        console.print()
        if not auth:
            print_info("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            return

        console.print("[bold]Current User[/bold]", style="cyan")
        console.print()

        table = Table(show_header=False, box=None)
        table.add_column("Field", style="dim")
        table.add_column("Value")

        table.add_row("Email", auth.email)
        if auth.display_name:
            table.add_row("Name", auth.display_name)
        table.add_row("Provider", auth.auth_provider)
        table.add_row("User ID", auth.firebase_uid[:16] + "...")

        console.print(table)

        # Check token status
        config = load_config()
        token_expires = config.get("token_expires_at")
        if token_expires:
            from datetime import datetime

            try:
                expires_dt = datetime.fromisoformat(token_expires.replace("Z", "+00:00"))
                now = datetime.now(UTC)
                if expires_dt > now:
                    remaining = expires_dt - now
                    minutes = int(remaining.total_seconds() / 60)
                    console.print(f"\n[dim]Token expires in {minutes} minutes[/dim]")
                else:
                    console.print(
                        "\n[yellow]Token expired - will auto-refresh on next request[/yellow]"
                    )
            except ValueError:
                pass

    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in whoami command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in whoami command: {e}", exc_info=True)
        _print_bug_hint()
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in whoami command: {e}")
        _print_bug_hint()
        raise typer.Exit(1)


# =============================================================================
# Configuration Commands
# =============================================================================


def _run_config_validation(json_output: bool = False, include_schema: bool = False) -> None:
    """Run configuration validation and display results.

    S4.T2: Validates provider CLIs and configuration settings.

    Args:
        json_output: If True, output JSON instead of human-readable format
        include_schema: If True, include schema validation results
    """
    import json

    from obra.config import CONFIG_PATH, LLM_PROVIDERS, check_provider_status
    from obra.config.loaders import load_config_with_warnings

    # Check all providers
    provider_results = {}
    for provider_key in LLM_PROVIDERS:
        status = check_provider_status(provider_key)
        provider_results[provider_key] = {
            "name": LLM_PROVIDERS[provider_key].get("name", provider_key),
            "installed": status.installed,
            "cli_command": status.cli_command,
            "install_hint": status.install_hint,
            "docs_url": status.docs_url,
        }

    # Load configuration
    config_data, warnings, config_exists = load_config_with_warnings()
    config_exists = config_exists or bool(config_data)
    schema = _config_schema()
    schema_warnings = _config_schema_version_warnings(config_data, schema)
    if schema and config_data:
        unknown_keys = _config_unknown_keys(config_data, schema)
        if unknown_keys:
            preview = ", ".join(sorted(unknown_keys)[:10])
            suffix = "..." if len(unknown_keys) > 10 else ""
            warnings.append(
                "Unknown config keys in "
                f"{CONFIG_PATH}: {preview}{suffix}. "
                "Hint: remove or check spelling; see `obra config show --json` for valid keys."
            )

    warnings.extend(schema_warnings)

    schema_issues: dict[str, object] = {}
    if include_schema and schema:
        schema_issues = {
            "unknown_keys": _config_unknown_keys(config_data, schema),
            "missing_sections": _config_schema_missing_sections(config_data, schema)
            if config_data
            else [],
            "type_mismatches": [
                {"path": path, "expected": expected, "actual": actual}
                for path, expected, actual in _config_schema_type_mismatches(config_data, schema)
            ],
        }

    # Overall status
    all_installed = all(p["installed"] for p in provider_results.values())

    if json_output:
        # S4.T4: JSON output structure
        output = {
            "status": "valid" if (all_installed and config_exists) else "issues_found",
            "providers": provider_results,
            "configuration": {
                "path": str(CONFIG_PATH),
                "exists": config_exists,
                "keys_present": list(config_data.keys()) if config_data else [],
            },
            "warnings": warnings,
            "schema": {
                "version": str(schema.get("config_version")) if schema else None,
                "config_version": config_data.get("config_version") if config_data else None,
                "issues": schema_issues if include_schema else {},
            },
        }
        console.print(json.dumps(output, indent=2))
    else:
        # S4.T3: Human-readable output with colors and icons
        _display_validation_human(
            provider_results,
            config_exists,
            str(CONFIG_PATH),
            warnings,
            schema_issues if include_schema else None,
        )


def _display_validation_human(
    provider_results: dict,
    config_exists: bool,
    config_path: str,
    warnings: list[str],
    schema_issues: dict[str, object] | None,
) -> None:
    """Display validation results in human-readable format with colors and icons.

    S4.T3: Display validation with ✓/✗ icons and colored output.

    Args:
        provider_results: Provider validation results
        config_exists: Whether config file exists
        config_path: Path to config file
    """
    console.print()
    console.print("[bold]Configuration Validation[/bold]", style="cyan")
    console.print()

    # Provider CLI checks
    console.print("[bold]Provider CLIs:[/bold]")
    for provider_key, result in provider_results.items():
        if result["installed"]:
            icon = "[green]✓[/green]"
            status_text = f"[green]{result['cli_command']} installed[/green]"
        else:
            icon = "[red]✗[/red]"
            status_text = f"[red]{result['cli_command']} not found[/red]"
            if result["install_hint"]:
                status_text += f"\n    [dim]{result['install_hint']}[/dim]"

        console.print(f"  {icon} {result['name']}: {status_text}")

    console.print()

    # Configuration file check
    console.print("[bold]Configuration:[/bold]")
    if config_exists:
        icon = "[green]✓[/green]"
        status_text = f"[green]Config found at {config_path}[/green]"
    else:
        icon = "[yellow]⚠[/yellow]"
        status_text = "[yellow]No config file (using defaults)[/yellow]"

    console.print(f"  {icon} {status_text}")
    console.print()

    if warnings:
        console.print("[bold]Schema Warnings:[/bold]")
        for warning in warnings:
            console.print(f"  [yellow]⚠[/yellow] {warning}")
        console.print()

    if schema_issues is not None:
        console.print("[bold]Schema Validation:[/bold]")
        unknown = schema_issues.get("unknown_keys", [])
        missing = schema_issues.get("missing_sections", [])
        mismatches = schema_issues.get("type_mismatches", [])

        if not unknown and not missing and not mismatches:
            console.print("  [green]✓[/green] No schema issues found")
        else:
            if unknown:
                preview = ", ".join(unknown[:10])
                suffix = "..." if len(unknown) > 10 else ""
                console.print(f"  [yellow]⚠[/yellow] Unknown keys: {preview}{suffix}")
            if missing:
                preview = ", ".join(missing[:10])
                suffix = "..." if len(missing) > 10 else ""
                console.print(f"  [yellow]⚠[/yellow] Missing sections: {preview}{suffix}")
            if mismatches:
                preview = ", ".join(
                    f"{item['path']} ({item['expected']} -> {item['actual']})"
                    for item in mismatches[:5]
                )
                suffix = "..." if len(mismatches) > 5 else ""
                console.print(f"  [yellow]⚠[/yellow] Type mismatches: {preview}{suffix}")
        console.print()

    # Overall status
    all_installed = all(p["installed"] for p in provider_results.values())
    if all_installed and config_exists:
        print_success("All checks passed!")
    elif all_installed:
        print_warning("Providers installed but no config file found (using defaults)")
    else:
        print_warning("Some provider CLIs are not installed")
        console.print(
            "\n[dim]Tip: Install the providers you plan to use with obra run --impl-provider[/dim]"
        )


# Create config subcommand group (S3.T0)
config_app = typer.Typer(
    name="config",
    help="Manage Obra configuration (TUI, show, get, set, reset, validate)",
    invoke_without_command=True,
    rich_markup_mode="rich",
)
app.add_typer(config_app, name="config", rich_help_panel="User Commands")


# Config helper functions (shared by callback and subcommands)
@lru_cache(maxsize=1)
def _config_schema() -> dict[str, object]:
    """Load the packaged default config schema."""
    try:
        from obra.config.explorer.utils import load_default_config_schema

        schema = load_default_config_schema()
        if isinstance(schema, dict):
            return schema
    except Exception:
        return {}
    return {}


@lru_cache(maxsize=1)
def _config_schema_paths() -> set[str]:
    """Cache all schema dot-paths for fast lookup."""
    schema = _config_schema()
    if not schema:
        return set()

    from obra.config.explorer.utils import iter_schema_paths

    return {path for path, _ in iter_schema_paths(schema)}


@lru_cache(maxsize=1)
def _config_deprecated_paths() -> set[str]:
    """Return deprecated config paths that map to new hierarchy."""
    from obra.config.loaders import CONFIG_PATH_ALIASES

    return set(CONFIG_PATH_ALIASES.keys())


def _config_normalize_path(path: str) -> tuple[str, str | None]:
    """Normalize deprecated config paths to canonical ones."""
    from obra.config.loaders import resolve_config_alias

    canonical = resolve_config_alias(path)
    if canonical != path:
        return canonical, f"Config key '{path}' is deprecated; use '{canonical}'."
    return path, None


def _config_is_known_path(path: str) -> bool:
    """Check if a path exists in the schema (fallback to descriptions)."""
    normalized, _ = _config_normalize_path(path)
    schema_paths = _config_schema_paths()
    if schema_paths:
        return normalized in schema_paths

    from obra.config.explorer.descriptions import get_description

    return get_description(normalized) is not None


def _config_get_schema_value(path: str) -> object | None:
    """Get a schema value by dotted path."""
    current: object = _config_schema()
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def _config_schema_has_children(path: str) -> bool:
    """Check if a schema path has children."""
    normalized, _ = _config_normalize_path(path)
    schema_paths = _config_schema_paths()
    if schema_paths:
        prefix = f"{normalized}."
        return any(other.startswith(prefix) for other in schema_paths)

    from obra.config.explorer.descriptions import get_all_paths

    prefix = f"{normalized}."
    return any(other.startswith(prefix) for other in get_all_paths())


def _config_unknown_keys(
    config: dict[str, object],
    schema: dict[str, object],
    prefix: str = "",
) -> list[str]:
    """Return config keys not present in the schema."""
    unknown: list[str] = []
    for key, value in config.items():
        path = f"{prefix}.{key}" if prefix else key
        if key not in schema:
            if path in _config_deprecated_paths():
                continue
            unknown.append(path)
            continue
        schema_value = schema.get(key)
        if isinstance(value, dict) and isinstance(schema_value, dict):
            unknown.extend(_config_unknown_keys(value, schema_value, path))
    return unknown


def _config_schema_type_mismatches(
    config: dict[str, object],
    schema: dict[str, object],
    prefix: str = "",
) -> list[tuple[str, str, str]]:
    """Return (path, expected_type, actual_type) for schema mismatches."""
    mismatches: list[tuple[str, str, str]] = []
    for key, value in config.items():
        if key not in schema:
            continue
        path = f"{prefix}.{key}" if prefix else key
        schema_value = schema.get(key)

        if isinstance(schema_value, dict):
            if isinstance(value, dict):
                mismatches.extend(_config_schema_type_mismatches(value, schema_value, path))
            else:
                mismatches.append((path, "object", type(value).__name__))
            continue

        if schema_value is None:
            continue

        if isinstance(schema_value, list):
            if not isinstance(value, list):
                mismatches.append((path, "list", type(value).__name__))
            continue

        if isinstance(schema_value, bool):
            if not isinstance(value, bool):
                mismatches.append((path, "bool", type(value).__name__))
            continue

        if isinstance(schema_value, int):
            if not isinstance(value, int) or isinstance(value, bool):
                mismatches.append((path, "int", type(value).__name__))
            continue

        if isinstance(schema_value, float):
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                mismatches.append((path, "float", type(value).__name__))
            continue

        if isinstance(schema_value, str):
            if not isinstance(value, str):
                mismatches.append((path, "str", type(value).__name__))
            continue

        if not isinstance(value, type(schema_value)):
            mismatches.append((path, type(schema_value).__name__, type(value).__name__))

    return mismatches


def _config_schema_missing_sections(
    config: dict[str, object],
    schema: dict[str, object],
) -> list[str]:
    """Return top-level schema sections missing from config."""
    missing: list[str] = []
    for key, value in schema.items():
        if isinstance(value, dict) and key not in config:
            missing.append(key)
    return missing


def _config_schema_version_warnings(
    config: dict[str, object],
    schema: dict[str, object],
) -> list[str]:
    """Return schema version warnings based on config_version."""
    warnings: list[str] = []
    schema_version = schema.get("config_version")
    if schema_version is None:
        return warnings

    expected = str(schema_version)
    current = config.get("config_version")
    if current is None:
        if config:
            warnings.append(
                f"Config schema version missing. Add config_version: {expected} to your config."
            )
        return warnings

    if str(current) != expected:
        warnings.append(
            f"Config schema version mismatch (config={current}, expected={expected}). "
            "Update your config to the latest schema."
        )

    return warnings


def _config_emit_warnings(warnings: list[str]) -> None:
    """Emit warnings for config load or schema issues."""
    for warning in warnings:
        err_console.print(f"[yellow]Warning:[/yellow] {warning}", style="yellow")


def _config_emit_error(message: str, detail: str = "") -> None:
    """Emit config error to stderr."""
    prefix = "Error: "
    print(f"{prefix}{message}", file=sys.stderr)
    if detail:
        print(detail, file=sys.stderr)


def _config_get_nested_value(config: dict[str, object], path: str) -> object | None:
    """Get nested value from config dict by dotted path."""
    parts = path.split(".")
    current: object = config
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def _config_set_nested_value(config: dict[str, object], path: str, value: object) -> None:
    """Set nested value in config dict by dotted path."""
    parts = path.split(".")
    current: dict[str, object] = config
    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]  # type: ignore[assignment]
    current[parts[-1]] = value


def _config_flatten(data: dict[str, object], prefix: str = "") -> dict[str, object]:
    """Flatten nested config dict to dotted paths."""
    flat: dict[str, object] = {}
    for key, value in data.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(_config_flatten(value, path))
        else:
            flat[path] = value
    return flat


def _config_apply_defaults(config_data: dict[str, object]) -> dict[str, object]:
    """Apply default values to config dict."""
    import copy

    from obra.config.explorer.descriptions import CONFIG_DEFAULTS

    schema = _config_schema()
    if schema:
        try:
            from obra.config.explorer.utils import merge_with_default_schema

            return merge_with_default_schema(cast(dict[str, object], config_data))
        except Exception:
            pass

    merged = copy.deepcopy(config_data)
    for path, default_value in CONFIG_DEFAULTS.items():
        if _config_get_nested_value(merged, path) is None:
            _config_set_nested_value(merged, path, default_value)
    return merged


def _config_format_human_value(value: object) -> str:
    """Format value for human-readable output."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _config_redact_value(path: str, value: object) -> object:
    """Redact sensitive values."""
    from obra.config.explorer.descriptions import is_sensitive

    if is_sensitive(path):
        return "***"
    return value


def _config_redact(data: dict[str, object]) -> dict[str, object]:
    """Redact all sensitive values in config dict."""
    redacted: dict[str, object] = {}
    for path, value in _config_flatten(data).items():
        _config_set_nested_value(redacted, path, _config_redact_value(path, value))
    return redacted


def _config_prune_deprecated_paths(config_data: dict[str, object]) -> dict[str, object]:
    """Remove deprecated top-level paths from config display."""
    pruned = dict(config_data)
    for path in _config_deprecated_paths():
        pruned.pop(path, None)
    return pruned


def _config_parse_value(raw: str) -> object:
    """Parse string value to appropriate type."""
    stripped = raw.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in ("'", '"'):
        return stripped[1:-1]
    lower = stripped.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if re.fullmatch(r"-?\d+", stripped):
        return int(stripped)
    if re.fullmatch(r"-?\d+\.\d+", stripped):
        return float(stripped)
    return stripped


def _config_infer_expected_type(path: str, current_config: dict[str, object]) -> type | None:
    """Infer expected type for a config path."""
    schema_value = _config_get_schema_value(path)
    if isinstance(schema_value, (bool, int, float, list, dict, str)):
        return type(schema_value)

    existing = _config_get_nested_value(current_config, path)
    if isinstance(existing, (bool, int, float, list, dict, str)):
        return type(existing)
    return None


def _config_path_has_children(path: str) -> bool:
    """Check if a config path has child paths."""
    return _config_schema_has_children(path)


def _config_load_scope(
    scope: str,
    warn_unknown_keys: bool = False,
) -> tuple[dict[str, object], bool, dict[str, object], list[str]]:
    """Load config for the given scope (local or server)."""
    from obra.config import CONFIG_PATH
    from obra.config.loaders import load_config_with_warnings

    if scope == "server":
        from obra.api import APIClient

        api_client = APIClient.from_config()
        server_config = api_client.get_user_config()
        return server_config.get("resolved", {}), True, server_config.get("resolved", {}), []

    config_data, warnings, config_exists = load_config_with_warnings()
    if warn_unknown_keys:
        schema = _config_schema()
        if schema and config_data:
            unknown_keys = _config_unknown_keys(config_data, schema)
            if unknown_keys:
                preview = ", ".join(sorted(unknown_keys)[:10])
                suffix = "..." if len(unknown_keys) > 10 else ""
                warnings.append(
                    "Unknown config keys in "
                    f"{CONFIG_PATH}: {preview}{suffix}. "
                    "Hint: remove or check spelling; see `obra config show --json` for valid keys."
                )

    effective = _config_apply_defaults(config_data)
    if not config_exists:
        print("info: local config not found; using defaults", file=sys.stderr)
    return effective, config_exists, config_data, warnings


def _config_print_show(config_data: dict[str, object], scope: str, json_output: bool) -> None:
    """Print config in show format."""
    import json

    redacted = _config_redact(_config_prune_deprecated_paths(config_data))
    if json_output:
        payload = {"scope": scope, "data": redacted}
        print(json.dumps(payload, ensure_ascii=True))
        return

    for path, value in sorted(_config_flatten(redacted).items()):
        print(f"{path}: {_config_format_human_value(value)}")


def _config_launch_tui() -> None:
    """Launch the interactive config TUI."""
    from obra.config import load_config

    try:
        from obra.config.explorer import run_explorer

        # Load local config and apply defaults so all settings are visible
        # (matches VS Code, Firefox, Docker pattern - show all settings with defaults)
        local_config = load_config()
        try:
            from obra.config.loaders import CONFIG_PATH_ALIASES

            for legacy_path in CONFIG_PATH_ALIASES:
                local_config.pop(legacy_path, None)
        except Exception:
            pass
        try:
            from obra.config.explorer.utils import merge_with_default_schema  # noqa: PLC0415
            local_config = merge_with_default_schema(local_config)
        except Exception:
            local_config = _config_apply_defaults(local_config)

        # Try to get server config if authenticated
        server_config: dict = {}
        api_client = None
        try:
            from obra.api import APIClient

            api_client = APIClient.from_config()
            config_data = api_client.get_user_config()
            server_config = config_data.get("resolved", {})
            server_config["_preset"] = config_data.get("preset", "unknown")
        except (APIError, ConfigurationError, ConnectionError):
            # Server unavailable or not authenticated - offline mode
            logger.debug("Server config unavailable, using offline mode")
        except Exception as e:
            # Log unexpected errors but continue in offline mode
            logger.warning(f"Unexpected error fetching server config: {e}")

        run_explorer(
            local_config=local_config,
            server_config=server_config,
            api_client=api_client,
        )
    except ImportError:
        print_error("Config explorer not available")
        console.print("\nUse 'obra config show' to view current configuration.")
        console.print("Edit ~/.obra/client-config.yaml directly to make changes.")
        raise typer.Exit(1)


@config_app.callback(invoke_without_command=True)
@handle_encoding_errors
def config_callback(
    ctx: typer.Context,
    # Hidden aliases for deprecated flags (S3.T2 - backwards compatibility)
    show: bool = typer.Option(
        False,
        "--show",
        "-s",
        hidden=True,
        help="[DEPRECATED] Use 'obra config show' instead",
    ),
    get_path: str | None = typer.Option(
        None,
        "--get",
        hidden=True,
        help="[DEPRECATED] Use 'obra config get <path>' instead",
    ),
    set_path: str | None = typer.Option(
        None,
        "--set",
        hidden=True,
        help="[DEPRECATED] Use 'obra config set <path> <value>' instead",
    ),
    set_value: str | None = typer.Option(
        None,
        "--value",
        hidden=True,
        help="[DEPRECATED] Value for --set (use 'obra config set <path> <value>' instead)",
    ),
    reset: bool = typer.Option(
        False,
        "--reset",
        hidden=True,
        help="[DEPRECATED] Use 'obra config reset' instead",
    ),
    validate: bool = typer.Option(
        False,
        "--validate",
        hidden=True,
        help="[DEPRECATED] Use 'obra config validate' instead",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        hidden=True,
        help="[DEPRECATED] Use subcommands with --json instead",
    ),
    confirm: bool = typer.Option(False, "--confirm", hidden=True),
    scope: str = typer.Option("local", "--scope", hidden=True),
    verbose: bool = typer.Option(False, "--verbose", "-v", hidden=True),
) -> None:
    """Manage Obra configuration.

    Without subcommands, launches the interactive configuration TUI.

    Subcommands:
        show      - Display current configuration
        get       - Get value for a specific config path
        set       - Set a config value
        reset     - Reset configuration to defaults
        validate  - Validate provider CLIs and configuration

    Examples:
        obra config                              # Launch TUI
        obra config show                         # Show all config
        obra config show --json                  # Show as JSON
        obra config get llm.orchestrator.provider
        obra config set llm.orchestrator.provider openai
        obra config reset
        obra config validate
    """
    try:
        import json

        from obra.config import save_config
        from obra.config.explorer.descriptions import get_choices

        # Handle deprecated flag usage with warnings (S3.T2)
        deprecated_flags = [validate, reset, show, bool(get_path), bool(set_path)]
        if any(deprecated_flags):
            # Validate flag combinations
            if sum(1 for flag in deprecated_flags if flag) > 1:
                _config_emit_error(
                    "Only one of --show, --get, --set, --reset, or --validate may be used at a time"
                )
                raise typer.Exit(2)

            if confirm and not set_path:
                _config_emit_error("--confirm is only valid with --set")
                raise typer.Exit(2)

            if set_path and json_output and not confirm:
                _config_emit_error("--set --json requires --confirm")
                raise typer.Exit(2)

            if json_output and not (validate or show or get_path or (set_path and confirm)):
                _config_emit_error(
                    "--json is only valid with --show, --get, --validate, or --set --confirm"
                )
                raise typer.Exit(2)

            if scope not in ("local", "server"):
                _config_emit_error("Invalid scope. Use --scope local or --scope server")
                raise typer.Exit(2)

            if set_path:
                _config_emit_error(
                    "The --set flag is deprecated and no longer functional.\n"
                    "Use 'obra config set <path> <value>' instead."
                )
                raise typer.Exit(2)

            # Handle --validate (deprecated)
            if validate:
                err_console.print(
                    "[yellow]Warning: --validate is deprecated. "
                    "Use 'obra config validate' instead.[/yellow]",
                    style="yellow",
                )
                _run_config_validation(json_output=json_output)
                return

            # Handle --reset (deprecated)
            if reset:
                err_console.print(
                    "[yellow]Warning: --reset is deprecated. "
                    "Use 'obra config reset' instead.[/yellow]",
                    style="yellow",
                )
                # C14: Check for non-interactive mode before prompting
                if not sys.stdin.isatty():
                    console.print(
                        "Non-interactive mode: skipping reset confirmation (defaulting to cancel)"
                    )
                    return

                do_reset = typer.confirm("Reset configuration to defaults?")
                if not do_reset:
                    console.print("Cancelled")
                    return

                save_config({})
                print_success("Configuration reset to defaults")
                return

            # Handle --show (deprecated)
            if show:
                err_console.print(
                    "[yellow]Warning: --show is deprecated. "
                    "Use 'obra config show' instead.[/yellow]",
                    style="yellow",
                )
                config_data, _, _, warnings = _config_load_scope(scope, warn_unknown_keys=True)
                _config_emit_warnings(warnings)
                _config_print_show(config_data, scope, json_output)
                return

            # Handle --get (deprecated)
            if get_path:
                err_console.print(
                    "[yellow]Warning: --get is deprecated. "
                    f"Use 'obra config get {get_path}' instead.[/yellow]",
                    style="yellow",
                )
                normalized_path, warning = _config_normalize_path(get_path)
                if warning:
                    _config_emit_warnings([warning])
                if not _config_is_known_path(normalized_path):
                    _config_emit_error(f"Unknown config path '{get_path}'")
                    raise typer.Exit(1)

                config_data, _, _, warnings = _config_load_scope(scope)
                _config_emit_warnings(warnings)
                value = _config_get_nested_value(config_data, normalized_path)
                value = _config_redact_value(normalized_path, value)

                if json_output:
                    payload = {"scope": scope, "data": {normalized_path: value}}
                    print(json.dumps(payload, ensure_ascii=True))
                else:
                    print(_config_format_human_value(value))
                return

            # Handle --set (deprecated)
            if set_path:
                err_console.print(
                    "[yellow]Warning: --set is deprecated. "
                    f"Use 'obra config set {set_path} <value>' instead.[/yellow]",
                    style="yellow",
                )
                normalized_path, warning = _config_normalize_path(set_path)
                if warning:
                    _config_emit_warnings([warning])
                if not _config_is_known_path(normalized_path):
                    _config_emit_error(f"Unknown config path '{set_path}'")
                    raise typer.Exit(1)

                if _config_path_has_children(normalized_path):
                    _config_emit_error(f"Cannot set non-leaf config path '{set_path}'")
                    raise typer.Exit(1)

                config_data, _, _, warnings = _config_load_scope(scope)
                _config_emit_warnings(warnings)
                raw_value = set_value or ""
                choices = get_choices(normalized_path, config_data)
                if choices and raw_value not in choices:
                    _config_emit_error(
                        f"Invalid value '{raw_value}' for {normalized_path}",
                        f"Valid choices: {', '.join(choices)}",
                    )
                    raise typer.Exit(1)

                parsed_value = _config_parse_value(raw_value)
                expected_type = _config_infer_expected_type(normalized_path, config_data)
                if expected_type is bool and not isinstance(parsed_value, bool):
                    _config_emit_error(
                        f"Expected boolean for {normalized_path}, got '{raw_value}'"
                    )
                    raise typer.Exit(1)
                if expected_type is int and not isinstance(parsed_value, int):
                    _config_emit_error(
                        f"Expected integer for {normalized_path}, got '{raw_value}'"
                    )
                    raise typer.Exit(1)
                if expected_type is float and not isinstance(parsed_value, (int, float)):
                    _config_emit_error(
                        f"Expected number for {normalized_path}, got '{raw_value}'"
                    )
                    raise typer.Exit(1)

                if scope == "server":
                    from obra.api import APIClient

                    api_client = APIClient.from_config()
                    server_config = api_client.update_user_config(
                        overrides={normalized_path: parsed_value}
                    )
                    config_data = server_config.get("resolved", {})
                else:
                    local_config = load_config()
                    _config_set_nested_value(local_config, normalized_path, parsed_value)
                    save_config(local_config)
                    config_data = _config_apply_defaults(local_config)

                if not json_output:
                    print_success(f"Set {normalized_path} = {raw_value}")
                if confirm:
                    _config_print_show(config_data, scope, json_output)
                return

        # If no subcommand was invoked, launch TUI (default behavior)
        if ctx.invoked_subcommand is None:
            _config_launch_tui()

    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in config command: {e}", exc_info=True)
        raise typer.Exit(1)
    except typer.Exit:
        raise
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in config command: {e}", exc_info=True)
        raise typer.Exit(1)
    except OSError as e:
        print_error(f"Failed to access configuration file: {e}")
        logger.error(f"File I/O error in config command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in config command: {e}")
        raise typer.Exit(1)


# Config subcommands (S3.T1)
@config_app.command(name="show")
@handle_encoding_errors
def config_show(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    scope: str = typer.Option("local", "--scope", help="Config scope: local or server"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show where each value comes from"
    ),
) -> None:
    """Display current configuration.

    Shows all configuration values with their current settings.
    Use --json for machine-readable output.
    Use --scope server to show server-side configuration.

    Examples:
        obra config show
        obra config show --json
        obra config show --scope server
        obra config show --verbose

    Exit Codes:
        0: Success
        1: Configuration error
    """
    try:
        if scope not in ("local", "server"):
            _config_emit_error("Invalid scope. Use --scope local or --scope server")
            raise typer.Exit(2)

        config_data, _, _, warnings = _config_load_scope(scope, warn_unknown_keys=True)
        _config_emit_warnings(warnings)
        _config_print_show(config_data, scope, json_output)

    except ConfigurationError as e:
        display_obra_error(e, console)
        raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in config show: {e}")
        raise typer.Exit(1)


@config_app.command(name="get")
@handle_encoding_errors
def config_get(
    path: str = typer.Argument(..., help="Configuration path (e.g., llm.orchestrator.provider)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    scope: str = typer.Option("local", "--scope", help="Config scope: local or server"),
) -> None:
    """Get value for a specific configuration path.

    Retrieves the value of a single configuration key.
    Use dotted paths to access nested values.

    Examples:
        obra config get llm.orchestrator.provider
        obra config get llm.orchestrator.model --json
        obra config get api.timeout --scope server

    Exit Codes:
        0: Success
        1: Unknown path or error
    """
    try:
        import json

        if scope not in ("local", "server"):
            _config_emit_error("Invalid scope. Use --scope local or --scope server")
            raise typer.Exit(2)

        normalized_path, warning = _config_normalize_path(path)
        if warning:
            _config_emit_warnings([warning])
        if not _config_is_known_path(normalized_path):
            _config_emit_error(f"Unknown config path '{path}'")
            raise typer.Exit(1)

        config_data, _, _, warnings = _config_load_scope(scope)
        _config_emit_warnings(warnings)
        value = _config_get_nested_value(config_data, normalized_path)
        value = _config_redact_value(normalized_path, value)

        if json_output:
            payload = {"scope": scope, "data": {normalized_path: value}}
            print(json.dumps(payload, ensure_ascii=True))
        else:
            print(_config_format_human_value(value))

    except ConfigurationError as e:
        display_obra_error(e, console)
        raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in config get: {e}")
        raise typer.Exit(1)


@config_app.command(name="set")
@handle_encoding_errors
def config_set(
    path: str = typer.Argument(..., help="Configuration path to set"),
    value: str = typer.Argument(..., help="Value to set"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON after setting"),
    scope: str = typer.Option("local", "--scope", help="Config scope: local or server"),
    confirm: bool = typer.Option(False, "--confirm", help="Show config after changes"),
) -> None:
    """Set a configuration value.

    Sets a single configuration key to the specified value.
    Values are automatically parsed (true/false become booleans, numbers stay numbers).

    Examples:
        obra config set llm.orchestrator.provider openai
        obra config set api.timeout 30
        obra config set debug true --confirm

    Exit Codes:
        0: Success
        1: Invalid path, value, or error
    """
    try:
        from obra.config import save_config
        from obra.config.explorer.descriptions import get_choices, get_lock_reason, is_locked

        if scope not in ("local", "server"):
            _config_emit_error("Invalid scope. Use --scope local or --scope server")
            raise typer.Exit(2)

        normalized_path, warning = _config_normalize_path(path)
        if warning:
            _config_emit_warnings([warning])
        if not _config_is_known_path(normalized_path):
            _config_emit_error(f"Unknown config path '{path}'")
            raise typer.Exit(1)

        if _config_path_has_children(normalized_path):
            _config_emit_error(f"Cannot set non-leaf config path '{path}'")
            raise typer.Exit(1)

        config_data, _, raw_config, warnings = _config_load_scope(scope)
        _config_emit_warnings(warnings)
        if is_locked(normalized_path):
            reason = get_lock_reason(normalized_path) or "This setting is locked."
            _config_emit_error(reason)
            raise typer.Exit(1)
        raw_value = value
        choices = get_choices(normalized_path, config_data)
        if choices and raw_value not in choices:
            _config_emit_error(
                f"Invalid value '{raw_value}' for {normalized_path}",
                f"Valid choices: {', '.join(choices)}",
            )
            raise typer.Exit(1)

        parsed_value = _config_parse_value(raw_value)
        expected_type = _config_infer_expected_type(normalized_path, config_data)
        if expected_type is bool and not isinstance(parsed_value, bool):
            _config_emit_error(f"Expected boolean for {normalized_path}, got '{raw_value}'")
            raise typer.Exit(1)
        if expected_type is int and not isinstance(parsed_value, int):
            _config_emit_error(f"Expected integer for {normalized_path}, got '{raw_value}'")
            raise typer.Exit(1)
        if expected_type is float and not isinstance(parsed_value, (int, float)):
            _config_emit_error(f"Expected number for {normalized_path}, got '{raw_value}'")
            raise typer.Exit(1)

        if scope == "server":
            from obra.api import APIClient

            api_client = APIClient.from_config()
            server_config = api_client.update_user_config(
                overrides={normalized_path: parsed_value}
            )
            config_data = server_config.get("resolved", {})
        else:
            _config_set_nested_value(raw_config, normalized_path, parsed_value)
            if normalized_path in ("llm.orchestrator.provider", "llm.implementation.provider"):
                if parsed_value == "openai":
                    llm_section = raw_config.setdefault("llm", {})
                    git_section = llm_section.setdefault("git", {})
                    git_section["skip_check"] = True
            save_config(raw_config)
            config_data = _config_apply_defaults(raw_config)

        if not json_output:
            print_success(f"Set {normalized_path} = {raw_value}")
        if confirm or json_output:
            _config_print_show(config_data, scope, json_output)

    except ConfigurationError as e:
        display_obra_error(e, console)
        raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in config set: {e}")
        raise typer.Exit(1)


@config_app.command(name="reset")
@handle_encoding_errors
def config_reset(
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force delete and regenerate config file (bypasses normal save)",
    ),
) -> None:
    """Reset configuration to defaults.

    Clears all local configuration settings, reverting to defaults.
    Requires confirmation unless --yes is provided.

    Use --force when the config file is corrupted or has deprecated
    structures that prevent normal operation.

    Examples:
        obra config reset
        obra config reset --yes
        obra config reset --force --yes

    Exit Codes:
        0: Success or cancelled
        1: Error
    """
    try:
        from pathlib import Path

        from obra.config import save_config
        from obra.config.loaders import CONFIG_PATH

        if not yes:
            # C14: Check for non-interactive mode before prompting
            if not sys.stdin.isatty():
                console.print(
                    "Non-interactive mode: skipping reset confirmation (defaulting to cancel)"
                )
                console.print("Use --yes flag to skip confirmation.")
                return

            action = "force delete and regenerate" if force else "reset"
            do_reset = typer.confirm(f"{action.capitalize()} configuration to defaults?")
            if not do_reset:
                console.print("Cancelled")
                return

        if force:
            # Force mode: directly delete the file and recreate fresh
            config_path = Path(CONFIG_PATH)
            if config_path.exists():
                config_path.unlink()
                console.print(f"Deleted: {config_path}")

            # Ensure parent directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)

            # Write clean empty config with header comment
            with open(config_path, "w", encoding="utf-8") as f:
                f.write("# Obra client configuration\n")
                f.write("# Use 'obra config' to configure settings\n")
                f.write("{}\n")

            console.print(f"Regenerated: {config_path}")
            print_success("Configuration force-reset to defaults")
        else:
            save_config({})
            print_success("Configuration reset to defaults")

    except ConfigurationError as e:
        display_obra_error(e, console)
        raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in config reset: {e}")
        raise typer.Exit(1)


@config_app.command(name="validate")
@handle_encoding_errors
def config_validate(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    schema: bool = typer.Option(
        False, "--schema", help="Validate config keys and types against schema"
    ),
) -> None:
    """Validate provider CLIs and configuration.

    Checks that provider CLIs are installed and configuration is valid.
    Reports status for each provider and overall configuration health.

    Examples:
        obra config validate
        obra config validate --json
        obra config validate --schema

    Exit Codes:
        0: All checks passed
        1: Issues found or error
    """
    try:
        _run_config_validation(json_output=json_output, include_schema=schema)
    except typer.Exit:
        raise
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in config validate: {e}")
        raise typer.Exit(1)


# =============================================================================
# Documentation Commands
# =============================================================================

# Create docs subcommand group (S3.T3)
docs_app = typer.Typer(
    name="docs",
    help="Access local Obra documentation",
    invoke_without_command=True,
    rich_markup_mode="rich",
)
app.add_typer(docs_app, name="docs", rich_help_panel="User Commands")


def _docs_show_default() -> None:
    """Show default docs output with paths to documentation files."""
    package_root = Path(__file__).parent
    readme_path = package_root / "README.md"
    llm_onboarding_path = package_root / ".obra" / "LLM_ONBOARDING.md"

    console.print()
    console.print("[bold]Obra Documentation (Local)[/bold]", style="cyan")
    console.print()
    console.print("[bold]Package Documentation:[/bold]")
    console.print(f"  README:           {readme_path}")
    console.print()
    console.print("[bold]LLM Operator Guide:[/bold]")
    console.print(f"  LLM_ONBOARDING:   {llm_onboarding_path}")
    console.print("  Quick access:     [cyan]obra docs llm[/cyan]")
    console.print()
    console.print("[dim]Use 'cat <path>' or your text editor to read these files.[/dim]")


def _docs_show_llm() -> None:
    """Show path to LLM_ONBOARDING.md for LLM operators."""
    package_root = Path(__file__).parent
    llm_onboarding_path = package_root / ".obra" / "LLM_ONBOARDING.md"

    console.print()
    console.print("[bold]LLM Operator Guide[/bold]", style="cyan")
    console.print()
    console.print(f"Path: {llm_onboarding_path}")
    console.print()
    console.print("[dim]Use 'cat' or your text editor to read this file.[/dim]")


@docs_app.callback(invoke_without_command=True)
@handle_encoding_errors
def docs_callback(
    ctx: typer.Context,
    # Hidden alias for deprecated flag (S3.T3 - backwards compatibility)
    llm: bool = typer.Option(
        False,
        "--llm",
        hidden=True,
        help="[DEPRECATED] Use 'obra docs llm' instead",
    ),
) -> None:
    """Access local Obra documentation.

    Displays paths to documentation files shipped with the package.

    Subcommands:
        llm  - Show path to LLM operator guide

    Examples:
        obra docs           # Show all doc paths
        obra docs llm       # Show LLM operator guide path
    """
    # Handle deprecated --llm flag
    if llm:
        err_console.print(
            "[yellow]Warning: --llm is deprecated. Use 'obra docs llm' instead.[/yellow]",
            style="yellow",
        )
        _docs_show_llm()
        return

    # If no subcommand was invoked, show default docs output
    if ctx.invoked_subcommand is None:
        _docs_show_default()


@docs_app.command(name="llm")
@handle_encoding_errors
def docs_llm() -> None:
    """Show path to LLM operator guide.

    Displays the path to LLM_ONBOARDING.md, which contains guidance
    for AI assistants using Obra.

    Examples:
        obra docs llm

    Exit Codes:
        0: Always (informational command)
    """
    _docs_show_llm()


@app.command(rich_help_panel="User Commands")
@handle_encoding_errors
def doctor(
    report: bool = typer.Option(
        False,
        "--report",
        help="Submit diagnostic report if checks fail (for troubleshooting)",
    ),
) -> None:
    """Run health checks on your Obra environment.

    Validates:
    - Python version compatibility
    - Authentication status
    - Provider CLI availability (claude, codex, gemini, ollama)
    - API connectivity and server compatibility
    - Working directory write permissions
    - Provider-specific configuration (git for Codex, etc.)

    Run this before 'obra run' to catch configuration issues early.

    Examples:
        $ obra doctor
        $ obra doctor --report   # Auto-submit if issues found
    """
    import platform

    console.print()
    console.print("[bold]Obra Health Check[/bold]", style="cyan")
    console.print()

    # Show client info first (not a check, just informational)
    console.print("[bold]Client Info:[/bold]")
    console.print(f"  Obra: v{__version__}")
    console.print(f"  Platform: {platform.system()} {platform.release()}")
    console.print()

    checks_passed = 0
    total_checks = 6  # Python, Auth, Provider CLIs, API, Working Dir, Provider Config

    # Check 1: Python version
    console.print("[bold]Python Version:[/bold]")
    python_version = sys.version_info
    version_str = f"{python_version.major}.{python_version.minor}.{python_version.micro}"

    if python_version >= (3, 12):
        console.print(f"  [green]✓[/green] Python {version_str} (recommended)")
        checks_passed += 1
    else:
        console.print(f"  [yellow]⚠[/yellow] Python {version_str} (Python 3.12+ recommended)")
        console.print(
            "    [dim]Obra works with Python 3.10+, but 3.12+ is recommended for best performance[/dim]"
        )
        if python_version >= (3, 10):
            checks_passed += 1  # Still passes, just with warning

    console.print()

    # Check 2: Authentication status
    console.print("[bold]Authentication:[/bold]")
    try:
        from obra.auth import get_current_auth

        auth = get_current_auth()

        if auth:
            console.print(f"  [green]✓[/green] Logged in as {auth.email}")
            checks_passed += 1
        else:
            console.print("  [yellow]⚠[/yellow] Not logged in")
            console.print("    [dim]Run 'obra login' to authenticate[/dim]")
    except Exception as e:
        console.print(f"  [red]✗[/red] Authentication check failed: {e}")
        logger.debug(f"Auth check error: {e}", exc_info=True)

    console.print()

    # Check 3: Provider CLIs
    console.print("[bold]Provider CLIs:[/bold]")
    try:
        from obra.config import LLM_PROVIDERS, check_provider_status

        provider_count = 0
        for provider_key in LLM_PROVIDERS:
            status = check_provider_status(provider_key)
            provider_name = LLM_PROVIDERS[provider_key].get("name", provider_key)

            if status.installed:
                console.print(f"  [green]✓[/green] {provider_name} ({status.cli_command})")
                provider_count += 1
            else:
                console.print(f"  [red]✗[/red] {provider_name} ({status.cli_command}) - not found")

        # At least one provider installed counts as passing
        if provider_count > 0:
            checks_passed += 1
    except Exception as e:
        console.print(f"  [red]✗[/red] Provider check failed: {e}")
        logger.debug(f"Provider check error: {e}", exc_info=True)

    console.print()

    # Check 4: API Connectivity and Server Compatibility
    console.print("[bold]API Connectivity:[/bold]")
    try:
        from obra.api import APIClient
        from obra.config import get_api_base_url

        # Create unauthenticated client for version check
        client = APIClient(base_url=get_api_base_url())

        try:
            server_info = client.get_version()
            server_version = server_info.get("version", "N/A")
            api_version = server_info.get("api_version", "N/A")
            compatible = server_info.get("compatible", True)
            min_client = server_info.get("min_client_version", "0.0.0")

            console.print("  [green]✓[/green] Obra API reachable")
            console.print(f"    [dim]Server: v{server_version} (API {api_version})[/dim]")

            if compatible:
                console.print("    [dim]Client compatible with server[/dim]")
                checks_passed += 1
            else:
                console.print(
                    f"    [yellow]⚠ Client update required (minimum: {min_client})[/yellow]"
                )
                console.print("    [dim]Run: pip install --upgrade obra[/dim]")
                # Still count as passed since API is reachable
                checks_passed += 1

        except APIError as e:
            if e.status_code == 0:
                console.print("  [red]✗[/red] Cannot reach Obra API")
                console.print("    [dim]Check your network connection[/dim]")
            else:
                console.print(f"  [yellow]⚠[/yellow] API returned error: {e}")
            logger.debug(f"API error in doctor: {e}", exc_info=True)
        except Exception as e:
            console.print("  [red]✗[/red] Cannot reach Obra API")
            console.print(f"    [dim]Error: {e}[/dim]")
            logger.debug(f"Connection error in doctor: {e}", exc_info=True)

    except Exception as e:
        console.print(f"  [red]✗[/red] API check failed: {e}")
        logger.debug(f"API check error: {e}", exc_info=True)

    console.print()

    # Check 5: Working Directory
    console.print("[bold]Working Directory:[/bold]")
    try:
        cwd = Path.cwd()
        console.print(f"  Path: {cwd}")

        # Test if we can write to the directory
        test_file = cwd / ".obra_doctor_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
            console.print("  [green]✓[/green] Directory is writable")
            checks_passed += 1
        except PermissionError:
            console.print("  [red]✗[/red] Directory is not writable")
            console.print("    [dim]Obra needs write access to create files[/dim]")
        except OSError as e:
            console.print(f"  [yellow]⚠[/yellow] Write test failed: {e}")
            # Still pass if it's not a permission issue (e.g., disk full is recoverable)
            checks_passed += 1

    except Exception as e:
        console.print(f"  [red]✗[/red] Working directory check failed: {e}")
        logger.debug(f"Working directory check error: {e}", exc_info=True)

    console.print()

    # Check 6: Provider Configuration
    # Validates provider-specific requirements before execution
    console.print("[bold]Provider Configuration:[/bold]")
    try:
        from obra.config.loaders import load_config_with_warnings

        config, warnings, _ = load_config_with_warnings()
        llm_config = config.get("llm", {})
        selected_provider = os.environ.get("OBRA_PROVIDER") or llm_config.get(
            "provider", DEFAULT_PROVIDER
        )

        schema = _config_schema()
        schema_warnings = _config_schema_version_warnings(config, schema)
        if warnings or schema_warnings:
            console.print("  [yellow]⚠[/yellow] Config warnings detected")
            for warning in warnings + schema_warnings:
                console.print(f"    [dim]{warning}[/dim]")

        provider_issues = []
        provider_warnings = []

        # Codex-specific checks
        if selected_provider == "openai":
            # Check 6a: Git repository status for Codex
            cwd = Path.cwd()
            is_git_repo = (cwd / ".git").exists() or any(
                (parent / ".git").exists() for parent in cwd.parents
            )

            # Check config for auto_init_git and skip_git_check
            codex_config = llm_config.get("codex", {})
            auto_init_git = codex_config.get("auto_init_git", False)
            skip_git_check = codex_config.get("skip_git_check", False)

            if is_git_repo:
                console.print("  [green]✓[/green] Git repository detected (Codex requirement)")
            elif auto_init_git:
                console.print(
                    "  [green]✓[/green] Git auto-init enabled (llm.codex.auto_init_git: true)"
                )
            elif skip_git_check:
                console.print(
                    "  [yellow]⚠[/yellow] Git check disabled (llm.codex.skip_git_check: true)"
                )
                provider_warnings.append("Git safety features bypassed")
            else:
                console.print("  [red]✗[/red] Not in a git repository")
                console.print(
                    "    [dim]Codex requires git. Options:[/dim]"
                )
                console.print("    [dim]  1. Run 'git init' in your project[/dim]")
                console.print(
                    "    [dim]  2. Set llm.codex.auto_init_git: true in config[/dim]"
                )
                console.print(
                    "    [dim]  3. Set llm.codex.skip_git_check: true to bypass[/dim]"
                )
                provider_issues.append("Git repository required for Codex")

        # Gemini-specific checks
        elif selected_provider == "google":
            console.print("  [green]✓[/green] Gemini provider configured")
            console.print("    [dim]Sandbox mode: permissive (for execution)[/dim]")

        # Anthropic/Claude-specific checks
        elif selected_provider == "anthropic":
            console.print("  [green]✓[/green] Claude provider configured")

        # Ollama-specific checks
        elif selected_provider == "ollama":
            console.print("  [green]✓[/green] Ollama provider configured")
            console.print("    [dim]Ensure Ollama server is running locally[/dim]")

        else:
            console.print(f"  [yellow]⚠[/yellow] Unknown provider: {selected_provider}")
            provider_warnings.append(f"Unrecognized provider: {selected_provider}")

        # Determine pass/fail for this check
        if not provider_issues:
            if provider_warnings:
                console.print(
                    f"  [yellow]⚠[/yellow] {len(provider_warnings)} warning(s) - check config"
                )
            checks_passed += 1
        else:
            console.print(f"  [red]✗[/red] {len(provider_issues)} issue(s) need resolution")

    except Exception as e:
        console.print(f"  [red]✗[/red] Provider config check failed: {e}")
        logger.debug(f"Provider config check error: {e}", exc_info=True)

    console.print()

    # FEAT-MODEL-QUALITY-001 S3.T1: Show LLM Config with quality tier
    console.print("[bold]LLM Config:[/bold]")
    try:
        llm_provider = os.environ.get("OBRA_PROVIDER", DEFAULT_PROVIDER)
        llm_model = os.environ.get("OBRA_MODEL", DEFAULT_MODEL)
        quality_tier = resolve_quality_tier(llm_provider, llm_model)
        tier_suffix = " (auto-permissive)" if quality_tier == "fast" else ""
        console.print(f"  Provider: {llm_provider}")
        console.print(f"  Model: {llm_model}")
        console.print(f"  Quality tier: {quality_tier}{tier_suffix}")
    except Exception as e:
        console.print(f"  [yellow]⚠[/yellow] Could not resolve LLM config: {e}")
        logger.debug(f"LLM config resolution error: {e}", exc_info=True)

    console.print()

    # Summary - Report Card Style
    console.print("[bold]Overall Health:[/bold]")
    percentage = int((checks_passed / total_checks) * 100)

    if percentage == 100:
        status_icon = "[green]✓[/green]"
        status_text = "[green]Excellent - All checks passed![/green]"
    elif percentage >= 80:
        status_icon = "[green]✓[/green]"
        status_text = "[green]Good - System is functional[/green]"
    elif percentage >= 60:
        status_icon = "[yellow]⚠[/yellow]"
        status_text = "[yellow]Fair - Some issues detected[/yellow]"
    else:
        status_icon = "[red]✗[/red]"
        status_text = "[red]Poor - Multiple issues need attention[/red]"

    console.print(f"  {status_icon} {checks_passed}/{total_checks} checks passed ({percentage}%)")
    console.print(f"  {status_text}")
    console.print()

    # Offer to report issues if checks failed
    if percentage < 100:
        failed_checks = total_checks - checks_passed
        if report:
            # Auto-submit diagnostic report
            _offer_bug_report(
                context="doctor diagnostics",
                command_used="obra doctor --report",
                failure_reason=f"{failed_checks} health check(s) failed ({percentage}%)",
                auto_report=True,
            )
        else:
            console.print("[dim]Having trouble? Run 'obra doctor --report' to submit diagnostics[/dim]")
            console.print()


# =============================================================================
# Plan Management Commands
# =============================================================================


# Create plans subcommand group
plans_app = typer.Typer(
    name="plans",
    help="Manage uploaded plan files",
    no_args_is_help=True,
)
app.add_typer(plans_app, name="plans")


@plans_app.command("list")
@handle_encoding_errors
def plans_list(
    limit: int = typer.Option(
        50,
        "--limit",
        "-n",
        help="Maximum number of plans to list (max: 100)",
    ),
) -> None:
    """List uploaded plan files.

    Displays all plans uploaded by the current user, ordered by
    creation time (most recent first).

    Examples:
        $ obra plans list
        $ obra plans list --limit 10
    """
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()

        # Get plans from server
        client = APIClient.from_config()
        plans = client.list_plans(limit=limit)

        console.print()
        if not plans:
            print_info("No plans uploaded")
            console.print("\nUpload a plan with: [cyan]obra plans upload path/to/plan.yaml[/cyan]")
            return

        console.print(f"[bold]Uploaded Plans[/bold] ({len(plans)} total)", style="cyan")
        console.print()

        table = Table()
        table.add_column("Plan ID", style="cyan")
        table.add_column("Name", style="bold")
        table.add_column("Stories", justify="right")
        table.add_column("Uploaded", style="dim")

        for plan in plans:
            plan_id_short = plan.get("plan_id", "")[:8] + "..."
            name = plan.get("name", "N/A")
            story_count = str(plan.get("story_count", 0))
            created_at = plan.get("created_at", "N/A")

            # Format timestamp if it's ISO format
            if "T" in created_at:
                from datetime import datetime

                try:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    created_at = dt.strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError):
                    # Invalid timestamp format, use as-is
                    pass

            table.add_row(plan_id_short, name, story_count, created_at)

        console.print(table)
        console.print()
        console.print('[dim]Use with:[/dim] [cyan]obra run --plan-id <plan_id> "objective"[/cyan]')

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in plans list command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in plans list command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in plans list command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in plans list command: {e}")
        raise typer.Exit(1)


@plans_app.command("show")
@handle_encoding_errors
def plans_show(
    plan_id: str = typer.Argument(..., help="Plan ID to display"),
) -> None:
    """Display details of an uploaded plan file.

    Shows complete information about a plan including:
    - Plan metadata (name, work_id, description)
    - Story list with titles and status
    - Task count per story

    Examples:
        $ obra plans show abc123
        $ obra plans show abc12345-6789-...
    """
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()

        # Get plan details from server
        client = APIClient.from_config()
        plan = client.get_plan(plan_id)

        if not plan:
            print_error(f"Plan not found: {plan_id}")
            raise typer.Exit(1)

        console.print()
        console.print("[bold cyan]Plan Details[/bold cyan]")
        console.print("=" * 60)
        console.print()

        # Basic info
        console.print(f"[bold]Plan ID:[/bold]   {plan.get('plan_id', 'N/A')}")
        console.print(f"[bold]Name:[/bold]      {plan.get('name', 'N/A')}")
        console.print(f"[bold]Work ID:[/bold]   {plan.get('work_id', 'N/A')}")

        # Format and display creation time
        created_at = plan.get("created_at", "N/A")
        if "T" in str(created_at):
            from datetime import datetime

            try:
                dt = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
                created_at = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
            except (ValueError, TypeError):
                pass
        console.print(f"[bold]Uploaded:[/bold]  {created_at}")

        # Description if present
        if plan.get("description"):
            console.print("[bold]Description:[/bold]")
            console.print(f"  {plan.get('description')}")

        # Stories
        stories = plan.get("stories", [])
        if stories:
            console.print()
            console.print(f"[bold]Stories[/bold] ({len(stories)} total)")
            console.print("-" * 40)

            story_table = Table(show_header=True, header_style="bold")
            story_table.add_column("ID", style="cyan")
            story_table.add_column("Title")
            story_table.add_column("Status", style="dim")
            story_table.add_column("Tasks", justify="right")

            for story in stories:
                story_id = story.get("id", "?")
                title = story.get("title", "Untitled")
                status = story.get("status", "pending")
                task_count = len(story.get("tasks", []))
                story_table.add_row(story_id, title, status, str(task_count))

            console.print(story_table)

        console.print()
        console.print(
            f'[dim]Use with:[/dim] [cyan]obra --plan-id {plan_id[:8]}... "your objective"[/cyan]'
        )

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in plans show command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in plans show command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in plans show command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in plans show command: {e}")
        raise typer.Exit(1)


@plans_app.command("delete")
@handle_encoding_errors
def plans_delete(
    plan_id: str = typer.Argument(..., help="Plan ID to delete"),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Skip confirmation prompt",
    ),
) -> None:
    """Delete an uploaded plan file.

    Permanently removes the plan from the server. This cannot be undone.
    Existing sessions using this plan are not affected.

    Examples:
        $ obra plans delete abc123-uuid
        $ obra plans delete abc123-uuid --force
    """
    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()

        # Get plan details first
        client = APIClient.from_config()

        console.print()
        console.print("[dim]Fetching plan details...[/dim]")

        try:
            plan = client.get_plan(plan_id)
            plan_name = plan.get("name", "Unknown")
            story_count = plan.get("story_count", 0)

            console.print()
            console.print("[bold]Plan Details[/bold]", style="yellow")
            console.print(f"ID: {plan_id}")
            console.print(f"Name: {plan_name}")
            console.print(f"Stories: {story_count}")
            console.print()

        except (APIError, ObraError) as e:
            # Plan not found or error fetching - proceed with deletion anyway
            logger.warning(f"Could not fetch plan details: {e}")
            plan_name = "Unknown"

        # Confirm deletion
        if not force:
            # C14: Check for non-interactive mode before prompting
            if not sys.stdin.isatty():
                # Non-interactive mode: default to not deleting (safe default)
                console.print(
                    "Non-interactive mode: skipping deletion confirmation (defaulting to cancel)"
                )
                console.print("Use --force to delete without confirmation")
                return

            confirm = typer.confirm(
                f"Are you sure you want to delete plan '{plan_name}'?",
                default=False,
            )
            if not confirm:
                console.print("Cancelled")
                return

        # Delete plan
        console.print("[dim]Deleting plan...[/dim]")
        result = client.delete_plan(plan_id)

        if result.get("success"):
            console.print()
            print_success(f"Plan deleted: {plan_name}")
        else:
            print_error("Failed to delete plan")
            raise typer.Exit(1)

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in plans delete command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in plans delete command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in plans delete command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in plans delete command: {e}")
        raise typer.Exit(1)


@plans_app.command("upload")
@handle_encoding_errors
def plans_upload(
    file_path: Path = typer.Argument(
        ..., help="Path to MACHINE_PLAN file (JSON or YAML) to upload"
    ),
    validate_only: bool = typer.Option(
        False,
        "--validate-only",
        help="Only validate the plan file without uploading",
    ),
) -> None:
    """Upload a MACHINE_PLAN file (JSON or YAML) to Obra SaaS.

    Validates and uploads a plan file to Firestore for later use.
    After upload, use the returned plan_id with 'obra run --plan-id'.

    Examples:
        $ obra plans upload docs/development/MY_PLAN.yaml
        $ obra plans upload --validate-only plan.yaml

    Exit Codes:
        0: Upload successful or validation passed
        1: Upload failed or validation failed
    """
    try:
        command = UploadPlanCommand()
        exit_code = command.execute(str(file_path), validate_only)

        if exit_code != 0:
            raise typer.Exit(exit_code)

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in plans upload command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in plans upload command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in plans upload command: {e}", exc_info=True)
        raise typer.Exit(1)
    except OSError as e:
        print_error(f"Failed to read plan file: {e}")
        logger.error(f"File I/O error in plans upload command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in plans upload command: {e}")
        raise typer.Exit(1)


# NOTE: 'plans validate' command removed - use 'dobra plan validate' instead
# Plan validation is a local operation, not a SaaS operation.
# See CHORE-DOBRA-CLI-001 for migration details.


# =============================================================================
# Sync Commands (Local Observability)
# =============================================================================

sync_app = typer.Typer(
    name="sync",
    help="Sync session data to local files for observability",
    no_args_is_help=True,
)
app.add_typer(sync_app, name="sync", rich_help_panel="User Commands")


@sync_app.command("plan")
@handle_encoding_errors
@require_terms_accepted
def sync_plan(
    session_id: str | None = typer.Argument(
        None,
        help="Session ID to sync (defaults to most recent)",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory (defaults to .obra/)",
    ),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        max=3,
        help="Verbosity level (0-3, use -v/-vv/-vvv)",
    ),
) -> None:
    """Sync session plan to local YAML file.

    Downloads the execution plan for a session and saves it to
    .obra/plan.yaml for local observability. The YAML file includes:
    - Session metadata (objective, status, progress)
    - Plan items with status (pending, in_progress, completed, failed)
    - Acceptance criteria for each item

    Examples:
        $ obra sync plan
        $ obra sync plan abc123
        $ obra sync plan --output ./my-project/.obra/
    """
    from datetime import datetime

    setup_logging(verbose)

    try:
        from obra.api import APIClient
        from obra.auth import ensure_valid_token, get_current_auth

        # Ensure authenticated
        auth = get_current_auth()
        if not auth:
            print_error("Not logged in")
            console.print("\nRun 'obra login' to authenticate.")
            raise typer.Exit(1)

        ensure_valid_token()

        # Get API client
        client = APIClient.from_config()

        # Resolve session ID
        if session_id:
            target_session_id = session_id
        else:
            # Get most recent session
            sessions = client.list_sessions(limit=1)
            if not sessions:
                print_info("No sessions found")
                console.print("\nRun 'obra run \"objective\"' to start a new session.")
                return
            target_session_id = sessions[0].get("session_id", "")

        console.print()
        console.print("[dim]Fetching plan data...[/dim]")

        # Get session info and plan
        session = client.get_session(target_session_id)
        plan_data = client.get_session_plan(target_session_id)

        # Prepare YAML output structure
        plan_items = plan_data.get("plan_items", [])
        total_count = plan_data.get("total_count", len(plan_items))
        completed_count = plan_data.get("completed_count", 0)

        meta: dict[str, Any] = {
            "synced_at": datetime.now(UTC).isoformat(),
            "session_id": session.get("session_id", target_session_id),
            "objective": session.get("objective", "N/A"),
            "status": session.get("status", "N/A"),
            "phase": session.get("current_phase", "N/A"),
            "iteration": session.get("iteration", 0),
        }
        progress: dict[str, Any] = {
            "total": total_count,
            "completed": completed_count,
            "percentage": round(completed_count / total_count * 100) if total_count > 0 else 0,
        }
        items: list[dict[str, Any]] = []

        # Format plan items
        for item in plan_items:
            formatted_item = {
                "id": item.get("item_id", item.get("id", "")),
                "order": item.get("order", 0),
                "title": item.get("title", "Untitled"),
                "status": item.get("status", "pending"),
            }

            # Add optional fields if present
            if item.get("acceptance_criteria"):
                formatted_item["acceptance_criteria"] = item["acceptance_criteria"]
            if item.get("started_at"):
                formatted_item["started_at"] = item["started_at"]
            if item.get("completed_at"):
                formatted_item["completed_at"] = item["completed_at"]

            items.append(formatted_item)

        yaml_content: dict[str, Any] = {
            "_meta": meta,
            "progress": progress,
            "items": items,
        }

        # Determine output path
        if output_dir:
            obra_dir = output_dir
        else:
            obra_dir = Path.cwd() / ".obra"

        obra_dir.mkdir(parents=True, exist_ok=True)
        output_path = obra_dir / "plan.yaml"

        # Write YAML file with human-readable formatting
        with open(output_path, "w", encoding="utf-8") as f:
            # Write header comment
            f.write("# Obra Session Plan\n")
            f.write(f"# Synced: {meta['synced_at']}\n")
            f.write(f"# Session: {meta['session_id'][:8]}...\n")
            f.write("#\n")
            f.write("# Status indicators:\n")
            f.write("#   pending     - Not yet started\n")
            f.write("#   in_progress - Currently executing\n")
            f.write("#   completed   - Successfully finished\n")
            f.write("#   failed      - Execution failed\n")
            f.write("\n")

            yaml.safe_dump(
                yaml_content,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
                width=100,
            )

        console.print()
        print_success(f"Plan synced to {output_path}")
        console.print()
        console.print(f"[bold]Session[/bold]: {meta['session_id'][:8]}...")
        console.print(f"[bold]Objective[/bold]: {meta['objective']}")
        console.print(
            f"[bold]Progress[/bold]: {completed_count}/{total_count} items "
            f"({progress['percentage']}%)"
        )

        if verbose > 0:
            console.print()
            console.print("[bold]Items[/bold]:")
            for item in items:
                status = item["status"]
                if status == "completed":
                    status_icon = "[green]✓[/green]"
                elif status == "in_progress":
                    status_icon = "[yellow]⏳[/yellow]"
                elif status == "failed":
                    status_icon = "[red]✗[/red]"
                else:
                    status_icon = "[dim]○[/dim]"
                console.print(f"  {status_icon} {item['title']}")

    except APIError as e:
        display_obra_error(e, console)
        logger.error(f"API error in sync plan command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ConfigurationError as e:
        display_obra_error(e, console)
        logger.error(f"Configuration error in sync plan command: {e}", exc_info=True)
        raise typer.Exit(1)
    except ObraError as e:
        display_obra_error(e, console)
        logger.error(f"Obra error in sync plan command: {e}", exc_info=True)
        raise typer.Exit(1)
    except OSError as e:
        print_error(f"Failed to write plan file: {e}")
        logger.error(f"File I/O error in sync plan command: {e}", exc_info=True)
        raise typer.Exit(1)
    except Exception as e:
        display_error(e, console)
        logger.exception(f"Unexpected error in sync plan command: {e}")
        raise typer.Exit(1)


# =============================================================================
# Feedback Commands (Beta Tester Feedback System)
# =============================================================================

feedback_app = typer.Typer(
    name="feedback",
    help="Submit bug reports, feature requests, and feedback",
    invoke_without_command=True,
    rich_markup_mode="rich",
)
app.add_typer(feedback_app, name="feedback", rich_help_panel="Feedback & Bug Reporting")


# =============================================================================
# Bug Shortcut Command (Top-level for discoverability)
# =============================================================================


@app.command(rich_help_panel="Feedback & Bug Reporting")
@handle_encoding_errors
def bug(
    summary: str = typer.Argument(..., help="One-line bug description"),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        help="Non-interactive mode (no prompts, for orchestrator use)",
    ),
    format_output: str = typer.Option(
        "text",
        "--format",
        "-f",
        help="Output format: text, json",
    ),
    severity: str = typer.Option(
        "medium",
        "--severity",
        "-s",
        help="Bug severity: critical, high, medium, low",
    ),
    error: str = typer.Option(
        "",
        "--error",
        "-e",
        help="Error message if any",
    ),
    privacy: str = typer.Option(
        "standard",
        "--privacy",
        "-p",
        help="Privacy level: full, standard, minimal",
    ),
) -> None:
    """Quick bug report shortcut.

    Shortcut for `obra feedback bug`. For more options, use the full command.

    Examples:
        obra bug "App crashes on startup"
        obra bug "Orchestrator hangs" --severity high
        obra bug "Error in derive" --error "ValueError: invalid"

    For more options (attachments, session ID, etc.):
        obra feedback bug --help
    """
    from obra.feedback import FeedbackCollector

    try:
        privacy_level = _get_privacy_level(privacy)
        collector = FeedbackCollector(privacy_level=privacy_level)

        # Auto-detect recent session
        session_id = _get_recent_session_id()
        if session_id and not non_interactive:
            console.print(f"[dim]Auto-detected session: {session_id}[/dim]")

        report = collector.create_bug_report(
            summary=summary,
            severity=_get_severity(severity),
            error_message=error,
            session_id=session_id,
        )

        # Check telemetry consent before submission (S4.T2)
        _check_telemetry_consent(non_interactive=non_interactive)

        result = collector.submit(report)

        if format_output == "json":
            import json
            print(json.dumps(result, indent=2, default=str))
            raise typer.Exit(0 if result.get("success") else 1)
        else:
            _display_submission_result(result, console)
            raise typer.Exit(0 if result.get("success") else 1)

    except typer.Exit:
        raise
    except Exception as e:
        if format_output == "json":
            import json
            print(json.dumps({"success": False, "error": str(e)}, indent=2))
        else:
            print_error(f"Failed to submit bug report: {e}")
            logger.exception("Bug report submission failed")
        raise typer.Exit(1)


def _get_privacy_level(privacy: str) -> "PrivacyLevel":
    """Convert string privacy level to enum."""
    from obra.feedback import PrivacyLevel

    mapping = {
        "full": PrivacyLevel.FULL,
        "standard": PrivacyLevel.STANDARD,
        "minimal": PrivacyLevel.MINIMAL,
    }
    return mapping.get(privacy.lower(), PrivacyLevel.STANDARD)


def _get_severity(severity: str) -> "Severity":
    """Convert string severity to enum."""
    from obra.feedback import Severity

    mapping = {
        "critical": Severity.CRITICAL,
        "high": Severity.HIGH,
        "medium": Severity.MEDIUM,
        "low": Severity.LOW,
    }
    return mapping.get(severity.lower(), Severity.MEDIUM)


def _get_recent_session_id() -> str | None:
    """Get the most recent session ID from session logs.

    Returns:
        Session ID string or None if no recent session found.
    """
    try:
        from obra.feedback.session_logger import SessionConsoleLogger
        session_id, _ = SessionConsoleLogger.get_recent_session_log()
        return cast(str | None, session_id)
    except Exception:
        return None


def _offer_bug_report(
    error: Exception | None = None,
    context: str = "operation",
    session_id: str | None = None,
    command_used: str | None = None,
    objective: str | None = None,
    auto_report: bool = False,
    failure_reason: str | None = None,
) -> None:
    """Offer to file a bug report after a failure.

    Prompts user to submit feedback with pre-filled error context.
    Supports both hard failures (exceptions) and soft failures (e.g., 0 items completed).

    Args:
        error: The exception that occurred (optional for soft failures)
        context: Description of what was happening (e.g., "orchestration", "derive")
        session_id: Session ID if known
        command_used: The command that was run
        objective: The user's objective (what they were trying to accomplish)
        auto_report: If True, skip prompt and submit automatically (for CI/CD)
        failure_reason: Human-readable failure reason (for soft failures without exception)
    """
    import traceback

    # Determine summary and error details based on failure type
    if error:
        error_type = type(error).__name__
        error_message = str(error)
        error_tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        summary = f"{context.title()} failed: {error_type}"
        error_display = f"{error_type}: {error_message[:80]}..."
    else:
        error_type = "SoftFailure"
        error_message = failure_reason or "Operation did not complete successfully"
        error_tb = ""
        summary = f"{context.title()} failed: {failure_reason or 'no items completed'}"
        error_display = failure_reason or "No items completed"

    # Build description with objective if available
    description_parts = [f"Automatic bug report from {context} failure."]
    if objective:
        # Truncate very long objectives for the description
        obj_preview = objective[:500] + "..." if len(objective) > 500 else objective
        description_parts.append(f"Objective: {obj_preview}")
    description = "\n\n".join(description_parts)

    session_id = session_id or _get_recent_session_id()

    # Auto-report mode: skip prompts entirely
    if auto_report:
        try:
            from obra.feedback import FeedbackCollector, PrivacyLevel, Severity

            collector = FeedbackCollector(privacy_level=PrivacyLevel.FULL)
            report = collector.create_bug_report(
                summary=summary,
                severity=Severity.HIGH,
                description=description,
                error_message=error_message,
                error_traceback=error_tb,
                command_used=command_used or "",
                objective=objective or "",
                session_id=session_id,
            )
            result = collector.submit(report)
            console.print()

            # Build captured data summary
            captured_parts = []
            if report.observability_events:
                captured_parts.append(f"{len(report.observability_events)} events")
            if report.console_log:
                captured_parts.append(f"{len(report.console_log.split(chr(10)))} lines log")
            if objective:
                captured_parts.append("objective")
            captured_str = f" ({', '.join(captured_parts)})" if captured_parts else ""

            if result.get("success"):
                console.print(f"[dim]Bug report auto-submitted: {result.get('report_id', 'N/A')}{captured_str}[/dim]")
            else:
                console.print(f"[dim]Bug report saved locally{captured_str} (will sync later)[/dim]")
        except Exception as e:
            console.print(f"[dim]Auto-report failed: {e}[/dim]")
        return

    # Interactive mode: prompt user
    console.print()
    console.print("[bold yellow]Would you like to report this issue?[/bold yellow]")
    console.print("[dim]Your report helps us fix bugs faster.[/dim]")
    console.print()

    console.print("[dim]The report will include:[/dim]")
    console.print(f"  [dim]• Error: {error_display}[/dim]")
    if objective:
        obj_short = objective[:60] + "..." if len(objective) > 60 else objective
        console.print(f"  [dim]• Objective: {obj_short}[/dim]")
    if session_id:
        console.print("  [dim]• Session logs and events[/dim]")
    console.print("  [dim]• System info (OS, Obra version)[/dim]")
    console.print()

    try:
        response = console.input("[Y] Report  [n] Skip  [p] Preview > ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        console.print("\n[dim]Skipped.[/dim]")
        return

    if response in ("", "y", "yes"):
        # Submit the bug report
        try:
            from obra.feedback import FeedbackCollector, PrivacyLevel, Severity

            collector = FeedbackCollector(privacy_level=PrivacyLevel.FULL)
            report = collector.create_bug_report(
                summary=summary,
                severity=Severity.HIGH,
                description=description,
                error_message=error_message,
                error_traceback=error_tb,
                command_used=command_used or "",
                objective=objective or "",
                session_id=session_id,
            )

            result = collector.submit(report)
            _display_submission_result(
                result,
                console,
                events_count=len(report.observability_events),
                console_lines=len(report.console_log.split("\n")) if report.console_log else 0,
                has_objective=bool(objective),
            )

        except Exception as submit_error:
            print_error(f"Failed to submit report: {submit_error}")
            console.print("[dim]You can manually report at: obra feedback bug 'description'[/dim]")

    elif response in ("p", "preview"):
        # Show preview then ask again
        try:
            import json

            from obra.feedback import FeedbackCollector, PrivacyLevel, Severity

            collector = FeedbackCollector(privacy_level=PrivacyLevel.FULL)
            report = collector.create_bug_report(
                summary=summary,
                severity=Severity.HIGH,
                description=description,
                error_message=error_message,
                error_traceback=error_tb,
                command_used=command_used or "",
                objective=objective or "",
                session_id=session_id,
            )

            preview_data = collector.preview_submission(report)
            console.print()
            console.print("[bold cyan]Preview - Data that will be submitted:[/bold cyan]")
            console.print(json.dumps(preview_data, indent=2, default=str))
            console.print()

            try:
                confirm = console.input("[Y] Submit  [n] Cancel > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[dim]Cancelled.[/dim]")
                return

            if confirm in ("", "y", "yes"):
                result = collector.submit(report)
                _display_submission_result(
                    result,
                    console,
                    events_count=len(report.observability_events),
                    console_lines=len(report.console_log.split("\n")) if report.console_log else 0,
                    has_objective=bool(objective),
                )
            else:
                console.print("[dim]Report saved as draft. Submit later with: obra feedback drafts[/dim]")

        except Exception as preview_error:
            print_error(f"Failed to generate preview: {preview_error}")
    else:
        console.print("[dim]Skipped. Report later with: obra feedback bug 'description'[/dim]")


def _display_submission_result(
    result: dict,
    console,
    events_count: int = 0,
    console_lines: int = 0,
    has_system_info: bool = True,
    has_objective: bool = False,
) -> None:
    """Display feedback submission result with details of captured data.

    Args:
        result: Submission result dict from collector.submit()
        console: Rich console for output
        events_count: Number of observability events included
        console_lines: Number of console log lines included
        has_system_info: Whether system info was included
        has_objective: Whether objective was included
    """
    if result.get("success"):
        console.print()
        print_success("Feedback submitted successfully!")
        console.print(f"[dim]Report ID: {result.get('report_id', 'N/A')}[/dim]")

        # Show what was captured for confidence
        captured_parts = []
        if events_count > 0:
            captured_parts.append(f"{events_count} events")
        if console_lines > 0:
            captured_parts.append(f"{console_lines} lines console log")
        if has_objective:
            captured_parts.append("objective")
        if has_system_info:
            captured_parts.append("system info")

        if captured_parts:
            console.print(f"[dim]Included: {', '.join(captured_parts)}[/dim]")

        if result.get("stored_locally"):
            console.print("[yellow]Note: Stored locally (will sync when online)[/yellow]")
    else:
        print_error(f"Submission failed: {result.get('message', 'Unknown error')}")


@feedback_app.callback(invoke_without_command=True)
@handle_encoding_errors
def feedback_callback(
    ctx: typer.Context,
) -> None:
    """Submit bug reports, feature requests, and feedback.

    Subcommands:
        bug      - Submit a bug report
        feature  - Request a new feature
        comment  - Submit general feedback
        drafts   - Manage saved drafts

    Privacy Levels:
        full     - Maximum data for debugging (prompts, logs, system info)
        standard - Balanced data (truncated prompts, errors, basic system info)
        minimal  - Essential data only (summary, category, Obra version)

    Examples:
        obra feedback bug "App crashes on startup"
        obra feedback feature "Add dark mode"
        obra feedback comment "Great documentation!"
    """
    # If no subcommand was invoked, show help
    if ctx.invoked_subcommand is None:
        console.print()
        console.print("[bold cyan]Obra Feedback System[/bold cyan]")
        console.print()
        console.print("Submit bug reports, feature requests, and feedback to help improve Obra.")
        console.print()
        console.print("[bold]Commands:[/bold]")
        console.print("  obra feedback bug 'App crashes'     # Bug report")
        console.print("  obra feedback feature 'Add X'       # Feature request")
        console.print("  obra feedback comment 'Nice work!'  # General comment")
        console.print()
        console.print("[dim]Run 'obra feedback --help' for more options.[/dim]")


@feedback_app.command("bug")
@handle_encoding_errors
def feedback_bug(
    summary: str = typer.Argument(..., help="One-line bug summary"),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        help="Non-interactive mode (no prompts, for orchestrator use)",
    ),
    format_output: str = typer.Option(
        "text",
        "--format",
        "-f",
        help="Output format: text, json",
    ),
    severity: str = typer.Option(
        "medium",
        "--severity",
        "-s",
        help="Bug severity: critical, high, medium, low",
    ),
    description: str = typer.Option(
        "",
        "--description",
        "-d",
        help="Detailed description",
    ),
    steps: str = typer.Option(
        "",
        "--steps",
        help="Steps to reproduce (use \\n for newlines)",
    ),
    expected: str = typer.Option(
        "",
        "--expected",
        help="Expected behavior",
    ),
    actual: str = typer.Option(
        "",
        "--actual",
        help="Actual behavior",
    ),
    error: str = typer.Option(
        "",
        "--error",
        "-e",
        help="Error message if any",
    ),
    command: str = typer.Option(
        "",
        "--command",
        help="The obra command that triggered the bug",
    ),
    session_id: str = typer.Option(
        None,
        "--session",
        help="Session ID for context (auto-detected if recent)",
    ),
    workaround: str = typer.Option(
        "",
        "--workaround",
        "-w",
        help="Known workaround if any",
    ),
    attach: list[Path] = typer.Option(
        None,
        "--attach",
        "-a",
        help="Attach files (logs, screenshots)",
    ),
    privacy: str = typer.Option(
        "standard",
        "--privacy",
        "-p",
        help="Privacy level: full, standard, minimal",
    ),
    preview: bool = typer.Option(
        False,
        "--preview",
        help="Preview what will be sent without submitting",
    ),
) -> None:
    """Submit a bug report.

    Include as much detail as possible to help diagnose the issue.
    System information and recent logs are automatically collected
    based on your chosen privacy level.

    Examples:
        obra feedback bug "App crashes on startup"
        obra feedback bug "Orchestrator hangs" --severity high
        obra feedback bug "Error in derive" --error "ValueError: invalid input"
        obra feedback bug "Crash with spaces" --session abc-123 --attach session.log

    Privacy Levels:
        full     - Include full prompts, logs, and system details
        standard - Include truncated prompts, errors, basic info (default)
        minimal  - Summary, severity, and Obra version only
    """
    from obra.feedback import FeedbackCollector

    try:
        privacy_level = _get_privacy_level(privacy)
        collector = FeedbackCollector(privacy_level=privacy_level)

        # Convert attachment paths to strings
        attachment_paths = [str(p) for p in attach] if attach else []

        # Auto-detect recent session if not provided
        effective_session_id = session_id or _get_recent_session_id()
        if effective_session_id and not session_id and not non_interactive:
            console.print(f"[dim]Auto-detected session: {effective_session_id}[/dim]")

        report = collector.create_bug_report(
            summary=summary,
            severity=_get_severity(severity),
            description=description,
            steps_to_reproduce=steps.replace("\\n", "\n") if steps else "",
            expected_behavior=expected,
            actual_behavior=actual,
            error_message=error,
            command_used=command,
            session_id=effective_session_id,
            workaround=workaround,
            attachment_paths=attachment_paths,
        )

        if preview:
            import json

            if format_output == "json":
                preview_data = collector.preview_submission(report)
                print(json.dumps(preview_data, indent=2, default=str))
            else:
                console.print()
                console.print("[bold cyan]Preview - Data that will be submitted:[/bold cyan]")
                console.print()
                preview_data = collector.preview_submission(report)
                console.print(json.dumps(preview_data, indent=2, default=str))
                console.print()
                console.print("[dim]Run without --preview to submit.[/dim]")
            return

        # Check telemetry consent before submission (S4.T2)
        _check_telemetry_consent(non_interactive=non_interactive)

        result = collector.submit(report)

        if format_output == "json":
            import json
            print(json.dumps(result, indent=2, default=str))
            # Exit with appropriate code
            raise typer.Exit(0 if result.get("success") else 1)
        else:
            _display_submission_result(result, console)
            # Exit with appropriate code
            raise typer.Exit(0 if result.get("success") else 1)

    except typer.Exit:
        raise
    except Exception as e:
        if format_output == "json":
            import json
            print(json.dumps({"success": False, "error": str(e)}, indent=2))
        else:
            print_error(f"Failed to submit bug report: {e}")
            logger.exception("Bug report submission failed")
        raise typer.Exit(1)


@feedback_app.command("feature")
@handle_encoding_errors
def feedback_feature(
    title: str = typer.Argument(..., help="Feature title"),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        help="Non-interactive mode (no prompts, for orchestrator use)",
    ),
    format_output: str = typer.Option(
        "text",
        "--format",
        help="Output format: text, json",
    ),
    use_case: str = typer.Option(
        "",
        "--use-case",
        "-u",
        help="Why do you need this feature?",
    ),
    description: str = typer.Option(
        "",
        "--description",
        "-d",
        help="Detailed description of the feature",
    ),
    workaround: str = typer.Option(
        "",
        "--workaround",
        "-w",
        help="How do you handle this currently?",
    ),
    impact: str = typer.Option(
        "",
        "--impact",
        "-i",
        help="How would this help your work?",
    ),
    frequency: str = typer.Option(
        "",
        "--frequency",
        "-f",
        help="How often would you use this? (daily, weekly, monthly)",
    ),
    similar: str = typer.Option(
        "",
        "--similar",
        help="Have you seen this in other tools?",
    ),
    privacy: str = typer.Option(
        "standard",
        "--privacy",
        "-p",
        help="Privacy level: full, standard, minimal",
    ),
    preview: bool = typer.Option(
        False,
        "--preview",
        help="Preview what will be sent without submitting",
    ),
) -> None:
    """Request a new feature.

    Describe the feature you'd like to see in Obra. Include your use case
    and how it would help your workflow.

    Examples:
        obra feedback feature "Add dark mode"
        obra feedback feature "Export to PDF" --use-case "Share reports with team"
        obra feedback feature "Git integration" --frequency daily --impact "Save 10 min/day"

    Tips:
        - Be specific about the problem you're trying to solve
        - Include frequency of need to help prioritize
        - Mention similar features in other tools if applicable
    """
    from obra.feedback import FeedbackCollector

    try:
        privacy_level = _get_privacy_level(privacy)
        collector = FeedbackCollector(privacy_level=privacy_level)

        report = collector.create_feature_request(
            feature_title=title,
            use_case=use_case,
            description=description,
            current_workaround=workaround,
            business_impact=impact,
            frequency_of_need=frequency,
            similar_tools=similar,
        )

        if preview:
            import json

            if format_output == "json":
                preview_data = collector.preview_submission(report)
                print(json.dumps(preview_data, indent=2, default=str))
            else:
                console.print()
                console.print("[bold cyan]Preview - Data that will be submitted:[/bold cyan]")
                console.print()
                preview_data = collector.preview_submission(report)
                console.print(json.dumps(preview_data, indent=2, default=str))
                console.print()
                console.print("[dim]Run without --preview to submit.[/dim]")
            return

        # Check telemetry consent before submission (S4.T2)
        _check_telemetry_consent(non_interactive=non_interactive)

        result = collector.submit(report)

        if format_output == "json":
            import json
            print(json.dumps(result, indent=2, default=str))
            raise typer.Exit(0 if result.get("success") else 1)
        else:
            _display_submission_result(result, console)
            raise typer.Exit(0 if result.get("success") else 1)

    except typer.Exit:
        raise
    except Exception as e:
        if format_output == "json":
            import json
            print(json.dumps({"success": False, "error": str(e)}, indent=2))
        else:
            print_error(f"Failed to submit feature request: {e}")
            logger.exception("Feature request submission failed")
        raise typer.Exit(1)


@feedback_app.command("comment")
@handle_encoding_errors
def feedback_comment(
    text: str = typer.Argument(..., help="Your feedback"),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        help="Non-interactive mode (no prompts, for orchestrator use)",
    ),
    format_output: str = typer.Option(
        "text",
        "--format",
        help="Output format: text, json",
    ),
    category: str = typer.Option(
        "general",
        "--category",
        "-c",
        help="Category: general, documentation, ux, performance",
    ),
    suggestion: str = typer.Option(
        "",
        "--suggestion",
        "-s",
        help="Improvement suggestion",
    ),
    privacy: str = typer.Option(
        "standard",
        "--privacy",
        "-p",
        help="Privacy level: full, standard, minimal",
    ),
    preview: bool = typer.Option(
        False,
        "--preview",
        help="Preview what will be sent without submitting",
    ),
) -> None:
    """Submit general feedback or a comment.

    Share your thoughts about Obra - what's working well, what could be better,
    or general observations about your experience.

    Examples:
        obra feedback comment "Great documentation!"
        obra feedback comment "Slow on large projects" --category performance
        obra feedback comment "Hard to find settings" --category ux --suggestion "Add search"

    Categories:
        general       - General feedback (default)
        documentation - Feedback about docs
        ux            - User experience feedback
        performance   - Performance observations
    """
    from obra.feedback import FeedbackCollector

    try:
        privacy_level = _get_privacy_level(privacy)
        collector = FeedbackCollector(privacy_level=privacy_level)

        report = collector.create_comment(
            summary=text[:80] + ("..." if len(text) > 80 else ""),
            description=text,
            category=category,
            suggestion=suggestion,
        )

        if preview:
            import json

            if format_output == "json":
                preview_data = collector.preview_submission(report)
                print(json.dumps(preview_data, indent=2, default=str))
            else:
                console.print()
                console.print("[bold cyan]Preview - Data that will be submitted:[/bold cyan]")
                console.print()
                preview_data = collector.preview_submission(report)
                console.print(json.dumps(preview_data, indent=2, default=str))
                console.print()
                console.print("[dim]Run without --preview to submit.[/dim]")
            return

        # Check telemetry consent before submission (S4.T2)
        _check_telemetry_consent(non_interactive=non_interactive)

        result = collector.submit(report)

        if format_output == "json":
            import json
            print(json.dumps(result, indent=2, default=str))
            raise typer.Exit(0 if result.get("success") else 1)
        else:
            _display_submission_result(result, console)
            raise typer.Exit(0 if result.get("success") else 1)

    except typer.Exit:
        raise
    except Exception as e:
        if format_output == "json":
            import json
            print(json.dumps({"success": False, "error": str(e)}, indent=2))
        else:
            print_error(f"Failed to submit comment: {e}")
            logger.exception("Comment submission failed")
        raise typer.Exit(1)


@feedback_app.command("drafts")
@handle_encoding_errors
def feedback_drafts(
    delete: str = typer.Option(
        None,
        "--delete",
        "-d",
        help="Delete a draft by report ID",
    ),
) -> None:
    """List and manage feedback drafts.

    Drafts are automatically saved when creating feedback reports.
    Use this command to view, resume, or delete saved drafts.

    Examples:
        obra feedback drafts                    # List all drafts
        obra feedback drafts --delete abc-123   # Delete a draft
    """
    from obra.feedback import FeedbackCollector

    try:
        collector = FeedbackCollector()

        if delete:
            if collector.delete_draft(delete):
                print_success(f"Draft deleted: {delete}")
            else:
                print_error(f"Draft not found: {delete}")
            return

        drafts = collector.list_drafts()

        console.print()
        if not drafts:
            print_info("No drafts saved")
            return

        console.print(f"[bold cyan]Saved Drafts[/bold cyan] ({len(drafts)} total)")
        console.print()

        table = Table()
        table.add_column("Report ID", style="cyan")
        table.add_column("Type", style="bold")
        table.add_column("Summary")
        table.add_column("Created", style="dim")

        for draft in drafts:
            report_id = draft.get("report_id", "")[:8] + "..."
            feedback_type = draft.get("type", "unknown")
            summary = draft.get("summary", "")[:40] + ("..." if len(draft.get("summary", "")) > 40 else "")
            created = draft.get("created_at", "N/A")

            if "T" in str(created):
                try:
                    from datetime import datetime

                    dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    created = dt.strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError):
                    pass

            table.add_row(report_id, feedback_type, summary, created)

        console.print(table)
        console.print()
        console.print("[dim]Delete with: obra feedback drafts --delete <report_id>[/dim]")

    except Exception as e:
        print_error(f"Failed to list drafts: {e}")
        logger.exception("Draft listing failed")
        raise typer.Exit(1)


@feedback_app.command("sync")
@handle_encoding_errors
def feedback_sync() -> None:
    """Sync pending feedback to server.

    Attempts to submit any feedback that was stored locally due to
    network issues. Run this when you regain connectivity.

    Examples:
        obra feedback sync
    """
    from obra.feedback import FeedbackCollector

    try:
        collector = FeedbackCollector()
        result = collector.sync_pending()

        console.print()
        if result["synced"] > 0:
            print_success(f"Synced {result['synced']} pending report(s)")
        if result["failed"] > 0:
            console.print(f"[yellow]Failed to sync {result['failed']} report(s)[/yellow]")
        if result["remaining"] > 0:
            console.print(f"[dim]{result['remaining']} report(s) still pending[/dim]")
        if result["synced"] == 0 and result["failed"] == 0:
            print_info("No pending reports to sync")

    except Exception as e:
        print_error(f"Sync failed: {e}")
        logger.exception("Feedback sync failed")
        raise typer.Exit(1)


# =============================================================================
# Triage Commands (FEEDBACK-TRIAGE-001: Feedback Triage Orchestration)
# =============================================================================

triage_app = typer.Typer(
    name="triage",
    help="Evaluate and classify feedback submissions",
    rich_markup_mode="rich",
)
app.add_typer(triage_app, name="triage", rich_help_panel="Feedback & Bug Reporting")


@triage_app.command("evaluate")
@handle_encoding_errors
def triage_evaluate(
    feedback_id: str = typer.Option(
        ...,
        "--feedback-id",
        help="Feedback ID to evaluate (e.g., bug-xxx-xxx)",
    ),
    format_output: str = typer.Option(
        "text",
        "--format",
        "-f",
        help="Output format: text, json",
    ),
) -> None:
    """Evaluate a feedback submission through the triage workflow.

    This command runs the feedback through automated triage stages:
    1. Validation (spam detection, quality scoring)
    2. Classification (bug/enhancement/question)
    3. Severity assignment (for bugs: P0/P1/P2/P3)
    4. Routing decision (accept/reject/escalate)

    Examples:
        obra triage evaluate --feedback-id bug-abc-123
        obra triage evaluate --feedback-id bug-abc-123 --format json
    """
    import json

    from obra.workflow.feedback_triage import FeedbackTriageWorkflow

    try:
        # For now, we'll use a mock feedback submission
        # In a future story, this will fetch from Firestore
        # TODO(FEEDBACK-TRIAGE-001 S3): Integrate with StateManager to fetch real feedback
        feedback = {
            "id": feedback_id,
            "type": "bug",
            "description": "Application crashes when clicking the submit button. "
            "Error message: NullPointerException at line 42.",
            "metadata": {
                "version": "2.0.0",
                "environment": "production",
            },
        }

        # Execute triage workflow
        workflow = FeedbackTriageWorkflow()
        decision = workflow.execute(feedback)

        if format_output == "json":
            # JSON output for machine consumption
            output = {
                "feedback_id": feedback_id,
                "decision": decision.decision,
                "confidence": decision.confidence,
                "reasoning": decision.reasoning,
                "severity": decision.severity,
                "human_review_required": decision.human_review_required,
                "destination": decision.destination,
                "metadata": decision.metadata,
            }
            console.print(json.dumps(output, indent=2))
        else:
            # Human-readable output
            console.print()
            console.print(f"[bold]Feedback Triage Result[/bold]")
            console.print(f"ID: {feedback_id}")
            console.print()

            # Decision
            decision_color = {
                "accept": "green",
                "reject": "red",
                "escalate": "yellow",
            }.get(decision.decision, "white")
            console.print(f"Decision: [{decision_color}]{decision.decision.upper()}[/{decision_color}]")
            console.print(f"Confidence: {decision.confidence:.2f}")

            # Severity (for bugs)
            if decision.severity:
                severity_color = {
                    "P0": "red",
                    "P1": "yellow",
                    "P2": "blue",
                    "P3": "cyan",
                }.get(decision.severity, "white")
                console.print(f"Severity: [{severity_color}]{decision.severity}[/{severity_color}]")

            # Human review flag
            if decision.human_review_required:
                console.print("[yellow]⚠ Human review required[/yellow]")

            # Reasoning
            console.print()
            console.print("[bold]Reasoning:[/bold]")
            console.print(f"  {decision.reasoning}")

            # Destination
            if decision.destination:
                console.print()
                console.print(f"[dim]Destination: {decision.destination}[/dim]")

            console.print()

    except FileNotFoundError as e:
        print_error(f"Configuration error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Triage evaluation failed: {e}")
        logger.exception("Triage evaluation failed")
        raise typer.Exit(1)


# =============================================================================
# Telemetry Commands (FEEDBACK-TRIAGE-001 S4: Privacy Controls)
# =============================================================================


def _load_feedback_config() -> dict[str, Any]:
    """Load feedback config with customer overrides.

    Loads from:
    1. obra/config/defaults/feedback.yaml (default)
    2. .obra/config/feedback.yaml (customer override, if exists)

    Returns:
        Merged configuration dictionary
    """
    # Load default config
    obra_root = Path(__file__).parent
    default_config_path = obra_root / "config" / "defaults" / "feedback.yaml"

    if not default_config_path.exists():
        raise ConfigurationError(f"Default feedback config not found: {default_config_path}")

    with open(default_config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    # Check for customer override
    customer_config_path = Path.cwd() / ".obra" / "config" / "feedback.yaml"
    if customer_config_path.exists():
        with open(customer_config_path, "r", encoding="utf-8") as f:
            customer_config = yaml.safe_load(f) or {}
            # Merge customer config (customer values override defaults)
            config.update(customer_config)

    return config


def _save_feedback_consent(consent: bool) -> None:
    """Save telemetry consent to customer config.

    Args:
        consent: True to enable, False to disable
    """
    customer_config_path = Path.cwd() / ".obra" / "config" / "feedback.yaml"
    customer_config_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing customer config if present
    if customer_config_path.exists():
        with open(customer_config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {}

    # Update telemetry_consent
    config["telemetry_consent"] = consent

    # Save back to file
    with open(customer_config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)


def _check_telemetry_consent(non_interactive: bool = False) -> bool:
    """Check if user has consented to telemetry.

    Args:
        non_interactive: If True, will not prompt and will raise exception if no consent

    Returns:
        True if consent is granted, False otherwise

    Raises:
        typer.Exit: If non-interactive mode and consent not granted (exit code 1)
    """
    try:
        config = _load_feedback_config()
        consent = config.get("telemetry_consent")

        # If consent is explicitly granted, allow submission
        if consent is True:
            return True

        # If consent is explicitly denied, block submission
        if consent is False:
            if non_interactive:
                print_error("Telemetry disabled. Enable with: obra telemetry enable")
                raise typer.Exit(1)
            else:
                console.print()
                console.print("[yellow]⚠ Telemetry is disabled[/yellow]")
                console.print("Enable with: obra telemetry enable")
                console.print()
                raise typer.Exit(1)

        # If consent not yet given (None), prompt interactively or require action
        if consent is None:
            if non_interactive:
                print_error("Telemetry consent required. Enable with: obra telemetry enable")
                raise typer.Exit(1)
            console.print()
            console.print("[yellow]⚠ Telemetry consent not configured[/yellow]")
            console.print()
            console.print("Before submitting feedback, you must consent to data collection.")
            console.print("To see what data is collected: obra telemetry explain")
            console.print()

            # Interactive prompt to enable telemetry inline
            allow = typer.confirm("Enable telemetry and submit feedback?", default=False)
            if allow:
                _save_feedback_consent(True)
                console.print("[green]Telemetry enabled. Submitting feedback...[/green]")
                return True

            _save_feedback_consent(False)
            console.print()
            console.print("Telemetry disabled. Enable later with: obra telemetry enable")
            console.print()
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Failed to check telemetry consent: {e}")
        raise typer.Exit(1)


telemetry_app = typer.Typer(
    name="telemetry",
    help="Manage telemetry and feedback data collection",
    rich_markup_mode="rich",
)
app.add_typer(telemetry_app, name="telemetry", rich_help_panel="Feedback & Bug Reporting")


@telemetry_app.command("enable")
@handle_encoding_errors
def telemetry_enable() -> None:
    """Enable telemetry and feedback data collection.

    Grants consent for Obra to collect diagnostic data when you submit
    bug reports or feedback. Data is used to improve Obra and prioritize fixes.

    You can revoke consent at any time with: obra telemetry disable

    Example:
        obra telemetry enable
    """
    try:
        _save_feedback_consent(True)
        print_success("✓ Telemetry enabled")
        console.print()
        console.print("Thank you for helping improve Obra!")
        console.print("Data will be collected when you submit feedback with: obra feedback bug/feature/comment")
        console.print()
        console.print("To see what data is collected: obra telemetry explain")
        console.print("To disable: obra telemetry disable")
    except Exception as e:
        print_error(f"Failed to enable telemetry: {e}")
        raise typer.Exit(1)


@telemetry_app.command("disable")
@handle_encoding_errors
def telemetry_disable() -> None:
    """Disable telemetry and feedback data collection.

    Revokes consent for data collection. Bug reports and feedback submissions
    will be blocked until you re-enable telemetry.

    Example:
        obra telemetry disable
    """
    try:
        _save_feedback_consent(False)
        print_success("✓ Telemetry disabled")
        console.print()
        console.print("Data collection has been disabled.")
        console.print("Note: Feedback submission will be blocked until you re-enable telemetry.")
        console.print()
        console.print("To re-enable: obra telemetry enable")
    except Exception as e:
        print_error(f"Failed to disable telemetry: {e}")
        raise typer.Exit(1)


@telemetry_app.command("status")
@handle_encoding_errors
def telemetry_status() -> None:
    """Show current telemetry consent status and data collection settings.

    Displays:
    - Whether telemetry is enabled or disabled
    - What data is currently being collected
    - How to change settings

    Example:
        obra telemetry status
    """
    try:
        config = _load_feedback_config()
        consent = config.get("telemetry_consent")
        data_level = config.get("data_level", "minimal")

        console.print()
        console.print("[bold]Telemetry Status[/bold]")
        console.print()

        # Consent status
        if consent is None:
            console.print("Status: [yellow]Not configured[/yellow]")
            console.print("You have not yet been asked for consent.")
            console.print()
            console.print("To enable: obra telemetry enable")
            console.print("To disable: obra telemetry disable")
        elif consent:
            console.print("Status: [green]Enabled[/green]")
            console.print("Data collection is active when you submit feedback.")
        else:
            console.print("Status: [red]Disabled[/red]")
            console.print("Data collection is blocked.")

        console.print()
        console.print(f"Data level: {data_level}")
        console.print()

        # Data fields
        data_fields = config.get("data_fields", {}).get(data_level, [])
        if data_fields:
            console.print("[bold]Data collected:[/bold]")
            for field in data_fields:
                console.print(f"  • {field}")

        console.print()
        console.print("For more details: obra telemetry explain")
        console.print()

    except Exception as e:
        print_error(f"Failed to get telemetry status: {e}")
        raise typer.Exit(1)


@telemetry_app.command("explain")
@handle_encoding_errors
def telemetry_explain() -> None:
    """Explain what data is collected and why.

    Provides detailed information about:
    - What data Obra collects
    - Why each piece of data is collected
    - How data is protected (redaction, encryption)
    - Your privacy controls

    Example:
        obra telemetry explain
    """
    console.print()
    console.print("[bold cyan]What data does Obra collect?[/bold cyan]")
    console.print()

    console.print("[bold]When you submit feedback (bug/feature/comment):[/bold]")
    console.print()

    console.print("📊 [bold]Minimal data level[/bold] (default):")
    console.print("  • Feedback type (bug, feature request, comment)")
    console.print("  • Your description")
    console.print("  • Obra version")
    console.print("  • Timestamp")
    console.print("  • Platform (Linux, macOS, Windows)")
    console.print("  • Python version")
    console.print()

    console.print("📈 [bold]Detailed data level[/bold] (opt-in):")
    console.print("  • All minimal data, plus:")
    console.print("  • Session ID (for tracking related issues)")
    console.print("  • Stack trace (if error occurred)")
    console.print("  • Environment variables (redacted)")
    console.print("  • Recent logs (last 50 lines)")
    console.print("  • Command history (last 10 commands)")
    console.print("  • Active task ID")
    console.print()

    console.print("[bold cyan]How is your data protected?[/bold cyan]")
    console.print()
    console.print("🔒 [bold]Automatic redaction:[/bold]")
    console.print("  • API keys, tokens, passwords")
    console.print("  • AWS credentials")
    console.print("  • GitHub tokens")
    console.print("  • Home directory paths → replaced with ~")
    console.print("  • Usernames → replaced with [USER]")
    console.print("  • SSH keys, .env files, credentials")
    console.print()

    console.print("[bold cyan]Your privacy controls:[/bold cyan]")
    console.print()
    console.print("✓ You must explicitly consent before ANY data is sent")
    console.print("✓ In interactive mode, you can preview data before sending")
    console.print("✓ You can revoke consent at any time")
    console.print("✓ Non-interactive submissions are blocked without consent")
    console.print()

    console.print("[bold cyan]Why collect this data?[/bold cyan]")
    console.print()
    console.print("Your feedback helps us:")
    console.print("  • Prioritize bug fixes")
    console.print("  • Understand common issues")
    console.print("  • Improve error messages")
    console.print("  • Build features users actually need")
    console.print()

    console.print("[bold cyan]Commands:[/bold cyan]")
    console.print("  obra telemetry enable     - Grant consent")
    console.print("  obra telemetry disable    - Revoke consent")
    console.print("  obra telemetry status     - Check current settings")
    console.print()


# =============================================================================
# Derive Command (FEAT-AUTO-INTENT-001 S3.T0, S3.T1)
# =============================================================================


@app.command(rich_help_panel="Derivation")
@handle_encoding_errors
@require_terms_accepted
def derive(
    objective: str | None = typer.Argument(
        None,
        help="Objective to derive (uses active intent if not provided)",
    ),
    working_dir: Path | None = typer.Option(
        None,
        "--dir",
        "-d",
        help="Working directory (defaults to current directory)",
    ),
    project_id: str | None = typer.Option(
        None,
        "--project",
        help="Project ID override (optional)",
    ),
    continue_intent: bool = typer.Option(
        False,
        "--continue",
        help="Continue with active intent (explicit flag, S3.T1)",
    ),
    resume_session: str | None = typer.Option(
        None,
        "--resume",
        "-r",
        help="Resume an existing session by ID",
    ),
    continue_from: str | None = typer.Option(
        None,
        "--continue-from",
        "-c",
        help="Continue from a failed/escalated session (creates new session, skips completed tasks)",
    ),
    plan_id: str | None = typer.Option(
        None,
        "--plan-id",
        help=(
            "Use an uploaded plan by ID (from 'obra plans upload'). "
            "Requires local YAML at docs/development/{PLAN_ID}_MACHINE_PLAN.json."
        ),
    ),
    plan_file: Path | None = typer.Option(
        None,
        "--plan-file",
        help="Upload and use a plan file in one step",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        "-m",
        help="Implementation model (e.g., opus, gpt-5.2, gemini-2.5-flash)",
    ),
    fast_model: str | None = typer.Option(
        None,
        "--fast-model",
        help="Fast tier model override (used for extraction and quick validation)",
    ),
    high_model: str | None = typer.Option(
        None,
        "--high-model",
        help="High tier model override (used for complex reasoning)",
    ),
    impl_provider: str | None = typer.Option(
        None,
        "--impl-provider",
        "-p",
        help="Implementation provider (anthropic, openai, google). Requires provider CLI (claude/codex/gemini).",
    ),
    thinking_level: str | None = typer.Option(
        None,
        "--thinking-level",
        "-t",
        help="Thinking/reasoning level (off, low, medium, high, maximum)",
    ),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        max=3,
        help="Verbosity level (0-3, use -v/-vv/-vvv)",
    ),
    stream: bool = typer.Option(
        False,
        "--stream",
        "-s",
        help="Enable real-time LLM output streaming",
    ),
    plan_only: bool = typer.Option(
        False,
        "--plan-only",
        help="Create plan without executing (client-side exit after planning)",
    ),
    permissive: bool = typer.Option(
        False,
        "--permissive",
        help="Bypass P1 planning blockers (proceed with warnings)",
    ),
    defaults_json: bool = typer.Option(
        False,
        "--defaults-json",
        help="Print proposed defaults as JSON and exit when refinement is blocked",
    ),
    no_closeout: bool = typer.Option(
        False,
        "--no-closeout",
        help="Skip close-out story injection",
    ),
    skip_intent: bool = typer.Option(
        False,
        "--skip-intent",
        help="Skip intent generation for vague objectives (S2.T3)",
    ),
    review_intent: bool = typer.Option(
        False,
        "--review-intent",
        help="Display generated intent and prompt for approval before derive (S2.T4)",
    ),
    scaffolded: bool = typer.Option(
        False,
        "--scaffolded",
        help="Force scaffolded intent enrichment (requires planning.scaffolded.enabled)",
    ),
    no_scaffolded: bool = typer.Option(
        False,
        "--no-scaffolded",
        help="Skip scaffolded intent enrichment even when enabled",
    ),
    isolated: bool | None = typer.Option(
        None,
        "--isolated",
        help="Run agent in isolated environment (prevents reading host CLI config)",
    ),
    no_isolated: bool | None = typer.Option(
        None,
        "--no-isolated",
        help="Disable isolation (use host CLI config, even in CI)",
    ),
    full_review: bool = typer.Option(
        False,
        "--full-review",
        help="Run all review agents (overrides auto-detection)",
    ),
    skip_review: bool = typer.Option(
        False,
        "--skip-review",
        help="Skip the review phase entirely",
    ),
    review_agents: str | None = typer.Option(
        None,
        "--review-agents",
        help=f"Comma-separated review agents to run ({', '.join(ALLOWED_AGENTS)})",
    ),
    with_security: bool = typer.Option(
        False,
        "--with-security",
        help="Add the security review agent",
    ),
    with_testing: bool = typer.Option(
        False,
        "--with-testing",
        help="Add the testing review agent",
    ),
    with_docs: bool = typer.Option(
        False,
        "--with-docs",
        help="Add the docs review agent",
    ),
    with_code_quality: bool = typer.Option(
        False,
        "--with-code-quality",
        help="Add the code_quality review agent",
    ),
    no_security: bool = typer.Option(
        False,
        "--no-security",
        help="Remove the security review agent",
    ),
    no_testing: bool = typer.Option(
        False,
        "--no-testing",
        help="Remove the testing review agent",
    ),
    no_docs: bool = typer.Option(
        False,
        "--no-docs",
        help="Remove the docs review agent",
    ),
    no_code_quality: bool = typer.Option(
        False,
        "--no-code-quality",
        help="Remove the code_quality review agent",
    ),
    review_format: str | None = typer.Option(
        None,
        "--review-format",
        help="Review output format (text or json)",
        show_choices=True,
    ),
    review_quiet: bool = typer.Option(
        False,
        "--review-quiet",
        help="Suppress review output",
    ),
    review_summary_only: bool = typer.Option(
        False,
        "--review-summary-only",
        help="Show only review summary counts",
    ),
    fail_on_p1: bool = typer.Option(
        False,
        "--fail-on-p1",
        help="Exit with status 1 when P1 findings are present",
    ),
    fail_on_p2: bool = typer.Option(
        False,
        "--fail-on-p2",
        help="Exit with status 1 when P1 or P2 findings are present",
    ),
    review_timeout: int | None = typer.Option(
        None,
        "--review-timeout",
        min=1,
        help="Per-agent review timeout in seconds",
    ),
    auto_report: bool = typer.Option(
        False,
        "--auto-report",
        help="Automatically submit bug reports on failure (no prompt, for CI/CD)",
    ),
    skip_git_check: bool = typer.Option(
        False,
        "--skip-git-check",
        help="Skip git repository validation (GIT-HARD-001)",
    ),
    auto_init_git: bool = typer.Option(
        False,
        "--auto-init-git",
        help="Auto-initialize git repository if not present (GIT-HARD-001)",
    ),
    force_empty: bool = typer.Option(
        False, "--force-empty", help="Force EMPTY project state (new/minimal project)"
    ),
    force_existing: bool = typer.Option(
        False, "--force-existing", help="Force EXISTING project state (established codebase)"
    ),
) -> None:
    """Derive execution plan from objective or active intent.

    Obra's derive command creates an execution plan from your objective.
    If you don't provide an objective, it will use the active intent
    for the current project (created via 'obra intent new').

    Examples:
        obra derive "add user authentication"
        obra derive                              # Uses active intent
        obra derive --continue                   # Explicit continue with active intent
        obra derive "refactor API" --plan-only
        obra derive --stream -vv

    With active intent:
        obra intent new "add auth"
        obra derive                              # Uses "add auth" intent
        obra derive --continue                   # Explicit form

    Environment Variables:
        OBRA_MODEL          Default model (e.g., opus, gpt-5.2, gemini-2.5-flash)
        OBRA_FAST_MODEL     Fast tier override (e.g., haiku, gpt-5.1-codex-mini)
        OBRA_HIGH_MODEL     High tier override (e.g., opus, gpt-5.2)
        OBRA_PROVIDER       Default provider (anthropic, openai, google)
        OBRA_THINKING_LEVEL Default thinking level (off, low, medium, high, maximum)
        OBRA_ISOLATED       Enable/disable isolation (true/false)

    Precedence: CLI flags > environment variables > config file

    Reference: FEAT-AUTO-INTENT-001 S3.T0, S3.T1
    """
    from obra.intent import IntentStorage

    # Resolve working directory
    work_dir = working_dir or Path.cwd()
    storage = IntentStorage()
    proj_id = storage.get_project_id(work_dir)

    # Validate force flags are mutually exclusive
    if force_empty and force_existing:
        console.print()
        print_error("Cannot specify both --force-empty and --force-existing")
        console.print()
        raise typer.Exit(1)

    # Determine objective source
    if objective:
        # Explicit objective provided
        final_objective = objective
        if not continue_intent:
            # S3.T4: Non-blocking notice when creating new intent while active exists
            active_intent = storage.load_active(proj_id)
            if active_intent:
                console.print()
                print_info(
                    f"Note: Active intent '{active_intent.slug}' exists. "
                    "New derivation will create a separate intent."
                )
                console.print("      To use the active intent, run: [cyan]obra derive[/cyan] (no objective)")
                console.print()
    elif continue_intent or objective is None:
        # No objective: use active intent (S3.T0, S3.T1)
        active_intent = storage.load_active(proj_id)

        if not active_intent:
            # S3.T3: Error handling for missing active intent
            console.print()
            print_error("No active intent found for this project")
            console.print()
            console.print("To create an intent:")
            console.print("  [cyan]obra intent new 'your objective'[/cyan]")
            console.print()
            console.print("Or provide an objective directly:")
            console.print("  [cyan]obra derive 'your objective'[/cyan]")
            console.print()
            raise typer.Exit(1)

        # Use the raw objective from the active intent
        final_objective = active_intent.raw_objective or active_intent.problem_statement
        console.print()
        print_info(f"Using active intent: {active_intent.slug}")
        console.print(f"  [dim]Problem: {active_intent.problem_statement[:60]}...[/dim]")
        console.print()
    else:
        # Should not reach here, but handle gracefully
        console.print()
        print_error("No objective provided and no active intent found")
        console.print()
        console.print("Usage:")
        console.print("  [cyan]obra derive 'objective'[/cyan]")
        console.print("  [cyan]obra derive[/cyan] (uses active intent)")
        console.print()
        raise typer.Exit(1)

    # Call _run_derive with the resolved objective
    _run_derive(
        objective=final_objective,
        working_dir=work_dir,
        project_id=project_id,
        resume_session=resume_session,
        continue_from=continue_from,
        plan_id=plan_id,
        plan_file=plan_file,
        model=model,
        fast_model=fast_model,
        high_model=high_model,
        impl_provider=impl_provider,
        thinking_level=thinking_level,
        verbose=verbose,
        stream=stream,
        plan_only=plan_only,
        permissive=permissive,
        defaults_json=defaults_json,
        no_closeout=no_closeout,
        skip_intent=skip_intent,
        review_intent=review_intent,
        isolated=isolated,
        no_isolated=no_isolated,
        full_review=full_review,
        skip_review=skip_review,
        review_agents=review_agents,
        with_security=with_security,
        with_testing=with_testing,
        with_docs=with_docs,
        with_code_quality=with_code_quality,
        no_security=no_security,
        no_testing=no_testing,
        no_docs=no_docs,
        no_code_quality=no_code_quality,
        review_format=review_format,
        review_quiet=review_quiet,
        review_summary_only=review_summary_only,
        fail_on_p1=fail_on_p1,
        fail_on_p2=fail_on_p2,
        review_timeout=review_timeout,
        auto_report=auto_report,
        skip_git_check=skip_git_check,
        auto_init_git=auto_init_git,
    )


# =============================================================================
# Intent Commands (FEAT-AUTO-INTENT-001)
# =============================================================================

intent_app = typer.Typer(
    name="intent",
    help="Manage intent capture for derivation workflows",
    rich_markup_mode="rich",
)
app.add_typer(intent_app, name="intent", rich_help_panel="Derivation")


@intent_app.command("new")
@handle_encoding_errors
def intent_new(
    objective: str = typer.Argument(
        None, help="User objective (natural language). Omit if using --prd or --plan."
    ),
    prd: Path | None = typer.Option(
        None, "--prd", help="Path to PRD file to extract intent from"
    ),
    plan: Path | None = typer.Option(
        None, "--plan", help="Path to plan file (structured or prose) to extract intent from"
    ),
    force_empty: bool = typer.Option(
        False, "--force-empty", help="Force EMPTY project state (new/minimal project)"
    ),
    force_existing: bool = typer.Option(
        False, "--force-existing", help="Force EXISTING project state (established codebase)"
    ),
    detect_project_state: bool = typer.Option(
        False, "--detect-project-state", help="Enable project state detection for PRD/plan inputs (skipped by default)"
    ),
) -> None:
    """Create a new intent from an objective or file.

    Generates a structured intent with problem statement, assumptions,
    requirements, acceptance criteria, and non-goals using LLM.

    The intent is saved to ~/.obra/intents/{project}/ and set as the
    active intent for the project.

    Examples:
        obra intent new "add user authentication"
        obra intent new --prd docs/AUTH_PRD.md
        obra intent new --plan docs/IMPLEMENTATION_PLAN.md
        obra intent new --plan docs/MACHINE_PLAN.json

    The intent can then be used with 'obra derive' or 'obra derive --continue'.
    """
    from obra.config.llm import get_project_planning_config
    from obra.hybrid.handlers.intent import IntentHandler
    from obra.intent import IntentStorage
    from obra.intent.detection import is_structured_plan_file
    from obra.intent.models import InputType

    try:
        working_dir = Path.cwd()
        storage = IntentStorage()
        project_id = storage.get_project_id(working_dir)

        # Validate inputs
        input_count = sum([bool(objective), bool(prd), bool(plan)])
        if input_count > 1:
            console.print()
            print_error("Cannot specify multiple input types")
            console.print("  Use one of:")
            console.print("    • obra intent new 'objective'")
            console.print("    • obra intent new --prd <file>")
            console.print("    • obra intent new --plan <file>")
            console.print()
            raise typer.Exit(1)

        if input_count == 0:
            console.print()
            print_error("Must specify an input")
            console.print("  Use one of:")
            console.print("    • obra intent new 'objective'")
            console.print("    • obra intent new --prd <file>")
            console.print("    • obra intent new --plan <file>")
            console.print()
            raise typer.Exit(1)

        # Validate force flags are mutually exclusive
        if force_empty and force_existing:
            console.print()
            print_error("Cannot specify both --force-empty and --force-existing")
            console.print()
            raise typer.Exit(1)

        # Determine input type and source
        if prd:
            if not prd.exists():
                console.print()
                print_error(f"PRD file not found: {prd}")
                console.print()
                raise typer.Exit(1)

            input_source = str(prd)
            input_type = InputType.PRD
            console.print()
            print_info(f"Extracting intent from PRD: {prd.name}")
            console.print()
        elif plan:
            if not plan.exists():
                console.print()
                print_error(f"Plan file not found: {plan}")
                console.print()
                raise typer.Exit(1)

            input_source = str(plan)
            # Auto-detect structured vs prose plan
            if is_structured_plan_file(plan):
                input_type = InputType.STRUCTURED_PLAN
                console.print()
                print_info(f"Mechanically extracting intent from structured plan: {plan.name}")
                console.print()
            else:
                input_type = InputType.PROSE_PLAN
                console.print()
                print_info(f"Extracting intent from prose plan: {plan.name}")
                console.print()
        else:
            input_source = objective
            input_type = None  # Auto-detect
            console.print()
            print_info(f"Generating intent from: {objective[:60]}...")
            console.print()

        # Get LLM config
        planning_config = get_project_planning_config(working_dir)
        llm_config = {
            "provider": planning_config.get("provider", DEFAULT_PROVIDER),
            "model": planning_config.get("model", DEFAULT_MODEL),
            "thinking_level": planning_config.get("thinking_level", DEFAULT_THINKING_LEVEL),
        }

        # Generate intent
        handler = IntentHandler(
            working_dir=working_dir,
            project=project_id,
            llm_config=llm_config,
        )
        intent = handler.generate(
            input_source,
            input_type=input_type,
            force_empty=force_empty,
            force_existing=force_existing,
            detect_project_state_flag=detect_project_state,
        )

        # Save intent
        file_path = storage.save(intent)

        # Write project-local pointer for LLM discoverability
        pointer_path = storage.write_project_pointer(working_dir, intent)

        console.print()
        print_success(f"Created intent: {intent.id}")
        console.print()
        console.print(f"  [cyan]Problem:[/cyan] {intent.problem_statement}")
        console.print(f"  [cyan]Requirements:[/cyan] {len(intent.requirements)} items")
        console.print(f"  [cyan]Acceptance:[/cyan] {len(intent.acceptance_criteria)} criteria")
        console.print()
        console.print(f"  [dim]Saved to: {file_path}[/dim]")
        console.print()

        # Machine-parseable output for LLM agents
        console.print("[dim]── LLM-parseable output ──[/dim]")
        console.print(f"INTENT_ACTIVE=true")
        console.print(f"INTENT_ID={intent.id}")
        console.print(f"INTENT_FILE={pointer_path}")
        console.print(f"INTENT_SUMMARY={intent.problem_statement[:100]}...")
        console.print()

        console.print("Next steps:")
        console.print("  • [cyan]obra derive[/cyan] - Derive plan using this intent")
        console.print("  • [cyan]obra intent show[/cyan] - View intent details")
        console.print()

    except Exception as e:
        console.print()
        display_error(e, console)
        logger.exception("Intent generation failed")
        raise typer.Exit(1)


@intent_app.command("list")
@handle_encoding_errors
def intent_list(
    here: bool = typer.Option(
        False, "--here", help="Show only intents for current project"
    ),
) -> None:
    """List all intents.

    Shows PROJECT, CREATED, SLUG, and STATUS columns for all intents.
    Use --here to filter to the current project only.

    Examples:
        obra intent list
        obra intent list --here
    """
    from obra.intent import IntentStorage

    try:
        working_dir = Path.cwd()
        storage = IntentStorage()
        project_id = storage.get_project_id(working_dir) if here else None

        intents = storage.list_intents(project=project_id)

        if not intents:
            console.print()
            if here:
                print_info("No intents found for this project")
                console.print()
                console.print("Create an intent with:")
                console.print("  [cyan]obra intent new 'your objective'[/cyan]")
            else:
                print_info("No intents found")
            console.print()
            return

        # Build table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("PROJECT", style="dim")
        table.add_column("CREATED", style="yellow")
        table.add_column("SLUG", style="green")
        table.add_column("STATUS", justify="center")

        for intent in intents:
            status = "✓ Active" if intent.get("is_active") else ""
            table.add_row(
                intent.get("project", ""),
                intent.get("created", ""),
                intent.get("slug", ""),
                status,
            )

        console.print()
        console.print(table)
        console.print()
        console.print(f"  Total: {len(intents)} intent(s)")
        console.print()

    except Exception as e:
        console.print()
        display_error(e, console)
        logger.exception("Intent list failed")
        raise typer.Exit(1)


@intent_app.command("show")
@handle_encoding_errors
def intent_show(
    intent_id: str | None = typer.Argument(
        None, help="Intent ID to show (full, timestamp, or slug). Omit to show active intent."
    ),
    machine: bool = typer.Option(
        False, "--machine", help="Output in machine-parseable key=value format for LLM agents"
    ),
) -> None:
    """Show details of an intent.

    If no ID is provided, shows the active intent for the current project.
    Otherwise, resolves the ID (supports full ID, timestamp, or slug) and
    displays the specified intent.

    Use --machine for LLM-parseable output format.

    Examples:
        obra intent show                           # Show active intent
        obra intent show 20260110T1200-add-auth    # Full ID
        obra intent show 20260110T1200             # Timestamp only
        obra intent show add-auth                  # Slug only
        obra intent show --machine                 # Machine-parseable output
    """
    from obra.intent import IntentStorage

    try:
        working_dir = Path.cwd()
        storage = IntentStorage()
        project_id = storage.get_project_id(working_dir)

        # Load intent
        if intent_id:
            # Resolve partial ID to full ID
            resolved_id = storage.resolve_id(intent_id, project_id)
            if not resolved_id:
                if machine:
                    console.print("INTENT_ACTIVE=false")
                    console.print(f"INTENT_ERROR=Intent not found: {intent_id}")
                    console.print("INTENT_HINT=Run 'obra intent list --here' to see available intents")
                else:
                    console.print()
                    print_error(f"Intent not found: {intent_id}")
                    console.print()
                    console.print("Available intents:")
                    console.print("  [cyan]obra intent list --here[/cyan]")
                    console.print()
                raise typer.Exit(1)

            intent = storage.load(resolved_id, project_id)
            if not intent:
                if machine:
                    console.print("INTENT_ACTIVE=false")
                    console.print(f"INTENT_ERROR=Failed to load intent: {resolved_id}")
                else:
                    console.print()
                    print_error(f"Failed to load intent: {resolved_id}")
                    console.print()
                raise typer.Exit(1)
        else:
            # Load active intent
            intent = storage.load_active(project_id)
            if not intent:
                if machine:
                    console.print("INTENT_ACTIVE=false")
                    console.print("INTENT_HINT=Run 'obra intent new \"<objective>\"' to create an intent")
                else:
                    console.print()
                    print_info("No active intent for this project")
                    console.print()
                    console.print("Create an intent with:")
                    console.print("  [cyan]obra intent new 'your objective'[/cyan]")
                    console.print()
                raise typer.Exit(0)

        # Get pointer file path
        pointer_path = working_dir / ".obra" / "active_intent.yaml"
        intent_file_path = storage.root / intent.project / f"{intent.id}.md"

        if machine:
            # Machine-parseable output for LLM agents
            console.print("INTENT_ACTIVE=true")
            console.print(f"INTENT_ID={intent.id}")
            console.print(f"INTENT_PROJECT={intent.project}")
            console.print(f"INTENT_STATUS={intent.status.value}")
            console.print(f"INTENT_FILE={pointer_path}")
            console.print(f"INTENT_FULL_PATH={intent_file_path}")
            console.print(f"INTENT_SUMMARY={intent.problem_statement}")
            if intent.requirements:
                console.print(f"INTENT_REQUIREMENTS={'|'.join(intent.requirements)}")
            if intent.acceptance_criteria:
                console.print(f"INTENT_ACCEPTANCE_CRITERIA={'|'.join(intent.acceptance_criteria)}")
            if intent.assumptions:
                console.print(f"INTENT_ASSUMPTIONS={'|'.join(intent.assumptions)}")
            if intent.non_goals:
                console.print(f"INTENT_NON_GOALS={'|'.join(intent.non_goals)}")
        else:
            # Human-readable output
            console.print()
            console.print(f"[bold cyan]Intent: {intent.slug}[/bold cyan]")
            console.print(f"[dim]ID: {intent.id}[/dim]")
            console.print(f"[dim]Project: {intent.project}[/dim]")
            console.print(f"[dim]Status: {intent.status.value}[/dim]")
            console.print()

            console.print("[bold]Problem Statement:[/bold]")
            console.print(f"  {intent.problem_statement}")
            console.print()

            if intent.assumptions:
                console.print("[bold]Assumptions:[/bold]")
                for assumption in intent.assumptions:
                    console.print(f"  • {assumption}")
                console.print()

            if intent.requirements:
                console.print("[bold]Requirements:[/bold]")
                for req in intent.requirements:
                    console.print(f"  • {req}")
                console.print()

            if intent.acceptance_criteria:
                console.print("[bold]Acceptance Criteria:[/bold]")
                for criterion in intent.acceptance_criteria:
                    console.print(f"  • {criterion}")
                console.print()

            if intent.non_goals:
                console.print("[bold]Non-Goals:[/bold]")
                for non_goal in intent.non_goals:
                    console.print(f"  • {non_goal}")
                console.print()

            if intent.context_amendments:
                console.print("[bold]Context Amendments:[/bold]")
                for amendment in intent.context_amendments:
                    console.print(f"  • {amendment}")
                console.print()

            console.print("Next steps:")
            console.print("  • [cyan]obra derive[/cyan] - Derive plan using this intent")
            console.print("  • [cyan]obra context add 'info'[/cyan] - Amend the intent")
            console.print()

    except typer.Exit:
        raise
    except Exception as e:
        if machine:
            console.print("INTENT_ACTIVE=false")
            console.print(f"INTENT_ERROR={e}")
        else:
            console.print()
            display_error(e, console)
        logger.exception("Intent show failed")
        raise typer.Exit(1)


@intent_app.command("use")
@handle_encoding_errors
def intent_use(
    intent_id: str = typer.Argument(
        ..., help="Intent ID to set as active (full, timestamp, or slug)"
    ),
) -> None:
    """Set an intent as the active intent for the current project.

    The active intent is used by 'obra derive' (with no objective) and
    'obra context add' commands.

    Examples:
        obra intent use 20260110T1200-add-auth    # Full ID
        obra intent use 20260110T1200             # Timestamp only
        obra intent use add-auth                  # Slug only
    """
    from obra.intent import IntentStorage

    try:
        working_dir = Path.cwd()
        storage = IntentStorage()
        project_id = storage.get_project_id(working_dir)

        # Resolve partial ID to full ID
        resolved_id = storage.resolve_id(intent_id, project_id)
        if not resolved_id:
            console.print()
            print_error(f"Intent not found: {intent_id}")
            console.print()
            console.print("Available intents:")
            console.print("  [cyan]obra intent list --here[/cyan]")
            console.print()
            raise typer.Exit(1)

        # Set as active
        success = storage.set_active(resolved_id, project_id)
        if not success:
            console.print()
            print_error(f"Failed to set active intent: {resolved_id}")
            console.print()
            raise typer.Exit(1)

        # Load intent for pointer file and summary
        intent = storage.load(resolved_id, project_id)
        if intent:
            # Write project-local pointer for LLM discoverability
            pointer_path = storage.write_project_pointer(working_dir, intent)

            console.print()
            print_success(f"Active intent set: {resolved_id}")
            console.print()

            # Machine-parseable output for LLM agents
            console.print("[dim]── LLM-parseable output ──[/dim]")
            console.print(f"INTENT_ACTIVE=true")
            console.print(f"INTENT_ID={intent.id}")
            console.print(f"INTENT_FILE={pointer_path}")
            console.print(f"INTENT_SUMMARY={intent.problem_statement[:100] if intent.problem_statement else ''}...")
            console.print()
        else:
            console.print()
            print_success(f"Active intent set: {resolved_id}")
            console.print()

        console.print("Next steps:")
        console.print("  • [cyan]obra derive[/cyan] - Derive plan using this intent")
        console.print("  • [cyan]obra intent show[/cyan] - View intent details")
        console.print()

    except typer.Exit:
        raise
    except Exception as e:
        console.print()
        display_error(e, console)
        logger.exception("Intent use failed")
        raise typer.Exit(1)


@intent_app.command("delete")
@handle_encoding_errors
def intent_delete(
    intent_id: str = typer.Argument(
        ..., help="Intent ID to delete (full, timestamp, or slug)"
    ),
) -> None:
    """Delete an intent from storage.

    If the intent is currently active, it will be removed from active status
    and a warning will be displayed.

    Examples:
        obra intent delete 20260110T1200-add-auth    # Full ID
        obra intent delete 20260110T1200             # Timestamp only
        obra intent delete add-auth                  # Slug only
    """
    from obra.intent import IntentStorage

    try:
        working_dir = Path.cwd()
        storage = IntentStorage()
        project_id = storage.get_project_id(working_dir)

        # Resolve partial ID to full ID
        resolved_id = storage.resolve_id(intent_id, project_id)
        if not resolved_id:
            console.print()
            print_error(f"Intent not found: {intent_id}")
            console.print()
            console.print("Available intents:")
            console.print("  [cyan]obra intent list --here[/cyan]")
            console.print()
            raise typer.Exit(1)

        # Check if this is the active intent
        active_intent = storage.load_active(project_id)
        is_active = active_intent and active_intent.id == resolved_id

        if is_active:
            console.print()
            print_warning(f"Warning: Deleting active intent: {resolved_id}")
            console.print()

        # Delete
        success = storage.delete(resolved_id, project_id)
        if not success:
            console.print()
            print_error(f"Failed to delete intent: {resolved_id}")
            console.print()
            raise typer.Exit(1)

        # Remove project pointer if this was the active intent
        if is_active:
            storage.remove_project_pointer(working_dir)

        console.print()
        print_success(f"Deleted intent: {resolved_id}")
        console.print()

        if is_active:
            console.print("Note: This was the active intent. Set a new active intent with:")
            console.print("  [cyan]obra intent use <id>[/cyan]")
            console.print()

    except typer.Exit:
        raise
    except Exception as e:
        console.print()
        display_error(e, console)
        logger.exception("Intent delete failed")
        raise typer.Exit(1)


@intent_app.command("export")
@handle_encoding_errors
def intent_export() -> None:
    """Export the active intent to the project docs/intents/ directory.

    Copies the active intent markdown file to docs/intents/{intent-id}.md
    in the current project directory.

    Example:
        obra intent export
    """
    from obra.intent import IntentStorage

    try:
        working_dir = Path.cwd()
        storage = IntentStorage()
        project_id = storage.get_project_id(working_dir)

        # Load active intent
        intent = storage.load_active(project_id)
        if not intent:
            console.print()
            print_info("No active intent for this project")
            console.print()
            console.print("Create an intent with:")
            console.print("  [cyan]obra intent new 'your objective'[/cyan]")
            console.print()
            raise typer.Exit(0)

        # Create docs/intents/ directory
        export_dir = working_dir / "docs" / "intents"
        export_dir.mkdir(parents=True, exist_ok=True)

        # Copy intent file
        intent_file = storage.root / project_id / f"{intent.id}.md"
        export_file = export_dir / f"{intent.id}.md"

        if not intent_file.exists():
            console.print()
            print_error(f"Intent file not found: {intent_file}")
            console.print()
            raise typer.Exit(1)

        import shutil
        shutil.copy2(intent_file, export_file)

        console.print()
        print_success(f"Exported intent: {intent.id}")
        console.print()
        console.print(f"  [dim]Saved to: {export_file}[/dim]")
        console.print()

    except typer.Exit:
        raise
    except Exception as e:
        console.print()
        display_error(e, console)
        logger.exception("Intent export failed")
        raise typer.Exit(1)


# =============================================================================
# Verify Command
# =============================================================================


@app.command(rich_help_panel="User Commands")
@handle_encoding_errors
def verify(
    auto: bool = typer.Option(
        False,
        "--auto",
        help="Attempt automatic verification (best-effort file checks)",
    ),
    intent_id: str | None = typer.Option(
        None,
        "--intent",
        help="Verify specific intent ID (default: active intent)",
    ),
) -> None:
    """Verify completion against active intent acceptance criteria.

    Checks the current project state against the acceptance criteria
    defined in the active intent. Generates a verification report
    and optionally archives the intent if all criteria pass.

    Examples:
        obra verify              # Verify active intent (manual review)
        obra verify --auto       # Attempt automatic verification
        obra verify --intent add-auth  # Verify specific intent
    """
    from pathlib import Path

    from obra.intent.storage import IntentStorage
    from obra.intent.verification import (
        archive_intent,
        save_verification_report,
        verify_completion,
    )

    try:
        storage = IntentStorage()
        working_dir = Path.cwd()
        project = storage.get_project_id(working_dir)

        # Load intent to verify
        if intent_id:
            # Resolve partial ID
            resolved_id = storage.resolve_id(intent_id, project)
            if not resolved_id:
                console.print()
                print_error(f"Intent not found: {intent_id}")
                console.print()
                console.print("  [dim]Use 'obra intent list' to see available intents[/dim]")
                console.print()
                raise typer.Exit(1)
            intent = storage.load(resolved_id, project)
            if not intent:
                console.print()
                print_error(f"Failed to load intent: {resolved_id}")
                console.print()
                raise typer.Exit(1)
        else:
            # Use active intent
            intent = storage.load_active(project)
            if not intent:
                console.print()
                print_error("No active intent to verify")
                console.print()
                console.print("  [dim]Use 'obra intent list' to see available intents[/dim]")
                console.print()
                console.print('  [dim]Or create one with: obra derive "objective"[/dim]')
                console.print()
                raise typer.Exit(1)

        console.print()
        console.print(f"[bold]Verifying Intent:[/bold] {intent.id}")
        console.print(f"[dim]Problem: {intent.problem_statement}[/dim]")
        console.print()

        # Run verification
        report = verify_completion(
            intent,
            project_dir=working_dir if auto else None,
            auto_verify=auto,
        )

        # Save verification report
        report_path = save_verification_report(report)

        # Display results
        status_emoji = {
            "passed": "✓",
            "failed": "✗",
            "partial": "⚠",
            "skipped": "○",
        }
        emoji = status_emoji.get(report.status.value, "?")

        console.print(f"[bold]Verification Status:[/bold] {emoji} {report.status.value.upper()}")
        console.print()
        console.print(f"  {report.summary}")
        console.print()

        if report.results:
            console.print("[bold]Acceptance Criteria:[/bold]")
            console.print()
            for result in report.results:
                check = "[green]✓[/green]" if result.passed else "[red]✗[/red]"
                console.print(f"  {check} {result.criterion}")
                if result.notes:
                    console.print(f"    [dim]{result.notes}[/dim]")
            console.print()

        console.print("[bold]Statistics:[/bold]")
        console.print(f"  Total: {report.total_criteria}")
        console.print(f"  Passed: {report.passed_criteria}")
        console.print(f"  Failed: {report.failed_criteria}")
        console.print()

        console.print(f"[dim]Report saved: {report_path}[/dim]")
        console.print()

        # If all criteria passed, offer to archive
        if report.passed:
            console.print("[bold green]All acceptance criteria met![/bold green]")
            console.print()

            # Auto-archive the intent
            if archive_intent(intent.id, project, storage):
                console.print("[dim]Intent archived and marked complete[/dim]")
                console.print()
            else:
                console.print("[dim yellow]Warning: Failed to archive intent[/dim]")
                console.print()
        else:
            console.print("[yellow]Some criteria not yet met. Continue working on this intent.[/yellow]")
            console.print()
            console.print("  [dim]Use: obra derive --continue[/dim]")
            console.print()

    except typer.Exit:
        raise
    except Exception as e:
        console.print()
        display_error(e, console)
        logger.exception("Verification failed")
        raise typer.Exit(1)


# =============================================================================
# Autonomous Runner
# =============================================================================


@app.command(rich_help_panel="User Commands")
@handle_encoding_errors
def auto(
    plan: str = typer.Option(
        ...,
        "--plan",
        "-p",
        help="WORK_ID for the machine plan (e.g., AUTO-RUN-001)",
    ),
    max_stories: int | None = typer.Option(
        None,
        "--max-stories",
        "-m",
        help="Maximum number of stories to execute (default: all)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show execution plan without running stories",
    ),
) -> None:
    """Execute multi-story workplans autonomously.

    The auto-runner executes stories sequentially from MACHINE_PLAN.json
    without continuous LLM attention, solving the completion bias problem.

    Examples:
        obra auto --plan AUTO-RUN-001              # Execute all stories
        obra auto --plan AUTO-RUN-001 --max-stories 2  # Execute 2 stories
        obra auto --plan AUTO-RUN-001 --dry-run    # Show plan only

    Story Execution:
        Each story runs as a separate `obra run` session.
        The runner updates story status in the machine plan after completion.

    Error Handling:
        - Transient errors: Automatic retry (configurable)
        - Breakpoints: Halt execution for human intervention
        - Failed stories: Skip and continue (or escalate based on config)

    Configuration:
        Set in .obra/config.yaml or config/default_config.yaml:
            auto:
              enabled: true
              retry_count: 3
              retry_delay_seconds: 5
              error_assessor: null  # null=disabled, "fast"=use fast-tier, or model name
              escalate_on_skip: true

    Related Commands:
        - obra run: Execute a single story objective
        - obra derive: Create execution plans from objectives
    """
    import yaml
    from obra.auto.runner import AutoRunner

    # Build plan path
    plan_path = Path.cwd() / "docs" / "development" / f"{plan}_MACHINE_PLAN.json"

    if not plan_path.exists():
        print_error(f"Machine plan not found: {plan_path}")
        print_info("Expected location: docs/development/{WORK_ID}_MACHINE_PLAN.json")
        raise typer.Exit(1)

    if dry_run:
        print_info(f"[DRY-RUN] Autonomous execution plan for {plan}")
        print_info(f"Plan file: {plan_path}")
        print()

    try:
        # Load configuration from default config file
        # Note: obra package uses direct YAML loading, not src.core.config.Config
        config_path = Path(__file__).parent.parent / "config" / "default_config.yaml"
        if not config_path.exists():
            # Fallback for installed package (config not bundled)
            logger.warning(f"Config file not found at {config_path}, using defaults")
            auto_config = {}
        else:
            config = yaml.safe_load(config_path.read_text())
            auto_config = config.get("orchestration", {}).get("auto", {})

        # Extract configuration values
        retry_count = auto_config.get("retry_count", 2)
        retry_delay = auto_config.get("retry_delay_seconds", 30)
        escalate_on_skip = auto_config.get("escalate_on_skip", True)
        error_assessor_config = auto_config.get("error_assessor")

        # Create error assessor if configured
        error_assessor = None
        if error_assessor_config:
            from obra.auto.assessor import ErrorAssessor
            from obra.config import get_llm_config

            # Resolve model name (handle "fast" tier)
            # "fast" maps to haiku for cost-effective error assessment
            if error_assessor_config == "fast":
                model_name = "haiku"
            else:
                model_name = error_assessor_config

            # Get LLM config from obra.config (client config)
            # This gives us provider, model, auth info for CLI subprocess invocation
            llm_config = get_llm_config()

            # Override model with the assessor-specific model
            if llm_config:
                llm_config = dict(llm_config)  # Make a copy
                llm_config["model"] = model_name
            else:
                # Fallback if no LLM config available
                llm_config = {
                    "provider": "anthropic",
                    "model": model_name
                }

            error_assessor = ErrorAssessor(
                enabled=True,
                llm_config=llm_config
            )
            logger.info(f"Error assessor enabled with model: {model_name}")

        runner = AutoRunner(
            str(plan_path),
            retry_count=retry_count,
            retry_delay_seconds=retry_delay,
            escalate_on_skip=escalate_on_skip,
            error_assessor=error_assessor
        )
        exit_code = runner.run(max_stories=max_stories, dry_run=dry_run)

        if exit_code == 0:
            print_success("Autonomous execution completed successfully.")
        else:
            print_error(f"Autonomous execution failed with exit code {exit_code}")
            raise typer.Exit(exit_code)

    except KeyboardInterrupt:
        print_warning("\nAutonomous execution interrupted by user.")
        print_info("Current story state has been saved to plan.")
        raise typer.Exit(0)
    except Exception as e:
        print_error(f"Autonomous execution error: {e}")
        logger.exception("Auto-runner failed")
        raise typer.Exit(1)


# =============================================================================
# Entry Point
# =============================================================================


def main() -> None:
    """Main entry point for the CLI.

    Tier 2: Includes command typo suggestions for better discoverability.
    """
    # Windows UTF-8 setup BEFORE any output (including --help)
    # This must run before Typer/Rich output anything with Unicode
    if sys.platform == "win32":
        os.environ["PYTHONUTF8"] = "1"
        # Reconfigure stdout/stderr for UTF-8 with fallback for unprintable chars
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    # FEAT-CLI-VERSION-NOTIFY-001: Check for updates in background (non-blocking)
    check_for_updates_async()

    # Tier 2: Wrap app() to catch unknown commands and suggest alternatives
    try:
        app()
    except SystemExit as e:
        # Check if this is an unknown command error (exit code 2 from Click)
        if e.code == 2 and len(sys.argv) > 1:
            import difflib

            # Get the command that was attempted
            attempted_cmd = sys.argv[1]

            # Skip if it starts with - (it's a flag, not a command)
            if attempted_cmd.startswith("-"):
                raise

            # Get all available command names
            all_commands = [cmd.name for cmd in app.registered_commands if cmd.name]

            # Find close matches
            suggestions = difflib.get_close_matches(attempted_cmd, all_commands, n=3, cutoff=0.6)

            if suggestions:
                console.print()
                console.print("[yellow]💡 Did you mean:[/yellow]")
                for suggestion in suggestions:
                    console.print(f"   • obra {suggestion}")
                console.print()
                console.print("[dim]Run 'obra --help' for full command list.[/dim]")
                raise SystemExit(2)
        raise


if __name__ == "__main__":
    main()
