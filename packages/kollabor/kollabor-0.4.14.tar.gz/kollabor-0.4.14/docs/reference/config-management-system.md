---
title: Configuration Management System
description: Complete configuration system with modal UI, widget support, and persistence
category: reference
status: implemented
---

# Configuration Management System

## Overview

The Kollabor CLI implements a comprehensive configuration management system with interactive modal UI, widget-based editing, validation, and persistence to `.kollabor-cli/config.json`. Users can configure the system through the `/config` command with a rich modal interface.

**Status**: Fully implemented and operational

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│              Configuration Management System                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────┐    ┌─────────────────┐               │
│  │ /config Command│───>│ModalRenderer    │               │
│  │ System Commands│    │ - Display modal │               │
│  └────────────────┘    │ - Widget render │               │
│                        └────────┬────────┘               │
│                                 │                          │
│  ┌──────────────────────────────▼───────────────────┐    │
│  │           Widget System                          │    │
│  ├──────────────────────────────────────────────────┤    │
│  │ • Checkbox   • Slider      • Text Input         │    │
│  │ • Dropdown   • ColorPicker • FilePicker         │    │
│  └──────────────────┬───────────────────────────────┘    │
│                     │                                     │
│  ┌──────────────────▼───────────────────────────────┐    │
│  │        ModalActionHandler                        │    │
│  │  - Collect widget changes                        │    │
│  │  - Validate changes                              │    │
│  │  - Apply to ConfigService                        │    │
│  └──────────────────┬───────────────────────────────┘    │
│                     │                                     │
│  ┌──────────────────▼───────────────────────────────┐    │
│  │         ConfigService / ConfigManager            │    │
│  │  - Load from file                                │    │
│  │  - Save to file                                  │    │
│  │  - Dot notation access                           │    │
│  │  - Validation                                    │    │
│  └──────────────────────────────────────────────────┘    │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Core Components

### 1. ConfigService / ConfigManager

**Location**: `core/config/manager.py`, `core/config/service.py`

The configuration service provides centralized config management with persistence.

**Key Methods**:

```python
class ConfigManager:
    def load_config_file() -> Dict[str, Any]:
        """Load configuration from .kollabor-cli/config.json"""

    def save_config_file(config: Dict[str, Any]) -> bool:
        """Save configuration to file with atomic write"""

    def get(key_path: str, default: Any = None) -> Any:
        """Get value using dot notation (e.g., 'terminal.render_fps')"""

    def set(key_path: str, value: Any) -> bool:
        """Set value and save to file"""
```

**Example Usage**:
```python
# Get configuration value
fps = config_manager.get("terminal.render_fps", 20)

# Set and save configuration value
success = config_manager.set("terminal.render_fps", 30)
```

### 2. /config Command

**Location**: `core/commands/system_commands.py`

The `/config` command opens the configuration modal with all available settings.

**Implementation**:
```python
async def handle_config(self, command: SlashCommand) -> CommandResult:
    """Handle /config command"""
    from ..ui.config_widgets import ConfigWidgetDefinitions

    # Get complete modal definition with all widgets
    modal_definition = ConfigWidgetDefinitions.get_config_modal_definition()

    return CommandResult(
        success=True,
        message="Configuration modal opened",
        ui_config=UIConfig(
            type="modal",
            title=modal_definition["title"],
            width=modal_definition["width"],
            modal_config=modal_definition
        ),
        display_type="modal"
    )
```

### 3. ConfigWidgetDefinitions

**Location**: `core/ui/config_widgets.py`

Defines the complete modal structure with all configuration widgets organized into sections.

**Modal Structure**:
```python
{
    "title": "System Configuration",
    "footer": "↑↓/PgUp/PgDn navigate • Enter toggle • Ctrl+S save • Esc cancel",
    "width": 120,
    "height": 40,
    "sections": [
        {
            "title": "Terminal Settings",
            "widgets": [
                {
                    "type": "slider",
                    "label": "Render FPS",
                    "config_path": "terminal.render_fps",
                    "min_value": 1,
                    "max_value": 60,
                    "step": 1,
                    "help": "Terminal refresh rate (1-60 FPS)"
                },
                # ... more widgets
            ]
        },
        # ... more sections
    ],
    "actions": [
        {"key": "Ctrl+S", "label": "Save", "action": "save"},
        {"key": "Escape", "label": "Cancel", "action": "cancel"}
    ]
}
```

**Available Sections**:
1. **Terminal Settings**: FPS, status lines, thinking effect, shimmer speed, render cache
2. **Input Settings**: Ctrl+C exit, backspace enabled, history limit
3. **LLM Settings**: API URL, model, temperature, max history
4. **Application Settings**: Name, version
5. **Plugin Settings**: Enable/disable plugins (dynamically discovered)
6. **Plugin Config Sections**: Plugin-specific widgets (dynamically loaded)

### 4. ModalRenderer

**Location**: `core/ui/modal_renderer.py`

Renders the configuration modal with widget support and action handling.

**Key Features**:
- Alternate buffer management (preserves main display)
- Widget rendering and focus management
- Keyboard navigation (arrow keys, PgUp/PgDn)
- Action handler integration for save/cancel
- Section-based layout with titles

**Initialization**:
```python
modal_renderer = ModalRenderer(
    terminal_renderer=terminal_renderer,
    visual_effects=visual_effects,
    config_service=config_service  # Required for save functionality
)
```

### 5. ModalActionHandler

**Location**: `core/ui/modal_actions.py`

Handles modal actions (save/cancel) with configuration persistence.

**Save Flow**:
```python
async def _handle_save_action(self, widgets: List[Any]) -> Dict[str, Any]:
    """Handle save action with config persistence"""

    # 1. Collect widget changes
    changes = ConfigMerger.collect_widget_changes(widgets)

    # 2. Validate changes
    validation = ConfigMerger.validate_config_changes(
        self.config_service,
        changes
    )

    if not validation["valid"]:
        return {"success": False, "message": "Invalid configuration"}

    # 3. Apply changes to config
    success = ConfigMerger.apply_widget_changes(
        self.config_service,
        changes
    )

    # 4. Save to file
    if success:
        self.config_service.save_config_file()

    return {
        "success": success,
        "message": f"Saved {len(changes)} configuration changes",
        "changes_count": len(changes)
    }
```

### 6. ConfigMerger

**Location**: `core/ui/config_merger.py`

Utilities for collecting, validating, and applying widget changes to configuration.

**Key Methods**:

```python
class ConfigMerger:
    @staticmethod
    def collect_widget_changes(widgets: List[Any]) -> Dict[str, Any]:
        """Collect changed values from widgets with pending changes"""

    @staticmethod
    def validate_config_changes(config_service, changes: Dict) -> Dict:
        """Validate configuration changes before applying"""

    @staticmethod
    def apply_widget_changes(config_service, changes: Dict) -> bool:
        """Apply validated changes to config service"""
```

## Widget System

### Available Widget Types

**Location**: `core/config/plugin_schema.py`

```python
class WidgetType(Enum):
    CHECKBOX = "checkbox"           # Boolean toggle
    SLIDER = "slider"               # Numeric range
    TEXT_INPUT = "text_input"       # String input
    DROPDOWN = "dropdown"           # Selection from options
    COLOR_PICKER = "color_picker"   # Color selection
    FILE_PICKER = "file_picker"     # File path selection
    DIRECTORY_PICKER = "directory_picker"  # Directory path
    MULTI_SELECT = "multi_select"   # Multiple selections
    KEY_VALUE = "key_value"         # Key-value pairs
    CODE_EDITOR = "code_editor"     # Multi-line code
```

### Widget Definition Format

Each widget in the modal definition has:

```python
{
    "type": "slider",                    # Widget type
    "label": "Render FPS",               # Display label
    "config_path": "terminal.render_fps", # Dot notation path
    "min_value": 1,                      # Type-specific properties
    "max_value": 60,
    "step": 1,
    "help": "Terminal refresh rate"      # Help text
}
```

### Widget Lifecycle

```
1. Widget Creation
   ├─> ConfigWidgetDefinitions.get_config_modal_definition()
   ├─> Modal definition with all widgets
   └─> Passed to ModalRenderer

2. Widget Rendering
   ├─> ModalRenderer.show_modal(ui_config)
   ├─> Create widget instances
   ├─> Load current values from config_service
   └─> Render in alternate buffer

3. User Interaction
   ├─> Navigate with arrow keys
   ├─> Edit focused widget (Enter, type, etc.)
   ├─> Widget stores pending value
   └─> Visual feedback (highlight, value change)

4. Save Action (Ctrl+S)
   ├─> ModalActionHandler.handle_action("save", widgets)
   ├─> Collect pending changes from widgets
   ├─> Validate all changes
   ├─> Apply to ConfigService
   ├─> ConfigManager.save_config_file()
   └─> Return success/failure

5. Cancel Action (Escape)
   ├─> Discard pending changes
   ├─> Close modal
   └─> Restore main display
```

## Configuration File Structure

### Location

**Priority-based resolution**:
1. `.kollabor-cli/config.json` (local, project-specific)
2. `~/.kollabor-cli/config.json` (global, user default)

### Schema

```json
{
  "terminal": {
    "render_fps": 20,
    "status_lines": 3,
    "thinking_effect": "shimmer",
    "shimmer_speed": 5,
    "render_cache_enabled": true
  },
  "input": {
    "ctrl_c_exit": false,
    "backspace_enabled": true,
    "history_limit": 100
  },
  "core": {
    "llm": {
      "api_url": "http://localhost:1234",
      "model": "qwen/qwen3-4b",
      "temperature": 0.7,
      "max_history": 90
    }
  },
  "application": {
    "name": "Kollabor CLI",
    "version": "1.0.0"
  },
  "plugins": {
    "tmux": {
      "enabled": true
    },
    "save_conversation": {
      "enabled": true
    }
  }
}
```

### Dot Notation Access

Configuration values are accessed using dot notation:

```python
# Read
fps = config.get("terminal.render_fps", 20)
model = config.get("core.llm.model", "qwen/qwen3-4b")

# Write
config.set("terminal.render_fps", 30)
config.set("core.llm.temperature", 0.8)
```

## User Workflow

### Opening Configuration Modal

```
User types: /config
    │
    ├─> SystemCommands.handle_config()
    │   ├─ Load modal definition
    │   └─ Return CommandResult with modal UI config
    │
    ├─> CommandExecutor processes result
    │
    ├─> ModalController._enter_modal_mode()
    │   ├─ Create ModalRenderer with config_service
    │   ├─ Enter alternate buffer
    │   └─ Render modal with widgets
    │
    └─> Modal displayed to user
```

### Editing Configuration

```
User navigates with ↑/↓ (or PgUp/PgDn)
    │
    ├─> Focus moves between widgets
    ├─> Visual highlight shows focused widget
    └─> Help text displays for focused widget

User edits widget (Enter for toggle, type for input, etc.)
    │
    ├─> Widget updates pending value
    ├─> Visual feedback shows change
    └─> Original value preserved until save
```

### Saving Changes

```
User presses Ctrl+S
    │
    ├─> ModalController detects save action
    │
    ├─> ModalActionHandler.handle_action("save", widgets)
    │   ├─ Collect pending changes from widgets
    │   ├─ Validate all changes
    │   │   ├─ Type checking
    │   │   ├─ Range validation
    │   │   └─ Required field checks
    │   │
    │   ├─ Apply validated changes to ConfigService
    │   │   ├─ config.set("terminal.render_fps", 30)
    │   │   ├─ config.set("core.llm.temperature", 0.8)
    │   │   └─ ... for each change
    │   │
    │   └─> ConfigManager.save_config_file()
    │       ├─ Serialize to JSON
    │       ├─ Write to .kollabor-cli/config.json
    │       └─ Atomic file write (temp + rename)
    │
    ├─> Show success message: "Saved N configuration changes"
    │
    └─> Close modal and return to main display
```

### Canceling Changes

```
User presses Escape
    │
    ├─> ModalController detects cancel action
    ├─> Discard all pending widget changes
    ├─> Close modal
    └─> Return to main display (no changes saved)
```

## Plugin Integration

### Plugin Configuration Widgets

Plugins can provide their own configuration widgets through the `get_config_widgets()` method.

**Example Plugin Config**:

```python
class WorkflowEnforcementPlugin:
    def get_config_widgets(self) -> List[Dict[str, Any]]:
        """Return widget definitions for plugin config"""
        return [
            {
                "type": "checkbox",
                "label": "Require Tool Calls",
                "config_path": "plugins.workflow_enforcement.require_tool_calls",
                "help": "Require <terminal> tags for commands"
            },
            {
                "type": "slider",
                "label": "Timeout (seconds)",
                "config_path": "plugins.workflow_enforcement.timeout",
                "min_value": 0,
                "max_value": 300,
                "step": 5,
                "help": "Timeout for workflow enforcement"
            }
        ]
```

### Plugin Discovery

The config modal automatically discovers plugins and includes:
1. **Plugin Enable/Disable**: Checkbox for each discovered plugin
2. **Plugin Config Sections**: Dynamically loaded from `get_config_widgets()`

**Discovery Process**:
```python
# In ConfigWidgetDefinitions
plugins = ConfigWidgetDefinitions.get_available_plugins()
# Returns: [{"type": "checkbox", "label": "Tmux", ...}, ...]

sections = ConfigWidgetDefinitions.get_plugin_config_sections()
# Returns: [{title: "Workflow Settings", widgets: [...]}, ...]
```

## Validation System

### Validation Types

**Location**: `core/config/plugin_schema.py`

```python
class ValidationType(Enum):
    NONE = "none"                # No validation
    STRING = "string"            # Must be string
    INTEGER = "integer"          # Must be integer
    FLOAT = "float"              # Must be float
    BOOLEAN = "boolean"          # Must be boolean
    URL = "url"                  # Valid URL format
    EMAIL = "email"              # Valid email format
    FILE_PATH = "file_path"      # Valid file path
    DIRECTORY_PATH = "directory_path"  # Valid directory
    JSON = "json"                # Valid JSON
    REGEX = "regex"              # Matches regex pattern
```

### Validation Flow

```python
# In ModalActionHandler
validation = ConfigMerger.validate_config_changes(config_service, changes)

# Returns:
{
    "valid": bool,
    "errors": ["Error message 1", "Error message 2", ...]
}

# If validation fails
if not validation["valid"]:
    return {
        "success": False,
        "message": f"Invalid configuration: {', '.join(validation['errors'])}"
    }
```

### Built-in Validations

1. **Type Checking**: Ensures value matches expected type
2. **Range Validation**: For sliders (min/max bounds)
3. **Required Fields**: Ensures critical fields are present
4. **Format Validation**: URL, email, path formats

## Keyboard Shortcuts

### Modal Navigation

- **↑ / ↓**: Navigate between widgets
- **PgUp / PgDn**: Jump between sections
- **Enter**: Toggle checkbox or edit focused widget
- **Ctrl+S**: Save all changes
- **Escape**: Cancel and close modal

### Widget Editing

- **Checkbox**: Enter toggles on/off
- **Slider**: ← / → adjust value, PgUp/PgDn larger steps
- **Text Input**: Type to edit, Enter to confirm
- **Dropdown**: ↑ / ↓ select option, Enter confirm

## Integration Points

### 1. Initialization

```python
# In Application or InputHandler
config_manager = ConfigManager(config_path)
config = config_manager.load_config_file()

# Config service used throughout app
llm_service = LLMService(config=config)
terminal_renderer = TerminalRenderer(config=config)
```

### 2. Modal Creation

```python
# In ModalController
modal_renderer = ModalRenderer(
    terminal_renderer=self.renderer,
    visual_effects=getattr(self.renderer, "visual_effects", None),
    config_service=self.config  # CRITICAL: Enables save functionality
)
```

### 3. Command Registration

```python
# In SystemCommands
registry.register_command(CommandDefinition(
    name="config",
    description="Configure system settings",
    category=CommandCategory.SYSTEM,
    handler=self.handle_config
))
```

## Testing

### Test Locations

1. **Config Manager**: `tests/unit/test_config_manager.py`
2. **Modal Actions**: `tests/unit/test_modal_actions.py`
3. **Widget System**: `tests/unit/test_widgets.py`
4. **Integration**: `tests/integration/test_config_modal.py`

### Manual Testing

```bash
# Test configuration modal
1. Run: kollab
2. Type: /config
3. Modal opens with all settings
4. Navigate with arrow keys
5. Edit values (Enter, type, etc.)
6. Press Ctrl+S to save
7. Verify changes in .kollabor-cli/config.json

# Test validation
1. Open /config
2. Set invalid value (e.g., FPS = 999)
3. Press Ctrl+S
4. Should show validation error

# Test cancel
1. Open /config
2. Edit several values
3. Press Escape
4. Verify no changes saved
```

## Troubleshooting

### Issue: Save Not Working

**Symptoms**:
- Ctrl+S pressed but no changes saved
- No success message

**Diagnosis**:
```python
# Check if action_handler exists
if not hasattr(modal_renderer, "action_handler"):
    # config_service not passed to ModalRenderer
```

**Solution**: Ensure `config_service` passed when creating ModalRenderer

### Issue: Widget Changes Not Detected

**Symptoms**:
- Save says "No changes to save"
- Changes made but not collected

**Diagnosis**: Widget not storing pending value properly

**Solution**: Check widget implementation of value tracking

### Issue: Validation Errors

**Symptoms**:
- Save fails with validation error
- Error message unclear

**Solution**: Check validation rules in widget definition

### Issue: Config File Not Updated

**Symptoms**:
- Save succeeds but file unchanged
- Old values persist

**Diagnosis**:
```python
# Check file permissions
ls -la .kollabor-cli/config.json

# Check save implementation
config_manager.save_config_file(config)  # Should return True
```

## Design Rationale

### Why Modal UI?

1. **Rich Interaction**: Full widget support (sliders, dropdowns, etc.)
2. **Organization**: Sections group related settings
3. **Discovery**: All settings visible in one place
4. **Validation**: Immediate feedback on invalid values
5. **Safety**: Cancel discards changes, save confirms

### Why Dot Notation?

1. **Simplicity**: Easy to understand and use
2. **Flexibility**: Supports nested configuration
3. **Consistency**: Same pattern throughout app
4. **Type Safety**: Can be validated at access time

### Why Widget System?

1. **Extensibility**: Plugins can add their own widgets
2. **Consistency**: Uniform editing experience
3. **Validation**: Type-appropriate input constraints
4. **UX**: Visual feedback for all interactions

## Future Enhancements

### Potential Improvements

1. **Config Profiles**: Save/load different configurations
2. **Config Import/Export**: Share configurations
3. **Config Diff**: Show what changed since last save
4. **Config History**: Undo/redo configuration changes
5. **Config Search**: Search for specific settings
6. **Live Preview**: See changes before saving
7. **Config Templates**: Predefined configuration sets

### Plugin Enhancements

1. **Plugin Categories**: Group plugins by function
2. **Plugin Dependencies**: Handle plugin requirements
3. **Plugin Conflicts**: Detect conflicting plugins
4. **Plugin Profiles**: Plugin configurations per profile

## Related Documentation

- [Modal System Implementation Guide](modal-system-implementation-guide.md) - Original design document
- [Hook System SDK](hook-system-sdk.md) - Plugin development
- [Architecture Overview](architecture-overview.md) - System architecture
- [Slash Commands Guide](slash-commands-guide.md) - Command system

## References

- `core/config/manager.py` - Config loading and saving
- `core/config/service.py` - Config service layer
- `core/ui/config_widgets.py` - Widget definitions
- `core/ui/modal_renderer.py` - Modal rendering
- `core/ui/modal_actions.py` - Save/cancel handling
- `core/ui/config_merger.py` - Change collection and application
- `core/commands/system_commands.py` - /config command implementation
- `tests/unit/test_config_manager.py` - Test suite
