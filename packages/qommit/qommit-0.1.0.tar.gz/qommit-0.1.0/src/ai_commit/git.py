"""Git operations for retrieving changes."""

import subprocess
from dataclasses import dataclass


@dataclass
class GitChanges:
    """Container for git changes."""

    staged_diff: str
    unstaged_diff: str
    staged_files: list[str]
    unstaged_files: list[str]

    @property
    def has_staged_changes(self) -> bool:
        return bool(self.staged_diff.strip())

    @property
    def has_unstaged_changes(self) -> bool:
        return bool(self.unstaged_diff.strip())

    @property
    def has_any_changes(self) -> bool:
        return self.has_staged_changes or self.has_unstaged_changes


def run_git_command(args: list[str]) -> str:
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            raise RuntimeError("Not a git repository") from e
        raise RuntimeError(f"Git command failed: {e.stderr}") from e


def get_staged_diff() -> str:
    """Get the diff of staged changes."""
    return run_git_command(["diff", "--cached"])


def get_unstaged_diff() -> str:
    """Get the diff of unstaged changes."""
    return run_git_command(["diff"])


def get_staged_files() -> list[str]:
    """Get list of staged files."""
    output = run_git_command(["diff", "--cached", "--name-only"])
    return [f for f in output.strip().split("\n") if f]


def get_unstaged_files() -> list[str]:
    """Get list of unstaged files."""
    output = run_git_command(["diff", "--name-only"])
    return [f for f in output.strip().split("\n") if f]


def get_untracked_files() -> list[str]:
    """Get list of untracked files."""
    output = run_git_command(["ls-files", "--others", "--exclude-standard"])
    return [f for f in output.strip().split("\n") if f]


def get_all_changes() -> GitChanges:
    """Get all git changes (staged and unstaged)."""
    return GitChanges(
        staged_diff=get_staged_diff(),
        unstaged_diff=get_unstaged_diff(),
        staged_files=get_staged_files(),
        unstaged_files=get_unstaged_files(),
    )


def stage_all_changes() -> None:
    """Stage all changes including untracked files."""
    run_git_command(["add", "-A"])


def stage_files(files: list[str]) -> None:
    """Stage specific files."""
    if files:
        run_git_command(["add"] + files)


def create_commit(message: str) -> str:
    """Create a commit with the given message."""
    return run_git_command(["commit", "-m", message])


def get_recent_commits(count: int = 5) -> list[str]:
    """Get recent commit messages for style reference."""
    try:
        output = run_git_command(
            ["log", f"-{count}", "--pretty=format:%s"]
        )
        return [msg for msg in output.strip().split("\n") if msg]
    except RuntimeError:
        return []
