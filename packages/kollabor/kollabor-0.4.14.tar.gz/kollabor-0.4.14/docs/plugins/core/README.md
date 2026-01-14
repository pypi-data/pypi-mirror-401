# Core Plugins Specifications

This directory contains comprehensive specifications for Kollabor CLI core plugins.

## Purpose

Core plugin specs provide complete architectural documentation for recreating,
understanding, and extending Kollabor's plugin system. Each spec includes:

- Architecture overview and design patterns
- Complete API documentation with method signatures
- Data models and type definitions
- UI workflows and interaction patterns
- Event system integration
- Error handling strategies
- Testing strategies with mock dependencies
- Implementation checklists

## Available Specs

### tmux_plugin_spec.md

Comprehensive specification for the Tmux Plugin.

features:
  - tmux session management (new, view, list, kill)
  - live streaming view with keyboard passthrough
  - isolated tmux server (configurable)
  - session cycling with keyboard navigation
  - configurable capture lines from history

slash commands:
  - /terminal new <name> [cmd]   create session
  - /terminal view [name]        live view (cycles if no name)
  - /terminal list               list all sessions
  - /terminal kill <name>        kill session
  - /t                           alias for /terminal

architecture:
  - isolated tmux server with configurable socket
  - live modal integration with input callback
  - status bar integration

### resume_conversation_plugin_spec.md

Comprehensive specification for the Resume Conversation Plugin.

features:
  - session management (resume, browse, search, filter)
  - conversation branching from any message point
  - modal-based interactive session selection
  - search with relevance scoring
  - current conversation branching

slash commands:
  - /resume [id] [--force]      resume or browse sessions
  - /sessions [search query]    browse or search
  - /branch [id] [index]        three-step branching workflow

architecture:
  - event-driven with MODAL_COMMAND_SELECTED hook
  - dependency injection (6 services)
  - modal UI with keyboard navigation
  - message coordinator integration

## Usage

These specs are intended for:

1. recreating plugins from scratch
2. understanding plugin architecture patterns
3. extending existing plugins
4. training new developers on plugin system
5. documenting plugin capabilities

## Directory Structure

```
docs/plugins/
├── core/                        # Core plugin specifications
│   ├── README.md               # This file
│   ├── tmux_plugin_spec.md     # Tmux session management
│   └── resume_conversation_plugin_spec.md
└── community/                   # Community plugin specs (future)
```

## Related Documentation

- /docs/reference/hook-system-sdk.md      # Hook system development guide
- /docs/reference/slash-commands-guide.md # Slash command system
- /docs/features/RESUME_COMMAND_SPEC.md   # Resume feature requirements
- /CLAUDE.md                              # Plugin development guidelines

## Contributing

When adding new plugin specs, ensure they include:

- [x] complete architecture overview
- [x] all method signatures with docstrings
- [x] data model definitions
- [x] workflow diagrams
- [x] event system integration details
- [x] error handling patterns
- [x] testing strategy
- [x] implementation checklist
- [x] configuration examples
- [x] dependency requirements

## Maintenance

Plugin specs should be updated when:

- plugin architecture changes significantly
- new features are added to plugins
- event system integration changes
- data models are modified
- breaking changes are introduced

Keep specs synchronized with actual plugin implementations to ensure
they remain useful as reference documentation.
