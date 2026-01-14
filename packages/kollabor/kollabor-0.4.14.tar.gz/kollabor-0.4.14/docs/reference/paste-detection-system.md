---
title: Paste Detection System
description: Dual paste detection system architecture and implementation
category: reference
status: implemented
---

# Paste Detection System

## Overview

The Kollabor CLI implements a sophisticated dual paste detection system that handles both large pasted content and rapid typing detection. The system ensures pasted content is properly stored, displayed with placeholders, and expanded on submission.

**Status**: Fully implemented and active

## Architecture

### Dual System Design

The paste detection system consists of two complementary subsystems:

1. **PRIMARY System (Chunk-Based)**: Always active, handles large content
2. **SECONDARY System (Timing-Based)**: Disabled by default, detects rapid typing

```
┌────────────────────────────────────────────────────────────┐
│                  Paste Detection System                    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌─────────────────────┐    ┌──────────────────────┐     │
│  │  PRIMARY (Active)   │    │ SECONDARY (Disabled) │     │
│  │  Chunk-Based        │    │ Timing-Based         │     │
│  ├─────────────────────┤    ├──────────────────────┤     │
│  │ • >10 char chunks   │    │ • Rapid typing       │     │
│  │ • Always enabled    │    │ • <50ms between keys │     │
│  │ • In InputLoopMgr   │    │ • Configurable       │     │
│  └─────────────────────┘    └──────────────────────┘     │
│           │                            │                   │
│           └────────────┬───────────────┘                   │
│                        │                                   │
│                  ┌─────▼──────┐                           │
│                  │PasteProc   │                           │
│                  │ - Storage  │                           │
│                  │ - Expand   │                           │
│                  └────────────┘                           │
└────────────────────────────────────────────────────────────┘
```

## Components

### PasteProcessor

**Location**: `core/io/input/paste_processor.py`

The main paste processing component that handles storage, placeholder creation, and expansion.

**Key Responsibilities**:
- Store pasted content in paste bucket
- Create placeholders: `[Pasted #N X lines, Y chars]`
- Expand placeholders with actual content on submit
- Manage paste IDs and counters

**State Management**:

```python
# PRIMARY system (always active)
_paste_bucket: Dict[str, str]       # {paste_id: actual_content}
_paste_counter: int                 # Counter for paste numbering
_current_paste_id: Optional[str]    # Currently building paste ID
_last_paste_time: float             # Last chunk timestamp

# SECONDARY system (disabled)
paste_detection_enabled: bool = False  # Only enables SECONDARY
_paste_buffer: list                 # Temporary paste buffer
_last_char_time: float              # Last character time
_paste_cooldown: float              # Cooldown period
```

**Important**: The `paste_detection_enabled` flag ONLY controls the SECONDARY timing-based system. The PRIMARY chunk-based system is always active.

### InputLoopManager Integration

**Location**: `core/io/input/input_loop_manager.py`

The PRIMARY chunk-based detection happens in the input loop:

```python
# Detect large paste chunks (>10 characters)
if len(chunk) > 10:
    # Trigger paste handling
    await paste_processor.handle_chunk_paste(chunk)
```

**Detection Criteria**:
- Chunk size >10 characters
- Immediate storage in paste bucket
- Placeholder insertion in buffer

## Paste Flow

### 1. Paste Detection (PRIMARY)

```
User pastes content (e.g., 200 chars)
    │
    ├─> InputLoopManager receives chunk (>10 chars)
    │
    ├─> PasteProcessor.handle_chunk_paste()
    │   ├─ Generate paste_id: "paste_001"
    │   ├─ Store in bucket: {"paste_001": "actual content..."}
    │   └─ Create placeholder: "[Pasted #1 5 lines, 200 chars]"
    │
    └─> Buffer shows placeholder to user
```

### 2. Placeholder Display

The user sees:
```
> This is my message [Pasted #1 5 lines, 200 chars] and more text
```

Instead of the full pasted content, which would clutter the display.

### 3. Content Expansion (On Submit)

```
User presses Enter
    │
    ├─> BufferManager.get_content_and_clear()
    │   └─> PasteProcessor.expand_paste_placeholders(message)
    │       ├─ Find all [Pasted #N ...] patterns
    │       ├─ Replace with actual content from bucket
    │       └─ Return expanded message
    │
    └─> Full content sent to LLM
```

**Expansion Pattern**:
```python
pattern = r'\[Pasted #\d+ \d+ lines?, \d+ chars?\]'
# Matches: [Pasted #1 5 lines, 200 chars]
#          [Pasted #2 1 line, 45 chars]
```

## API Reference

### PasteProcessor Methods

#### `handle_chunk_paste(chunk: str) -> str`

Handle a large paste chunk (PRIMARY system).

**Parameters**:
- `chunk`: Pasted content (>10 chars)

**Returns**: Placeholder string to display

**Example**:
```python
placeholder = await paste_processor.handle_chunk_paste(
    "This is a large pasted content..."
)
# Returns: "[Pasted #1 3 lines, 150 chars]"
```

#### `expand_paste_placeholders(message: str) -> str`

Expand all paste placeholders in a message.

**Parameters**:
- `message`: Message containing placeholders

**Returns**: Message with placeholders replaced by actual content

**Example**:
```python
message = "Check this [Pasted #1 3 lines, 150 chars] out"
expanded = paste_processor.expand_paste_placeholders(message)
# Returns: "Check this <actual content> out"
```

#### `start_paste(paste_id: str, timestamp: float)`

Start tracking a new paste operation.

**Parameters**:
- `paste_id`: Unique identifier for paste
- `timestamp`: When paste started

#### `add_paste_chunk(content: str, paste_id: str)`

Add content to an in-progress paste.

**Parameters**:
- `content`: Content chunk to add
- `paste_id`: Paste identifier

#### `finalize_paste(paste_id: str) -> Dict[str, Any]`

Finalize a paste and create placeholder.

**Parameters**:
- `paste_id`: Paste identifier

**Returns**: Dict with placeholder and paste stats

### Properties

#### `paste_bucket: Dict[str, str]`

Read-only access to stored paste content.

#### `current_paste_id: Optional[str]`

Currently building paste ID (if any).

#### `last_paste_time: float`

Timestamp of last paste chunk.

## Configuration

### Current Settings

**PRIMARY System** (always active):
- Chunk threshold: 10 characters
- No configuration required
- Always enabled for user experience

**SECONDARY System** (disabled):
```python
paste_detection_enabled: bool = False  # Feature flag
paste_threshold_ms: float = 50.0       # Rapid typing threshold
paste_min_chars: int = 5               # Minimum chars to consider
paste_timeout_ms: float = 100.0        # Buffer timeout
```

### Enabling SECONDARY System

The SECONDARY timing-based system is currently disabled because:
1. PRIMARY system handles the common case (large pastes)
2. Timing-based detection can have false positives
3. Not all terminals provide accurate timing information

To enable (if needed):
```python
paste_processor.paste_detection_enabled = True
```

**Note**: This only affects the SECONDARY system. PRIMARY remains active regardless.

## Integration Points

### 1. InputHandler Initialization

```python
self._paste_processor = PasteProcessor(
    buffer_manager=buffer_manager,
    display_callback=display_controller.update_display
)

self._input_loop_manager = InputLoopManager(
    renderer=renderer,
    key_parser=key_parser,
    error_handler=error_handler,
    paste_processor=paste_processor,  # Inject processor
    config=config
)
```

### 2. Buffer Submission

```python
# In InputHandler or InputLoopManager
content = self.buffer_manager.get_content_and_clear()
expanded_content = self._paste_processor.expand_paste_placeholders(content)
# Send expanded_content to LLM
```

### 3. Display Updates

```python
# After paste detection
if self._display_callback:
    await self._display_callback()  # Trigger re-render
```

## Testing

### Test Cases

**Location**: `tests/unit/test_paste_processor.py`

1. **test_paste_detection_disabled**: Verify SECONDARY system is off by default
2. **test_chunk_paste_handling**: Verify PRIMARY system detects large chunks
3. **test_placeholder_creation**: Verify placeholder format
4. **test_placeholder_expansion**: Verify content expansion
5. **test_multiple_pastes**: Verify multiple paste handling
6. **test_paste_bucket_storage**: Verify storage and retrieval

### Manual Testing

```bash
# Test PRIMARY system (always works)
1. Run: kollab
2. Paste >10 chars of content
3. Should see: [Pasted #1 X lines, Y chars]
4. Press Enter
5. Full content sent to LLM

# Test multiple pastes
1. Paste content A
2. Type some text
3. Paste content B
4. Should see: text [Pasted #1 ...] more text [Pasted #2 ...]
5. Press Enter
6. Both pastes expanded
```

## Troubleshooting

### Issue: Paste Not Detected

**Symptom**: Large paste shows as individual characters

**Causes**:
1. Terminal not sending chunks (rare)
2. Content <10 chars (below threshold)

**Solution**: This is expected behavior for small content

### Issue: Placeholder Not Expanding

**Symptom**: Placeholder sent to LLM instead of content

**Causes**:
1. Paste bucket not populated
2. Paste ID mismatch
3. Expansion not called

**Solution**: Check logs for paste_processor operations

### Issue: SECONDARY System Not Working

**Symptom**: Rapid typing not detected as paste

**Expected**: SECONDARY system is disabled by default

**Solution**: This is intentional. Use PRIMARY system for actual pastes.

## Design Rationale

### Why Two Systems?

1. **PRIMARY (Chunk-Based)**:
   - Handles the common case (actual pastes)
   - Reliable across all terminals
   - No false positives
   - Always appropriate to use

2. **SECONDARY (Timing-Based)**:
   - Theoretical edge case coverage
   - Terminal-dependent timing accuracy
   - Potential false positives (fast typers)
   - Currently not needed

### Why Placeholders?

1. **Performance**: Don't re-render huge content blocks
2. **Usability**: User sees summary, not 1000-line paste
3. **Editing**: Easier to see structure with placeholders
4. **Expansion**: Actual content still sent to LLM

### Why Disabled by Default?

The `paste_detection_enabled = False` setting:
- Only affects SECONDARY timing-based detection
- PRIMARY chunk-based detection is always on
- Avoids false positives from fast typing
- Simplifies system (one reliable method)

## Future Enhancements

### Potential Improvements

1. **Visual Feedback**: Color-code paste placeholders
2. **Paste Preview**: Hover or shortcut to preview content
3. **Paste Editing**: Edit pasted content before submit
4. **Paste History**: Save and recall previous pastes
5. **Smart Expansion**: Selectively expand certain pastes

### If SECONDARY System Needed

To enable timing-based detection:
```python
# In config or initialization
paste_processor.paste_detection_enabled = True
paste_processor.paste_threshold_ms = 50.0  # Adjust for terminal
paste_processor.paste_min_chars = 5
```

**When to use**:
- Terminal doesn't send large chunks
- Need to detect rapid typing as paste
- Accurate timing available

## Related Documentation

- [Buffer Transition and Render State](buffer-transition-and-render-state.md) - Input buffer management
- [Architecture Overview](architecture-overview.md) - System architecture
- [Input System](../reference/input-system.md) - Complete input handling

## References

- `core/io/input/paste_processor.py` - Main implementation
- `core/io/input/input_loop_manager.py` - PRIMARY detection
- `core/io/input/key_press_handler.py` - SECONDARY integration point
- `tests/unit/test_paste_processor.py` - Test suite
