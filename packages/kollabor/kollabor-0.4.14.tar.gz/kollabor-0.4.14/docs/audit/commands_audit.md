# Commands Directory Audit

Audit of core/commands/ directory to determine what is CORE infrastructure
vs PLUGIN functionality.

## Summary

The commands directory contains both CORE infrastructure (command registry,
parser, executor) and built-in commands that could be plugins.

**Total Files:** 6
**CORE Infrastructure:** 5 files
**PLUGIN Candidates:** 1 file (containing 8 commands)

---

## CORE Infrastructure (Keep in core/)

### core/commands/__init__.py
**status:** CORE
**reason:** Module exports only, part of core package structure
**notes:** Re-exports event model types, no logic

### core/commands/parser.py
**status:** CORE
**reason:** Essential command parsing infrastructure
**notes:**
- SlashCommandParser class
- Command detection and validation
- Argument parsing with shlex
- Parameter extraction
- Without this, command system cannot function

### core/commands/executor.py
**status:** CORE
**reason:** Essential command execution infrastructure
**notes:**
- SlashCommandExecutor class
- Executes command handlers with event integration
- Error handling and result processing
- Modal triggering orchestration
- Without this, commands cannot run

### core/commands/registry.py
**status:** CORE
**reason:** Essential command registration infrastructure
**notes:**
- SlashCommandRegistry class
- Command registration and lookup
- Conflict detection
- Plugin command tracking
- Search and discovery
- Without this, plugins cannot register commands

### core/commands/menu_renderer.py
**status:** CORE (borderline)
**reason:** Command menu is part of the command system infrastructure
**notes:**
- CommandMenuRenderer class
- Renders interactive command menu when user types '/'
- Filtering and navigation
- Could be argued as plugin, but menu discovery is core UX

---

## PLUGIN Candidates (Should be plugins)

### core/commands/system_commands.py

**status:** SHOULD BE PLUGIN(S)
**reason:** Contains 8 built-in commands that are optional features

This file is essentially a "built-in plugin" that could be split into
multiple plugins. The SystemCommandsPlugin class follows the plugin pattern
but lives in core/.

#### Built-in Commands Analysis:

| Command | Category | Current | Should Be | Priority | Reason |
|---------|----------|---------|-----------|----------|--------|
| /help | SYSTEM | core | **CORE** | n/a | Essential for discoverability |
| /version | SYSTEM | core | **CORE** | n/a | Basic app info |
| /config | SYSTEM | core | PLUGIN | low | Configuration editing is optional |
| /status | SYSTEM | core | PLUGIN | low | Diagnostics are optional |
| /resume | CONVERSATION | core | PLUGIN | medium | Session management feature |
| /profile | SYSTEM | core | PLUGIN | high | Profile management is optional |
| /agent | AGENT | core | PLUGIN | high | Agent system is optional |
| /skill | AGENT | core | PLUGIN | high | Skills are agent-specific |

#### Recommended Plugin Splits:

1. **CORE (keep in system_commands.py):**
   - `/help` - Minimal help showing basic commands
   - `/version` - Show version info

2. **ProfileManagementPlugin (NEW):**
   - `/profile` command
   - All profile CRUD operations
   - Profile selection modal
   - Create/edit/delete profile handlers
   - **complexity:** medium
   - **dependencies:** profile_manager, llm_service, event_bus

3. **AgentManagementPlugin (NEW):**
   - `/agent` command
   - Agent selection, creation, editing, deletion
   - Agent modal definitions
   - **complexity:** medium
   - **dependencies:** agent_manager, llm_service, event_bus

4. **SkillManagementPlugin (NEW):**
   - `/skill` command
   - Skill load/unload/toggle
   - Skill creation, editing, deletion
   - **complexity:** medium
   - **dependencies:** agent_manager, llm_service, event_bus

5. **ConfigurationPlugin (NEW):**
   - `/config` command
   - Config tree modal
   - Config editing UI
   - **complexity:** low
   - **dependencies:** config_manager, event_bus

6. **DiagnosticsPlugin (NEW):**
   - `/status` command
   - System status display
   - **complexity:** low
   - **dependencies:** command_registry, event_bus

7. **SessionPlugin (NEW):**
   - `/resume` command
   - Session selection, search, filter
   - **complexity:** high
   - **dependencies:** conversation_manager, llm_service, event_bus

---

## Migration Recommendations

### Phase 1: Extract Profile Management (High Priority)
**complexity:** medium
**dependencies:** profile_manager, llm_service integration

Move `/profile` command to plugins/profile_management_plugin.py

### Phase 2: Extract Agent/Skill Management (High Priority)
**complexity:** medium
**dependencies:** agent_manager, modal definitions

Move `/agent` and `/skill` commands to plugins/agent_management_plugin.py

### Phase 3: Extract Configuration (Low Priority)
**complexity:** low
**dependencies:** config_manager integration

Move `/config` to plugins/configuration_plugin.py

### Phase 4: Extract Diagnostics (Low Priority)
**complexity:** low
**dependencies:** minimal

Move `/status` to plugins/diagnostics_plugin.py

### Phase 5: Extract Session Management (Medium Priority)
**complexity:** high
**dependencies:** conversation_manager, search functionality

Move `/resume` to plugins/session_plugin.py

### Keep in Core
- `/help` - Essential for new users
- `/version` - Basic application info

---

## Estimated Migration Effort

| Plugin | Lines to Move | Complexity | Estimated Effort |
|--------|---------------|------------|------------------|
| ProfileManagementPlugin | ~800 | medium | 2-3 hours |
| AgentManagementPlugin | ~600 | medium | 2-3 hours |
| SkillManagementPlugin | ~400 | medium | 1-2 hours |
| ConfigurationPlugin | ~100 | low | 1 hour |
| DiagnosticsPlugin | ~50 | low | 0.5 hours |
| SessionPlugin | ~400 | high | 3-4 hours |

**Total:** ~2350 lines, ~10-14 hours

---

## Post-Migration Structure

```
core/commands/
  __init__.py           # Module exports
  parser.py             # Command parsing (CORE)
  executor.py           # Command execution (CORE)
  registry.py           # Command registration (CORE)
  menu_renderer.py      # Command menu UI (CORE)
  system_commands.py    # /help, /version only (CORE, simplified)

plugins/
  profile_management_plugin.py    # /profile
  agent_management_plugin.py       # /agent
  skill_management_plugin.py       # /skill (could merge with agent)
  configuration_plugin.py          # /config
  diagnostics_plugin.py            # /status
  session_plugin.py                # /resume
```

---

## Risks and Considerations

1. **User Expectations:** Users may expect these commands to be built-in
   - Mitigation: Include core plugins in default installation

2. **Dependency Management:** Commands depend on profile_manager, agent_manager
   - Mitigation: Use dependency injection, check for None gracefully

3. **Modal Definitions:** Heavy use of modal definitions in handlers
   - Mitigation: Keep modal rendering in core UI, only handlers move

4. **Event Integration:** Commands use event_bus for coordination
   - Mitigation: Ensure event bus available to all plugins

5. **Testing:** Each command has multiple code paths
   - Mitigation: Migrate tests alongside commands
