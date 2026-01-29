# qommit

AI-powered git commit message generator using PydanticAI.

## Installation

```bash
# Run directly with uvx (after publishing)
uvx qommit

# Or install with uv
uv tool install qommit

# For local development
uvx --from . qommit
```

## Usage

```bash
# Commit staged changes (default command)
qommit

# Stage all changes and commit
qommit -a

# Dry run - just show the generated message
qommit -n

# Use a specific model for this run
qommit -m openai:gpt-4o

# Skip confirmation prompt
qommit -y
```

## Configuration

Settings are stored in a cross-platform config directory:
- **macOS**: `~/Library/Application Support/qommit/settings.yml`
- **Linux**: `~/.config/qommit/settings.yml`
- **Windows**: `%APPDATA%\qommit\settings.yml`

### Model Configuration

```bash
# Set default model
qommit model set openai:gpt-4o
qommit model set anthropic:claude-3-5-sonnet-latest
qommit model set google-gla:gemini-1.5-pro

# Show current model
qommit model show
```

Model priority (highest to lowest):
1. `--model` / `-m` flag
2. `QOMMIT_MODEL` environment variable
3. Configured default (via `qommit model set`)
4. Built-in default: `openai:gpt-4o-mini`

### System Prompt Configuration

```bash
# Edit system prompt in your default editor ($VISUAL or $EDITOR)
qommit prompt edit

# Show current system prompt
qommit prompt show

# Reset to default prompt
qommit prompt reset
```

### View Configuration

```bash
# Show all current settings
qommit config
```

## Supported Models

Any model supported by PydanticAI can be used:

- **OpenAI**: `openai:gpt-4o`, `openai:gpt-4o-mini`, `openai:gpt-4-turbo`
- **Anthropic**: `anthropic:claude-3-5-sonnet-latest`, `anthropic:claude-3-opus-latest`
- **Google**: `google-gla:gemini-1.5-pro`
- And more...

Make sure you have the appropriate API key set for your chosen model provider:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`

## All Commands

```
qommit [OPTIONS]              Generate commit message (default)
  -m, --model TEXT            Model to use for this run
  -a, --all                   Stage all changes first
  -n, --dry-run               Don't create commit
  -y, --yes                   Skip confirmation

qommit model set NAME         Set default model
qommit model show             Show current model

qommit prompt edit            Edit system prompt in editor
qommit prompt show            Show current system prompt
qommit prompt reset           Reset prompt to default

qommit config                 Show all configuration
qommit --version              Show version
qommit --help                 Show help
```
