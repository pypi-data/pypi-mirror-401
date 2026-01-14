---
name: help
description: List available commands and show usage information
arguments: [command]
---

# Help Command

Display available slash commands with descriptions and usage examples.

## Usage

```bash
/help              # List all available commands
/help <command>    # Show detailed help for specific command
```

## Examples

```bash
/help              # Show all commands
/help ai           # Detailed help for /ai command
/help spec         # Detailed help for /spec command
```

## Available Commands

### Core Commands

- `/ai <task>` - Universal routing to specialized agents for any task
- `/help [command]` - Show this help or detailed command usage
- `/status [--json]` - Show orchestration health, running agents, context usage
- `/context` - Display context usage and optimization recommendations
- `/cleanup [--dry-run]` - Run maintenance tasks (archive old files, clean stale agents)

### Domain Commands

- `/git [message]` - Smart atomic commits with conventional format
- `/spec <action> [args]` - Specification workflow utilities
- `/implement <task-id|phase|next>` - Implement tasks from specifications
- `/validate <target>` - Run validation against acceptance criteria
- `/swarm <task>` - Execute complex tasks with parallel agent coordination

## Command Categories

**Task Orchestration**: `/ai`, `/swarm`
**Development Workflow**: `/spec`, `/implement`, `/validate`, `/git`
**System Management**: `/status`, `/context`, `/cleanup`, `/help`

## Getting Detailed Help

For detailed help on any command, use:

```bash
/help <command-name>
```

This will show:

- Full command syntax
- Available arguments and options
- Usage examples
- Related commands

## See Also

- `.claude/commands/` - All command definitions
- `.claude/agents/` - Available agents
- `.claude/GETTING_STARTED.md` - Introduction to the orchestration system
