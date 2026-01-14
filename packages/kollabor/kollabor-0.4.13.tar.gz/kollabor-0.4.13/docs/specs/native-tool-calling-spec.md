# Native Tool Calling Integration Spec

## Agent Investigation Results

### Agent 1: MCP Registry
```
tool_registry[tool_name] = {
    "server": str,
    "definition": Dict,  # Open-ended, no schema enforced
    "enabled": bool
}

list_available_tools() returns:
[{name, server, enabled, definition}, ...]
```

### Agent 2: LLM Call Flow
```
call_llm invocations:
  - llm_service.py:1275 (_process_message_batch)
  - llm_service.py:1421 (_continue_conversation)
  - Both route to _call_llm() at line 1712

Current call (NO tools):
  return await self.api_service.call_llm(
      conversation_history=self.conversation_history,
      max_history=self.max_history,
      streaming_callback=self._handle_streaming_chunk
      # MISSING: tools parameter!
  )
```

### Agent 3: Adapter Schemas
```
Generic format (works for both adapters):
{
    "name": "tool_name",
    "description": "...",
    "parameters": {...}  # JSON Schema - adapters auto-convert
}

OpenAI wraps in: {type: "function", function: {...}}
Anthropic uses: {name, description, input_schema}
```

### Agent 4: Response Handling
```
Native tool detection:
  api_service.has_pending_tool_calls()  # exists, never called
  api_service.get_last_tool_calls()     # exists, never called
  api_service.last_stop_reason          # "tool_use" when tools called

Integration point:
  After _call_llm() in _process_message_batch() ~line 1275
```

### Agent 5: Tool Execution
```
MCP execution:
  mcp_integration.call_mcp_tool(tool_name, arguments)

Result formatting for native calls:
  api_service.format_tool_result(tool_id, result, is_error)
  Returns: {role: "tool", tool_call_id: ..., content: ...}

Current (text-based):
  Results added as role="user" message (text batched)
```

---

## Implementation Plan

### Step 1: Add method to export MCP tools as API schemas

File: `core/llm/mcp_integration.py`

```python
def get_tool_definitions_for_api(self) -> List[Dict[str, Any]]:
    """Convert registered MCP tools to API tool schema format."""
    tools = []
    for tool_name, tool_info in self.tool_registry.items():
        if not tool_info["enabled"]:
            continue

        definition = tool_info.get("definition", {})
        tools.append({
            "name": tool_name,
            "description": definition.get("description", f"MCP tool: {tool_name}"),
            "parameters": definition.get("parameters", {
                "type": "object",
                "properties": {},
                "required": []
            })
        })
    return tools
```

### Step 2: Pass tools to _call_llm()

File: `core/llm/llm_service.py`

```python
# In __init__ or initialize(), get tool definitions:
self.native_tools = None  # Will be populated from MCP

# New method to load tools:
async def _load_native_tools(self):
    if self.mcp_integration:
        self.native_tools = self.mcp_integration.get_tool_definitions_for_api()

# Modify _call_llm() at line 1712:
async def _call_llm(self) -> str:
    return await self.api_service.call_llm(
        conversation_history=self.conversation_history,
        max_history=self.max_history,
        streaming_callback=self._handle_streaming_chunk,
        tools=self.native_tools  # ADD THIS
    )
```

### Step 3: Check for native tool calls after response

File: `core/llm/llm_service.py`

```python
# In _process_message_batch() after line 1275:
response = await self._call_llm()

# Check for native tool calls
if self.api_service.has_pending_tool_calls():
    native_results = await self._execute_native_tool_calls()
    # Add results to conversation and continue
    for result in native_results:
        msg = self.api_service.format_tool_result(
            result.tool_id,
            result.output if result.success else result.error,
            is_error=not result.success
        )
        self._add_conversation_message(msg)
    # Continue conversation (will call LLM again with results)
    self.turn_completed = False
```

### Step 4: Execute native tool calls

File: `core/llm/llm_service.py`

```python
async def _execute_native_tool_calls(self) -> List[ToolExecutionResult]:
    """Execute tool calls from native API response."""
    results = []
    for tc in self.api_service.get_last_tool_calls():
        # Convert to tool_executor format
        tool_data = {
            "type": "mcp_tool",
            "id": tc.tool_id,
            "name": tc.tool_name,
            "arguments": tc.arguments
        }
        result = await self.tool_executor.execute_tool(tool_data)
        results.append(result)
    return results
```

---

## Files to Modify

1. `core/llm/mcp_integration.py`
   - Add `get_tool_definitions_for_api()` method

2. `core/llm/llm_service.py`
   - Add `native_tools` attribute
   - Add `_load_native_tools()` method
   - Add `_execute_native_tool_calls()` method
   - Modify `_call_llm()` to pass tools
   - Modify `_process_message_batch()` to check for tool_calls
   - Modify `_continue_conversation()` similarly

3. Already done in `core/llm/api_communication_service.py`:
   - `call_llm()` accepts tools parameter
   - `last_tool_calls` stored
   - `has_pending_tool_calls()` method
   - `format_tool_result()` method

---

## Testing

1. Register an MCP tool with definition
2. Start conversation
3. Ask LLM to use the tool
4. Verify:
   - Tools sent in request payload
   - tool_calls in response
   - Tool executed
   - Result sent back
   - LLM continues with result

---

## Fallback

Keep XML-based tool parsing as fallback for:
- LLMs that don't support native tool calling
- Models on APIs that don't implement tools
- Backwards compatibility

Check both `api_service.has_pending_tool_calls()` AND `response_parser.get_all_tools()`.
