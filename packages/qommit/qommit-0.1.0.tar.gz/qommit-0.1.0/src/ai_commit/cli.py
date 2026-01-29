"""CLI for qommit."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

import click

from ai_commit.generator import generate_commit_message
from ai_commit.git import (
    GitChanges,
    create_commit,
    get_all_changes,
    get_recent_commits,
    stage_all_changes,
)
from ai_commit.settings import (
    DEFAULT_MODEL,
    DEFAULT_SYSTEM_PROMPT,
    edit_in_editor,
    get_config_path,
    get_model,
    get_system_prompt,
    reset_system_prompt,
    set_model,
    set_system_prompt,
)


def print_changes_summary(changes: GitChanges) -> None:
    """Print a summary of the changes."""
    if changes.staged_files:
        click.echo(click.style("Staged files:", fg="green"))
        for f in changes.staged_files:
            click.echo(f"  {f}")

    if changes.unstaged_files:
        click.echo(click.style("Unstaged files:", fg="yellow"))
        for f in changes.unstaged_files:
            click.echo(f"  {f}")


class DefaultGroup(click.Group):
    """A click Group that runs a default command if no subcommand is given."""

    def __init__(
        self,
        name: str | None = None,
        commands: dict[str, click.Command] | None = None,
        *,
        default_cmd: str = "run",
        **attrs: Any,
    ) -> None:
        super().__init__(name, commands, **attrs)
        self.default_cmd = default_cmd

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        # Don't insert default command if --help or --version is passed
        if not args:
            args = [self.default_cmd]
        elif args[0].startswith("-") and args[0] not in ("--help", "-h", "--version"):
            args = [self.default_cmd, *args]
        return super().parse_args(ctx, args)


@click.group(cls=DefaultGroup, default_cmd="run")
@click.version_option(package_name="qommit")
def main() -> None:
    """AI-powered git commit message generator.

    Run without subcommands to generate a commit message, or use subcommands
    to configure settings.

    \b
    Examples:
        qommit              # Generate commit for staged changes
        qommit -a           # Stage all and commit
        qommit model set anthropic:claude-3-5-sonnet-latest
        qommit prompt edit  # Edit system prompt in your editor
    """
    pass


@main.command("run")
@click.option(
    "--model",
    "-m",
    "model_override",
    help="Model to use for this run (overrides config).",
)
@click.option(
    "--all",
    "-a",
    "stage_all",
    is_flag=True,
    help="Stage all changes before committing.",
)
@click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Generate message but don't create commit.",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Skip confirmation prompt.",
)
def run_commit(
    model_override: str | None,
    stage_all: bool,
    dry_run: bool,
    yes: bool,
) -> None:
    """Generate an AI-powered commit message and create a commit."""
    try:
        asyncio.run(_run_commit_async(model_override, stage_all, dry_run, yes))
    except KeyboardInterrupt:
        click.echo("\nAborted.")
        sys.exit(1)
    except RuntimeError as e:
        click.echo(click.style(f"Error: {e}", fg="red"), err=True)
        sys.exit(1)


async def _run_commit_async(
    model_override: str | None,
    stage_all: bool,
    dry_run: bool,
    yes: bool,
) -> None:
    """Async implementation for commit generation."""
    # Show which model we're using
    effective_model = get_model() if model_override is None else model_override
    click.echo(click.style(f"Using model: {effective_model}", fg="cyan"))
    click.echo()

    # Get current changes
    changes = get_all_changes()

    if not changes.has_any_changes:
        click.echo("No changes to commit.")
        sys.exit(0)

    # Stage all if requested
    if stage_all and changes.has_unstaged_changes:
        click.echo("Staging all changes...")
        stage_all_changes()
        changes = get_all_changes()

    # Check if we have staged changes
    if not changes.has_staged_changes:
        click.echo(
            click.style(
                "No staged changes. Use -a to stage all changes, or stage manually with git add.",
                fg="yellow",
            )
        )
        print_changes_summary(changes)
        sys.exit(1)

    # Show summary
    print_changes_summary(changes)
    click.echo()

    # Get recent commits for style reference
    recent_commits = get_recent_commits(5)

    # Generate commit message
    click.echo("Generating commit message...")
    commit_msg = await generate_commit_message(
        changes=changes,
        recent_commits=recent_commits,
        include_unstaged=False,
        model_override=model_override,
    )

    # Display the generated message
    click.echo()
    click.echo(click.style("Generated commit message:", fg="green", bold=True))
    click.echo(click.style("-" * 40, fg="green"))
    click.echo(commit_msg.format())
    click.echo(click.style("-" * 40, fg="green"))
    click.echo()

    if dry_run:
        click.echo("Dry run - no commit created.")
        return

    # Confirm and commit
    if yes or click.confirm("Create this commit?", default=True):
        result = create_commit(commit_msg.format())
        click.echo(click.style("Commit created successfully!", fg="green"))
        click.echo(result)
    else:
        click.echo("Commit aborted.")


# ============================================================================
# Model commands
# ============================================================================


@main.group()
def model() -> None:
    """Manage the AI model configuration."""
    pass


@model.command("set")
@click.argument("name")
def model_set(name: str) -> None:
    """Set the default model.

    \b
    Examples:
        qommit model set openai:gpt-4o
        qommit model set anthropic:claude-3-5-sonnet-latest
        qommit model set google-gla:gemini-1.5-pro
    """
    set_model(name)
    click.echo(click.style(f"Default model set to: {name}", fg="green"))
    click.echo(f"Config saved to: {get_config_path()}")


@model.command("show")
def model_show() -> None:
    """Show the current model configuration."""
    current = get_model()
    click.echo(f"Current model: {click.style(current, fg='cyan')}")
    if current == DEFAULT_MODEL:
        click.echo("(using default)")
    click.echo(f"Config file: {get_config_path()}")


# ============================================================================
# Prompt commands
# ============================================================================


@main.group()
def prompt() -> None:
    """Manage the system prompt configuration."""
    pass


@prompt.command("edit")
def prompt_edit() -> None:
    """Edit the system prompt in your default editor.

    Opens the current system prompt in your $VISUAL or $EDITOR.
    Save and close to update, or leave empty to cancel.
    """
    current_prompt = get_system_prompt()
    click.echo("Opening system prompt in editor...")

    edited = edit_in_editor(current_prompt)

    if edited is None:
        click.echo(click.style("Edit cancelled (empty content).", fg="yellow"))
        return

    if edited == current_prompt:
        click.echo("No changes made.")
        return

    set_system_prompt(edited)
    click.echo(click.style("System prompt updated!", fg="green"))
    click.echo(f"Config saved to: {get_config_path()}")


@prompt.command("show")
def prompt_show() -> None:
    """Show the current system prompt."""
    current = get_system_prompt()
    is_default = current == DEFAULT_SYSTEM_PROMPT

    click.echo(click.style("Current system prompt:", fg="cyan", bold=True))
    click.echo("-" * 40)
    click.echo(current)
    click.echo("-" * 40)

    if is_default:
        click.echo("(using default prompt)")
    click.echo(f"Config file: {get_config_path()}")


@prompt.command("reset")
def prompt_reset() -> None:
    """Reset the system prompt to the default."""
    if click.confirm("Reset system prompt to default?"):
        reset_system_prompt()
        click.echo(click.style("System prompt reset to default.", fg="green"))
    else:
        click.echo("Cancelled.")


# ============================================================================
# Config command
# ============================================================================


@main.command("config")
def show_config() -> None:
    """Show the current configuration."""
    click.echo(click.style("qommit configuration", fg="cyan", bold=True))
    click.echo(f"Config file: {get_config_path()}")
    click.echo()
    click.echo(f"Model: {get_model()}")
    click.echo(f"Custom prompt: {'Yes' if get_system_prompt() != DEFAULT_SYSTEM_PROMPT else 'No (using default)'}")


if __name__ == "__main__":
    main()
