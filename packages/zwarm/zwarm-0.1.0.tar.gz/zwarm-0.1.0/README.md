# zwarm

Multi-agent CLI orchestration research platform. Coordinate multiple coding agents (Codex, Claude Code) with delegation, conversation, and trajectory alignment.

## Installation

```bash
# From the workspace (recommended during development)
cd /path/to/labs
uv sync

# Or install directly
uv pip install -e ./zwarm
```

**Requirements:**
- Python 3.13+
- `codex` CLI installed (for Codex adapter)
- `claude` CLI installed (for Claude Code adapter)

## Quick Start

```bash
# 1. Test an executor directly
zwarm exec --task "What is 2+2?"

# 2. Run the orchestrator with a task
zwarm orchestrate --task "Create a hello world Python function"

# 3. Check state after running
zwarm status

# 4. View event history
zwarm history
```

### Task Input Options

```bash
# Direct task
zwarm orchestrate --task "Build a REST API"

# From file
zwarm orchestrate --task-file task.md

# From stdin
echo "Fix the bug in auth.py" | zwarm orchestrate
```

## Configuration

zwarm looks for configuration in this order:
1. `--config` flag (YAML file)
2. `config.toml` in working directory
3. Default settings

### Minimal config.toml

```toml
[weave]
enabled = true
project = "your-wandb-entity/zwarm"

[executor]
adapter = "codex_mcp"  # or "claude_code"
```

### Environment Variables

```bash
# Enable Weave tracing (alternative to config.toml)
export WEAVE_PROJECT="your-entity/zwarm"

# Required for adapters
export OPENAI_API_KEY="..."      # for Codex
export ANTHROPIC_API_KEY="..."   # for Claude Code
```

### Full Configuration Reference

```yaml
# config.yaml
orchestrator:
  max_steps: 100              # Maximum orchestrator steps

executor:
  adapter: codex_mcp          # Default adapter: codex_mcp | claude_code
  model: null                 # Model override (adapter-specific)
  sandbox: workspace-write    # Codex sandbox mode

weave:
  enabled: true
  project: your-entity/zwarm

state_dir: .zwarm             # State directory for sessions/events

watchers:
  enabled: []                 # List of enabled watchers
  config:
    progress:
      stuck_threshold: 5
    budget:
      max_steps: 50
      max_sessions: 10
    scope:
      keywords: []
```

## Adapters

zwarm supports multiple CLI coding agents through adapters.

### Codex MCP (default)

Uses Codex via MCP server for true conversational sessions.

```bash
# Sync mode (conversational)
zwarm exec --adapter codex_mcp --task "Add a login function"

# The orchestrator can have back-and-forth conversations
# using delegate() and converse() tools
```

**Requires:** `codex` CLI installed, `OPENAI_API_KEY` set

### Claude Code

Uses Claude Code CLI for execution.

```bash
zwarm exec --adapter claude_code --task "Fix the type errors"
```

**Requires:** `claude` CLI installed, authenticated

## Watchers (Trajectory Alignment)

Watchers are composable guardrails that monitor agent behavior and can intervene when things go wrong.

### Available Watchers

| Watcher | Description |
|---------|-------------|
| `progress` | Detects stuck/spinning agents |
| `budget` | Monitors step/session limits |
| `scope` | Detects scope creep from original task |
| `pattern` | Custom regex pattern matching |
| `quality` | Code quality checks |

### Enabling Watchers

```yaml
# config.yaml
watchers:
  enabled:
    - progress
    - budget
    - scope
  config:
    progress:
      stuck_threshold: 5      # Flag after 5 similar steps
    budget:
      max_steps: 50
      max_sessions: 10
    scope:
      keywords:
        - "refactor"
        - "rewrite"
```

### Watcher Actions

Watchers can return different actions:
- `continue` - Keep going
- `warn` - Log warning but continue
- `pause` - Pause for human review
- `stop` - Stop the orchestrator

## Weave Integration

zwarm integrates with [Weave](https://wandb.ai/site/weave) for tracing and observability.

### Enabling Weave

```bash
# Via environment variable
export WEAVE_PROJECT="your-entity/zwarm"

# Or via config.toml
[weave]
enabled = true
project = "your-entity/zwarm"
```

### What Gets Traced

- Orchestrator `step()` calls with tool inputs/outputs
- Individual adapter calls (`_call_codex`, `_call_claude`)
- Delegation tools (`delegate`, `converse`, `end_session`)
- All tool executions

View traces at: `https://wandb.ai/your-entity/zwarm/weave`

## CLI Reference

### orchestrate

Start an orchestrator session to delegate tasks.

```bash
zwarm orchestrate [OPTIONS]

Options:
  -t, --task TEXT           Task description
  -f, --task-file PATH      Read task from file
  -c, --config PATH         Config file (YAML)
  --adapter TEXT            Executor adapter override
  --resume                  Resume from previous state
  --set KEY=VALUE           Override config values
```

### exec

Run a single executor directly (for testing).

```bash
zwarm exec [OPTIONS]

Options:
  -t, --task TEXT           Task to execute
  -f, --task-file PATH      Read task from file
  --adapter TEXT            Adapter to use [default: codex_mcp]
  --model TEXT              Model override
  --mode [sync|async]       Execution mode [default: sync]
```

### status

Show current orchestrator state.

```bash
zwarm status [OPTIONS]

Options:
  --sessions                Show session details
  --tasks                   Show task details
  --json                    Output as JSON
```

### history

Show event history.

```bash
zwarm history [OPTIONS]

Options:
  -n, --limit INTEGER       Number of events [default: 20]
  --session TEXT            Filter by session ID
  --json                    Output as JSON
```

### configs

Manage configuration files.

```bash
zwarm configs list          # List available configs
zwarm configs show NAME     # Show config contents
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Orchestrator                         │
│  (Plans, delegates, supervises - does NOT write code)   │
├─────────────────────────────────────────────────────────┤
│                    Delegation Tools                      │
│   delegate() | converse() | check_session() | bash()    │
└───────────────┬─────────────────────┬───────────────────┘
                │                     │
        ┌───────▼───────┐     ┌───────▼───────┐
        │  Codex MCP    │     │  Claude Code  │
        │   Adapter     │     │    Adapter    │
        └───────┬───────┘     └───────┬───────┘
                │                     │
        ┌───────▼───────┐     ┌───────▼───────┐
        │    codex      │     │    claude     │
        │  mcp-server   │     │     CLI       │
        └───────────────┘     └───────────────┘
```

### Key Concepts

- **Orchestrator**: Plans and delegates but never writes code directly
- **Executors**: CLI agents (Codex, Claude) that do the actual coding
- **Sessions**: Conversations with executors (sync or async)
- **Watchers**: Trajectory aligners that monitor and intervene

### State Management

All state is stored in flat files under `.zwarm/`:

```
.zwarm/
├── state.json              # Current state
├── events.jsonl            # Append-only event log
├── sessions/
│   └── <session-id>/
│       ├── messages.json   # Conversation history
│       └── metadata.json   # Session info
└── orchestrator/
    └── messages.json       # Orchestrator history (for resume)
```

## Development

### Running Tests

```bash
# From workspace root
uv run pytest wbal/tests/ -v

# zwarm doesn't have its own tests yet
```

### Project Structure

```
zwarm/
├── src/zwarm/
│   ├── adapters/           # Executor adapters
│   │   ├── base.py         # ExecutorAdapter protocol
│   │   ├── codex_mcp.py    # Codex MCP adapter
│   │   └── claude_code.py  # Claude Code adapter
│   ├── cli/
│   │   └── main.py         # Typer CLI
│   ├── core/
│   │   ├── config.py       # Configuration loading
│   │   ├── models.py       # ConversationSession, Message, etc.
│   │   └── state.py        # Flat-file state management
│   ├── tools/
│   │   └── delegation.py   # delegate, converse, etc.
│   ├── watchers/
│   │   ├── base.py         # Watcher protocol
│   │   ├── builtin.py      # Built-in watchers
│   │   └── manager.py      # WatcherManager
│   ├── prompts/
│   │   └── orchestrator.py # Orchestrator system prompt
│   └── orchestrator.py     # Main Orchestrator class
├── configs/                # Example configurations
├── README.md
└── pyproject.toml
```

## Research Context

zwarm is a research platform exploring:

1. **Agent reliability** - Can orchestrators reliably delegate and verify work?
2. **Agent meta-capability** - Can agents effectively use other agents?
3. **Long-running agents** - Can agents run for days, not hours?

See [ZWARM_PLAN.md](ZWARM_PLAN.md) for detailed design documentation.

## License

Research project - see repository license.
