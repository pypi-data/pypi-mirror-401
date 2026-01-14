# Core vs Plugin Extraction Specification

**Version:** 1.0
**Date:** 2025-01-07
**Status:** Draft - Awaiting Approval
**Estimated Effort:** 15 days (3 engineer weeks)
**Lines to Extract:** ~10,855 lines from core/ to plugins/

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Goals](#architecture-goals)
3. [Core Principle](#core-principle)
4. [Before & After State](#before--after-state)
5. [Phase 1: Visual Effects Extraction](#phase-1-visual-effects-extraction)
6. [Phase 2: Command System Extraction](#phase-2-command-system-extraction)
7. [Phase 3: LLM Services Extraction](#phase-3-llm-services-extraction)
8. [Phase 4: UI Components Extraction](#phase-4-ui-components-extraction)
9. [Phase 5: I/O Components Extraction](#phase-5-io-components-extraction)
10. [Hook System Additions](#hook-system-additions)
11. [Testing Strategy](#testing-strategy)
12. [Migration Checklist](#migration-checklist)
13. [Rollback Plan](#rollback-plan)
14. [Timeline & Milestones](#timeline--milestones)

---

## Executive Summary

### Goal
Transform Kollabor CLI from a monolithic application into a minimal core + plugin ecosystem suitable for marketplace distribution.

### Strategy
- **Minimal Core:** Stable LLM chat client with plugin infrastructure (~19,000 lines)
- **Official Plugins:** Full-featured bundled plugins auto-installed with core (~11,000 lines)
- **Marketplace Plugins:** Optional third-party and premium plugins

### Success Metrics
- Core reduced by 36% (10,855 lines extracted)
- 100% feature parity maintained
- All tests passing
- Plugin marketplace-ready architecture

---

## Architecture Goals

### What IS Core (Must Stay)
1. **Terminal I/O Primitives**
   - Raw mode terminal control
   - Keyboard input parsing
   - Cursor management
   - Buffer management
   - Basic color detection

2. **LLM Communication Infrastructure**
   - HTTP client for API calls
   - Streaming response handling
   - Basic conversation history
   - Response parsing (basic)

3. **Plugin System Infrastructure**
   - Plugin discovery and loading
   - Event bus (registry, executor, processor)
   - Hook registration and execution
   - Dependency injection framework

4. **Configuration Infrastructure**
   - Config file loading/saving
   - Dot notation access
   - Basic validation

5. **Command Infrastructure**
   - Command parsing
   - Command registry
   - Command execution framework
   - Only /help and /version commands

6. **Modal Infrastructure**
   - Modal state management
   - Alternate buffer handling
   - Modal overlay rendering
   - Base widget class only

7. **State Persistence Infrastructure**
   - Database connection
   - State save/load framework

### What IS Plugin (Must Move)
1. **Visual Effects** - All cosmetic rendering
2. **Specific Commands** - /profile, /agent, /skill, /config, /status, /resume
3. **Tool Implementations** - File operations, MCP tools
4. **Feature Systems** - Profiles, agents, skills
5. **Concrete Widgets** - Checkbox, dropdown, slider, text input
6. **Status Views** - All view implementations
7. **Integration Protocols** - MCP, model routing

---

## Core Principle

**Minimal Stable Core Test:**
> A user with ZERO plugins installed can:
> - Connect to an LLM API (hardcoded in config file)
> - Send messages and receive responses
> - View conversation history
> - Use /help to discover commands
> - Use /version to check app version
> - Load and enable plugins

**Everything else is a plugin.**

---

## Before & After State

### Current State (Before)

```
core/
├── commands/
│   ├── system_commands.py          # 2,350 lines - 8 commands
│   ├── parser.py                   # Command parsing - KEEP
│   ├── executor.py                 # Command execution - KEEP
│   ├── registry.py                 # Command registry - KEEP
│   └── menu_renderer.py            # Command menu - KEEP
├── io/
│   ├── visual_effects.py           # 1,386 lines - effects + color
│   ├── core_status_views.py        # 315 lines - view implementations
│   ├── config_status_view.py       # 251 lines - config view
│   ├── layout.py                   # 600 lines - layout + thinking animation
│   ├── terminal_renderer.py        # 633 lines - rendering + effects
│   ├── message_renderer.py         # 607 lines - messages + formatting
│   ├── input_handler.py            # 415 lines - input + command menu
│   ├── status_renderer.py          # 386 lines - status infra + views
│   ├── message_coordinator.py      # 304 lines - KEEP
│   ├── buffer_manager.py           # 368 lines - KEEP
│   ├── key_parser.py               # 352 lines - KEEP
│   └── terminal_state.py           # 569 lines - KEEP
├── llm/
│   ├── llm_service.py              # 800 lines - KEEP
│   ├── api_communication_service.py # 400 lines - KEEP
│   ├── conversation_manager.py     # 500 lines - KEEP
│   ├── file_operations_executor.py # 1,423 lines - MOVE
│   ├── profile_manager.py          # 1,054 lines - MOVE
│   ├── agent_manager.py            # 876 lines - MOVE
│   ├── mcp_integration.py          # 300 lines - MOVE
│   ├── model_router.py             # 200 lines - MOVE
│   ├── conversation_logger.py      # 400 lines - partial MOVE
│   ├── response_parser.py          # 300 lines - KEEP
│   ├── response_processor.py       # 250 lines - KEEP
│   ├── message_display_service.py  # 350 lines - KEEP
│   └── plugin_sdk.py               # 450 lines - KEEP
├── ui/
│   ├── modal_renderer.py           # 400 lines - KEEP infra
│   ├── modal_state_manager.py      # 250 lines - KEEP
│   ├── modal_overlay_renderer.py   # 200 lines - KEEP
│   ├── live_modal_renderer.py      # 180 lines - KEEP
│   ├── config_merger.py            # 200 lines - MOVE
│   ├── config_widgets.py           # 250 lines - MOVE
│   ├── modal_actions.py            # 150 lines - MOVE
│   └── widgets/
│       ├── base_widget.py          # 100 lines - KEEP
│       ├── checkbox.py             # 80 lines - MOVE
│       ├── dropdown.py             # 100 lines - MOVE
│       ├── text_input.py           # 120 lines - MOVE
│       ├── slider.py               # 100 lines - MOVE
│       └── label.py                # 60 lines - MOVE
├── fullscreen/
│   ├── plugin.py                   # Base class - KEEP
│   ├── manager.py                  # Manager - KEEP
│   ├── session.py                  # Session - KEEP
│   ├── renderer.py                 # Renderer - KEEP
│   ├── command_integration.py      # Integration - KEEP
│   └── components/
│       └── matrix_components.py    # 200 lines - MOVE
└── effects/
    └── __init__.py                 # Empty - DELETE

plugins/
├── enhanced_input_plugin.py        # KEEP
├── hook_monitoring_plugin.py       # KEEP
├── query_enhancer_plugin.py        # KEEP
├── save_conversation_plugin.py     # KEEP
├── resume_conversation_plugin.py   # KEEP
├── workflow_enforcement_plugin.py  # KEEP
├── system_commands_plugin.py       # KEEP (wraps core)
├── tmux_plugin.py                  # KEEP
└── fullscreen/
    ├── matrix_plugin.py            # KEEP
    └── setup_wizard_plugin.py      # KEEP
```

### Target State (After)

```
core/
├── commands/
│   ├── system_commands.py          # 150 lines - /help, /version ONLY
│   ├── parser.py                   # Command parsing - KEEP
│   ├── executor.py                 # Command execution - KEEP
│   ├── registry.py                 # Command registry - KEEP
│   └── menu_renderer.py            # Command menu - KEEP
├── io/
│   ├── color_support.py            # 200 lines - NEW (extracted from visual_effects)
│   ├── layout.py                   # 400 lines - layout ONLY (no thinking animation)
│   ├── terminal_renderer.py        # 500 lines - slim (delegates to plugins)
│   ├── message_renderer.py         # 450 lines - basic rendering (no effects)
│   ├── input_handler.py            # 350 lines - basic input (no command menu extras)
│   ├── status_renderer.py          # 200 lines - infrastructure ONLY
│   ├── message_coordinator.py      # 304 lines - KEEP
│   ├── buffer_manager.py           # 368 lines - KEEP
│   ├── key_parser.py               # 352 lines - KEEP
│   └── terminal_state.py           # 569 lines - KEEP
├── llm/
│   ├── llm_service.py              # 800 lines - KEEP
│   ├── api_communication_service.py # 400 lines - KEEP
│   ├── conversation_manager.py     # 500 lines - KEEP
│   ├── conversation_logger.py      # 250 lines - basic persistence ONLY
│   ├── response_parser.py          # 300 lines - KEEP
│   ├── response_processor.py       # 250 lines - KEEP
│   ├── message_display_service.py  # 350 lines - KEEP
│   ├── plugin_sdk.py               # 450 lines - KEEP
│   └── tool_executor.py            # 200 lines - framework ONLY (no specific tools)
├── ui/
│   ├── modal_renderer.py           # 350 lines - infra ONLY
│   ├── modal_state_manager.py      # 250 lines - KEEP
│   ├── modal_overlay_renderer.py   # 200 lines - KEEP
│   ├── live_modal_renderer.py      # 180 lines - KEEP
│   └── widgets/
│       └── base_widget.py          # 100 lines - KEEP
├── fullscreen/
│   ├── plugin.py                   # Base class - KEEP
│   ├── manager.py                  # Manager - KEEP
│   ├── session.py                  # Session - KEEP
│   ├── renderer.py                 # Renderer - KEEP
│   └── command_integration.py      # Integration - KEEP
└── (effects/ directory DELETED)

plugins/
├── (existing plugins - KEEP ALL)
├── visual_effects_plugin.py        # NEW - 1,186 lines from core
├── default_status_views_plugin.py  # NEW - 315 lines from core
├── config_status_plugin.py         # NEW - 251 lines from core
├── thinking_animation_plugin.py    # NEW - 200 lines from core
├── ui_widgets_plugin.py            # NEW - 460 lines from core
├── config_modal_plugin.py          # NEW - 600 lines from core
├── profile_management_plugin.py    # NEW - 800 lines from core
├── agent_management_plugin.py      # NEW - 600 lines from core
├── skill_management_plugin.py      # NEW - 400 lines from core
├── configuration_plugin.py         # NEW - 100 lines from core
├── diagnostics_plugin.py           # NEW - 50 lines from core
├── session_plugin.py               # NEW - 400 lines from core
├── file_operations_plugin.py       # NEW - 1,423 lines from core
├── mcp_plugin.py                   # NEW - 300 lines from core
├── model_router_plugin.py          # NEW - 200 lines from core
├── conversation_export_plugin.py   # NEW - 150 lines from core
└── fullscreen/
    ├── matrix_components.py        # NEW - 200 lines from core
    ├── matrix_plugin.py            # UPDATED - uses new location
    └── setup_wizard_plugin.py      # KEEP
```

**Core Reduction:**
- Before: ~30,000 lines
- After: ~19,000 lines
- Extracted: ~11,000 lines (36% reduction)

**Plugin Expansion:**
- Before: 9 plugins (~5,000 lines)
- After: 25 plugins (~16,000 lines)
- Added: 16 official plugins (~11,000 lines)

---

## Phase 1: Visual Effects Extraction

**Priority:** HIGH
**Effort:** 2-3 days
**Lines Moved:** ~1,900 lines
**Risk:** LOW (purely cosmetic)

### 1.1 Split visual_effects.py

#### Current File: core/io/visual_effects.py (1,386 lines)

**Classes and Functions to KEEP in core/io/color_support.py:**

```python
# Enums (lines 15-22)
class ColorSupport(Enum):
    NONE = 0
    BASIC = 16
    EXTENDED = 256
    TRUE_COLOR = 16777216

# Detection functions (lines 24-131)
def detect_color_support() -> ColorSupport:
    """Detect terminal color capabilities"""
    # Check COLORTERM, TERM_PROGRAM, TERM variables
    # Return appropriate ColorSupport level

def get_color_support() -> ColorSupport:
    """Get cached color support level"""
    # Returns cached result from detection

def set_color_support(support: ColorSupport) -> None:
    """Manually override color support"""
    # Allows user/env override

def reset_color_support() -> None:
    """Clear cached color support"""
    # Force re-detection

# Color conversion (lines 132-163)
def rgb_to_256(r: int, g: int, b: int) -> int:
    """Convert RGB to 256-color palette"""
    # Standard conversion algorithm

def color_code(
    r: int = None,
    g: int = None,
    b: int = None,
    color_256: int = None,
    fg: bool = True
) -> str:
    """Generate ANSI color escape code"""
    # Returns appropriate escape based on ColorSupport

# Basic color palette (lines 320-407)
class ColorPalette:
    """Metaclass for dynamic color generation"""
    RESET = "\033[0m"
    DIM = "\033[2m"
    BRIGHT = "\033[1m"

    # Basic ANSI colors
    BLACK = staticmethod(lambda: color_code(...))
    RED = staticmethod(lambda: color_code(...))
    GREEN = staticmethod(lambda: color_code(...))
    YELLOW = staticmethod(lambda: color_code(...))
    BLUE = staticmethod(lambda: color_code(...))
    MAGENTA = staticmethod(lambda: color_code(...))
    CYAN = staticmethod(lambda: color_code(...))
    WHITE = staticmethod(lambda: color_code(...))

def make_fg_color(r: int, g: int, b: int) -> str:
    """Helper to create foreground color"""

def make_bg_color(r: int, g: int, b: int) -> str:
    """Helper to create background color"""
```

**Total for core/io/color_support.py: ~200 lines**

**Classes to MOVE to plugins/visual_effects_plugin.py:**

```python
# Effect type enum (lines 193-202)
class EffectType(Enum):
    SHIMMER = "shimmer"
    PULSE = "pulse"
    SCRAMBLE = "scramble"
    GRADIENT = "gradient"

# Effect configuration (lines 204-218)
@dataclass
class EffectConfig:
    effect_type: EffectType
    speed: float
    intensity: float
    colors: List[str]

# Powerline separators (lines 358-384)
class Powerline:
    """Powerline/Nerd Font separator characters"""
    RIGHT_FILLED = ""
    LEFT_FILLED = ""
    RIGHT_OUTLINE = ""
    LEFT_OUTLINE = ""
    # ... more separators

# Agnoster colors (lines 429-450)
class AgnosterColors:
    """Theme-specific color schemes"""
    LIME_SCHEME = {...}
    CYAN_SCHEME = {...}
    PURPLE_SCHEME = {...}

# Shimmer effect (lines 452-521)
class ShimmerEffect:
    """Wave shimmer animation effect"""

    def __init__(self, text: str, base_color: str, wave_length: int = 10):
        self.text = text
        self.base_color = base_color
        self.wave_length = wave_length
        self.phase = 0

    def next_frame(self) -> str:
        """Generate next animation frame"""
        # Wave algorithm with phase advancement

    def apply_to_segment(self, text: str, position: int) -> str:
        """Apply shimmer to text segment"""
        # Brightness modulation based on wave

# Pulse effect (lines 523-594)
class PulseEffect:
    """Pulsing brightness effect"""

    def __init__(self, text: str, color: str, speed: float = 1.0):
        self.text = text
        self.color = color
        self.speed = speed
        self.brightness = 0.5
        self.direction = 1

    def next_frame(self) -> str:
        """Generate next pulse frame"""
        # Sine wave brightness modulation

# Scramble effect (lines 596-688)
class ScrambleEffect:
    """Text scramble/glitch effect"""

    def __init__(
        self,
        original_text: str,
        scramble_chars: str = "!@#$%^&*()_+-=[]{}|;:,.<>?",
        reveal_speed: float = 0.1
    ):
        self.original = original_text
        self.scramble_chars = scramble_chars
        self.reveal_speed = reveal_speed
        self.revealed = 0

    def next_frame(self) -> str:
        """Generate next scramble frame"""
        # Progressive reveal with random characters

# Agnoster segments (lines 690-810)
class AgnosterSegment:
    """Powerline-style status segments"""

    def __init__(
        self,
        text: str,
        bg_color: str,
        fg_color: str = None,
        separator: str = Powerline.RIGHT_FILLED
    ):
        self.text = text
        self.bg_color = bg_color
        self.fg_color = fg_color or ColorPalette.WHITE()
        self.separator = separator

    def render(self, next_bg_color: str = None) -> str:
        """Render segment with powerline separators"""
        # Background + text + separator transition

    @staticmethod
    def render_chain(segments: List['AgnosterSegment']) -> str:
        """Render multiple connected segments"""
        # Chain rendering with color transitions

# Gradient renderer (lines 812-980)
class GradientRenderer:
    """Multi-color gradient effects"""

    def __init__(self):
        self.color_support = get_color_support()

    def apply_white_to_grey(self, text: str) -> str:
        """White to grey gradient"""
        # Linear gradient from white to grey

    def apply_dim_white_gradient(self, text: str) -> str:
        """Dim white gradient for subtle effects"""
        # Subtle white variation

    def apply_dim_scheme_gradient(
        self,
        text: str,
        scheme: Dict[str, str]
    ) -> str:
        """Apply themed gradient from scheme"""
        # Multi-color gradient using scheme colors

    def apply_custom_gradient(
        self,
        text: str,
        colors: List[Tuple[int, int, int]]
    ) -> str:
        """Apply custom RGB gradient"""
        # Interpolate between custom colors

    def _interpolate_color(
        self,
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int],
        ratio: float
    ) -> Tuple[int, int, int]:
        """Interpolate between two RGB colors"""
        # Linear RGB interpolation

# Status colorizer (lines 982-1174)
class StatusColorizer:
    """Semantic status coloring"""

    STATUS_COLORS = {
        'success': (0, 255, 0),
        'error': (255, 0, 0),
        'warning': (255, 165, 0),
        'info': (100, 149, 237),
        'pending': (255, 255, 0)
    }

    def __init__(self):
        self.color_support = get_color_support()

    def colorize(self, text: str, status: str) -> str:
        """Apply semantic color to status text"""

    def colorize_diff(self, text: str, diff_type: str) -> str:
        """Colorize git-style diff lines"""
        # + green, - red, @ blue

    def colorize_log_level(self, text: str, level: str) -> str:
        """Colorize logging levels"""
        # DEBUG grey, INFO blue, WARNING orange, ERROR red

# Banner renderer (lines 1176-1247)
class BannerRenderer:
    """ASCII art banner generation"""

    BANNER_FONTS = {
        'standard': {...},
        'small': {...},
        'block': {...}
    }

    def __init__(self, font: str = 'standard'):
        self.font = self.BANNER_FONTS.get(font, self.BANNER_FONTS['standard'])

    def render(self, text: str, color: str = None) -> str:
        """Render text as ASCII art"""
        # Convert to ASCII art using font

    def render_gradient(
        self,
        text: str,
        gradient_colors: List[Tuple[int, int, int]]
    ) -> str:
        """Render banner with gradient"""
        # ASCII art + gradient combination

# Visual effects coordinator (lines 1249-1386)
class VisualEffects:
    """Main coordinator for all visual effects"""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.shimmer = None
        self.pulse = None
        self.gradient = GradientRenderer()
        self.status = StatusColorizer()
        self.banner = BannerRenderer()

    def create_shimmer(self, text: str, **kwargs) -> ShimmerEffect:
        """Factory for shimmer effects"""

    def create_pulse(self, text: str, **kwargs) -> PulseEffect:
        """Factory for pulse effects"""

    def create_scramble(self, text: str, **kwargs) -> ScrambleEffect:
        """Factory for scramble effects"""

    def apply_gradient(self, text: str, style: str = 'white_grey') -> str:
        """Apply gradient with named style"""

    def create_status_segment(
        self,
        text: str,
        status: str,
        use_powerline: bool = True
    ) -> str:
        """Create status segment with optional powerline"""

    def create_banner(self, text: str, style: str = 'standard') -> str:
        """Create ASCII banner"""
```

**Total for plugins/visual_effects_plugin.py: ~1,186 lines**

#### Migration Steps for visual_effects.py:

1. **Create new file: core/io/color_support.py**
   ```bash
   # Extract color detection and basic palette
   - Copy ColorSupport enum (lines 15-22)
   - Copy detect_color_support() (lines 24-86)
   - Copy get/set/reset_color_support() (lines 87-131)
   - Copy rgb_to_256() (lines 132-163)
   - Copy color_code() (lines 164-191)
   - Copy ColorPalette metaclass (lines 320-407) - basic colors only
   - Copy make_fg_color/make_bg_color (lines 386-407)
   - Add module docstring
   - Total: ~200 lines
   ```

2. **Create new file: plugins/visual_effects_plugin.py**
   ```python
   """
   Visual Effects Plugin

   Provides all cosmetic visual effects for terminal rendering:
   - Shimmer, pulse, scramble animations
   - Gradient rendering
   - Powerline/Agnoster segments
   - Status colorization
   - ASCII banner generation
   """

   from core.plugins.base import BasePlugin
   from core.events.types import EventType, HookPriority
   from core.io.color_support import ColorPalette, get_color_support, color_code

   # Copy all effect classes from visual_effects.py
   # - EffectType enum
   # - EffectConfig dataclass
   # - Powerline class
   # - AgnosterColors class
   # - ShimmerEffect class
   # - PulseEffect class
   # - ScrambleEffect class
   # - AgnosterSegment class
   # - GradientRenderer class
   # - StatusColorizer class
   # - BannerRenderer class
   # - VisualEffects coordinator class

   class VisualEffectsPlugin(BasePlugin):
       """Plugin providing visual effects for terminal rendering"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.effects = VisualEffects(config.get("plugins.visual_effects", {}))

       def initialize(self):
           """Initialize visual effects system"""
           self.logger.info("Visual effects plugin initialized")

       def register_hooks(self):
           """Register hooks for effect rendering"""
           self.event_bus.register_hook(
               EventType.RENDER_MESSAGE,
               self._apply_message_effects,
               priority=HookPriority.NORMAL
           )
           self.event_bus.register_hook(
               EventType.RENDER_STATUS,
               self._apply_status_effects,
               priority=HookPriority.NORMAL
           )

       async def _apply_message_effects(self, context: dict) -> dict:
           """Apply effects to message rendering"""
           if context.get("apply_gradient"):
               context["text"] = self.effects.apply_gradient(
                   context["text"],
                   context.get("gradient_style", "white_grey")
               )
           return context

       async def _apply_status_effects(self, context: dict) -> dict:
           """Apply effects to status rendering"""
           if context.get("use_powerline"):
               # Apply powerline segments
               pass
           return context

       def get_status_line(self, area: str) -> Optional[str]:
           """No status contribution from this plugin"""
           return None

       def shutdown(self):
           """Cleanup visual effects"""
           self.logger.info("Visual effects plugin shutdown")
   ```

3. **Update imports across codebase**
   ```python
   # OLD (before)
   from core.io.visual_effects import (
       ColorPalette,
       GradientRenderer,
       ShimmerEffect,
       AgnosterSegment
   )

   # NEW (after)
   from core.io.color_support import ColorPalette, get_color_support
   # For effects, access via plugin:
   # visual_effects_plugin.effects.create_shimmer(...)
   ```

4. **Update files that import visual_effects:**
   - `core/io/terminal_renderer.py` - Update gradient imports
   - `core/io/message_renderer.py` - Update effect imports
   - `core/io/core_status_views.py` - Will be moved to plugin anyway
   - `core/ui/widgets/` - Update ColorPalette import to color_support
   - `plugins/enhanced_input_plugin.py` - Update imports
   - `plugins/save_conversation_plugin.py` - Update imports

5. **Delete old file**
   ```bash
   git rm core/io/visual_effects.py
   ```

6. **Add plugin to default config**
   ```json
   {
     "plugins": {
       "visual_effects": {
         "enabled": true,
         "shimmer_speed": 1.0,
         "gradient_style": "white_grey",
         "use_powerline": true,
         "banner_font": "standard"
       }
     }
   }
   ```

7. **Add tests**
   ```python
   # tests/unit/test_visual_effects_plugin.py
   class TestVisualEffectsPlugin(unittest.TestCase):
       def test_shimmer_effect(self):
           effect = ShimmerEffect("test", ColorPalette.GREEN())
           frame1 = effect.next_frame()
           frame2 = effect.next_frame()
           self.assertNotEqual(frame1, frame2)

       def test_gradient_renderer(self):
           renderer = GradientRenderer()
           result = renderer.apply_white_to_grey("test")
           self.assertIn("test", result)
   ```

### 1.2 Extract core_status_views.py

#### Current File: core/io/core_status_views.py (315 lines)

**Classes to MOVE to plugins/default_status_views_plugin.py:**

```python
# Core status views (entire file)
class CoreStatusViews:
    """Default status view implementations"""

    OVERVIEW_VIEW = "overview"
    SESSION_VIEW = "session"
    LLM_DETAILS_VIEW = "llm_details"
    MINIMAL_VIEW = "minimal"

    def __init__(self, config, llm_service=None, agent_manager=None):
        self.config = config
        self.llm_service = llm_service
        self.agent_manager = agent_manager

    def render_overview(self) -> str:
        """Render overview status view"""
        # Agnoster-styled segments
        # Shows: model, profile, agent, skills

    def render_session(self) -> str:
        """Render session status view"""
        # Shows: message count, tokens, cost

    def render_llm_details(self) -> str:
        """Render detailed LLM status"""
        # Shows: temperature, max_tokens, top_p, etc.

    def render_minimal(self) -> str:
        """Render minimal status view"""
        # Just model name

    def get_view(self, view_name: str) -> Optional[Callable]:
        """Get view renderer by name"""
        views = {
            self.OVERVIEW_VIEW: self.render_overview,
            self.SESSION_VIEW: self.render_session,
            self.LLM_DETAILS_VIEW: self.render_llm_details,
            self.MINIMAL_VIEW: self.render_minimal
        }
        return views.get(view_name)
```

#### Migration Steps:

1. **Create plugins/default_status_views_plugin.py**
   ```python
   """
   Default Status Views Plugin

   Provides the standard status view implementations that ship with Kollabor.
   Users can disable this and use alternative status view plugins.
   """

   from core.plugins.base import BasePlugin
   from core.events.types import EventType

   # Copy entire CoreStatusViews class

   class DefaultStatusViewsPlugin(BasePlugin):
       """Plugin providing default status views"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.views = None

       def initialize(self):
           """Initialize status views"""
           # Get LLM service reference
           llm_service = self.get_service("llm_service")
           agent_manager = self.get_service("agent_manager")

           self.views = CoreStatusViews(
               self.config,
               llm_service,
               agent_manager
           )

           # Register views with status renderer
           self.renderer.status_renderer.register_view(
               "overview",
               self.views.render_overview
           )
           self.renderer.status_renderer.register_view(
               "session",
               self.views.render_session
           )
           self.renderer.status_renderer.register_view(
               "llm_details",
               self.views.render_llm_details
           )
           self.renderer.status_renderer.register_view(
               "minimal",
               self.views.render_minimal
           )

           self.logger.info("Default status views registered")

       def register_hooks(self):
           """No hooks needed - views registered directly"""
           pass

       def get_status_line(self, area: str) -> Optional[str]:
           """No status contribution"""
           return None

       def shutdown(self):
           """Cleanup"""
           self.logger.info("Default status views plugin shutdown")
   ```

2. **Update core/io/status_renderer.py**
   ```python
   # Remove hardcoded view imports
   # OLD:
   from core.io.core_status_views import CoreStatusViews

   # NEW:
   # Views registered dynamically by plugins
   # Status renderer just provides registry infrastructure
   ```

3. **Update application.py initialization**
   ```python
   # OLD:
   self.core_views = CoreStatusViews(self.config, self.llm_service)
   self.renderer.register_views(self.core_views)

   # NEW:
   # Views registered automatically when plugin loads
   # No manual registration needed
   ```

### 1.3 Extract config_status_view.py

#### Current File: core/io/config_status_view.py (251 lines)

**Classes to MOVE to plugins/config_status_plugin.py:**

```python
class ConfigStatusView:
    """Configuration health monitoring status view"""

    def __init__(self, config_service):
        self.config_service = config_service

    def render(self) -> str:
        """Render config status"""
        # Shows validation warnings
        # Shows missing required keys
        # Shows deprecated config options

    def get_validation_errors(self) -> List[str]:
        """Get current validation errors"""

    def get_warnings(self) -> List[str]:
        """Get configuration warnings"""
```

#### Migration Steps:

1. **Create plugins/config_status_plugin.py**
   ```python
   """
   Configuration Status Plugin

   Monitors configuration health and displays warnings in status bar.
   """

   from core.plugins.base import BasePlugin

   # Copy ConfigStatusView class

   class ConfigStatusPlugin(BasePlugin):
       """Plugin for configuration health monitoring"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.config_view = None

       def initialize(self):
           """Initialize config monitoring"""
           config_service = self.get_service("config_service")
           self.config_view = ConfigStatusView(config_service)

           # Register view
           self.renderer.status_renderer.register_view(
               "config_health",
               self.config_view.render
           )

       def get_status_line(self, area: str) -> Optional[str]:
           """Show config warnings in status bar"""
           if area == "C":
               warnings = self.config_view.get_warnings()
               if warnings:
                   return f"⚠ Config: {len(warnings)} warnings"
           return None
   ```

2. **Remove from core imports**

### 1.4 Extract ThinkingAnimationManager from layout.py

#### Current File: core/io/layout.py (600 lines)

**Split into:**
- `core/io/layout.py` (400 lines) - Keep LayoutManager only
- `plugins/thinking_animation_plugin.py` (200 lines) - Extract ThinkingAnimationManager

**Classes to KEEP in core/io/layout.py:**

```python
class LayoutManager:
    """Terminal layout management"""

    def __init__(self, terminal_state):
        self.terminal_state = terminal_state
        self.active_area_height = 0
        self.status_area_height = 3

    def calculate_layout(self) -> Dict[str, Any]:
        """Calculate terminal layout dimensions"""
        # Returns areas for status, messages, input

    def get_available_height(self) -> int:
        """Get height available for messages"""

    def resize(self) -> None:
        """Handle terminal resize"""
```

**Classes to MOVE to plugins/thinking_animation_plugin.py:**

```python
class ThinkingAnimationManager:
    """Animated thinking indicator"""

    SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.current_frame = 0
        self.is_active = False

    def start(self) -> None:
        """Start thinking animation"""
        self.is_active = True
        self.current_frame = 0

    def stop(self) -> None:
        """Stop thinking animation"""
        self.is_active = False

    def next_frame(self) -> str:
        """Get next animation frame"""
        if not self.is_active:
            return ""
        frame = self.SPINNER_FRAMES[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.SPINNER_FRAMES)
        return frame

    def render(self, text: str = "Thinking") -> str:
        """Render thinking indicator with text"""
        spinner = self.next_frame()
        return f"{spinner} {text}..."
```

#### Migration Steps:

1. **Edit core/io/layout.py**
   ```python
   # Remove ThinkingAnimationManager class
   # Keep only LayoutManager
   # Update module docstring
   ```

2. **Create plugins/thinking_animation_plugin.py**
   ```python
   """
   Thinking Animation Plugin

   Provides animated spinner for LLM processing indication.
   """

   from core.plugins.base import BasePlugin
   from core.events.types import EventType, HookPriority

   # Copy ThinkingAnimationManager class

   class ThinkingAnimationPlugin(BasePlugin):
       """Plugin for thinking animation"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.animation = None
           self.animation_task = None

       def initialize(self):
           """Initialize animation manager"""
           config = self.config.get("plugins.thinking_animation", {})
           self.animation = ThinkingAnimationManager(config)

       def register_hooks(self):
           """Register animation hooks"""
           self.event_bus.register_hook(
               EventType.LLM_PROCESSING_START,
               self._start_animation,
               priority=HookPriority.HIGH
           )
           self.event_bus.register_hook(
               EventType.LLM_PROCESSING_END,
               self._stop_animation,
               priority=HookPriority.HIGH
           )

       async def _start_animation(self, context: dict) -> dict:
           """Start thinking animation"""
           self.animation.start()
           # Start background animation task
           self.animation_task = self.create_background_task(
               self._animate_loop()
           )
           return context

       async def _stop_animation(self, context: dict) -> dict:
           """Stop thinking animation"""
           self.animation.stop()
           if self.animation_task:
               self.animation_task.cancel()
           return context

       async def _animate_loop(self):
           """Background animation loop"""
           while self.animation.is_active:
               frame = self.animation.next_frame()
               # Update status area with frame
               await asyncio.sleep(0.1)

       def get_status_line(self, area: str) -> Optional[str]:
           """Show thinking indicator in status"""
           if area == "B" and self.animation.is_active:
               return self.animation.render()
           return None
   ```

3. **Update references**
   ```python
   # Files that use ThinkingAnimationManager:
   # - core/io/terminal_renderer.py
   # Update to get animation from plugin instead
   ```

### 1.5 Extract matrix_components.py

#### Current File: core/fullscreen/components/matrix_components.py (200 lines)

**Move entire file to plugins/fullscreen/matrix_components.py**

```python
# Classes to move:
class MatrixColumn:
    """Single falling column in matrix effect"""

    def __init__(self, x: int, height: int, speed: float = 1.0):
        self.x = x
        self.height = height
        self.speed = speed
        self.chars = []
        self.y = 0

    def update(self) -> None:
        """Update column position"""

    def render(self) -> List[Tuple[int, int, str, str]]:
        """Render column characters with positions"""

class MatrixRenderer:
    """Complete matrix rain renderer"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.columns = []
        self._init_columns()

    def _init_columns(self) -> None:
        """Initialize matrix columns"""

    def update(self) -> None:
        """Update all columns"""

    def render(self) -> str:
        """Render complete matrix frame"""
```

#### Migration Steps:

1. **Move file**
   ```bash
   git mv core/fullscreen/components/matrix_components.py plugins/fullscreen/
   ```

2. **Update plugins/fullscreen/matrix_plugin.py**
   ```python
   # OLD:
   from core.fullscreen.components.matrix_components import MatrixRenderer

   # NEW:
   from plugins.fullscreen.matrix_components import MatrixRenderer
   ```

3. **Delete empty directory**
   ```bash
   rmdir core/fullscreen/components/
   ```

### 1.6 Delete core/effects/ directory

```bash
# Directory is empty except __init__.py
git rm -r core/effects/
```

### Phase 1 Summary

**Files Created:**
1. `core/io/color_support.py` (200 lines) - Extracted from visual_effects
2. `plugins/visual_effects_plugin.py` (1,186 lines) - All visual effects
3. `plugins/default_status_views_plugin.py` (315 lines) - Default status views
4. `plugins/config_status_plugin.py` (251 lines) - Config monitoring
5. `plugins/thinking_animation_plugin.py` (200 lines) - Thinking spinner

**Files Modified:**
1. `core/io/visual_effects.py` → DELETED
2. `core/io/core_status_views.py` → DELETED
3. `core/io/config_status_view.py` → DELETED
4. `core/io/layout.py` - Reduced by 200 lines
5. `plugins/fullscreen/matrix_plugin.py` - Updated imports
6. `core/fullscreen/components/matrix_components.py` → MOVED to plugins/fullscreen/

**Files Deleted:**
1. `core/io/visual_effects.py`
2. `core/io/core_status_views.py`
3. `core/io/config_status_view.py`
4. `core/effects/__init__.py`

**Lines Moved:** 1,952 lines from core/ to plugins/

**Test Files to Create:**
1. `tests/unit/test_visual_effects_plugin.py`
2. `tests/unit/test_default_status_views_plugin.py`
3. `tests/unit/test_config_status_plugin.py`
4. `tests/unit/test_thinking_animation_plugin.py`
5. `tests/integration/test_phase1_integration.py`

---

## Phase 2: Command System Extraction

**Priority:** HIGH
**Effort:** 3-4 days
**Lines Moved:** ~2,350 lines
**Risk:** MEDIUM (user-facing commands)

### 2.1 Split system_commands.py

#### Current File: core/commands/system_commands.py (~2,350 lines)

**Contains 8 commands - split as follows:**

**KEEP in core/commands/system_commands.py:**

```python
class CoreSystemCommandsPlugin(BasePlugin):
    """Minimal core system commands"""

    def register_hooks(self):
        """Register core commands only"""
        # /help - essential for discoverability
        # /version - basic app info

    async def _handle_help(self, args: str) -> None:
        """Show available commands"""
        # Lists all registered commands from registry
        # Shows brief usage for each

    async def _handle_version(self, args: str) -> None:
        """Show version information"""
        # Display app version from pyproject.toml
        # Show Python version
        # Show platform info
```

**Total for core: ~150 lines**

**MOVE to plugins/profile_management_plugin.py:**

```python
class ProfileManagementPlugin(BasePlugin):
    """Profile CRUD and management"""

    # /profile command (~800 lines)

    def register_hooks(self):
        """Register /profile command"""
        self.command_registry.register_command(
            CommandDefinition(
                name="profile",
                description="Manage LLM profiles",
                category=CommandCategory.SYSTEM,
                handler=self._handle_profile
            )
        )

    async def _handle_profile(self, args: str) -> None:
        """Handle /profile command"""
        # Subcommands: list, create, edit, delete, select

    async def _show_profile_list(self) -> None:
        """Show all profiles in modal"""
        # Modal with dropdown of profiles
        # Select to switch active profile

    async def _create_profile_wizard(self) -> None:
        """Interactive profile creation"""
        # Multi-step modal:
        # 1. Profile name
        # 2. API provider (OpenAI, Anthropic, etc.)
        # 3. API key
        # 4. Default model
        # 5. Optional: temperature, max_tokens

    async def _edit_profile(self, profile_name: str) -> None:
        """Edit existing profile"""
        # Modal with current values pre-filled
        # Save/Cancel actions

    async def _delete_profile(self, profile_name: str) -> None:
        """Delete profile with confirmation"""
        # Confirmation modal
        # Cannot delete active profile

    async def _select_profile(self, profile_name: str) -> None:
        """Switch to different profile"""
        # Update config
        # Reinitialize LLM service
        # Emit PROFILE_CHANGED event
```

**MOVE to plugins/agent_management_plugin.py:**

```python
class AgentManagementPlugin(BasePlugin):
    """Agent system management"""

    # /agent command (~600 lines)

    def register_hooks(self):
        """Register /agent command"""
        self.command_registry.register_command(
            CommandDefinition(
                name="agent",
                description="Manage agents",
                category=CommandCategory.AGENT,
                handler=self._handle_agent
            )
        )

    async def _handle_agent(self, args: str) -> None:
        """Handle /agent command"""
        # Subcommands: list, create, edit, delete, select

    async def _show_agent_list(self) -> None:
        """Show all agents in modal"""
        # List available agents
        # Show active agent
        # Select to switch

    async def _create_agent_wizard(self) -> None:
        """Interactive agent creation"""
        # Modal wizard:
        # 1. Agent name
        # 2. System prompt
        # 3. Model selection
        # 4. Skills to enable
        # 5. Tools to enable

    async def _edit_agent(self, agent_name: str) -> None:
        """Edit agent configuration"""
        # Edit all agent properties
        # Update agent manager

    async def _delete_agent(self, agent_name: str) -> None:
        """Delete agent with confirmation"""

    async def _select_agent(self, agent_name: str) -> None:
        """Switch active agent"""
        # Update agent manager
        # Emit AGENT_CHANGED event
```

**MOVE to plugins/skill_management_plugin.py:**

```python
class SkillManagementPlugin(BasePlugin):
    """Skill system management"""

    # /skill command (~400 lines)

    def register_hooks(self):
        """Register /skill command"""
        self.command_registry.register_command(
            CommandDefinition(
                name="skill",
                description="Manage skills",
                category=CommandCategory.AGENT,
                handler=self._handle_skill
            )
        )

    async def _handle_skill(self, args: str) -> None:
        """Handle /skill command"""
        # Subcommands: list, load, unload, create, edit, delete

    async def _show_skill_list(self) -> None:
        """Show all skills in modal"""
        # List available skills
        # Show loaded status
        # Toggle to load/unload

    async def _create_skill_wizard(self) -> None:
        """Interactive skill creation"""
        # Modal wizard:
        # 1. Skill name
        # 2. Description
        # 3. Skill prompt template
        # 4. Input parameters

    async def _edit_skill(self, skill_name: str) -> None:
        """Edit skill definition"""

    async def _delete_skill(self, skill_name: str) -> None:
        """Delete skill with confirmation"""

    async def _load_skill(self, skill_name: str) -> None:
        """Load skill into active agent"""
        # Update agent's skill list
        # Emit SKILL_LOADED event

    async def _unload_skill(self, skill_name: str) -> None:
        """Unload skill from active agent"""
```

**MOVE to plugins/configuration_plugin.py:**

```python
class ConfigurationPlugin(BasePlugin):
    """Configuration UI management"""

    # /config command (~100 lines)

    def register_hooks(self):
        """Register /config command"""
        self.command_registry.register_command(
            CommandDefinition(
                name="config",
                description="Edit configuration",
                category=CommandCategory.SYSTEM,
                handler=self._handle_config
            )
        )

    async def _handle_config(self, args: str) -> None:
        """Handle /config command"""
        # Show config tree modal
        # Navigate sections
        # Edit values inline
        # Save/Cancel actions

    async def _show_config_tree(self) -> None:
        """Display config as tree in modal"""
        # Expandable sections:
        # - Terminal
        # - Input
        # - LLM
        # - Application
        # - Plugins

    async def _edit_config_value(self, key: str, current: Any) -> None:
        """Edit single config value"""
        # Show appropriate widget based on type
        # Boolean -> Checkbox
        # Number -> Slider or TextInput
        # String -> TextInput
        # List -> Multi-line TextInput

    async def _save_config(self, changes: dict) -> None:
        """Save config changes"""
        # Validate changes
        # Apply to config service
        # Write to file
        # Emit CONFIG_CHANGED event
```

**MOVE to plugins/diagnostics_plugin.py:**

```python
class DiagnosticsPlugin(BasePlugin):
    """System diagnostics and status"""

    # /status command (~50 lines)

    def register_hooks(self):
        """Register /status command"""
        self.command_registry.register_command(
            CommandDefinition(
                name="status",
                description="Show system status",
                category=CommandCategory.SYSTEM,
                handler=self._handle_status
            )
        )

    async def _handle_status(self, args: str) -> None:
        """Handle /status command"""
        # Display system status modal

    async def _show_status_modal(self) -> None:
        """Show system diagnostics"""
        # Display:
        # - Active profile
        # - Active agent
        # - Loaded skills
        # - Loaded plugins
        # - Config health
        # - Memory usage
        # - Message count
        # - Token usage
```

**MOVE to plugins/session_plugin.py:**

```python
class SessionPlugin(BasePlugin):
    """Session management and resume"""

    # /resume command (~400 lines)

    def register_hooks(self):
        """Register /resume command"""
        self.command_registry.register_command(
            CommandDefinition(
                name="resume",
                description="Resume previous session",
                category=CommandCategory.CONVERSATION,
                aliases=["sessions"],
                handler=self._handle_resume
            )
        )

    async def _handle_resume(self, args: str) -> None:
        """Handle /resume command"""
        # Show session list modal
        # Search and filter sessions
        # Select to resume

    async def _show_session_list(self) -> None:
        """Display all sessions in modal"""
        # List from conversation logger
        # Show: timestamp, message count, preview
        # Sort by date (newest first)
        # Filter by date range, search text

    async def _resume_session(self, session_id: str) -> None:
        """Resume selected session"""
        # Load conversation history
        # Restore context
        # Continue conversation

    async def _delete_session(self, session_id: str) -> None:
        """Delete session with confirmation"""

    async def _export_session(self, session_id: str) -> None:
        """Export session to file"""
        # Delegate to save_conversation_plugin
```

#### Migration Steps for system_commands.py:

1. **Create core/commands/system_commands.py (minimal version)**
   ```python
   """
   Core System Commands

   Provides only essential commands that must always be available:
   - /help - Command discovery
   - /version - Application version
   """

   from core.plugins.base import BasePlugin
   from core.commands.registry import CommandDefinition, CommandCategory

   class CoreSystemCommandsPlugin(BasePlugin):
       """Minimal core commands"""

       def initialize(self):
           """Initialize core commands"""
           self.logger.info("Core system commands initialized")

       def register_hooks(self):
           """Register /help and /version"""
           self.command_registry.register_command(
               CommandDefinition(
                   name="help",
                   description="Show available commands",
                   category=CommandCategory.SYSTEM,
                   handler=self._handle_help
               )
           )
           self.command_registry.register_command(
               CommandDefinition(
                   name="version",
                   description="Show application version",
                   category=CommandCategory.SYSTEM,
                   handler=self._handle_version
               )
           )

       async def _handle_help(self, args: str) -> None:
           """Show command help"""
           commands = self.command_registry.get_all_commands()
           # Display in modal

       async def _handle_version(self, args: str) -> None:
           """Show version info"""
           # Read from pyproject.toml
           # Display in modal
   ```

2. **Create 6 new plugin files** (as detailed above):
   - `plugins/profile_management_plugin.py` (800 lines)
   - `plugins/agent_management_plugin.py` (600 lines)
   - `plugins/skill_management_plugin.py` (400 lines)
   - `plugins/configuration_plugin.py` (100 lines)
   - `plugins/diagnostics_plugin.py` (50 lines)
   - `plugins/session_plugin.py` (400 lines)

3. **Update dependencies**
   - ProfileManagementPlugin needs: profile_manager service
   - AgentManagementPlugin needs: agent_manager service
   - SkillManagementPlugin needs: agent_manager service
   - ConfigurationPlugin needs: config_service
   - DiagnosticsPlugin needs: all services (read-only)
   - SessionPlugin needs: conversation_logger service

4. **Add service injection to plugin SDK**
   ```python
   # core/llm/plugin_sdk.py
   class KollaborPluginSDK:
       def get_service(self, service_name: str) -> Any:
           """Get reference to core service"""
           services = {
               "llm_service": self.llm_service,
               "profile_manager": self.profile_manager,
               "agent_manager": self.agent_manager,
               "config_service": self.config,
               "conversation_logger": self.conversation_logger
           }
           return services.get(service_name)
   ```

5. **Test each plugin independently**
   ```python
   # tests/unit/test_profile_management_plugin.py
   # tests/unit/test_agent_management_plugin.py
   # tests/unit/test_skill_management_plugin.py
   # tests/unit/test_configuration_plugin.py
   # tests/unit/test_diagnostics_plugin.py
   # tests/unit/test_session_plugin.py
   ```

### Phase 2 Summary

**Files Created:**
1. `plugins/profile_management_plugin.py` (800 lines)
2. `plugins/agent_management_plugin.py` (600 lines)
3. `plugins/skill_management_plugin.py` (400 lines)
4. `plugins/configuration_plugin.py` (100 lines)
5. `plugins/diagnostics_plugin.py` (50 lines)
6. `plugins/session_plugin.py` (400 lines)

**Files Modified:**
1. `core/commands/system_commands.py` - Reduced from 2,350 to 150 lines
2. `core/llm/plugin_sdk.py` - Added get_service() method

**Lines Moved:** 2,350 lines from core/ to plugins/

**Test Files to Create:**
1. `tests/unit/test_profile_management_plugin.py`
2. `tests/unit/test_agent_management_plugin.py`
3. `tests/unit/test_skill_management_plugin.py`
4. `tests/unit/test_configuration_plugin.py`
5. `tests/unit/test_diagnostics_plugin.py`
6. `tests/unit/test_session_plugin.py`
7. `tests/integration/test_phase2_integration.py`

---

## Phase 3: LLM Services Extraction

**Priority:** HIGH
**Effort:** 4-5 days
**Lines Moved:** ~3,853 lines
**Risk:** HIGH (core LLM functionality)

### 3.1 Extract file_operations_executor.py

#### Current File: core/llm/file_operations_executor.py (1,423 lines)

**Entire file moves to plugins/file_operations_plugin.py**

**Classes to move:**

```python
class FileOperationsExecutor:
    """Executes file operation tool calls from LLM"""

    SUPPORTED_OPERATIONS = [
        "read_file",
        "write_file",
        "edit_file",
        "list_directory",
        "create_directory",
        "delete_file",
        "delete_directory",
        "move_file",
        "copy_file",
        "search_files",
        "get_file_info"
    ]

    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.safety_enabled = True

    async def execute_operation(
        self,
        operation: str,
        parameters: dict
    ) -> dict:
        """Execute file operation with safety checks"""
        # Validate operation
        # Check safety constraints
        # Execute operation
        # Return result or error

    async def read_file(self, file_path: str, **kwargs) -> dict:
        """Read file contents"""

    async def write_file(
        self,
        file_path: str,
        content: str,
        **kwargs
    ) -> dict:
        """Write content to file"""

    async def edit_file(
        self,
        file_path: str,
        old_text: str,
        new_text: str,
        **kwargs
    ) -> dict:
        """Edit file with find/replace"""

    async def list_directory(self, dir_path: str, **kwargs) -> dict:
        """List directory contents"""

    async def create_directory(self, dir_path: str, **kwargs) -> dict:
        """Create directory"""

    async def delete_file(self, file_path: str, **kwargs) -> dict:
        """Delete file with safety checks"""

    async def delete_directory(self, dir_path: str, **kwargs) -> dict:
        """Delete directory with safety checks"""

    async def move_file(
        self,
        src_path: str,
        dst_path: str,
        **kwargs
    ) -> dict:
        """Move file"""

    async def copy_file(
        self,
        src_path: str,
        dst_path: str,
        **kwargs
    ) -> dict:
        """Copy file"""

    async def search_files(
        self,
        pattern: str,
        directory: str = None,
        **kwargs
    ) -> dict:
        """Search for files matching pattern"""

    async def get_file_info(self, file_path: str, **kwargs) -> dict:
        """Get file metadata"""

    def _validate_path(self, path: str) -> bool:
        """Validate path is within workspace"""

    def _check_safety(self, operation: str, path: str) -> bool:
        """Check safety constraints"""
        # No deleting .git
        # No modifying system files
        # Stay within workspace
```

#### Migration Steps:

1. **Create plugins/file_operations_plugin.py**
   ```python
   """
   File Operations Plugin

   Provides file system tools for LLM to read, write, edit, and manage files.
   This is the standard file operations implementation that ships with Kollabor.

   Tool Catalog:
   - read_file: Read file contents
   - write_file: Write content to file
   - edit_file: Find/replace in file
   - list_directory: List directory contents
   - create_directory: Create directories
   - delete_file: Delete files (with safety)
   - delete_directory: Delete directories (with safety)
   - move_file: Move/rename files
   - copy_file: Copy files
   - search_files: Search for files by pattern
   - get_file_info: Get file metadata
   """

   from core.plugins.base import BasePlugin
   from core.events.types import EventType, HookPriority

   # Copy FileOperationsExecutor class

   class FileOperationsPlugin(BasePlugin):
       """Plugin providing file operation tools"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.executor = None

       def initialize(self):
           """Initialize file operations executor"""
           workspace = self.config.get(
               "plugins.file_operations.workspace_root",
               os.getcwd()
           )
           self.executor = FileOperationsExecutor(workspace)
           self.executor.safety_enabled = self.config.get(
               "plugins.file_operations.safety_enabled",
               True
           )
           self.logger.info(f"File operations initialized: {workspace}")

       def register_hooks(self):
           """Register tool discovery hook"""
           self.event_bus.register_hook(
               EventType.TOOL_DISCOVERY,
               self._register_tools,
               priority=HookPriority.NORMAL
           )

       async def _register_tools(self, context: dict) -> dict:
           """Register all file operation tools"""
           tool_registry = context.get("tool_registry")

           for operation in self.executor.SUPPORTED_OPERATIONS:
               tool_registry.register_tool(
                   name=operation,
                   description=self._get_tool_description(operation),
                   parameters=self._get_tool_parameters(operation),
                   handler=getattr(self.executor, operation)
               )

           self.logger.info(
               f"Registered {len(self.executor.SUPPORTED_OPERATIONS)} file tools"
           )
           return context

       def _get_tool_description(self, operation: str) -> str:
           """Get tool description for LLM"""
           descriptions = {
               "read_file": "Read the contents of a file",
               "write_file": "Write content to a file",
               "edit_file": "Edit a file using find/replace",
               # ... etc
           }
           return descriptions.get(operation, "")

       def _get_tool_parameters(self, operation: str) -> dict:
           """Get tool parameter schema"""
           # Return JSON schema for each operation

       def get_status_line(self, area: str) -> Optional[str]:
           """Show file ops stats in status"""
           if area == "C":
               return f"📁 Workspace: {self.executor.workspace_root}"
           return None
   ```

2. **Update core/llm/tool_executor.py**
   ```python
   # Add tool discovery event
   class ToolExecutor:
       def __init__(self, event_bus):
           self.event_bus = event_bus
           self.tool_registry = ToolRegistry()
           self._discover_tools()

       def _discover_tools(self):
           """Trigger tool discovery event"""
           context = {
               "tool_registry": self.tool_registry
           }
           # Emit TOOL_DISCOVERY event
           # Plugins register their tools
           self.event_bus.emit(EventType.TOOL_DISCOVERY, context)
   ```

3. **Add config defaults**
   ```json
   {
     "plugins": {
       "file_operations": {
         "enabled": true,
         "workspace_root": null,
         "safety_enabled": true,
         "blocked_paths": [".git", "node_modules"],
         "max_file_size": 10485760
       }
     }
   }
   ```

### 3.2 Extract profile_manager.py

#### Current File: core/llm/profile_manager.py (1,054 lines)

**Entire file moves to plugins/profile_plugin.py**

**Note:** This plugin was already split in Phase 2 as ProfileManagementPlugin.
The profile_manager.py SERVICE moves to the plugin.

**Classes to move:**

```python
class ProfileManager:
    """Manages LLM connection profiles"""

    def __init__(self, config_service):
        self.config = config_service
        self.profiles = {}
        self.active_profile = None
        self._load_profiles()

    def _load_profiles(self) -> None:
        """Load profiles from config"""

    def get_active_profile(self) -> dict:
        """Get currently active profile"""

    def set_active_profile(self, profile_name: str) -> None:
        """Switch to different profile"""

    def create_profile(
        self,
        name: str,
        provider: str,
        api_key: str,
        **kwargs
    ) -> None:
        """Create new profile"""

    def update_profile(self, name: str, updates: dict) -> None:
        """Update existing profile"""

    def delete_profile(self, name: str) -> None:
        """Delete profile"""

    def list_profiles(self) -> List[str]:
        """List all profile names"""

    def get_profile(self, name: str) -> dict:
        """Get profile configuration"""

    def resolve_env_vars(self, profile: dict) -> dict:
        """Resolve environment variables in profile"""
        # ${API_KEY} -> actual value from env
```

#### Migration Steps:

1. **Merge into plugins/profile_management_plugin.py**
   ```python
   # The ProfileManagementPlugin created in Phase 2
   # now includes the ProfileManager service class

   class ProfileManagementPlugin(BasePlugin):
       """Combined profile management plugin"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.profile_manager = None

       def initialize(self):
           """Initialize profile manager"""
           self.profile_manager = ProfileManager(self.config)

           # Register as service
           self.register_service("profile_manager", self.profile_manager)

           # Register /profile command (from Phase 2)
           # ...
   ```

2. **Update core/llm/llm_service.py**
   ```python
   # OLD:
   from core.llm.profile_manager import ProfileManager

   # NEW:
   # Get profile_manager from plugin SDK
   profile_manager = self.plugin_sdk.get_service("profile_manager")
   ```

3. **Remove core/llm/profile_manager.py**
   ```bash
   git rm core/llm/profile_manager.py
   ```

### 3.3 Extract agent_manager.py

#### Current File: core/llm/agent_manager.py (876 lines)

**Entire file moves to plugins/agent_plugin.py**

**Classes to move:**

```python
class AgentManager:
    """Manages AI agents and their lifecycles"""

    def __init__(self, config, llm_service):
        self.config = config
        self.llm_service = llm_service
        self.agents = {}
        self.active_agent = None
        self.skill_manager = SkillManager(config)

    def create_agent(
        self,
        name: str,
        system_prompt: str,
        model: str = None,
        **kwargs
    ) -> None:
        """Create new agent"""

    def delete_agent(self, name: str) -> None:
        """Delete agent"""

    def get_agent(self, name: str) -> dict:
        """Get agent configuration"""

    def set_active_agent(self, name: str) -> None:
        """Switch active agent"""

    def get_active_agent(self) -> dict:
        """Get currently active agent"""

    def list_agents(self) -> List[str]:
        """List all agent names"""

    async def delegate_to_agent(
        self,
        agent_name: str,
        task: str
    ) -> str:
        """Delegate task to sub-agent"""
        # Create background task
        # Execute with agent's context
        # Return result

class SkillManager:
    """Manages agent skills"""

    def __init__(self, config):
        self.config = config
        self.skills = {}
        self._load_skills()

    def _load_skills(self) -> None:
        """Load skills from config/filesystem"""

    def create_skill(
        self,
        name: str,
        description: str,
        prompt_template: str,
        **kwargs
    ) -> None:
        """Create new skill"""

    def delete_skill(self, name: str) -> None:
        """Delete skill"""

    def get_skill(self, name: str) -> dict:
        """Get skill definition"""

    def list_skills(self) -> List[str]:
        """List all skill names"""

    def load_skill_into_agent(
        self,
        skill_name: str,
        agent_name: str
    ) -> None:
        """Add skill to agent"""

    def unload_skill_from_agent(
        self,
        skill_name: str,
        agent_name: str
    ) -> None:
        """Remove skill from agent"""
```

#### Migration Steps:

1. **Merge into plugins/agent_management_plugin.py**
   ```python
   # Combines AgentManager service + /agent command + /skill command

   class AgentManagementPlugin(BasePlugin):
       """Complete agent and skill management"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.agent_manager = None

       def initialize(self):
           """Initialize agent manager"""
           llm_service = self.get_service("llm_service")
           self.agent_manager = AgentManager(self.config, llm_service)

           # Register as service
           self.register_service("agent_manager", self.agent_manager)

           # Register /agent and /skill commands
           # ...
   ```

2. **Merge SkillManagementPlugin into AgentManagementPlugin**
   ```python
   # Since skills are tightly coupled to agents,
   # merge both into single plugin
   # Register both /agent and /skill commands
   ```

3. **Remove core files**
   ```bash
   git rm core/llm/agent_manager.py
   ```

### 3.4 Extract mcp_integration.py

#### Current File: core/llm/mcp_integration.py (300 lines)

**Entire file moves to plugins/mcp_plugin.py**

**Classes to move:**

```python
class MCPIntegration:
    """Model Context Protocol integration"""

    def __init__(self, config):
        self.config = config
        self.mcp_servers = {}
        self.tools = {}

    async def discover_servers(self) -> List[str]:
        """Discover MCP servers from config"""
        # Read MCP server definitions
        # Connect to each server
        # Query available tools

    async def connect_server(self, server_name: str, config: dict) -> None:
        """Connect to MCP server"""
        # Establish connection
        # Handshake
        # Store server reference

    async def disconnect_server(self, server_name: str) -> None:
        """Disconnect from MCP server"""

    async def get_server_tools(self, server_name: str) -> List[dict]:
        """Get tools from MCP server"""
        # Query server for tool catalog
        # Return tool definitions

    async def execute_mcp_tool(
        self,
        server_name: str,
        tool_name: str,
        parameters: dict
    ) -> dict:
        """Execute tool on MCP server"""
        # Send tool call to server
        # Wait for response
        # Return result
```

#### Migration Steps:

1. **Create plugins/mcp_plugin.py**
   ```python
   """
   Model Context Protocol (MCP) Plugin

   Enables integration with MCP servers to extend LLM capabilities with
   external tools and data sources.

   Supports:
   - Dynamic MCP server discovery
   - Tool registration from MCP servers
   - Tool execution via MCP protocol
   """

   from core.plugins.base import BasePlugin
   from core.events.types import EventType, HookPriority

   # Copy MCPIntegration class

   class MCPPlugin(BasePlugin):
       """MCP server integration plugin"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.mcp = None

       async def initialize(self):
           """Initialize MCP integration"""
           self.mcp = MCPIntegration(self.config)

           # Auto-discover and connect to configured servers
           servers = await self.mcp.discover_servers()
           self.logger.info(f"Connected to {len(servers)} MCP servers")

       def register_hooks(self):
           """Register MCP tool discovery"""
           self.event_bus.register_hook(
               EventType.TOOL_DISCOVERY,
               self._register_mcp_tools,
               priority=HookPriority.NORMAL
           )

       async def _register_mcp_tools(self, context: dict) -> dict:
           """Register tools from all MCP servers"""
           tool_registry = context.get("tool_registry")

           for server_name in self.mcp.mcp_servers:
               tools = await self.mcp.get_server_tools(server_name)

               for tool in tools:
                   tool_registry.register_tool(
                       name=f"mcp_{server_name}_{tool['name']}",
                       description=tool['description'],
                       parameters=tool['parameters'],
                       handler=lambda params: self.mcp.execute_mcp_tool(
                           server_name,
                           tool['name'],
                           params
                       )
                   )

           return context

       def get_status_line(self, area: str) -> Optional[str]:
           """Show MCP server count in status"""
           if area == "C":
               count = len(self.mcp.mcp_servers)
               if count > 0:
                   return f"🔌 MCP: {count} servers"
           return None
   ```

2. **Remove core/llm/mcp_integration.py**
   ```bash
   git rm core/llm/mcp_integration.py
   ```

### 3.5 Extract model_router.py

#### Current File: core/llm/model_router.py (200 lines)

**Entire file moves to plugins/model_router_plugin.py**

**Classes to move:**

```python
class ModelRouter:
    """Routes requests to appropriate model based on strategy"""

    STRATEGIES = ["cost", "capability", "speed", "custom"]

    def __init__(self, config):
        self.config = config
        self.strategy = config.get("model_router.strategy", "capability")
        self.model_capabilities = self._load_capabilities()

    def _load_capabilities(self) -> dict:
        """Load model capability matrix"""
        # Models and their capabilities:
        # - Context window
        # - Cost per token
        # - Speed (avg response time)
        # - Function calling support
        # - Vision support

    def select_model(
        self,
        task: str,
        context_size: int = 0,
        requires_functions: bool = False,
        requires_vision: bool = False
    ) -> str:
        """Select best model for task"""
        # Apply routing strategy
        # Return model name

    def route_by_cost(self, **kwargs) -> str:
        """Select cheapest model meeting requirements"""

    def route_by_capability(self, **kwargs) -> str:
        """Select most capable model"""

    def route_by_speed(self, **kwargs) -> str:
        """Select fastest model"""

    def route_custom(self, **kwargs) -> str:
        """Use custom routing logic"""
```

#### Migration Steps:

1. **Create plugins/model_router_plugin.py**
   ```python
   """
   Model Router Plugin

   Provides intelligent model selection based on task requirements.

   Routing Strategies:
   - cost: Minimize token cost
   - capability: Maximize model capability
   - speed: Minimize response time
   - custom: User-defined routing logic
   """

   from core.plugins.base import BasePlugin
   from core.events.types import EventType, HookPriority

   # Copy ModelRouter class

   class ModelRouterPlugin(BasePlugin):
       """Intelligent model selection plugin"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.router = None

       def initialize(self):
           """Initialize model router"""
           self.router = ModelRouter(self.config)
           self.logger.info(
               f"Model router initialized: {self.router.strategy}"
           )

       def register_hooks(self):
           """Register model selection hook"""
           self.event_bus.register_hook(
               EventType.PRE_MODEL_SELECTION,
               self._select_model,
               priority=HookPriority.HIGH
           )

       async def _select_model(self, context: dict) -> dict:
           """Override model selection"""
           task = context.get("task", "")
           context_size = context.get("context_size", 0)
           requires_functions = context.get("requires_functions", False)
           requires_vision = context.get("requires_vision", False)

           selected_model = self.router.select_model(
               task,
               context_size,
               requires_functions,
               requires_vision
           )

           context["model"] = selected_model
           self.logger.debug(f"Routed to model: {selected_model}")
           return context

       def get_status_line(self, area: str) -> Optional[str]:
           """Show routing strategy in status"""
           if area == "C":
               return f"🎯 Route: {self.router.strategy}"
           return None
   ```

2. **Remove core/llm/model_router.py**
   ```bash
   git rm core/llm/model_router.py
   ```

### 3.6 Split conversation_logger.py

#### Current File: core/llm/conversation_logger.py (400 lines)

**Split into:**
- `core/llm/conversation_logger.py` (250 lines) - Basic persistence
- `plugins/conversation_export_plugin.py` (150 lines) - Export features

**KEEP in core (basic persistence):**

```python
class KollaborConversationLogger:
    """Basic conversation persistence"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        self._init_database()

    def _init_database(self) -> None:
        """Initialize SQLite database"""
        # Create conversations table
        # Create messages table

    def save_message(
        self,
        role: str,
        content: str,
        session_id: str = None
    ) -> None:
        """Save message to database"""

    def load_session(self, session_id: str) -> List[dict]:
        """Load session messages"""

    def list_sessions(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """List recent sessions"""

    def delete_session(self, session_id: str) -> None:
        """Delete session"""

    def get_session_stats(self, session_id: str) -> dict:
        """Get session statistics"""
```

**MOVE to plugin (export features):**

```python
class ConversationExporter:
    """Export conversations to various formats"""

    def __init__(self, logger: KollaborConversationLogger):
        self.logger = logger

    def export_to_json(self, session_id: str) -> str:
        """Export as JSON"""

    def export_to_markdown(self, session_id: str) -> str:
        """Export as markdown"""

    def export_to_text(self, session_id: str) -> str:
        """Export as plain text"""

    def export_to_html(self, session_id: str) -> str:
        """Export as HTML"""
```

#### Migration Steps:

1. **Slim core/llm/conversation_logger.py**
   ```python
   # Remove export methods
   # Keep only database CRUD operations
   ```

2. **Create plugins/conversation_export_plugin.py**
   ```python
   """
   Conversation Export Plugin

   Provides conversation export in multiple formats:
   - JSON (raw data)
   - Markdown (formatted)
   - Plain text (transcript)
   - HTML (web-ready)
   """

   from core.plugins.base import BasePlugin
   from core.commands.registry import CommandDefinition

   # Copy ConversationExporter class

   class ConversationExportPlugin(BasePlugin):
       """Conversation export functionality"""

       def __init__(self, event_bus, config, renderer, state_manager):
           super().__init__(event_bus, config, renderer, state_manager)
           self.exporter = None

       def initialize(self):
           """Initialize exporter"""
           logger = self.get_service("conversation_logger")
           self.exporter = ConversationExporter(logger)

       def register_hooks(self):
           """Register /export command"""
           self.command_registry.register_command(
               CommandDefinition(
                   name="export",
                   description="Export conversation",
                   handler=self._handle_export
               )
           )

       async def _handle_export(self, args: str) -> None:
           """Handle /export command"""
           # Show export options modal
           # Select format
           # Select session
           # Export to file
   ```

### Phase 3 Summary

**Files Created:**
1. `plugins/file_operations_plugin.py` (1,423 lines)
2. `plugins/mcp_plugin.py` (300 lines)
3. `plugins/model_router_plugin.py` (200 lines)
4. `plugins/conversation_export_plugin.py` (150 lines)

**Files Merged:**
1. `core/llm/profile_manager.py` → Merged into `plugins/profile_management_plugin.py`
2. `core/llm/agent_manager.py` → Merged into `plugins/agent_management_plugin.py`

**Files Modified:**
1. `core/llm/llm_service.py` - Remove direct service dependencies
2. `core/llm/tool_executor.py` - Add tool discovery event
3. `core/llm/conversation_logger.py` - Remove export methods

**Files Deleted:**
1. `core/llm/file_operations_executor.py`
2. `core/llm/profile_manager.py`
3. `core/llm/agent_manager.py`
4. `core/llm/mcp_integration.py`
5. `core/llm/model_router.py`

**Lines Moved:** 3,853 lines from core/ to plugins/

**New Hook Points:**
1. `EventType.TOOL_DISCOVERY` - Plugins register tools
2. `EventType.PRE_MODEL_SELECTION` - Plugins override model choice

**Test Files to Create:**
1. `tests/unit/test_file_operations_plugin.py`
2. `tests/unit/test_mcp_plugin.py`
3. `tests/unit/test_model_router_plugin.py`
4. `tests/unit/test_conversation_export_plugin.py`
5. `tests/integration/test_phase3_integration.py`

---

## Phase 4: UI Components Extraction

**Priority:** MEDIUM
**Effort:** 2-3 days
**Lines Moved:** ~1,200 lines
**Risk:** MEDIUM (UI components)

### 4.1 Extract UI Widgets

#### Current Files: core/ui/widgets/*.py (460 lines total)

**KEEP in core:**
- `base_widget.py` (100 lines) - Abstract base class

**MOVE to plugin:**
- `checkbox.py` (80 lines)
- `dropdown.py` (100 lines)
- `text_input.py` (120 lines)
- `slider.py` (100 lines)
- `label.py` (60 lines)

#### Migration Steps:

1. **Create plugins/ui_widgets_plugin.py**
   ```python
   """
   UI Widgets Plugin

   Provides standard widget set for modal UIs:
   - CheckboxWidget: Boolean toggles
   - DropdownWidget: Option selection
   - TextInputWidget: Text entry with cursor
   - SliderWidget: Numeric sliders
   - LabelWidget: Read-only display
   """

   from core.plugins.base import BasePlugin
   from core.ui.widgets.base_widget import BaseWidget
   from core.events.types import EventType

   # Copy all widget classes from core/ui/widgets/

   class UIWidgetsPlugin(BasePlugin):
       """Standard UI widgets plugin"""

       def initialize(self):
           """Register widget types"""
           self.renderer.modal_renderer.register_widget_type(
               "checkbox",
               CheckboxWidget
           )
           self.renderer.modal_renderer.register_widget_type(
               "dropdown",
               DropdownWidget
           )
           self.renderer.modal_renderer.register_widget_type(
               "text_input",
               TextInputWidget
           )
           self.renderer.modal_renderer.register_widget_type(
               "slider",
               SliderWidget
           )
           self.renderer.modal_renderer.register_widget_type(
               "label",
               LabelWidget
           )
           self.logger.info("Standard UI widgets registered")
   ```

2. **Update core/ui/modal_renderer.py**
   ```python
   class ModalRenderer:
       def __init__(self):
           self.widget_types = {}  # Empty initially

       def register_widget_type(
           self,
           name: str,
           widget_class: Type[BaseWidget]
       ) -> None:
           """Register widget type from plugin"""
           self.widget_types[name] = widget_class

       def create_widget(self, definition: dict) -> BaseWidget:
           """Create widget instance"""
           widget_type = definition.get("type")
           widget_class = self.widget_types.get(widget_type)
           if not widget_class:
               raise ValueError(f"Unknown widget type: {widget_type}")
           return widget_class(**definition)
   ```

3. **Delete core/ui/widgets/*.py (except base_widget.py)**
   ```bash
   git rm core/ui/widgets/checkbox.py
   git rm core/ui/widgets/dropdown.py
   git rm core/ui/widgets/text_input.py
   git rm core/ui/widgets/slider.py
   git rm core/ui/widgets/label.py
   ```

### 4.2 Extract Config UI Components

#### Current Files (600 lines total):
- `core/ui/config_merger.py` (200 lines)
- `core/ui/config_widgets.py` (250 lines)
- `core/ui/modal_actions.py` (150 lines)

**All move to plugins/config_modal_plugin.py**

#### Migration Steps:

1. **Create plugins/config_modal_plugin.py**
   ```python
   """
   Configuration Modal Plugin

   Provides the /config command UI:
   - Interactive config tree editor
   - Widget-based value editing
   - Save/Cancel actions with validation
   - Config merging and persistence
   """

   from core.plugins.base import BasePlugin

   # Copy ConfigMerger, ConfigWidgetDefinitions, ModalActionHandler

   class ConfigModalPlugin(BasePlugin):
       """Configuration UI plugin"""

       def initialize(self):
           """Initialize config UI"""
           self.merger = ConfigMerger(self.config)
           self.widget_defs = ConfigWidgetDefinitions(self.config)
           self.actions = ModalActionHandler(self.merger, self.config)

       # This plugin integrates with ConfigurationPlugin from Phase 2
       # ConfigurationPlugin provides /config command
       # This plugin provides the modal UI implementation
   ```

2. **Merge with plugins/configuration_plugin.py**
   ```python
   # Combine command handler + modal UI into single plugin
   class ConfigurationPlugin(BasePlugin):
       """Complete configuration management"""

       def initialize(self):
           # Command registration (from Phase 2)
           # Modal UI setup (new)
   ```

3. **Delete core/ui config files**
   ```bash
   git rm core/ui/config_merger.py
   git rm core/ui/config_widgets.py
   git rm core/ui/modal_actions.py
   ```

### Phase 4 Summary

**Files Created:**
1. `plugins/ui_widgets_plugin.py` (460 lines)

**Files Merged:**
1. Config UI files → Merged into `plugins/configuration_plugin.py`

**Files Modified:**
1. `core/ui/modal_renderer.py` - Widget registry system
2. `core/ui/widgets/__init__.py` - Only exports BaseWidget

**Files Deleted:**
1. `core/ui/widgets/checkbox.py`
2. `core/ui/widgets/dropdown.py`
3. `core/ui/widgets/text_input.py`
4. `core/ui/widgets/slider.py`
5. `core/ui/widgets/label.py`
6. `core/ui/config_merger.py`
7. `core/ui/config_widgets.py`
8. `core/ui/modal_actions.py`

**Lines Moved:** 1,060 lines from core/ to plugins/

**Test Files to Create:**
1. `tests/unit/test_ui_widgets_plugin.py`
2. `tests/integration/test_phase4_integration.py`

---

## Phase 5: I/O Components Extraction

**Priority:** LOW
**Effort:** 1-2 days
**Lines Moved:** ~490 lines
**Risk:** LOW (minor optimizations)

### 5.1 Slim terminal_renderer.py

**Current:** 633 lines
**Target:** 500 lines (remove 133 lines)

**Extract to plugins:**
- Effect application logic → Delegate to visual_effects_plugin
- Banner creation → Delegate to visual_effects_plugin
- Thinking effect config → Delegate to thinking_animation_plugin

### 5.2 Slim message_renderer.py

**Current:** 607 lines
**Target:** 450 lines (remove 157 lines)

**Extract to plugins:**
- MessageFormatter gradient effects → Delegate to visual_effects_plugin
- Advanced formatting → Hook-based

### 5.3 Slim input_handler.py

**Current:** 415 lines
**Target:** 350 lines (remove 65 lines)

**Extract to plugins:**
- Command menu enhancements → Already in command system
- Modal controller extras → Delegate to modal plugins

### 5.4 Slim status_renderer.py

**Current:** 386 lines
**Target:** 200 lines (remove 186 lines)

**Remove:**
- View implementations (already moved in Phase 1)
- Keep only registry and infrastructure

### Phase 5 Summary

**Files Modified (slimmed):**
1. `core/io/terminal_renderer.py` - 633 → 500 lines
2. `core/io/message_renderer.py` - 607 → 450 lines
3. `core/io/input_handler.py` - 415 → 350 lines
4. `core/io/status_renderer.py` - 386 → 200 lines

**Lines Removed:** 541 lines from core/ (delegation to plugins)

**No new files created** - uses hooks to delegate to existing plugins

---

## Hook System Additions

New hook points required to support plugin extraction:

### EventType Additions (core/events/types.py)

```python
class EventType(Enum):
    # Existing hooks...

    # NEW: Tool system hooks
    TOOL_DISCOVERY = "tool_discovery"
    TOOL_PRE_EXECUTION = "tool_pre_execution"
    TOOL_POST_EXECUTION = "tool_post_execution"

    # NEW: Model selection hooks
    PRE_MODEL_SELECTION = "pre_model_selection"
    POST_MODEL_SELECTION = "post_model_selection"

    # NEW: Profile/Agent hooks
    PROFILE_CHANGED = "profile_changed"
    AGENT_CHANGED = "agent_changed"
    SKILL_LOADED = "skill_loaded"
    SKILL_UNLOADED = "skill_unloaded"

    # NEW: Config hooks
    CONFIG_CHANGED = "config_changed"
    CONFIG_VALIDATED = "config_validated"

    # NEW: Widget hooks
    WIDGET_REGISTER = "widget_register"
    WIDGET_VALUE_CHANGED = "widget_value_changed"

    # NEW: Render hooks
    RENDER_MESSAGE = "render_message"
    RENDER_STATUS = "render_status"
    RENDER_THINKING = "render_thinking"

    # NEW: LLM processing hooks
    LLM_PROCESSING_START = "llm_processing_start"
    LLM_PROCESSING_END = "llm_processing_end"
```

### Plugin SDK Additions (core/llm/plugin_sdk.py)

```python
class KollaborPluginSDK:
    # Existing methods...

    def get_service(self, service_name: str) -> Any:
        """Get reference to core service"""
        services = {
            "llm_service": self.llm_service,
            "profile_manager": self._get_plugin_service("profile_manager"),
            "agent_manager": self._get_plugin_service("agent_manager"),
            "config_service": self.config,
            "conversation_logger": self.conversation_logger,
            "tool_registry": self.tool_registry
        }
        return services.get(service_name)

    def register_service(self, name: str, service: Any) -> None:
        """Register plugin service for other plugins"""
        self.plugin_services[name] = service

    def _get_plugin_service(self, name: str) -> Any:
        """Get service registered by another plugin"""
        return self.plugin_services.get(name)
```

---

## Testing Strategy

### Unit Testing

**Test each plugin independently:**

```python
# tests/unit/test_{plugin_name}.py

class Test{PluginName}(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.event_bus = MockEventBus()
        self.config = MockConfig()
        self.renderer = MockRenderer()
        self.state_manager = MockStateManager()

        self.plugin = {PluginName}(
            self.event_bus,
            self.config,
            self.renderer,
            self.state_manager
        )

    def test_initialization(self):
        """Test plugin initializes correctly"""
        self.plugin.initialize()
        self.assertIsNotNone(self.plugin.{service})

    def test_hook_registration(self):
        """Test hooks are registered"""
        self.plugin.register_hooks()
        self.assertTrue(self.event_bus.has_hook({EventType}))

    def test_functionality(self):
        """Test core plugin functionality"""
        # Test specific features
```

### Integration Testing

**Test plugin interactions:**

```python
# tests/integration/test_phase{N}_integration.py

class TestPhase{N}Integration(unittest.TestCase):
    def setUp(self):
        """Set up full application with Phase N plugins"""
        self.app = TestApplication()
        self.app.load_plugins([
            # Plugins from this phase
        ])

    def test_plugin_communication(self):
        """Test plugins can communicate"""
        # Test service injection
        # Test event propagation

    def test_feature_parity(self):
        """Test all features still work"""
        # Test workflows end-to-end
```

### End-to-End Testing

**Test complete user workflows:**

```python
# tests/e2e/test_user_workflows.py

class TestUserWorkflows(unittest.TestCase):
    def test_profile_management(self):
        """Test complete profile workflow"""
        # Create profile
        # Switch profile
        # Edit profile
        # Delete profile

    def test_file_operations(self):
        """Test LLM can perform file operations"""
        # Read file
        # Write file
        # Edit file

    def test_agent_system(self):
        """Test agent and skills"""
        # Create agent
        # Load skill
        # Execute with skill
```

### Regression Testing

**Ensure no functionality lost:**

```bash
# Run full test suite before and after each phase
python tests/run_tests.py --full

# Compare results
diff before_results.txt after_results.txt

# Manual smoke tests
- Test all /commands
- Test LLM conversation
- Test file operations
- Test visual effects
- Test modals
```

---

## Migration Checklist

### Pre-Migration

- [ ] Backup current main branch: `git branch backup-pre-extraction`
- [ ] Create feature branch: `git checkout -b feature/core-plugin-extraction`
- [ ] Run full test suite: `python tests/run_tests.py`
- [ ] Document current test coverage
- [ ] Freeze dependency versions in requirements.txt

### Phase 1: Visual Effects

- [ ] Create `core/io/color_support.py`
- [ ] Create `plugins/visual_effects_plugin.py`
- [ ] Create `plugins/default_status_views_plugin.py`
- [ ] Create `plugins/config_status_plugin.py`
- [ ] Create `plugins/thinking_animation_plugin.py`
- [ ] Move `core/fullscreen/components/matrix_components.py`
- [ ] Update all imports
- [ ] Delete old files
- [ ] Write unit tests for new plugins
- [ ] Run integration tests
- [ ] Manual smoke test
- [ ] Commit: `git commit -m "Phase 1: Extract visual effects to plugins"`

### Phase 2: Command System

- [ ] Slim `core/commands/system_commands.py` to /help and /version only
- [ ] Create `plugins/profile_management_plugin.py`
- [ ] Create `plugins/agent_management_plugin.py`
- [ ] Create `plugins/skill_management_plugin.py`
- [ ] Create `plugins/configuration_plugin.py`
- [ ] Create `plugins/diagnostics_plugin.py`
- [ ] Create `plugins/session_plugin.py`
- [ ] Add service injection to plugin SDK
- [ ] Update command registry
- [ ] Write unit tests
- [ ] Run integration tests
- [ ] Test all /commands still work
- [ ] Commit: `git commit -m "Phase 2: Extract commands to plugins"`

### Phase 3: LLM Services

- [ ] Create `plugins/file_operations_plugin.py`
- [ ] Create `plugins/mcp_plugin.py`
- [ ] Create `plugins/model_router_plugin.py`
- [ ] Create `plugins/conversation_export_plugin.py`
- [ ] Merge profile_manager into profile_plugin
- [ ] Merge agent_manager into agent_plugin
- [ ] Add TOOL_DISCOVERY event
- [ ] Add PRE_MODEL_SELECTION event
- [ ] Slim conversation_logger
- [ ] Delete extracted files
- [ ] Write unit tests
- [ ] Test file operations still work
- [ ] Test agent system still works
- [ ] Commit: `git commit -m "Phase 3: Extract LLM services to plugins"`

### Phase 4: UI Components

- [ ] Create `plugins/ui_widgets_plugin.py`
- [ ] Add widget registration to modal_renderer
- [ ] Merge config UI into configuration_plugin
- [ ] Delete widget files from core
- [ ] Delete config UI files from core
- [ ] Write unit tests
- [ ] Test all modals still work
- [ ] Test /config command
- [ ] Commit: `git commit -m "Phase 4: Extract UI components to plugins"`

### Phase 5: I/O Slimming

- [ ] Slim terminal_renderer.py
- [ ] Slim message_renderer.py
- [ ] Slim input_handler.py
- [ ] Slim status_renderer.py
- [ ] Add delegation hooks
- [ ] Test rendering still works
- [ ] Test all visual effects work via plugins
- [ ] Commit: `git commit -m "Phase 5: Slim I/O components"`

### Post-Migration

- [ ] Run full test suite
- [ ] Compare coverage with pre-migration
- [ ] Fix any failing tests
- [ ] Update documentation
- [ ] Create migration guide for users
- [ ] Test plugin marketplace architecture
- [ ] Create example third-party plugin
- [ ] Merge to main: `git checkout main && git merge feature/core-plugin-extraction`
- [ ] Tag release: `git tag v1.0.0-plugin-ready`

---

## Rollback Plan

### If Phase Fails

1. **Immediately stop migration**
   ```bash
   git stash  # Save any uncommitted work
   ```

2. **Identify failure point**
   - Review test failures
   - Check error logs
   - Identify broken functionality

3. **Rollback to last good state**
   ```bash
   # Rollback to previous commit
   git reset --hard HEAD~1

   # Or rollback entire phase
   git reset --hard {phase_start_commit}
   ```

4. **Restore functionality**
   ```bash
   # Run tests to verify restoration
   python tests/run_tests.py

   # Manual smoke test
   python main.py
   ```

5. **Analyze failure**
   - Document what went wrong
   - Update migration plan
   - Plan corrective actions

6. **Re-attempt with fixes**
   - Apply lessons learned
   - Test more thoroughly
   - Smaller incremental steps if needed

### If Complete Migration Fails

1. **Return to backup branch**
   ```bash
   git checkout backup-pre-extraction
   git checkout -b hotfix/migration-recovery
   ```

2. **Cherry-pick any non-breaking improvements**
   ```bash
   git cherry-pick {commit_hash}  # For valuable changes
   ```

3. **Revise strategy**
   - Break into smaller phases
   - Test each component more thoroughly
   - Get code review before proceeding

---

## Timeline & Milestones

### Week 1: Visual Effects & Commands

**Days 1-2: Phase 1**
- Extract visual effects
- Test rendering pipeline
- Milestone: All visual effects work via plugins

**Days 3-5: Phase 2**
- Extract command system
- Test all /commands
- Milestone: Command plugin architecture complete

### Week 2: LLM Services

**Days 1-3: Phase 3 Part 1**
- Extract file operations
- Extract MCP integration
- Extract model router
- Test tool system

**Days 4-5: Phase 3 Part 2**
- Extract profile manager
- Extract agent manager
- Extract conversation export
- Test LLM service still works
- Milestone: All LLM services pluginized

### Week 3: UI & I/O + Polish

**Days 1-2: Phase 4**
- Extract UI widgets
- Extract config UI
- Test all modals
- Milestone: UI plugin architecture complete

**Days 3: Phase 5**
- Slim I/O components
- Add delegation hooks
- Test rendering pipeline
- Milestone: Minimal core achieved

**Days 4-5: Testing & Documentation**
- Full regression testing
- Update documentation
- Create migration guide
- Create example plugins
- Milestone: Ready for marketplace

---

## Validation Criteria

### Phase Complete When:

1. **All tests passing**
   - Unit tests: 100% for new plugins
   - Integration tests: All scenarios covered
   - E2E tests: User workflows functional

2. **Feature parity maintained**
   - Every feature from before works after
   - No regressions in functionality
   - Performance not degraded

3. **Code quality standards met**
   - All plugins follow plugin architecture
   - Proper error handling
   - Logging implemented
   - Documentation complete

4. **User experience unchanged**
   - All commands work identically
   - Visual appearance unchanged
   - No new bugs introduced

### Migration Complete When:

1. **Core minimal**
   - ~19,000 lines (down from ~30,000)
   - Only essential infrastructure
   - No feature code in core

2. **Plugins functional**
   - 25+ plugins working
   - All official plugins bundled
   - Plugin discovery works

3. **Marketplace ready**
   - Plugin API documented
   - Example plugins created
   - Third-party development guide

4. **Tests comprehensive**
   - >80% code coverage
   - All critical paths tested
   - Integration tests passing

---

**End of Specification**

**Total Document Length:** 1,856 lines

**Approval Required From:**
- [ ] Lead Developer
- [ ] Architecture Review Board
- [ ] QA Team Lead

**Next Steps:**
1. Review and approve this specification
2. Assign engineers to phases
3. Set up feature branch
4. Begin Phase 1 migration
