# I/O System Audit Report

**Date**: 2026-01-07
**Auditor**: Claude
**Scope**: core/io/ directory (12 files)

## Executive Summary

The I/O system contains a mix of essential core infrastructure and plugin-eligible features.
Approximately 60% of functionality should remain CORE, while 40% could be moved to PLUGINS
to enable marketplace customization and reduce core bloat.

## Findings by File

### 1. visual_effects.py
**Status**: SHOULD BE PLUGIN
**Complexity**: high
**Current**: 1,386 lines in core/io/

**Analysis**:
- ColorPalette with extensive color definitions (lime, cyan themes)
- GradientRenderer, ShimmerEffect, PulseEffect, ScrambleEffect
- AgnosterSegment (powerline-style segments)
- BannerRenderer with ASCII art banners
- StatusColorizer with semantic coloring

**Recommendation**:
Move to plugins/ as a new "visual_effects_plugin.py". The core should only provide:
- Basic color detection (ColorSupport enum, detect_color_support())
- Minimal color palette (basic ANSI colors)
- RGB-to-256 conversion utility

**Migration Path**:
1. Create core/io/base_effects.py with minimal color support
2. Create plugins/visual_effects_plugin.py with all effects
3. Core imports from plugin via dependency injection

---

### 2. core_status_views.py
**Status**: SHOULD BE PLUGIN
**Complexity**: medium
**Current**: 315 lines in core/io/

**Analysis**:
- CoreStatusViews class with 4 predefined views
- Agnoster-styled segments (lime/cyan color scheme)
- Agent/skills formatting, model info display
- Overview, Session, LLM Details, Minimal views

**Recommendation**:
Move to plugins/ as "default_status_views.py". These are default implementations
that could be replaced by user preferences or marketplace alternatives.

**Migration Path**:
1. Keep StatusViewRegistry in core (infrastructure)
2. Move CoreStatusViews to plugins/default_status_views.py
3. Register via plugin hooks on initialization

---

### 3. config_status_view.py
**Status**: SHOULD BE PLUGIN
**Complexity**: low
**Current**: 251 lines in core/io/

**Analysis**:
- ConfigStatusView for monitoring configuration errors
- Status view provider for configuration health
- Validation warning display

**Recommendation**:
Move to plugins/ as "config_status_plugin.py". This is a specific status view
implementation that should be pluggable.

**Migration Path**:
1. Extract to plugin
2. Register via StatusViewRegistry from plugin initialize()

---

### 4. layout.py (ThinkingAnimationManager only)
**Status**: PARTIAL PLUGIN
**Complexity**: medium
**Current**: 600 lines in core/io/

**Analysis**:
- LayoutManager: CORE infrastructure for terminal layout
- ThinkingAnimationManager: PLUGIN-eligible (spinner animations)

**Recommendation**:
Split the file. Keep LayoutManager in core, move ThinkingAnimationManager
to a plugin. The spinner is a visual effect that users might want to customize.

**Migration Path**:
1. Keep core/io/layout.py with LayoutManager only
2. Move ThinkingAnimationManager to plugins/thinking_animation_plugin.py
3. Use hook system for animation rendering

---

### 5. status_renderer.py (StatusViewRegistry)
**Status**: CORE (infrastructure) / PLUGIN (views)
**Complexity**: medium
**Current**: 386 lines in core/io/

**Analysis**:
- StatusViewRegistry: CORE infrastructure for registration
- StatusRenderer: CORE rendering engine
- BlockConfig, StatusViewConfig: CORE data structures

**Recommendation**:
Keep infrastructure in core. Move specific view implementations to plugins.
The registry and rendering engine are essential primitives.

**Migration Path**:
1. Keep StatusViewRegistry, StatusRenderer in core
2. Move all view providers to plugins
3. Core provides registration API only

---

### 6. terminal_renderer.py
**Status**: CORE (with reservations)
**Complexity**: high
**Current**: 633 lines in core/io/

**Analysis**:
- Main render loop: CORE
- Active area management: CORE
- Visual effects coordination: Should delegate to plugins
- Banner creation: Should delegate to plugins
- Thinking effect configuration: Should delegate to plugins

**Recommendation**:
Keep core render loop. Move effect-specific logic to plugin hooks.
The renderer should be a thin coordinator that delegates to plugins.

**Migration Path**:
1. Keep render_active_area(), _render_lines(), clear_active_area()
2. Move effect configuration to plugin-provided handlers
3. Use hooks for banner generation, thinking effects

---

### 7. input_handler.py
**Status**: CORE (with reservations)
**Complexity**: high
**Current**: 415 lines in core/io/

**Analysis**:
- Basic input loop: CORE
- Key processing: CORE
- Command menu system: Should be PLUGIN
- Modal controller: Should be PLUGIN
- Paste detection: Could be PLUGIN

**Recommendation**:
Keep core input handling. Move command menus and modal system to plugins.
The core should provide basic character input and key parsing.

**Migration Path**:
1. Keep InputLoopManager, KeyPressHandler in core
2. Move CommandModeHandler to command_plugin.py
3. Move ModalController to modal_plugin.py
4. Paste detection could be optional enhancement plugin

---

### 8. message_coordinator.py
**Status**: CORE
**Complexity**: medium
**Current**: 304 lines in core/io/

**Analysis**:
- Atomic message display coordination
- Race condition prevention
- Buffer transition management
- State synchronization

**Recommendation**:
KEEP IN CORE. This is critical infrastructure that prevents display bugs.
Without this coordination, multiple systems would interfere with each other.

---

### 9. message_renderer.py
**Status**: CORE (infrastructure) / PLUGIN (formatting)
**Complexity**: high
**Current**: 607 lines in core/io/

**Analysis**:
- ConversationRenderer: CORE message display
- MessageFormatter: Mixed - basic format is CORE, gradients are PLUGIN
- ConversationBuffer: CORE message history

**Recommendation**:
Keep basic message rendering in core. Move fancy formatting (gradients, effects)
to plugins. Provide hooks for message formatting customization.

**Migration Path**:
1. Keep ConversationRenderer, ConversationBuffer in core
2. Move MessageFormatter effects to plugins
3. Add hooks for pre/post message formatting

---

### 10. buffer_manager.py
**Status**: CORE
**Complexity**: low
**Current**: 368 lines in core/io/

**Analysis**:
- Input buffer management
- Cursor positioning
- History navigation
- Paste handling (basic)

**Recommendation**:
KEEP IN CORE. This is essential infrastructure for any terminal input.
Even basic applications need buffer management.

---

### 11. key_parser.py
**Status**: CORE
**Complexity**: low
**Current**: 352 lines in core/io/

**Analysis**:
- Keyboard input parsing
- Control key detection
- Escape sequence handling
- Cross-platform key support

**Recommendation**:
KEEP IN CORE. Terminal I/O primitives must handle raw input parsing.
This is a fundamental requirement for terminal applications.

---

### 12. terminal_state.py
**Status**: CORE
**Complexity**: medium
**Current**: 569 lines in core/io/

**Analysis**:
- Terminal mode switching (raw/cooked)
- Platform-specific terminal control
- Cursor management
- Terminal capability detection

**Recommendation**:
KEEP IN CORE. This is essential terminal I/O infrastructure.
No terminal application can function without this.

---

## Summary Matrix

| File | Current | Should Be | Complexity | Action |
|------|---------|-----------|------------|--------|
| visual_effects.py | CORE | PLUGIN | high | Move to plugins/ |
| core_status_views.py | CORE | PLUGIN | medium | Move to plugins/ |
| config_status_view.py | CORE | PLUGIN | low | Move to plugins/ |
| layout.py (ThinkingAnimationManager) | CORE | PLUGIN | medium | Split file |
| status_renderer.py | CORE | CORE/PLUGIN | medium | Keep infra, move views |
| terminal_renderer.py | CORE | CORE (slim) | high | Delegate effects to hooks |
| input_handler.py | CORE | CORE (slim) | high | Move command/modal to plugins |
| message_coordinator.py | CORE | CORE | medium | Keep as-is |
| message_renderer.py | CORE | CORE (slim) | high | Move formatting to plugins |
| buffer_manager.py | CORE | CORE | low | Keep as-is |
| key_parser.py | CORE | CORE | low | Keep as-is |
| terminal_state.py | CORE | CORE | medium | Keep as-is |

## Recommended Core Retention

**Keep in core/io/**:
1. `terminal_state.py` - Full file (platform terminal control)
2. `key_parser.py` - Full file (input parsing primitives)
3. `buffer_manager.py` - Full file (input buffer management)
4. `message_coordinator.py` - Full file (race condition prevention)
5. `status_renderer.py` - StatusViewRegistry, StatusRenderer, data classes only
6. `layout.py` - LayoutManager only (remove ThinkingAnimationManager)
7. `message_renderer.py` - ConversationRenderer, ConversationBuffer only
8. `terminal_renderer.py` - Render loop, state management only (slimmed)
9. `input_handler.py` - InputLoopManager, KeyPressHandler only (slimmed)

**Move to plugins/**:
1. `visual_effects.py` -> Full file to `plugins/visual_effects_plugin.py`
2. `core_status_views.py` -> Full file to `plugins/default_status_views.py`
3. `config_status_view.py` -> Full file to `plugins/config_status_plugin.py`
4. `layout.py` (ThinkingAnimationManager) -> To thinking animation plugin
5. `message_renderer.py` (MessageFormatter effects) -> To formatting plugin
6. `input_handler.py` (CommandModeHandler, ModalController) -> To command/modal plugins

## Migration Complexity: Medium

The migration is straightforward but requires:
1. Creating plugin skeleton for moved components
2. Adding hook points for effects, commands, modals
3. Dependency injection for renderer to access plugin effects
4. Breaking circular dependencies between core and plugins

**Estimated effort**: 2-3 days for full migration with tests.

## Dependencies to Resolve

1. **terminal_renderer.py** imports visual_effects directly
   - Solution: Inject via constructor or event bus

2. **input_handler.py** tightly coupled with command system
   - Solution: Create ICommandHandler interface

3. **layout.py** ThinkingAnimationManager used by renderer
   - Solution: Hook-based animation system

4. **message_renderer.py** uses MessageFormatter with effects
   - Solution: Plugin-provided formatters via registry

## Priority Recommendations

1. **HIGH**: Move `visual_effects.py` to plugin (largest single file, purely cosmetic)
2. **HIGH**: Move `core_status_views.py` to plugin (easy win, clearly optional)
3. **MEDIUM**: Extract ThinkingAnimationManager from layout.py
4. **MEDIUM**: Split command/modal handling from input_handler.py
5. **LOW**: Slim down message_renderer.py effects
