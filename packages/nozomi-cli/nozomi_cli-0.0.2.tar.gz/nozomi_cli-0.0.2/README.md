# Nozomi CLI

Command-line interface for [Nozomi](https://nozomi.sh) - the remote workspace platform for AI coding agents.

## Installation

```bash
# Using uv (recommended)
uvx nozomi-cli

# Or install globally
uv tool install nozomi-cli

# Or with pip
pip install nozomi-cli
```

## Quick Start

```bash
# Initialize (login + setup)
nozomi init

# Create a workspace
nozomi workspace create my-project --connect

# Run a task with a prompt
nozomi run "Fix the auth bug in login.py" --connect

# List your workspaces
nozomi workspace list

# Connect to a running task
nozomi task connect task_abc123
```

## Commands

### Authentication
- `nozomi init` - Interactive setup (login + config)
- `nozomi login` - Login via browser
- `nozomi logout` - Logout
- `nozomi whoami` - Show current user

### Workspaces
- `nozomi workspace list` - List all workspaces
- `nozomi workspace create <name>` - Create a new workspace
- `nozomi workspace setup [id]` - Run interactive setup
- `nozomi workspace connect [id]` - Connect to workspace

### Tasks
- `nozomi task list` - List tasks
- `nozomi task connect <id>` - Connect terminal to task
- `nozomi task stop <id>` - Stop a task
- `nozomi task sleep <id>` - Put task to sleep
- `nozomi task wake <id>` - Wake a sleeping task

### Quick Launch
- `nozomi run "<prompt>"` - Launch a task with AI harness

### Configuration
- `nozomi config show` - Show current config
- `nozomi config init` - Interactive config setup

## Global Options

- `--json` - Output in JSON format (for scripting)

## Configuration

User config is stored in `~/.nozomi/config.json`.

Project-specific config can be added to `.nozomi/config.json` in your project root:

```json
{
  "workspace_id": "ws_abc123",
  "default_machine_tier": "medium"
}
```

## License

MIT
