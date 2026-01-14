# Default Agent Specification

## Overview

This document specifies the implementation of default agent selection at both project and global levels, similar to how skill defaults work per-agent.

The feature allows users to:
- Set a project-level default agent (saved in `.kollabor-cli/config.json`)
- Set a global default agent (saved in `~/.kollabor-cli/config.json`)
- Toggle defaults via keyboard shortcuts in the `/agent` modal

## Motivation

Currently, Kollabor CLI always starts with the "default" agent on startup unless explicitly specified via `--agent` CLI argument. Users working on specific projects with specialized agents must manually switch agents every session.

This feature provides:
- Project-specific defaults (e.g., "coder" agent for backend projects)
- Global defaults for personal preference
- Consistent workflow with skill defaults (which use 's' key)

## Priority Order

Agent selection on startup follows this priority (highest to lowest):

1. **CLI argument**: `kollab --agent <name>` (one-time override, not persisted)
2. **Project default**: `.kollabor-cli/config.json` (project-specific)
3. **Global default**: `~/.kollabor-cli/config.json` (user preference)
4. **Fallback**: Agent named "default" in `agents/default/`

## Config Structure

### Global Config (`~/.kollabor-cli/config.json`)

```json
{
  "core": {
    "llm": {
      "default_agent": {
        "name": "coder",
        "level": "global"
      }
    }
  }
}
```

### Local Config (`.kollabor-cli/config.json`)

```json
{
  "core": {
    "llm": {
      "default_agent": {
        "name": "lint-editor",
        "level": "project"
      }
    }
  }
}
```

If an agent is set as default at both levels, project takes precedence (matches config resolution order).

## UI Changes

### Agent Modal Footer

```
↑↓ nav • Enter select • s project default • g global default • e edit • d del • Esc
```

### Agent List Indicators

| Indicator | Meaning |
|-----------|---------|
| `[*D]` | Active + Project Default |
| `[*G]` | Active + Global Default |
| `[*DG]`| Active + Both Project and Global Defaults |
| `[ D]` | Project Default (not active) |
| `[ G]` | Global Default (not active) |
| `[DG]` | Both Project and Global Defaults (not active) |
| `[*]` | Active only |
| `[  ]` | Neither active nor default |

Examples:
```
[*D] coder            Code specialist agent
[  ] default           General purpose agent
[ G] research          Investigation agent (global default)
```

### Modal Actions

| Key | Action | Behavior |
|-----|--------|----------|
| `s` | Toggle Project Default | Sets/clears project default for selected agent |
| `g` | Toggle Global Default | Sets/clears global default for selected agent |

## Implementation

### 1. Config Utilities (`core/utils/config_utils.py`)

Add functions to manage default agent settings:

```python
def get_default_agent() -> tuple[Optional[str], Optional[str]]:
    """
    Get the default agent from config.
    
    Returns:
        Tuple of (agent_name, level) where level is "project" or "global"
        Returns (None, None) if no default configured
    """
    # Check project-level first
    local_config_path = Path.cwd() / ".kollabor-cli" / "config.json"
    if local_config_path.exists():
        try:
            with open(local_config_path) as f:
                config = json.load(f)
                default = config.get("core", {}).get("llm", {}).get("default_agent")
                if default and default.get("level") == "project":
                    return (default.get("name"), "project")
        except Exception:
            pass
    
    # Check global-level
    global_config_path = Path.home() / ".kollabor-cli" / "config.json"
    if global_config_path.exists():
        try:
            with open(global_config_path) as f:
                config = json.load(f)
                default = config.get("core", {}).get("llm", {}).get("default_agent")
                if default and default.get("level") == "global":
                    return (default.get("name"), "global")
        except Exception:
            pass
    
    return (None, None)

def set_default_agent(agent_name: str, level: str) -> bool:
    """
    Set a default agent in config.
    
    Args:
        agent_name: Name of agent to set as default
        level: "project" or "global"
        
    Returns:
        True if saved successfully
    """
    if level == "project":
        config_path = Path.cwd() / ".kollabor-cli" / "config.json"
    else:
        config_path = Path.home() / ".kollabor-cli" / "config.json"
    
    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing config or create new
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {}
    
    # Ensure structure exists
    if "core" not in config:
        config["core"] = {}
    if "llm" not in config["core"]:
        config["core"]["llm"] = {}
    
    # Set default
    config["core"]["llm"]["default_agent"] = {
        "name": agent_name,
        "level": level
    }
    
    # Save
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return True

def clear_default_agent(level: str) -> bool:
    """
    Clear the default agent from config.
    
    Args:
        level: "project" or "global"
        
    Returns:
        True if cleared successfully
    """
    if level == "project":
        config_path = Path.cwd() / ".kollabor-cli" / "config.json"
    else:
        config_path = Path.home() / ".kollabor-cli" / "config.json"
    
    if not config_path.exists():
        return True  # Nothing to clear
    
    with open(config_path) as f:
        config = json.load(f)
    
    # Remove default_agent entry
    if "core" in config and "llm" in config["core"]:
        config["core"]["llm"].pop("default_agent", None)
    
    # Save
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return True

def get_all_default_agents() -> dict[str, str]:
    """
    Get all default agents from both config levels.
    
    Returns:
        Dict mapping level -> agent_name, e.g. {"project": "coder", "global": "research"}
        Only includes levels that have a default set
    """
    defaults = {}
    
    # Check project
    local_config_path = Path.cwd() / ".kollabor-cli" / "config.json"
    if local_config_path.exists():
        try:
            with open(local_config_path) as f:
                config = json.load(f)
                default = config.get("core", {}).get("llm", {}).get("default_agent")
                if default and default.get("level") == "project":
                    defaults["project"] = default.get("name")
        except Exception:
            pass
    
    # Check global
    global_config_path = Path.home() / ".kollabor-cli" / "config.json"
    if global_config_path.exists():
        try:
            with open(global_config_path) as f:
                config = json.load(f)
                default = config.get("core", {}).get("llm", {}).get("default_agent")
                if default and default.get("level") == "global":
                    defaults["global"] = default.get("name")
        except Exception:
            pass
    
    return defaults
```

### 2. Agent Manager (`core/llm/agent_manager.py`)

Add method to load default agent on startup:

```python
def load_default_agent(self, cli_agent_name: Optional[str] = None) -> Optional[str]:
    """
    Load the appropriate default agent based on priority.
    
    Priority:
    1. CLI agent name (highest, one-time override)
    2. Project default (.kollabor-cli/config.json)
    3. Global default (~/.kollabor-cli/config.json)
    4. Fallback to "default" agent
    
    Args:
        cli_agent_name: Agent name from CLI --agent argument
        
    Returns:
        Name of agent that was activated, or None if failed
    """
    from ..utils.config_utils import get_default_agent
    
    # Priority 1: CLI argument (one-time override)
    if cli_agent_name:
        if self.set_active_agent(cli_agent_name):
            logger.info(f"Loaded agent from CLI argument: {cli_agent_name}")
            return cli_agent_name
        else:
            logger.warning(f"CLI agent '{cli_agent_name}' not found, trying defaults")
    
    # Priority 2: Project default
    project_agent, level = get_default_agent()
    if level == "project" and project_agent:
        if self.set_active_agent(project_agent):
            logger.info(f"Loaded project default agent: {project_agent}")
            return project_agent
        else:
            logger.warning(f"Project default agent '{project_agent}' not found, trying next level")
    
    # Priority 3: Global default
    global_agent, level = get_default_agent()
    if level == "global" and global_agent:
        if self.set_active_agent(global_agent):
            logger.info(f"Loaded global default agent: {global_agent}")
            return global_agent
        else:
            logger.warning(f"Global default agent '{global_agent}' not found, trying fallback")
    
    # Priority 4: Fallback to "default" agent
    if self.set_active_agent("default", load_defaults=True):
        logger.info("Loaded fallback default agent")
        return "default"
    
    logger.error("Failed to load any agent")
    return None
```

### 3. System Commands (`core/commands/system_commands.py`)

#### Update Modal Definition

Modify `_get_agents_modal_definition()` to show default indicators:

```python
def _get_agents_modal_definition(self, skip_reload: bool = False) -> Optional[Dict[str, Any]]:
    """Get modal definition for agent selection with default indicators."""
    from ..utils.config_utils import get_all_default_agents
    
    # Get all default agents
    default_agents = get_all_default_agents()  # {"project": "coder", "global": "research"}
    project_default = default_agents.get("project")
    global_default = default_agents.get("global")
    
    # Refresh and get agents
    if not skip_reload:
        self.agent_manager.refresh()
    
    agents = self.agent_manager.list_agents()
    active_agent = self.agent_manager.get_active_agent()
    active_name = active_agent.name if active_agent else None
    
    if not agents:
        return None
    
    # Build agent list with indicators
    agent_items = []
    for agent in agents:
        is_active = agent.name == active_name
        is_project_default = agent.name == project_default
        is_global_default = agent.name == global_default
        
        # Build indicator
        indicator_parts = []
        if is_active:
            indicator_parts.append("*")
        if is_project_default:
            indicator_parts.append("D")
        if is_global_default:
            indicator_parts.append("G")
        
        indicator = "".join(indicator_parts) if indicator_parts else "  "
        
        skills = agent.list_skills()
        skill_count = f" ({len(skills)} skills)" if skills else ""
        description = agent.description or "No description"
        
        agent_items.append({
            "name": f"[{indicator}] {agent.name}{skill_count}",
            "description": description,
            "agent_name": agent.name,
            "action": "select_agent",
            "is_active": is_active,
            "is_project_default": is_project_default,
            "is_global_default": is_global_default
        })
    
    # Add clear option
    agent_items.append({
        "name": "    [Clear Agent]",
        "description": "Use default system prompt behavior",
        "agent_name": None,
        "action": "clear_agent"
    })
    
    return {
        "title": "Agents",
        "footer": "↑↓ nav • Enter select • s project default • g global default • e edit • d del • Esc",
        "width": 70,
        "height": 18,
        "sections": [
            {
                "title": f"Available Agents (active: {active_name or 'none'})",
                "commands": agent_items
            }
        ],
        "actions": [
            {"key": "Enter", "label": "Select", "action": "select"},
            {"key": "s", "label": "Project Default", "action": "toggle_project_default"},
            {"key": "g", "label": "Global Default", "action": "toggle_global_default"},
            {"key": "e", "label": "Edit", "action": "edit_agent_prompt"},
            {"key": "d", "label": "Delete", "action": "delete_agent_prompt"},
            {"key": "Escape", "label": "Close", "action": "cancel"}
        ]
    }
```

#### Add Modal Action Handlers

Add handlers for 's' and 'g' key presses in `_handle_modal_command()`:

```python
# Handle toggle project default
elif action == "toggle_project_default":
    agent_name = command.get("agent_name")
    if agent_name and self.agent_manager:
        from ..utils.config_utils import get_all_default_agents, set_default_agent, clear_default_agent
        
        # Check if this agent is already project default
        defaults = get_all_default_agents()
        current_project_default = defaults.get("project")
        
        if current_project_default == agent_name:
            # Clear it
            if clear_default_agent("project"):
                data["display_messages"] = [
                    ("system", f"[ok] Cleared project default agent", {}),
                ]
        else:
            # Set it
            if set_default_agent(agent_name, "project"):
                data["display_messages"] = [
                    ("system", f"[ok] Set '{agent_name}' as project default agent", {}),
                ]
            else:
                data["display_messages"] = [
                    ("error", f"[err] Failed to set project default", {}),
                ]
        
        # Reopen modal to show updated indicators
        modal_def = self._get_agents_modal_definition(skip_reload=True)
        if modal_def:
            data["show_modal"] = modal_def

# Handle toggle global default
elif action == "toggle_global_default":
    agent_name = command.get("agent_name")
    if agent_name and self.agent_manager:
        from ..utils.config_utils import get_all_default_agents, set_default_agent, clear_default_agent
        
        # Check if this agent is already global default
        defaults = get_all_default_agents()
        current_global_default = defaults.get("global")
        
        if current_global_default == agent_name:
            # Clear it
            if clear_default_agent("global"):
                data["display_messages"] = [
                    ("system", f"[ok] Cleared global default agent", {}),
                ]
        else:
            # Set it
            if set_default_agent(agent_name, "global"):
                data["display_messages"] = [
                    ("system", f"[ok] Set '{agent_name}' as global default agent", {}),
                ]
            else:
                data["display_messages"] = [
                    ("error", f"[err] Failed to set global default", {}),
                ]
        
        # Reopen modal to show updated indicators
        modal_def = self._get_agents_modal_definition(skip_reload=True)
        if modal_def:
            data["show_modal"] = modal_def
```

### 4. Application Startup (`core/application.py`)

Replace hardcoded default agent logic with new system:

**Before (lines 141-149):**
```python
self.agent_manager = AgentManager(self.config)
if agent_name:
    if not self.agent_manager.set_active_agent(agent_name):
        logger.warning(f"Agent '{agent_name}' not found")
else:
    # Load default skills for the default agent on startup
    default_agent = self.agent_manager.get_agent("default")
    if default_agent and default_agent.default_skills:
        self.agent_manager.set_active_agent("default", load_defaults=True)
```

**After:**
```python
self.agent_manager = AgentManager(self.config)
# Load default agent using priority system (CLI > project > global > fallback)
if not self.agent_manager.load_default_agent(agent_name):
    logger.warning("Failed to load any agent, system may not function correctly")
```

## Behavior Specifications

### Setting Defaults

1. **Project Default ('s' key)**:
   - Saves to `.kollabor-cli/config.json`
   - Overrideable by `--agent` CLI argument
   - Takes precedence over global default

2. **Global Default ('g' key)**:
   - Saves to `~/.kollabor-cli/config.json`
   - Used when no project default exists
   - Fallback when project default agent is not found

3. **Clearing Defaults**:
   - Pressing the same key again clears the default
   - Only one agent can be default per level

### Startup Flow

```
1. Check CLI --agent argument
   ├─ Found and valid → Use it (don't persist)
   └─ Not found or invalid → Continue
2. Check project default (.kollabor-cli/config.json)
   ├─ Found and valid → Use it
   └─ Not found or invalid → Continue
3. Check global default (~/.kollabor-cli/config.json)
   ├─ Found and valid → Use it
   └─ Not found or invalid → Continue
4. Fallback to "default" agent
   └─ Always try to load agent named "default"
```

### Edge Cases

1. **Default agent deleted**:
   - Log warning and fall through to next priority level
   - Config entry remains (user can re-create agent)

2. **Local config doesn't exist**:
   - Skip project default check
   - Continue to global default

3. **Both levels have same agent**:
   - Show both indicators: `[*DG]`
   - Still works correctly (only sets active once)

4. **No default configured**:
   - Falls back to "default" agent
   - Normal behavior (same as current system)

5. **Config file corrupted**:
   - Log error, continue without defaults
   - Doesn't crash the application

## Comparison with Skill Defaults

| Aspect | Skill Defaults | Agent Defaults |
|--------|---------------|----------------|
| **Storage** | Per-agent in `agent.json` | Config file (`config.json`) |
| **Scope** | Per-agent | Global or project-level |
| **Quantity** | Multiple per agent | One per level (project/global) |
| **Activation** | Auto-load when agent activates | Determines startup agent |
| **UI Key** | 's' key only | 's' (project) and 'g' (global) |
| **Persistence** | Saved with agent config | Saved in config files |

## Testing Checklist

- [ ] Project default saved to `.kollabor-cli/config.json`
- [ ] Global default saved to `~/.kollabor-cli/config.json`
- [ ] 's' key toggles project default correctly
- [ ] 'g' key toggles global default correctly
- [ ] Modal indicators display correctly for all combinations
- [ ] Startup respects priority order (CLI > project > global > fallback)
- [ ] Missing default agent falls through gracefully
- [ ] Local config missing skips project default check
- [ ] Config corruption doesn't crash application
- [ ] Same agent as both defaults shows `[*DG]` indicator
- [ ] Clearing default works correctly

## Migration Notes

No migration needed for existing users:
- System falls back to "default" agent if no defaults configured
- Existing behavior preserved (starts with "default" agent)
- Users opt-in by setting defaults via modal

## Future Enhancements

Potential future improvements:
1. Profile-specific defaults (different agent per LLM profile)
2. Directory-based defaults (different agent per subdirectory)
3. Time-based defaults (different agent for morning vs evening work)
4. Context-aware defaults (detect project type and auto-select agent)
