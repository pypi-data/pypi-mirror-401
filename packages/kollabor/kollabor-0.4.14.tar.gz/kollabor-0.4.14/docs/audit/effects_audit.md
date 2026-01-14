# Effects Directory Audit

## Executive Summary

The `core/effects/` directory is essentially empty (only `__init__.py` with a docstring).
However, visual effects are scattered across multiple locations in the codebase.

**Key Finding:** Visual effects are implemented in `core/io/visual_effects.py` (1,386 lines)
and `core/fullscreen/` directory, when most should be plugins.

---

## Findings

### 1. core/io/visual_effects.py (SHOULD BE SPLIT)

**Location:** `core/io/visual_effects.py`

**Status:** PARTIAL CORE / MOSTLY PLUGIN MATERIAL

**Analysis:**

This file contains 1,386 lines mixing essential color utilities with pure visual effects.

#### KEEP IN CORE (Terminal I/O primitives):

- `ColorSupport` enum (line 15) - Terminal capability detection
- `detect_color_support()` (line 24) - Environment detection logic
- `get_color_support()` (line 87) - Cached color support
- `set_color_support()` (line 116) - Manual override
- `reset_color_support()` (line 126) - Cache reset
- `rgb_to_256()` (line 132) - Color conversion utility
- `color_code()` (line 164) - Basic color code generation
- `ColorPalette` metaclass (line 320) - Dynamic color generation
- `ColorPalette.RESET`, `.DIM`, `.BRIGHT` - ANSI modifiers
- `make_fg_color()` (line 408), `make_bg_color()` (line 386) - Color helpers

#### MOVE TO PLUGINS (Specific effects):

- `ShimmerEffect` class (line 452) - Wave shimmer animation
- `PulseEffect` class (line 523) - Pulsing brightness effect
- `ScrambleEffect` class (line 596) - Text scramble shimmer
- `GradientRenderer` class (line 812) - Gradient effects
  - `apply_white_to_grey()`
  - `apply_dim_white_gradient()`
  - `apply_dim_scheme_gradient()`
  - `apply_custom_gradient()`
- `AgnosterSegment` class (line 690) - Powerline/agnoster segments
- `AgnosterColors` class (line 429) - Theme-specific colors
- `Powerline` class (line 358) - Separator characters
- `StatusColorizer` class (line 982) - Semantic status coloring
- `BannerRenderer` class (line 1176) - ASCII banner generation
- `VisualEffects` coordinator class (line 1249) - Main effects coordinator
- `EffectType` enum (line 193) - Effect type definitions
- `EffectConfig` dataclass (line 204) - Effect configuration

**Reason:** These are purely cosmetic effects that would be sold in a marketplace.
Users should be able to disable them without breaking core functionality.

**Complexity:** HIGH (large file, many classes)

**Dependencies:**
- Core color support detection (stays in core)
- Terminal renderer (uses color codes)
- Config system (for effect configuration)

**Migration Recommendation:**
1. Extract core color utilities to new `core/io/color_support.py`
2. Create `plugins/effects/` directory
3. Move each effect class to its own plugin file
4. Create `VisualEffectsPlugin` that registers effect hooks

---

### 2. core/fullscreen/ directory (MIXED - FRAMEWORK IS CORE, EFFECTS ARE PLUGINS)

#### 2a. FullScreen Framework - KEEP IN CORE

**Location:** `core/fullscreen/`

**Files:**
- `plugin.py` - Base class for full-screen plugins
- `manager.py` - Plugin lifecycle management
- `session.py` - Full-screen session management
- `renderer.py` - Terminal alternate buffer management
- `command_integration.py` - Slash command integration
- `__init__.py` - Package exports

**Reason:** This is infrastructure that enables ANY full-screen plugin to work.
It provides the alternate buffer management, input routing, and plugin lifecycle.

**Status:** CORE - Infrastructure layer

---

#### 2b. Matrix Components - MOVE TO PLUGINS

**Location:** `core/fullscreen/components/matrix_components.py`

**Classes:**
- `MatrixColumn` (line 8) - Single falling column
- `MatrixRenderer` (line 108) - Complete matrix rain renderer

**Reason:** Matrix rain is a purely cosmetic effect. It's exactly the type of
content that would be sold in a plugin marketplace.

**Current Status:** Already wrapped by `plugins/fullscreen/matrix_plugin.py`,
but the implementation is in core.

**Migration Path:**
1. Move `matrix_components.py` to `plugins/fullscreen/matrix_components.py`
2. Update import in `matrix_plugin.py`

**Complexity:** LOW (single file, clear dependencies)

**Dependencies:**
- `core.io.visual_effects.ColorPalette` - After migration, would need core color utilities

---

#### 2c. Example Plugin - SHOULD BE IN tests/ OR REMOVE

**Location:** `core/fullscreen/plugin.py` lines 168-204

**Class:** `ExamplePlugin`

**Reason:** Example code doesn't belong in production core. Should be in
`tests/` or `examples/` directory.

**Complexity:** LOW (single class, example only)

---

### 3. core/effects/__init__.py (REMOVE)

**Location:** `core/effects/__init__.py`

**Current:** Single docstring file, no actual code

**Reason:** Empty placeholder. Directory can be removed entirely.

---

## Summary Table

| File/Component | Current | Should Be | Complexity | Action |
|----------------|---------|-----------|------------|--------|
| ColorSupport detection | core/io | CORE | - | Keep |
| ColorPalette utilities | core/io | CORE | - | Keep |
| ShimmerEffect | core/io | PLUGIN | MED | Move |
| PulseEffect | core/io | PLUGIN | MED | Move |
| ScrambleEffect | core/io | PLUGIN | MED | Move |
| GradientRenderer | core/io | PLUGIN | MED | Move |
| AgnosterSegment | core/io | PLUGIN | LOW | Move |
| StatusColorizer | core/io | PLUGIN | LOW | Move |
| BannerRenderer | core/io | PLUGIN | LOW | Move |
| VisualEffects coordinator | core/io | PLUGIN | LOW | Move |
| FullScreen framework | core/fullscreen | CORE | - | Keep |
| MatrixColumn | core/fullscreen | PLUGIN | LOW | Move |
| MatrixRenderer | core/fullscreen | PLUGIN | LOW | Move |
| ExamplePlugin | core/fullscreen | REMOVE | LOW | Delete |
| effects/__init__.py | core/effects | DELETE | - | Remove |

---

## Migration Priority

### HIGH Priority:
1. Split `core/io/visual_effects.py` - Too large, violates SRP
2. Move matrix components to plugins - Already has plugin wrapper

### MEDIUM Priority:
3. Extract individual effect classes to plugin architecture

### LOW Priority:
4. Remove ExamplePlugin from production code
5. Remove empty `core/effects/` directory

---

## Recommended Architecture

```
core/io/
  color_support.py          # NEW: Core color utilities only
  # visual_effects.py REMOVED (split)

plugins/effects/            # NEW: Effects plugin directory
  __init__.py
  shimmer_plugin.py         # ShimmerEffect
  pulse_plugin.py           # PulseEffect
  scramble_plugin.py        # ScrambleEffect
  gradient_plugin.py        # GradientRenderer
  status_colorizer_plugin.py # StatusColorizer
  banner_plugin.py          # BannerRenderer
  powerline_plugin.py       # AgnosterSegment, Powerline

plugins/fullscreen/
  matrix_plugin.py          # Existing (already correct)
  matrix_components.py      # MOVE from core/fullscreen/components/
```

---

## Marketplace Impact

If Kollabor had a plugin marketplace, these would be premium items:

1. **Matrix Rain Effect** - $0.99
2. **Shimmer Thinking Animation** - $0.49
3. **Gradient Theme Pack** - $1.99
4. **Powerline Status Line** - $0.99
5. **Custom Banner Editor** - $1.49

All are currently bundled in core, preventing monetization.
