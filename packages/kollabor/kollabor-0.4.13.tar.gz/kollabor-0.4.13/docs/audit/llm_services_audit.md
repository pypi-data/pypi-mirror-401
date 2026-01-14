# LLM Services Audit Report

**Audit Date:** 2025-01-07
**Auditor:** Claude Code
**Scope:** core/llm/ directory

## Executive Summary

The core/llm/ directory contains 15+ files totaling approximately 7,000+ lines of code.
Based on the CORE vs PLUGIN criteria:

| Classification | Count | Files |
|----------------|-------|-------|
| CORE (essential) | 8 | llm_service.py, api_communication_service.py, conversation_manager.py, hook_system.py (infra), message_display_service.py (basic), response_parser.py, plugin_sdk.py (base), response_processor.py (basic) |
| PLUGIN (move to plugins/) | 5 | mcp_integration.py, model_router.py, profile_manager.py, file_operations_executor.py, agent_manager.py |
| HYBRID (partial split) | 2 | conversation_logger.py (enhanced features), hook_system.py (specific implementations) |

---

## Findings: Should Be PLUGIN

### Finding 1
```
location: core/llm/mcp_integration.py
function/class: MCPIntegration class
current: CORE
should_be: PLUGIN
reason: Per spec, "MCP integrations" should be plugins. MCP is an optional protocol
     that not all users need. The integration should be a plugin that registers
     hooks when MCP servers are configured.
complexity: medium
dependencies: Requires extracting MCP discovery/registration to plugin SDK;
     llm_service needs plugin hooks for tool registration
```

### Finding 2
```
location: core/llm/model_router.py
function/class: ModelRouter class (entire file)
current: CORE
should_be: PLUGIN
reason: Per spec, "Model routing strategies" should be plugins. Different users
     may want different routing logic (cost-based, capability-based, custom).
     Core should only provide a default "direct pass-through" interface.
complexity: low
dependencies: llm_service needs a simple model selection interface;
     plugin hooks for pre-model-selection
```

### Finding 3
```
location: core/llm/profile_manager.py
function/class: ProfileManager class (entire file - 1054 lines)
current: CORE
should_be: PLUGIN
reason: Profile management is configuration-layer functionality. Core should provide
     basic config loading (already exists in core/config/). Profile switching,
     creation wizards, and environment variable resolution are feature enhancements
     suitable for a plugin.
complexity: high
dependencies: Needs plugin hooks for config changes;
     core config system already supports external config merging
```

### Finding 4
```
location: core/llm/file_operations_executor.py
function/class: FileOperationsExecutor class (entire file - 1423 lines)
current: CORE
should_be: PLUGIN
reason: Per spec, "Tool implementations" should be plugins. This is a specific tool
     implementation (11 operation types with safety features). Core should provide
     the tool execution framework, not specific tools. Users may want different
     file operation tools or none at all.
complexity: high
dependencies: tool_executor needs plugin hooks for tool discovery;
     file_operations_executor becomes a plugin that registers its tools
```

### Finding 5
```
location: core/llm/agent_manager.py
function/class: AgentManager, SkillManager classes (entire file - 876 lines)
current: CORE
should_be: PLUGIN
reason: Agent/skill system is an extensibility feature, not core LLM functionality.
     The multi-agent coordination system is an advanced feature that should be
     optional. Core LLM service should handle single-agent interaction; multi-agent
     orchestration is a plugin concern.
complexity: high
dependencies: Needs plugin lifecycle hooks for agent background tasks;
     llm_service needs hooks for delegating to sub-agents
```

---

## Findings: Should Remain CORE

### Core File 1
```
location: core/llm/llm_service.py
function/class: LLMService class
current: CORE
should_be: CORE (unchanged)
reason: Central orchestration for all LLM operations. This is the primary service
     that coordinates API calls, streaming, tool execution, and response handling.
     The application cannot function without it.
```

### Core File 2
```
location: core/llm/api_communication_service.py
function/class: APICommunicationService class
current: CORE
should_be: CORE (unchanged)
reason: Per spec, "Basic LLM API communication" is core. This provides HTTP
     client functionality with rate limiting and retry logic - essential
     infrastructure for any LLM interaction.
```

### Core File 3
```
location: core/llm/conversation_manager.py
function/class: ConversationManager class
current: CORE
should_be: CORE (unchanged)
reason: Per spec, "Conversation history management (basic)" is core. This manages
     the in-memory conversation state and history - essential for maintaining
     context across requests.
```

### Core File 4
```
location: core/llm/response_parser.py
function/class: ResponseParser class
current: CORE
should_be: CORE (unchanged)
reason: Basic response parsing (extracting content from LLM responses, handling
     thinking tags, detecting question gates) is essential infrastructure that
     the core LLM service requires.
```

### Core File 5
```
location: core/llm/response_processor.py
function/class: ResponseProcessor class
current: CORE
should_be: CORE (unchanged)
reason: Response processing (streaming, chunk assembly, finalization) is part of
     the basic LLM communication infrastructure. The app cannot function without
     response processing.
```

### Core File 6
```
location: core/llm/message_display_service.py
function/class: MessageDisplayService class
current: CORE
should_be: CORE (unchanged)
reason: Message formatting and display coordination is essential infrastructure.
     However, the specific formatting rules could be moved to plugin hooks.
```

### Core File 7
```
location: core/llm/plugin_sdk.py
function/class: KollaborPluginSDK class
current: CORE
should_be: CORE (unchanged)
reason: The plugin SDK is infrastructure for the plugin system. Per spec,
     "Plugin loading/discovery mechanism" and "Base classes and interfaces" are core.
     This provides the API that plugins use to interact with the application.
```

---

## Findings: Hybrid (Partial Split Recommended)

### Hybrid 1
```
location: core/llm/hook_system.py
function/class: LLMHookSystem, HookRegistry, Event enum
current: CORE
should_be: HYBRID - split infrastructure from implementations
reason:
     - KEEP in CORE: HookRegistry, Event enum, registration mechanism (infrastructure)
     - MOVE to PLUGIN: Specific hook implementations that do actual work
     The hook system infrastructure enables plugins; specific hooks that implement
     features should be in plugins.
complexity: medium
dependencies: Need to separate infrastructure (registry, executor) from
     feature implementations (specific handlers)
```

### Hybrid 2
```
location: core/llm/conversation_logger.py
function/class: KollaborConversationLogger class
current: CORE
should_be: HYBRID - split basic logging from enhanced features
reason:
     - KEEP in CORE: Basic conversation persistence to database
     - MOVE to PLUGIN: Export functionality, advanced formatting, transcript features
     Core needs persistence for history. Enhanced export features (JSON, markdown,
     text with formatting) are plugin-worthy features.
complexity: low
dependencies: Extract export methods to plugin hooks; keep basic CRUD in core
```

---

## Migration Recommendations

### Priority 1 (High Impact, Low Complexity)
1. **mcp_integration.py → plugins/mcp_plugin.py**
   - Create MCP plugin that discovers servers and registers tool hooks
   - Add tool registration hooks to tool_executor

2. **model_router.py → plugins/model_router_plugin.py**
   - Create plugin that registers a pre-model-selection hook
   - Add simple default model selection to core llm_service

### Priority 2 (High Impact, Medium Complexity)
3. **file_operations_executor.py → plugins/file_operations_plugin.py**
   - Convert to plugin that registers 11 file operation tools
   - Add tool discovery hooks to tool_executor

4. **conversation_logger.py → partial split**
   - Keep basic persistence in core
   - Move export features to a "conversation_export_plugin.py"

### Priority 3 (High Impact, High Complexity)
5. **agent_manager.py → plugins/agent_plugin.py**
   - Requires designing plugin lifecycle hooks for background tasks
   - Needs architectural work for sub-agent delegation

6. **profile_manager.py → plugins/profile_plugin.py**
   - Convert to plugin that provides profile commands and UI
   - Core config system already supports external merging

---

## Complexity Estimates

| File to Move | Lines | Complexity | Reason |
|--------------|-------|------------|--------|
| mcp_integration.py | ~300 | medium | Straightforward plugin conversion |
| model_router.py | ~200 | low | Simple routing logic |
| file_operations_executor.py | ~1423 | high | Large file, many tools to register |
| agent_manager.py | ~876 | high | Background tasks, lifecycle management |
| profile_manager.py | ~1054 | high | Config system integration, UI |

**Total lines to move to plugins: ~3,853**

---

## Required Hook Points

To support these migrations, core needs these new hook points:

1. **tool_discovery** - Plugins can register available tools
2. **model_selection** - Plugins can override model choice
3. **mcp_server_discovery** - Plugins can register MCP servers
4. **conversation_export** - Plugins can provide export formats
5. **agent_task_start** - Plugins can intercept before sub-agent creation
6. **config_change** - Plugins can react to profile/config changes

---

## Conclusion

The core/llm/ directory has significant opportunity for consolidation:
- **~55%** of code (by line count) should move to plugins
- **5 files** identified for full migration to plugins
- **2 files** identified for partial split

Primary areas for extraction:
1. Tool implementations (file_operations_executor)
2. Integration protocols (mcp_integration)
3. Feature enhancements (profile_manager, agent_manager)
4. Routing logic (model_router)

This separation would:
- Reduce core maintenance burden
- Enable marketplace for alternative implementations
- Allow users to install only what they need
- Improve testability through smaller, focused modules
