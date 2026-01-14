# Testing Setup Wizard in tmux

Quick guide for testing the setup wizard plugin interactively.

## Setup

```bash
# Create fresh tmux session
tmux kill-session -t kollabor-cli 2>/dev/null
tmux new-session -d -s kollabor-cli -c /Users/malmazan/dev/kollabor-cli

# Optional: Set env vars for testing
tmux send-keys -t kollabor-cli 'export KOLLABOR_DEFAULT_TOKEN=test-token' Enter
```

## Launch Setup Wizard

```bash
# Start app (wizard shows on first run, or use /setup command)
tmux send-keys -t kollabor-cli 'python main.py' Enter
sleep 3

# Or trigger wizard manually via command
tmux send-keys -t kollabor-cli '/setup' Enter
sleep 2

# Capture current screen
tmux capture-pane -t kollabor-cli -p
```

## Navigate Wizard Pages

```bash
# Page navigation
tmux send-keys -t kollabor-cli Enter      # Next page / confirm
tmux send-keys -t kollabor-cli Escape     # Previous page / cancel
tmux send-keys -t kollabor-cli Right      # Next page (on non-form pages)
tmux send-keys -t kollabor-cli Left       # Previous page
tmux send-keys -t kollabor-cli 'q'        # Skip wizard

# Form navigation (API config page)
tmux send-keys -t kollabor-cli Tab        # Next field
tmux send-keys -t kollabor-cli Down       # Next field
tmux send-keys -t kollabor-cli Up         # Previous field

# Capture after each action
tmux capture-pane -t kollabor-cli -p
```

## Wizard Pages

| Page | Content | Key Actions |
|------|---------|-------------|
| 0 | Welcome | Enter: begin, Q: skip |
| 1 | API Config | Tab: fields, Enter: next |
| 2 | Token/Settings | Enter: next |
| 3 | Shortcuts | Enter: next |
| 4 | Features | Enter: next |
| 5 | Ready/Summary | Enter: save & start |

## Text Input

```bash
# Type text into current field
tmux send-keys -t kollabor-cli 'my-profile-name'

# Backspace to delete
tmux send-keys -t kollabor-cli BSpace

# Clear and retype
tmux send-keys -t kollabor-cli C-u  # Clear line (if supported)
```

## Full Test Script

```bash
#!/bin/bash
# Full wizard walkthrough

# Setup
tmux kill-session -t kollabor-cli 2>/dev/null
tmux new-session -d -s kollabor-cli -c /Users/malmazan/dev/kollabor-cli
tmux send-keys -t kollabor-cli 'python main.py' Enter
sleep 3

# Page 0: Welcome -> Start
tmux send-keys -t kollabor-cli Enter
sleep 1
tmux capture-pane -t kollabor-cli -p

# Page 1: API Config - fill form
tmux send-keys -t kollabor-cli 'my-test-profile'  # Profile name
tmux send-keys -t kollabor-cli Tab
tmux send-keys -t kollabor-cli 'https://api.example.com'  # API URL
tmux send-keys -t kollabor-cli Tab
tmux send-keys -t kollabor-cli 'gpt-4'  # Model
tmux send-keys -t kollabor-cli Enter  # Next page
sleep 1
tmux capture-pane -t kollabor-cli -p

# Page 2: Token page
tmux send-keys -t kollabor-cli Enter
sleep 1

# Page 3-4: Skip through
tmux send-keys -t kollabor-cli Enter
sleep 1
tmux send-keys -t kollabor-cli Enter
sleep 1

# Page 5: Ready - Save
tmux capture-pane -t kollabor-cli -p
tmux send-keys -t kollabor-cli Enter  # Save & start
sleep 2
tmux capture-pane -t kollabor-cli -p
```

## Debugging

```bash
# Watch live output
tmux attach -t kollabor-cli

# Check logs
tail -f .kollabor-cli/logs/kollabor.log

# Check saved config
cat .kollabor-cli/config.json | python -m json.tool
```

## File Location

```
/Users/malmazan/dev/kollabor-cli/plugins/fullscreen/setup_wizard_plugin.py
```

## Fixed Issues

1. [x] Form fields need same UX as Edit Profile modal
2. [x] Add required/optional labels to sections
3. [x] Show env var hints clearly
4. [x] Add status/validation feedback
5. [x] Token field should show env var name
6. [x] Temperature in "Advanced" section

## Notes

- API config page now has "Connection (required)", "Model (required)", "Advanced (optional)" sections
- Token page shows env var name dynamically based on profile name (KOLLABOR_{PROFILE}_TOKEN)
- Token page displays masked token value when env var is set
- Ready page shows configuration summary with [ok]/[--] status icons
- Validation status shows what's missing (endpoint, model, token)
