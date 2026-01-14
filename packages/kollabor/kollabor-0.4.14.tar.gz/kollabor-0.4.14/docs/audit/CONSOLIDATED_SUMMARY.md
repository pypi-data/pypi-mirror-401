# Core vs Plugin Audit - Consolidated Summary

**Date:** 2025-01-07
**Agents:** 6 parallel auditors
**Scope:** Entire codebase core/ vs plugins/ separation

---

## Executive Summary

The audit reveals significant opportunity to reduce core bloat and create a true marketplace-ready plugin ecosystem. Currently **~8,000+ lines of code** in core/ should be moved to plugins/.

### By the Numbers

| Area | Total Files | Should Stay Core | Should Be Plugin | Lines to Move |
|------|-------------|------------------|------------------|---------------|
| LLM Services | 15 | 8 | 5 (+ 2 hybrid) | ~3,853 |
| I/O System | 12 | 6 | 6 (partial) | ~1,952 |
| Commands | 6 | 5 | 1 (split into 7) | ~2,350 |
| UI | 16 | 8 | 8 | ~1,200 |
| Effects | 2 | 0 | 2 | ~1,500 |
| Plugins | 9 | 0 | 9 (correct) | 0 |
| **TOTAL** | **60** | **27** | **31+** | **~10,855** |

**Core Bloat:** Currently carrying 10,855+ lines that should be plugins (~36% reduction possible)

---

## Critical Findings by Area

### 1. Commands (HIGH PRIORITY)

**Problem:** Built-in commands in `core/commands/system_commands.py` are not plugins

**Impact:** 8 commands hardcoded in core when only 2 should be

| Command | Current | Should Be | Priority |
|---------|---------|-----------|----------|
| /help | core | **CORE** | n/a |
| /version | core | **CORE** | n/a |
| /profile | core | PLUGIN | HIGH |
| /agent | core | PLUGIN | HIGH |
| /skill | core | PLUGIN | HIGH |
| /config | core | PLUGIN | LOW |
| /status | core | PLUGIN | LOW |
| /resume | core | PLUGIN | MEDIUM |

**Recommended Plugins:**
- ProfileManagementPlugin (~800 lines)
- AgentManagementPlugin (~600 lines)
- SkillManagementPlugin (~400 lines)
- ConfigurationPlugin (~100 lines)
- DiagnosticsPlugin (~50 lines)
- SessionPlugin (~400 lines)

**Complexity:** Medium
**Effort:** 10-14 hours

---

### 2. Visual Effects (HIGH PRIORITY)

**Problem:** `core/io/visual_effects.py` is 1,386 lines of mostly plugin-worthy effects

**Impact:** Largest single file in core/ - contains marketplace-ready features

**Keep in Core:**
- ColorSupport enum, detect_color_support()
- Basic color palette (ANSI colors)
- rgb_to_256() conversion utility

**Move to Plugins:**
- ShimmerEffect, PulseEffect, ScrambleEffect
- GradientRenderer (all gradient methods)
- AgnosterSegment (powerline segments)
- StatusColorizer (semantic coloring)
- BannerRenderer (ASCII banners)
- VisualEffects coordinator

**Also move:**
- `core/fullscreen/components/matrix_components.py` → `plugins/fullscreen/`
- `core/io/core_status_views.py` → `plugins/default_status_views.py`
- `core/io/config_status_view.py` → `plugins/config_status_plugin.py`
- ThinkingAnimationManager from `core/io/layout.py` → `plugins/thinking_animation_plugin.py`

**Marketplace Value:**
- Matrix Rain Effect - $0.99
- Shimmer Animation - $0.49
- Gradient Theme Pack - $1.99
- Powerline Status - $0.99
- Custom Banner - $1.49

**Complexity:** HIGH
**Effort:** 2-3 days

---

### 3. LLM Services (HIGH PRIORITY)

**Problem:** Core contains 5 major feature files that should be plugins

**Impact:** 55% of core/llm/ code should be plugins

| File | Lines | Should Be | Reason |
|------|-------|-----------|--------|
| mcp_integration.py | ~300 | PLUGIN | MCP integrations are optional |
| model_router.py | ~200 | PLUGIN | Routing strategies are customizable |
| file_operations_executor.py | ~1,423 | PLUGIN | Tool implementations are features |
| agent_manager.py | ~876 | PLUGIN | Multi-agent is advanced feature |
| profile_manager.py | ~1,054 | PLUGIN | Profile mgmt is config feature |

**Recommended Plugins:**
- MCPPlugin (MCP server integration)
- ModelRouterPlugin (model selection strategies)
- FileOperationsPlugin (11 file operation tools)
- AgentPlugin (multi-agent orchestration)
- ProfilePlugin (profile CRUD + UI)

**Keep in Core:**
- llm_service.py (orchestrator)
- api_communication_service.py (HTTP client)
- conversation_manager.py (basic history)
- response_parser.py (basic parsing)
- response_processor.py (streaming)
- message_display_service.py (display coordination)
- plugin_sdk.py (plugin API)
- tool_executor.py (tool framework, not tools)

**Complexity:** MEDIUM to HIGH
**Effort:** 3-5 days

---

### 4. UI Widgets (MEDIUM PRIORITY)

**Problem:** Specific widgets in core when only base class should be

**Impact:** ~600 lines of widget implementations in core

**Keep in Core:**
- BaseWidget (abstract base class)
- ModalRenderer, ModalStateManager, LiveModalRenderer (infrastructure)
- ModalOverlayRenderer (terminal isolation)

**Move to Plugins:**
- CheckboxWidget
- DropdownWidget
- TextInputWidget
- SliderWidget
- LabelWidget
- config_merger.py
- config_widgets.py
- modal_actions.py

**Recommended Plugins:**
- UIWidgetsPlugin (standard widget bundle)
- ConfigModalPlugin (/config command UI)

**Marketplace Opportunity:** Third-party widget sets (animated, themed, etc.)

**Complexity:** MEDIUM
**Effort:** 1-2 days

---

### 5. I/O Components (MEDIUM PRIORITY)

**Problem:** Feature-specific components in core/io/

**Impact:** ~1,952 lines across multiple files

**Move to Plugins:**
- CommandModeHandler from input_handler.py
- ModalController from input_handler.py
- MessageFormatter effects from message_renderer.py

**Keep in Core:**
- terminal_state.py (platform control)
- key_parser.py (input parsing)
- buffer_manager.py (input buffer)
- message_coordinator.py (race condition prevention)
- Core render loop and state management

**Complexity:** MEDIUM
**Effort:** 2-3 days

---

## What's Already Correct

### Plugins (All Correctly Placed)

All 9 plugins in `plugins/` directory are correctly classified:
- enhanced_input_plugin.py - Optional UI enhancement
- hook_monitoring_plugin.py - Development tool
- query_enhancer_plugin.py - Optional query enhancement
- save_conversation_plugin.py - Export feature
- resume_conversation_plugin.py - Session management
- workflow_enforcement_plugin.py - Development workflow
- system_commands_plugin.py - Wraps core (acceptable pattern)
- tmux_plugin.py - External integration
- matrix_plugin.py - Visual effect
- setup_wizard_plugin.py - Onboarding (technically optional)

**One Note:** system_commands_plugin wraps CoreSystemCommandsPlugin. Consider making /help and /version always-loaded in core rather than discovered.

---

## Migration Priority Matrix

### MUST DO (Breaks marketplace model if not addressed)

1. **visual_effects.py** - Largest file, purely cosmetic, high value
2. **system_commands.py** - 6 commands should be separate plugins
3. **file_operations_executor.py** - Tool implementations must be pluggable

### SHOULD DO (Significant core reduction)

4. **profile_manager.py** - Large file, feature not infrastructure
5. **agent_manager.py** - Advanced feature, optional system
6. **UI widgets** - Enable third-party widget ecosystem
7. **core_status_views.py** - Default views should be pluggable

### NICE TO HAVE (Polish)

8. **mcp_integration.py** - Clean separation of protocols
9. **model_router.py** - Enable routing strategy marketplace
10. **ThinkingAnimationManager** - Pluggable spinner system
11. **config_status_view.py** - Pluggable status views
12. **MessageFormatter effects** - Pluggable formatting

---

## Architectural Changes Required

### New Hook Points Needed

To support plugin migrations, core needs:

1. **tool_discovery** - Plugins register tools
2. **model_selection** - Plugins override model choice
3. **widget_registration** - Plugins provide widgets
4. **status_view_registration** - Plugins provide views
5. **effect_registration** - Plugins provide visual effects
6. **command_discovery** - Already exists, expand
7. **mcp_server_discovery** - Plugins register MCP servers
8. **conversation_export** - Plugins provide formats
9. **agent_task_start** - Plugins intercept sub-agent creation
10. **config_change** - Plugins react to profile/config changes

### Infrastructure to Keep

Core must retain:
- Event bus (registry, executor, processor)
- Plugin discovery system (factory, registry, collector)
- Base classes and interfaces (BaseWidget, BasePlugin, etc.)
- Terminal I/O primitives (raw mode, cursor, state)
- Basic LLM communication (HTTP client, streaming)
- Configuration loading/saving
- State persistence
- Command parsing/execution infrastructure
- Modal infrastructure (not specific widgets)

---

## Estimated Migration Effort

| Phase | Components | Effort | Impact |
|-------|-----------|--------|--------|
| Phase 1 | visual_effects, system_commands | 5 days | Huge core reduction |
| Phase 2 | LLM services (5 files) | 5 days | Enable tool marketplace |
| Phase 3 | UI widgets, status views | 3 days | Enable widget marketplace |
| Phase 4 | I/O components | 2 days | Complete separation |
| **TOTAL** | **~31 files** | **15 days** | **~11k lines moved** |

---

## Post-Migration Structure

```
core/
  config/              # Config loading/saving only
  events/              # Event bus infrastructure
  io/                  # Terminal I/O primitives only
    color_support.py   # NEW: Basic color detection
    terminal_state.py
    key_parser.py
    buffer_manager.py
    message_coordinator.py
    layout.py          # LayoutManager only
    terminal_renderer.py  # Slim - delegates to plugins
    input_handler.py   # Slim - basic input only
    message_renderer.py   # Slim - basic rendering only
    status_renderer.py    # Infrastructure only
  llm/                 # Essential LLM services only
    llm_service.py
    api_communication_service.py
    conversation_manager.py
    response_parser.py
    response_processor.py
    message_display_service.py
    plugin_sdk.py
    tool_executor.py   # Framework, not tools
    conversation_logger.py  # Basic persistence only
  plugins/             # Plugin system infrastructure
    discovery.py
    factory.py
    registry.py
    collector.py
  ui/                  # Modal infrastructure only
    modal_renderer.py
    modal_state_manager.py
    modal_overlay_renderer.py
    live_modal_renderer.py
    widgets/
      base_widget.py   # Base class only
  commands/            # Command infrastructure only
    parser.py
    executor.py
    registry.py
    menu_renderer.py
    system_commands.py  # /help, /version ONLY
  fullscreen/          # Fullscreen framework only
    plugin.py
    manager.py
    session.py
    renderer.py
    command_integration.py

plugins/
  # Visual Effects
  visual_effects_plugin.py      # All effects from core
  default_status_views.py       # CoreStatusViews
  config_status_plugin.py       # ConfigStatusView
  thinking_animation_plugin.py  # Spinners

  # Commands (NEW)
  profile_management_plugin.py  # /profile
  agent_management_plugin.py    # /agent
  skill_management_plugin.py    # /skill
  configuration_plugin.py       # /config
  diagnostics_plugin.py         # /status
  session_plugin.py             # /resume

  # LLM Services (NEW)
  mcp_plugin.py                 # MCP integration
  model_router_plugin.py        # Model routing
  file_operations_plugin.py     # 11 file tools
  agent_plugin.py               # Multi-agent system
  profile_plugin.py             # Profile management

  # UI Widgets (NEW)
  ui_widgets_plugin.py          # All standard widgets
  config_modal_plugin.py        # Config UI

  # Existing (keep)
  enhanced_input_plugin.py
  hook_monitoring_plugin.py
  query_enhancer_plugin.py
  save_conversation_plugin.py
  resume_conversation_plugin.py
  workflow_enforcement_plugin.py
  tmux_plugin.py
  fullscreen/
    matrix_plugin.py
    matrix_components.py        # MOVED from core
    setup_wizard_plugin.py
```

---

## Risk Assessment

### Low Risk
- visual_effects.py - Purely cosmetic
- core_status_views.py - Views are already pluggable
- UI widgets - Infrastructure exists
- matrix_components.py - Already wrapped by plugin

### Medium Risk
- system_commands.py - Need to ensure /help, /version remain
- profile_manager.py - Config integration must work
- mcp_integration.py - Tool registration must be robust

### High Risk
- file_operations_executor.py - Heavy dependencies, safety critical
- agent_manager.py - Background tasks, lifecycle management
- Splitting large files - Must maintain all functionality

---

## Recommendations

### Immediate Actions (This Week)
1. ✅ Review this audit with team
2. Approve migration phases
3. Start with Phase 1 (visual_effects + system_commands)
4. Create migration spec for each component

### Short Term (Next 2 Weeks)
5. Complete Phase 1 migration
6. Test marketplace model with sample plugins
7. Document plugin APIs for each hook point
8. Start Phase 2 (LLM services)

### Medium Term (Next Month)
9. Complete all 4 phases
10. Publish plugin development guide
11. Create plugin marketplace infrastructure
12. Invite third-party plugin developers

---

## Questions for Decision

1. **Plugin Bundling:** Should we bundle "essential" plugins (widgets, status views) with core installation?
2. **Backward Compatibility:** Do we maintain compatibility or do breaking change?
3. **Migration Timeline:** All at once or incremental releases?
4. **Testing Strategy:** How do we ensure no functionality lost?
5. **Plugin Pricing:** Which plugins should be free vs premium?

---

## Audit Methodology

This audit was conducted by 6 parallel agents analyzing:
- plugins/ directory
- core/commands/
- core/effects/
- core/io/
- core/llm/
- core/ui/

Each agent applied criteria from `docs/CORE_VS_PLUGIN_AUDIT_SPEC.md`:
- CORE: Essential infrastructure the app cannot run without
- PLUGIN: Optional, extensible features suitable for marketplace

All findings are based on:
- Line count analysis
- Dependency analysis
- Functionality classification
- Marketplace viability
- Migration complexity assessment

---

**Audit Complete:** 2025-01-07
**Total Analysis Time:** ~3 minutes (parallel execution)
**Files Analyzed:** 60
**Recommendations:** 31+ migrations
**Potential Core Reduction:** ~11,000 lines (36%)
