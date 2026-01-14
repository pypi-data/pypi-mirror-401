# Question Gate Protocol

## Overview

The Question Gate Protocol is a system-level feature that suspends tool execution when the agent asks a clarifying question. This prevents runaway investigation loops and ensures user feedback is collected before deep dives.

## How It Works

1. Agent includes `<question>` tag in response when asking for clarification
2. System detects the tag and suspends any pending tool calls
3. User receives the question and can respond
4. When user responds, suspended tools are executed and results injected
5. Agent continues with full context (user response + tool results)

## Syntax

```xml
<question>
your question or options here
</question>
```

## Behavior

### When `<question>` tag is present:
- All tool calls in the response are SUSPENDED (not executed)
- Turn is marked as completed (returns control to user)
- Pending tools are stored in `LLMService.pending_tools`
- `question_gate_active` flag is set to True

### When user responds:
- `process_user_input()` checks for pending tools
- Suspended tools are executed
- Results are displayed and added to conversation history
- Question gate state is cleared
- Normal processing continues

## Configuration

Enable/disable in `config.json`:

```json
{
  "core": {
    "llm": {
      "question_gate_enabled": true
    }
  }
}
```

Default: `true` (enabled)

## Implementation Details

### Files Modified

1. **`core/llm/response_parser.py`**
   - Added `question_pattern` regex to detect `<question>` tags
   - Added `_extract_question()` method
   - Updated `parse_response()` to set `question_gate_active` flag
   - Added `has_question` to response metadata

2. **`core/llm/llm_service.py`**
   - Added `pending_tools` list to store suspended tools
   - Added `question_gate_active` flag
   - Added `question_gate_enabled` config option
   - Modified `_process_message_batch()` to check for question gate
   - Modified `_continue_conversation()` with same logic
   - Modified `process_user_input()` to inject queued tools

3. **`.kollabor-cli/agents/default/system_prompt.md`**
   - Added question gate protocol documentation
   - Includes usage examples and guidelines

4. **`.kollabor-cli/config.json`**
   - Added `question_gate_enabled: true` option

### Response Parser Changes

```python
# New pattern added
self.question_pattern = re.compile(
    r'<question>(.*?)</question>',
    re.DOTALL | re.IGNORECASE
)

# New extraction method
def _extract_question(self, content: str) -> Optional[str]:
    match = self.question_pattern.search(content)
    if match:
        return match.group(1).strip()
    return None
```

### LLM Service Changes

```python
# Question gate state
self.pending_tools: List[Dict[str, Any]] = []
self.question_gate_active = False
self.question_gate_enabled = config.get("core.llm.question_gate_enabled", True)

# In _process_message_batch() and _continue_conversation()
if self.question_gate_enabled and parsed_response.get("question_gate_active"):
    self.pending_tools = all_tools
    self.question_gate_active = True
    # Tools NOT executed - stored for later

# In process_user_input()
if self.question_gate_enabled and self.question_gate_active and self.pending_tools:
    tool_injection_results = await self.tool_executor.execute_all_tools(self.pending_tools)
    # Results displayed and added to conversation
    self.pending_tools = []
    self.question_gate_active = False
```

## Usage Examples

### Correct Usage

```
<terminal>grep -r "config" core/</terminal>

found 3 configuration patterns. need clarification:

<question>
which configuration aspect should i focus on?
  [1] api configuration (endpoints, keys)
  [2] runtime settings (timeouts, limits)
  [3] user preferences (themes, defaults)
</question>
```

The terminal command is suspended. User sees the question and can respond.

### Incorrect Usage (Avoided by Protocol)

```
<terminal>grep -r "config" core/</terminal>

found 3 patterns. which one?
  [1] api config
  [2] runtime config
  [3] user prefs

<terminal>cat core/config/api.py</terminal>
```

Without `<question>` tags, both terminal commands execute immediately. The question gate prevents this by requiring explicit `<question>` tags.

## Benefits

1. **Prevents runaway loops** - Agent can't keep investigating without user input
2. **Respects user attention** - Questions get answered before more work
3. **Preserves tool context** - Suspended tools execute with user's response
4. **Configurable** - Can be disabled if not needed

## System Prompt Integration

The agent system prompt includes the question gate protocol documentation at lines 233-296, teaching the agent:
- When to use `<question>` tags
- The syntax and behavior
- Correct vs incorrect usage examples
- Why the protocol exists
