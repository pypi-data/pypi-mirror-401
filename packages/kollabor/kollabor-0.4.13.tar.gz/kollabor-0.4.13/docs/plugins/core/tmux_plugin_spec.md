# Tmux Plugin Specification

## Overview

The Tmux Plugin provides seamless integration with tmux terminal multiplexer, allowing users to create, manage, and view tmux sessions directly from within Kollabor CLI.

**Location:** `plugins/tmux_plugin.py`

**Version:** 1.0.0

## Features

### Session Management

- **Create sessions**: Spawn new tmux sessions with custom commands
- **View live output**: Real-time streaming of session output in a modal overlay
- **List sessions**: Browse all managed and discovered tmux sessions
- **Kill sessions**: Terminate sessions with confirmation
- **Cycle sessions**: Navigate between multiple sessions with keyboard shortcuts

### Isolated Server (Default)

By default, the plugin uses a dedicated tmux server (`-L kollabor`) that is completely isolated from your main tmux server. This provides:

- No session name conflicts with your personal tmux sessions
- Clean separation between kollabor and your workflow
- Optional: Use your main tmux server via configuration

### Interactive Live View

The live view mode provides:
- Real-time session output streaming
- Modal viewport sized to terminal height - 10 (leaves room for header/footer)
- Keyboard input passthrough to tmux session
- Session cycling with Opt+Left/Right arrows
- In-session kill with Opt+x
- Customizable capture lines (default: 200 lines from history)

## Slash Commands

### `/terminal` (aliases: `/term`, `/tmux`, `/t`)

Main command for tmux session management.

#### Subcommands

| Subcommand | Arguments | Description |
|-----------|-----------|-------------|
| `new` | `<name> [command]` | Create new session with optional command |
| `view` | `[name]` | Live view session (cycles if no name) |
| `list` / `ls` | - | List all sessions |
| `kill` | `<name>` | Kill a session |
| `attach` | `<name>` | Get attach command for external tmux |
| `help` | - | Show help text |

#### Examples

```bash
# Create a session running a web server
/terminal new web python -m http.server 8080

# Create a session to follow logs
/terminal new logs tail -f /var/log/syslog

# View first available session
/t

# View specific session
/terminal view web

# List all sessions
/t ls

# Kill a session
/t kill web
```

## Configuration

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable the plugin |
| `show_status` | boolean | `true` | Show session count in status bar |
| `refresh_rate` | float | `0.1` | Live view refresh rate (seconds) |
| `capture_lines` | int | `200` | Lines to capture from pane history |
| `use_separate_server` | boolean | `true` | Use dedicated tmux server |
| `socket_name` | string | `"kollabor"` | Socket name for separate server |

### Configuration File

Edit `~/.kollabor-cli/config.json`:

```json
{
  "plugins": {
    "tmux": {
      "enabled": true,
      "show_status": true,
      "refresh_rate": 0.1,
      "capture_lines": 200,
      "use_separate_server": true,
      "socket_name": "kollabor"
    }
  }
}
```

### Using Your Main Tmux Server

If you prefer to use your main tmux server instead of the isolated kollabor server:

```json
{
  "plugins": {
    "tmux": {
      "use_separate_server": false
    }
  }
}
```

## Architecture

### Plugin Structure

```python
class TmuxPlugin:
    - _tmux_cmd(*args) -> List[str]     # Build commands with socket config
    - _capture_tmux_pane(name) -> List[str]  # Capture session output
    - _send_keys_to_tmux(name, keys)    # Forward input to session
    - _get_all_tmux_sessions() -> List[str]  # Discover all sessions
    - _cycle_session(forward) -> str    # Navigate between sessions
```

### Data Models

```python
@dataclass
class TmuxSession:
    name: str                          # Session identifier
    command: str                       # Startup command
    tmux_cmd: callable                 # Command builder with socket
    created_at: datetime               # Creation timestamp
    pid: Optional[int]                 # Process ID
```

### Event Integration

The plugin integrates with the event system:

- **Command Registration**: Registers `/terminal` command via `SlashCommandRegistry`
- **Live Modal Trigger**: Emits `LIVE_MODAL_TRIGGER` for view mode
- **Status View**: Registers status view for session count display

### Input Callbacks

Live view mode handles keyboard input:

| Key | Action |
|-----|--------|
| `Escape` | Exit live view |
| `Opt+Left` / `Alt+Left` | Previous session |
| `Opt+Right` / `Alt+Right` | Next session |
| `Opt+x` (code 8776) | Kill current session |
| Arrow keys | Forward to tmux session |
| `Ctrl+C` | Forward interrupt to session |
| Text input | Forward to session |

## External Access

### Attaching from Terminal

When using the default separate server:

```bash
# List kollabor sessions
tmux -L kollabor list-sessions

# Attach to a session
tmux -L kollabor attach -t <session_name>

# Kill a session
tmux -L kollabor kill-session -t <session_name>
```

When using your main tmux server (`use_separate_server: false`):

```bash
# Use standard tmux commands (no -L flag)
tmux list-sessions
tmux attach -t <session_name>
```

### Socket Location

The kollabor tmux server socket is located at:
- macOS/Linux: `/tmp/tmux-<uid>/kollabor`

## Dependencies

- **subprocess**: Executing tmux commands
- **core.events**: Event bus integration, command registration
- **core.io.visual_effects**: AgnosterSegment for status display

## Error Handling

The plugin handles various error scenarios:

- **Tmux not available**: Plugin disables gracefully with warning
- **Session not found**: Returns error message with suggestions
- **Command timeout**: 2-second timeout on capture operations
- **Capture failures**: Returns error message in view

## Testing

### Manual Testing

```bash
# Start kollabor in tmux
tmux new-session -s test -x 120 -y 40 "python main.py"
sleep 3

# Create a session
tmux send-keys -t test "/t new test-echo echo hello" Enter
sleep 1

# View the session
tmux send-keys -t test "/t view" Enter
sleep 2

# Capture output
tmux capture-pane -t test -p

# Cleanup
tmux kill-session -t test
```

### Unit Tests

Located in `tests/tmux_integration/test_tmux_integration.py`:
- Session creation and discovery
- Capture pane functionality
- Key forwarding
- Session cycling

## Implementation Checklist

- [x] Dedicated tmux server with configurable socket
- [x] Session management (new, view, list, kill)
- [x] Live modal view with streaming
- [x] Keyboard input passthrough
- [x] Session cycling navigation
- [x] Configurable capture lines
- [x] Status bar integration
- [x] Command aliases (/t, /term, /tmux)
- [x] Help text and attach instructions
- [x] Error handling and timeouts

## Related Documentation

- **Slash Commands Guide**: `/docs/reference/slash-commands-guide.md`
- **Plugin Development**: `/CLAUDE.md` (Plugin System section)
- **Live Modal System**: `/docs/reference/modal-system-implementation-guide.md`
