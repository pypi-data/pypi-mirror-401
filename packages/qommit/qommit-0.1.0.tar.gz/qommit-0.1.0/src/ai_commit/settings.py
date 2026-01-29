"""Settings management for ai-commit."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, cast

import platformdirs
import yaml

APP_NAME = "qommit"
DEFAULT_MODEL = "openai:gpt-4o-mini"

DEFAULT_SYSTEM_PROMPT = """\
You are an expert at writing clear, concise git commit messages following best practices.

Guidelines:
- Write a clear, imperative subject line (max 50 chars preferred, 72 max)
- Subject should complete: "If applied, this commit will..."
- Use conventional commit prefixes when appropriate (feat:, fix:, docs:, style:, refactor:, test:, chore:)
- Add a body only if the changes need explanation (wrap at 72 chars)
- Focus on WHY the change was made, not just WHAT changed
- Be specific but concise

You will receive:
1. The diff of changes to be committed
2. List of files being changed
3. Recent commit messages for style reference (if available)
"""

Settings = dict[str, Any]


def get_config_dir() -> Path:
    """Get the cross-platform config directory."""
    return Path(platformdirs.user_config_dir(APP_NAME))


def get_config_path() -> Path:
    """Get the path to the settings file."""
    return get_config_dir() / "settings.yml"


def ensure_config_dir() -> None:
    """Ensure the config directory exists."""
    get_config_dir().mkdir(parents=True, exist_ok=True)


def load_settings() -> Settings:
    """Load settings from the config file."""
    config_path = get_config_path()
    if not config_path.exists():
        return {}
    with open(config_path) as f:
        loaded = yaml.safe_load(f)
        if loaded is None:
            return {}
        return cast(Settings, loaded)


def save_settings(settings: Settings) -> None:
    """Save settings to the config file."""
    ensure_config_dir()
    config_path = get_config_path()
    with open(config_path, "w") as f:
        yaml.dump(settings, f, default_flow_style=False, sort_keys=False)


def get_model() -> str:
    """Get the configured model (env var takes precedence over config)."""
    env_model = os.environ.get("QOMMIT_MODEL")
    if env_model:
        return env_model
    settings = load_settings()
    model = settings.get("model")
    if isinstance(model, str):
        return model
    return DEFAULT_MODEL


def set_model(model: str) -> None:
    """Set the default model in config."""
    settings = load_settings()
    settings["model"] = model
    save_settings(settings)


def get_system_prompt() -> str:
    """Get the configured system prompt."""
    settings = load_settings()
    prompt = settings.get("system_prompt")
    if isinstance(prompt, str):
        return prompt
    return DEFAULT_SYSTEM_PROMPT


def set_system_prompt(prompt: str) -> None:
    """Set the system prompt in config."""
    settings = load_settings()
    settings["system_prompt"] = prompt
    save_settings(settings)


def reset_system_prompt() -> None:
    """Reset the system prompt to default."""
    settings = load_settings()
    if "system_prompt" in settings:
        del settings["system_prompt"]
    save_settings(settings)


def get_editor() -> str:
    """Get the default text editor."""
    return os.environ.get("VISUAL") or os.environ.get("EDITOR") or "vim"


def edit_in_editor(content: str) -> str | None:
    """Open content in the default editor and return the edited content.

    Returns None if the user cancels (empty file or unchanged).
    """
    editor = get_editor()

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
    ) as f:
        f.write(content)
        temp_path = f.name

    try:
        subprocess.run([editor, temp_path], check=True)
        with open(temp_path) as f:
            edited = f.read()
        return edited if edited.strip() else None
    except subprocess.CalledProcessError:
        return None
    finally:
        Path(temp_path).unlink(missing_ok=True)
