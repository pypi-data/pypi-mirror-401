"""AI-powered commit message generator using PydanticAI."""

from dataclasses import dataclass

from pydantic import BaseModel
from pydantic_ai import Agent

from ai_commit.git import GitChanges
from ai_commit.settings import get_model as settings_get_model
from ai_commit.settings import get_system_prompt


class CommitMessage(BaseModel):
    """Structured commit message output."""

    subject: str
    body: str | None = None

    def format(self) -> str:
        """Format the commit message for git."""
        if self.body:
            return f"{self.subject}\n\n{self.body}"
        return self.subject


@dataclass
class GeneratorContext:
    """Context for the commit message generator."""

    staged_diff: str
    unstaged_diff: str
    staged_files: list[str]
    unstaged_files: list[str]
    recent_commits: list[str]
    include_unstaged: bool


def create_agent(model: str, system_prompt: str) -> Agent[None, CommitMessage]:
    """Create a PydanticAI agent for commit message generation."""
    return Agent(model, output_type=CommitMessage, system_prompt=system_prompt)


def build_prompt(ctx: GeneratorContext) -> str:
    """Build the user prompt from the context."""
    parts: list[str] = []

    if ctx.include_unstaged and ctx.unstaged_diff:
        parts.append("## Unstaged Changes (will be staged)")
        parts.append(f"Files: {', '.join(ctx.unstaged_files)}")
        parts.append("```diff")
        parts.append(ctx.unstaged_diff)
        parts.append("```")
        parts.append("")

    if ctx.staged_diff:
        parts.append("## Staged Changes")
        parts.append(f"Files: {', '.join(ctx.staged_files)}")
        parts.append("```diff")
        parts.append(ctx.staged_diff)
        parts.append("```")
        parts.append("")

    if ctx.recent_commits:
        parts.append("## Recent Commits (for style reference)")
        for commit in ctx.recent_commits:
            parts.append(f"- {commit}")
        parts.append("")

    parts.append("Generate a commit message for these changes.")

    return "\n".join(parts)


async def generate_commit_message(
    changes: GitChanges,
    recent_commits: list[str],
    include_unstaged: bool = False,
    model_override: str | None = None,
) -> CommitMessage:
    """Generate a commit message using AI."""
    model = model_override if model_override else settings_get_model()
    system_prompt = get_system_prompt()
    agent = create_agent(model, system_prompt)

    ctx = GeneratorContext(
        staged_diff=changes.staged_diff,
        unstaged_diff=changes.unstaged_diff if include_unstaged else "",
        staged_files=changes.staged_files,
        unstaged_files=changes.unstaged_files if include_unstaged else [],
        recent_commits=recent_commits,
        include_unstaged=include_unstaged,
    )

    prompt = build_prompt(ctx)
    result = await agent.run(prompt)
    return result.output
