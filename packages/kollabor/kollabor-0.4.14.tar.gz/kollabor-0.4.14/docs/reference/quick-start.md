# Quick Start Guide

Get up and running with Kollabor CLI in minutes.

## Installation

The easiest way to install Kollabor:

```bash
pip install kollabor
```

Or use the one-line installer (auto-detects best method):

```bash
curl -sS https://raw.githubusercontent.com/kollaborai/kollabor-cli/main/install.sh | bash
```

macOS users can also use Homebrew:

```bash
brew install kollaborai/tap/kollabor
```

## First Run

Start Kollabor by running:

```bash
kollab
```

On first run, Kollabor creates:
- `~/.kollabor-cli/config.json` - Your configuration file
- `~/.kollabor-cli/projects/` - Project-specific conversations and logs

## Setting Up Your LLM

Before chatting, you need to configure an LLM provider. Kollabor works with any OpenAI-compatible API.

### Option 1: Environment Variables (Recommended)

Set these in your shell or `.env` file:

```bash
export KOLLABOR_API_ENDPOINT="https://api.openai.com/v1/chat/completions"
export KOLLABOR_API_TOKEN="sk-your-api-key-here"
export KOLLABOR_API_MODEL="gpt-4"
```

### Option 2: Using Profiles

Run Kollabor and type:

```
/profile create
```

Fill in the form:
- **Name**: A label for this profile (e.g., "openai", "local")
- **API URL**: Your API endpoint
- **API Key**: Your API token/key
- **Model**: The model name to use

Switch profiles anytime:

```
/profile set openai
```

List available profiles:

```
/profile list
```

## Basic Usage

### Chatting

Just type your message and press Enter:

```
How do I reverse a list in Python?
```

The LLM will respond in real-time. Type your next message when ready.

### Multi-line Input

Press `Alt+Enter` (or `Esc+Enter`) to insert a line break without sending. This lets you write multi-line prompts:

```
Here's a function I wrote:
def foo():
    pass

Can you explain what it does?
```

### Slash Commands

Type `/` to see available commands. Use arrow keys to navigate, Enter to select.

Common commands:
- `/help` - Show all commands
- `/save` - Save conversation
- `/profile` - Manage LLM profiles
- `/config` - Open settings
- `/version` - Show version info

## Essential Commands

### /help

Shows all available slash commands with descriptions. Type:

```
/help
```

Or use aliases: `h` or `?`

### /save

Save your conversation in various formats:

```
/save                    # Save to file (transcript format)
/save clipboard          # Copy to clipboard
/save local              # Save to current directory
/save markdown local     # Save as markdown to current directory
```

Aliases: `export`, `transcript`

### /profile

Manage your LLM API profiles:

```
/profile list            # Show all profiles
/profile set <name>      # Switch to a profile
/profile create          # Create a new profile
```

Aliases: `prof`, `llm`

### /config

Open the interactive configuration panel:

```
/config
```

Use arrow keys to navigate, Enter to toggle/edit, Ctrl+S to save, Escape to cancel.

Aliases: `settings`, `preferences`

### /terminal

Manage tmux sessions (if you use tmux):

```
/terminal list           # List sessions
/terminal new mysession   # Create new session
/terminal attach mysession  # Attach to session
```

Aliases: `tmux`, `term`, `t`

## Configuration File

Your settings live in `~/.kollabor-cli/config.json`. You can edit directly or use `/config`.

Key settings:

```json
{
  "core": {
    "llm": {
      "api_url": "https://api.openai.com/v1/chat/completions",
      "model": "gpt-4",
      "temperature": 0.7,
      "max_tokens": 4096
    }
  },
  "terminal": {
    "render_fps": 20
  }
}
```

## Common Workflows

### Quick Question

```bash
kollab "Explain recursion in simple terms"
```

### Interactive Session

```bash
kollab
# Then chat naturally
```

### Scripting with Pipe Mode

```bash
echo "Summarize this: $(cat report.txt)" | kollab -p
```

### Save Important Conversations

```
/chatting...
/save markdown important-chat.md
```

## Tips and Tricks

- **Arrow Up**: Recall previous messages in your current session
- **Ctrl+C**: Copy text (if enabled in config) or exit
- **Tab**: Type `/` then use Tab to complete command names
- **Multiple Projects**: Each directory gets its own conversation history
- **Color Mode**: Force specific colors with `KOLLABOR_COLOR_MODE=truecolor`

## Getting Help

- `/help` - Show available commands
- `/status` - View system diagnostics
- Check logs: `~/.kollabor-cli/projects/<encoded-path>/logs/kollabor.log`

## Next Steps

- Explore plugins in `~/.kollabor-cli/agents/`
- Customize your system prompt
- Read the full documentation at [docs/](../)
