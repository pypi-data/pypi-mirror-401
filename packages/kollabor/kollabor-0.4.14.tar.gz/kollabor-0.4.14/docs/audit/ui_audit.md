# UI Directory Audit: Core vs Plugin Classification

Audit Date: 2025-01-07
Auditor: Claude (Audit Mode)
Directory: core/ui/

---

## Executive Summary

The core/ui/ directory contains 16 files implementing a complete modal UI system.
The modal infrastructure is appropriately CORE, but specific widget implementations
and configuration-heavy components are candidates for plugin extraction.

**Findings:**
- 11 files appropriately classified as CORE (base modal infrastructure)
- 5 files that could be PLUGIN (specific widgets and config-heavy components)

---

## CORE: Base Modal Infrastructure (Keep in core/)

### location: core/ui/__init__.py
current: CORE
should_be: CORE (correct)
reason: Package init that exports public UI API. Essential infrastructure.
complexity: n/a

### location: core/ui/modal_renderer.py
class: ModalRenderer
current: CORE
should_be: CORE (correct)
reason: Main modal orchestrator using existing visual effects infrastructure.
     This is the base modal system that commands, config, and other features
     depend on. Moving this would break core application functionality.
complexity: high
dependencies: Uses widgets (could be plugin), modal_state_manager, modal_overlay_renderer

### location: core/ui/modal_overlay_renderer.py
class: ModalOverlayRenderer
current: CORE
should_be: CORE (correct)
reason: Pure modal overlay renderer that provides terminal isolation using
     direct terminal output and state save/restore. Essential for any modal
     functionality to work without chat interference.
complexity: medium
dependencies: TerminalState only

### location: core/ui/modal_state_manager.py
class: ModalStateManager
current: CORE
should_be: CORE (correct)
reason: Terminal state management for modal isolation. Handles alternate
     buffer switching (DECSET/DECRST 1049), terminal snapshots, and state
     restoration. This is primitive infrastructure for modals.
complexity: medium
dependencies: TerminalState only

### location: core/ui/live_modal_renderer.py
class: LiveModalRenderer
current: CORE
should_be: CORE (correct)
reason: Live modal renderer for streaming/updating content (used by tmux
     plugin for live session viewing). This is infrastructure for any
     live-updating modal display.
complexity: medium
dependencies: ModalStateManager, TerminalState, KeyPress

---

## PLUGIN Candidates: Specific Widgets (Could move to plugins)

### location: core/ui/widgets/checkbox.py
class: CheckboxWidget
current: CORE
should_be: PLUGIN
reason: Specific widget implementation for boolean toggles. Widget implementations
     beyond basic primitives are plugin material per the spec:
     "UI widgets beyond basics" should be plugins.
complexity: low
dependencies: BaseWidget, KeyPress, ColorPalette
migration: Extract to plugins/ui_widgets/ or a widgets plugin bundle

### location: core/ui/widgets/dropdown.py
class: DropdownWidget
current: CORE
should_be: PLUGIN
reason: Specific widget implementation for option selection. Widget implementations
     beyond basic primitives are plugin material per the spec.
complexity: low
dependencies: BaseWidget, KeyPress, ColorPalette
migration: Extract to plugins/ui_widgets/ or a widgets plugin bundle

### location: core/ui/widgets/text_input.py
class: TextInputWidget
current: CORE
should_be: PLUGIN
reason: Specific widget implementation for text entry with cursor handling.
     Widget implementations beyond basic primitives are plugin material.
complexity: medium
dependencies: BaseWidget, KeyPress, ColorPalette
migration: Extract to plugins/ui_widgets/ or a widgets plugin bundle

### location: core/ui/widgets/slider.py
class: SliderWidget
current: CORE
should_be: PLUGIN
reason: Specific widget implementation for numeric slider with visual bar.
     Widget implementations beyond basic primitives are plugin material.
complexity: medium
dependencies: BaseWidget, KeyPress, ColorPalette
migration: Extract to plugins/ui_widgets/ or a widgets plugin bundle

### location: core/ui/widgets/label.py
class: LabelWidget
current: CORE
should_be: PLUGIN
reason: Specific widget implementation for read-only display. While simple,
     it's still a concrete widget implementation that could be in a widget bundle.
complexity: low
dependencies: BaseWidget, ColorPalette
migration: Extract to plugins/ui_widgets/ or a widgets plugin bundle

---

## CORE: Widget Base Class (Must stay in core/)

### location: core/ui/widgets/base_widget.py
class: BaseWidget
current: CORE
should_be: CORE (correct)
reason: Abstract base class defining the widget interface. This is the
     foundation that plugin widgets would inherit from. Must stay in core.
complexity: low
dependencies: KeyPress, ABC

### location: core/ui/widgets/__init__.py
current: CORE
should_be: CORE (correct)
reason: Widget package exports. Provides the widget API that plugins would use.
complexity: n/a

---

## PLUGIN Candidates: Config-Specific Components

### location: core/ui/config_merger.py
class: ConfigMerger
current: CORE
should_be: PLUGIN
reason: Config persistence system for modal UI changes. This is specifically
     for the /config command's save/cancel functionality. The config system
     itself is core, but the modal-specific config merging is a feature.
complexity: medium
dependencies: ConfigService, logging
migration: Move to plugins/ as part of config_modal plugin or merge into an
            existing plugin that handles /config command

### location: core/ui/config_widgets.py
class: ConfigWidgetDefinitions
current: CORE
should_be: PLUGIN
reason: Defines which config values get which widgets in the modal.
     This is specifically for the /config command's UI definition.
     Contains hardcoded sections for Terminal, Input, LLM, Application, Plugin settings.
complexity: medium
dependencies: ConfigService, all widget types
migration: Move to plugins/ as part of config_modal plugin. The plugin would
            register its widget definitions with the modal renderer.

### location: core/ui/modal_actions.py
class: ModalActionHandler
current: CORE
should_be: PLUGIN
reason: Modal action handlers for save/cancel with config persistence.
     This is specifically for the /config command's action handling.
complexity: low
dependencies: ConfigMerger, ConfigService
migration: Move to plugins/ as part of config_modal plugin

---

## What MUST Stay in Core

The following components form the essential modal infrastructure and cannot be moved:

1. **modal_state_manager.py** - Terminal state isolation, alternate buffer management
2. **modal_overlay_renderer.py** - Direct terminal output for true modals
3. **live_modal_renderer.py** - Live streaming content display
4. **modal_renderer.py** - Main modal orchestrator (with widget integration hooks)
5. **widgets/base_widget.py** - Abstract base class for widget plugins

These provide the modal "primitive" that other features can use.

---

## What Should Become Plugins

### Option 1: Widget Bundle Plugin
Create a single `ui_widgets` plugin that provides all standard widgets:
- CheckboxWidget
- DropdownWidget
- TextInputWidget
- SliderWidget
- LabelWidget

**Complexity:** Medium
**Benefit:** Clean separation, allows marketplace for alternative widget sets

### Option 2: Config Modal Plugin
Create a `config_modal` plugin that handles /config command:
- config_merger.py
- config_widgets.py
- modal_actions.py

**Complexity:** Medium
**Benefit:** /config becomes fully optional, core shrinks

---

## Migration Complexity Estimates

### Widgets to Plugin Bundle
- **Complexity:** Medium
- **Steps:**
  1. Create plugins/ui_widgets_plugin.py
  2. Move widget files to plugins/ui_widgets/
  3. Register widgets with ModalRenderer via plugin SDK
  4. Update imports in modal_renderer.py
  5. Add plugin discovery for widget types

### Config Components to Config Plugin
- **Complexity:** Medium
- **Steps:**
  1. Create plugins/config_modal_plugin.py
  2. Move config_merger.py, config_widgets.py, modal_actions.py
  3. Register /config command via plugin
  4. Register modal definitions via plugin SDK
  5. Remove hardcoded config modal from core

---

## Dependencies Requiring Resolution

### If Widgets Move to Plugin
1. **modal_renderer.py** imports widget classes directly
   - Solution: Use dynamic widget registration via plugin SDK
   - Pattern: `renderer.register_widget_type('checkbox', CheckboxWidget)`

2. **config_widgets.py** creates widget instances
   - Solution: Move to plugin (see Option 2 above)
   - Or: Use widget factory that queries registered types

### If Config Components Move to Plugin
1. **modal_renderer.py** uses ConfigMerger
   - Solution: Make ModalRenderer accept an optional action handler
   - Core provides default no-op handler

2. **Import chains** between core modules
   - Solution: Plugin provides its own action handler implementation

---

## Recommendation

**Priority 1 (Do Now):** No immediate action needed

The modal UI system is appropriately structured with base infrastructure in core
and widget implementations that could theoretically be plugins. However, the
widget implementations are widely used across the application (config modal,
help modal, resume modal, etc.), so extracting them would require significant
refactoring for questionable benefit.

**Priority 2 (Future Cleanup):** Consider widget plugin bundle

If a plugin marketplace is planned, create a `ui_widgets` plugin that provides
the standard widgets. This would allow third-party developers to create custom
widget sets (e.g., "fancy_widgets" with animated sliders, color pickers, etc.).

**Priority 3 (Nice to Have):** Extract /config to plugin

The config-specific components (config_merger.py, config_widgets.py,
modal_actions.py) could move to a dedicated plugin to make the /config command
fully optional. This would reduce core size by ~600 lines.

---

## Summary Statistics

| Category | Files | Lines (approx) |
|----------|-------|----------------|
| CORE (infrastructure) | 6 | ~2,000 |
| CORE (base classes) | 2 | ~150 |
| PLUGIN candidates (widgets) | 5 | ~600 |
| PLUGIN candidates (config) | 3 | ~600 |
| **Total** | **16** | **~3,350** |

**Potential Core Reduction:** ~1,200 lines (36%) by extracting widgets and config components
**Actual Core Size After Migration:** ~2,150 lines (infrastructure only)
