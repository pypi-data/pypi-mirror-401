# Centralized Project Data Directory Specification

status: final
author: claude
date: 2026-01-12

## Overview

This specification describes changes to the .kollabor-cli directory system to:
1. Centralize project-specific data (conversations, logs) under ~/.kollabor-cli/projects/
2. Remove the need for local .kollabor-cli folders in project directories (cleaner repos)
3. Retain local .kollabor-cli ONLY for custom project-specific agents/skills (optional)
4. Merge global and local agents/skills with local taking precedence

## Directory Structure

### Global Home Directory

```
~/.kollabor-cli/
  config.json                    global user configuration
  agents/                        global agents (available everywhere)
    default/
      system_prompt.md
      agent.json
      [skills].md
    coder/
    research/
    ...
  projects/                      project-specific data
    Users_malmazan_dev_hello_world/
      config.json                project config overrides (optional)
      conversations/
        YYMMDDHHMM-session.jsonl
        snapshots/               conversation snapshots
        raw/                     raw conversation data
        conversation_memory/     intelligence cache
      logs/
        kollabor.log
    Users_malmazan_dev_other_project/
      conversations/
      logs/
```

### Local Project Directory (OPTIONAL)

Only created if user wants custom project-specific agents/skills:

```
/Users/malmazan/dev/hello_world/
  .kollabor-cli/                 OPTIONAL
    agents/
      my-custom-agent/
        system_prompt.md
        agent.json
        custom-skill.md
```

## Path Encoding

Project paths encoded by replacing path separators with underscores:

```
/Users/malmazan/dev/hello_world  ->  Users_malmazan_dev_hello_world
/home/user/projects/myapp        ->  home_user_projects_myapp
C:\Users\dev\project             ->  C_Users_dev_project (Windows)
```

implementation:
```python
def encode_project_path(project_path: Path) -> str:
    """Encode a project path to a safe directory name."""
    path_str = str(project_path.resolve())
    # Replace path separators with underscores
    encoded = path_str.replace("/", "_").replace("\\", "_")
    # Remove leading underscore if present (from root /)
    while encoded.startswith("_"):
        encoded = encoded[1:]
    return encoded

def decode_project_path(encoded: str) -> Path:
    """Decode an encoded project path back to a Path."""
    # Detect Windows paths (start with drive letter)
    if len(encoded) > 1 and encoded[1] == "_" and encoded[0].isalpha():
        # Windows: C_Users_... -> C:\Users\...
        path_str = encoded[0] + ":\\" + encoded[2:].replace("_", "\\")
    else:
        # Unix: Users_malmazan_... -> /Users/malmazan/...
        path_str = "/" + encoded.replace("_", "/")
    return Path(path_str)
```

## Resolution Priority

### Data Directories (conversations, logs)

ALWAYS use centralized location:
  ~/.kollabor-cli/projects/<encoded-path>/conversations/
  ~/.kollabor-cli/projects/<encoded-path>/logs/

### Config Resolution

1. local .kollabor-cli/config.json (if exists) - project overrides
2. ~/.kollabor-cli/projects/<encoded-path>/config.json - project defaults
3. ~/.kollabor-cli/config.json - global defaults

### Agent Resolution (--agent or /agent)

1. local .kollabor-cli/agents/<name>/ (project custom)
2. ~/.kollabor-cli/agents/<name>/ (global)

### Skill Resolution (--skill or /skill)

1. local .kollabor-cli/agents/<agent>/<skill>.md (project custom)
2. ~/.kollabor-cli/agents/<agent>/<skill>.md (global)

## Agent/Skill Listing Merge

When user runs /agent or /skill, show merged list with source indicators:

```
agents (local + global):
  [L] my-custom-agent    "Project-specific coding agent"
  [G] default            "General purpose assistant"
  [G] coder              "Fast implementation specialist"
  [G] research           "Investigation and analysis"
  [*] creative-writer    "Both local and global (local wins)"
```

legend:
  [L] = local only (project .kollabor-cli/agents/)
  [G] = global only (~/.kollabor-cli/agents/)
  [*] = exists in both (local takes precedence)

## Implementation Plan

### Phase 1: Core Path Utilities

file: core/utils/config_utils.py

new functions:
```python
def encode_project_path(project_path: Path) -> str:
    """Encode project path to safe directory name."""

def decode_project_path(encoded: str) -> Path:
    """Decode back to original path."""

def get_project_data_dir(project_path: Path = None) -> Path:
    """Get ~/.kollabor-cli/projects/<encoded>/ for current/given project."""

def get_conversations_dir(project_path: Path = None) -> Path:
    """Get conversations directory for project."""

def get_logs_dir(project_path: Path = None) -> Path:
    """Get logs directory for project."""

def get_local_agents_dir() -> Path | None:
    """Get local .kollabor-cli/agents/ if it exists, else None."""

def get_global_agents_dir() -> Path:
    """Get ~/.kollabor-cli/agents/."""
```

modified functions:
```python
def get_config_directory() -> Path:
    """Returns global ~/.kollabor-cli/ (no longer checks local for data)."""

def ensure_config_directory() -> Path:
    """Ensure global config dir and project data dir exist."""
```

### Phase 2: Update Application Initialization

file: core/application.py

changes:
```python
# In TerminalLLMChat.__init__():
self.config_dir = ensure_config_directory()  # Global ~/.kollabor-cli/
self.project_data_dir = get_project_data_dir()  # Project-specific
conversations_dir = get_conversations_dir()
conversations_dir.mkdir(parents=True, exist_ok=True)
```

### Phase 3: Update Logging Setup

file: core/logging/setup.py

changes:
```python
log_dir = get_logs_dir()
log_dir.mkdir(parents=True, exist_ok=True)
```

### Phase 4: Update Agent Manager

file: core/llm/agent_manager.py

add source tracking:
```python
@dataclass
class Agent:
    # ... existing fields ...
    source: str = "global"  # "local" or "global"
    overrides_global: bool = False
```

update discovery:
```python
def discover_agents(self) -> Dict[str, Agent]:
    """Discover agents from both local and global, local wins."""
    agents = {}

    # Load global agents first
    global_dir = get_global_agents_dir()
    for agent_dir in global_dir.iterdir():
        agent = Agent.from_directory(agent_dir)
        agent.source = "global"
        agents[agent.name] = agent

    # Load local agents (override global)
    local_dir = get_local_agents_dir()
    if local_dir:
        for agent_dir in local_dir.iterdir():
            agent = Agent.from_directory(agent_dir)
            agent.source = "local"
            if agent.name in agents:
                agent.overrides_global = True
            agents[agent.name] = agent

    return agents
```

### Phase 5: Update System Commands

file: core/commands/system_commands.py

changes:
- Show [L], [G], [*] indicators in agent/skill lists
- When creating agent, ask: local or global?
- Default to global for new agents

### Phase 6: Update Config Resolution

files: core/config/loader.py, core/config/service.py

new resolution order:
  1. Global: ~/.kollabor-cli/config.json
  2. Project: ~/.kollabor-cli/projects/<encoded>/config.json
  3. Local: .kollabor-cli/config.json (if exists)

## File Changes Summary

files to modify:
  core/utils/config_utils.py      Path utilities and resolution
  core/application.py             Initialization changes
  core/logging/setup.py           Log directory
  core/llm/agent_manager.py       Agent discovery merge
  core/commands/system_commands.py  UI for source indicators
  core/config/loader.py           Config resolution
  core/config/service.py          Config service updates

tests to add:
  tests/unit/test_path_encoding.py
  tests/unit/test_agent_merge.py

## Verification Plan

manual testing:
  1. Fresh start - verify dirs created in ~/.kollabor-cli/projects/
  2. Create local agent - verify [L] indicator
  3. Create global agent - verify [G] indicator
  4. Override global locally - verify [*] and local wins
  5. --agent flag - verify local>global priority
  6. --skill flag - verify correct source loading
  7. Conversations saved to project directory
  8. Logs saved to project directory
  9. Multiple projects - verify separate data directories

automated tests:
  - encode_project_path() with Unix/Windows paths
  - decode_project_path() round-trip
  - agent_merge_priority()
  - config_resolution_order()
