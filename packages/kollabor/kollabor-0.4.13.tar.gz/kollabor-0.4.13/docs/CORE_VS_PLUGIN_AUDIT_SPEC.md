# Core vs Plugin Audit Specification

## Purpose
Audit the Kollabor CLI codebase to identify functionality that should be:
- **CORE**: Essential, non-optional functionality the app cannot run without
- **PLUGIN**: Optional, extensible features suitable for a marketplace

## Core Criteria (MUST stay in core/)
- Application lifecycle (startup, shutdown, cleanup)
- Event bus infrastructure (not the events themselves, but the bus)
- Plugin loading/discovery mechanism
- Base classes and interfaces
- Terminal I/O primitives (raw mode, basic rendering)
- Configuration loading/saving infrastructure
- State persistence infrastructure
- Basic LLM API communication
- Conversation history management (basic)

## Plugin Criteria (SHOULD be a plugin)
- Specific visual effects (matrix rain, gradients, animations)
- Specific commands (/save, /matrix, /terminal, etc.)
- Enhanced input features (multi-line, syntax highlighting)
- Status line customizations
- Specific hooks implementations
- Model routing strategies
- Export formats
- UI widgets beyond basics
- MCP integrations
- Tool implementations

## Audit Instructions

### DO NOT:
- Modify any code
- Create any files (except your report)
- Delete anything
- Refactor anything

### DO:
- Read and analyze code structure
- Identify violations of core/plugin separation
- List specific files/functions that should move
- Provide migration recommendations
- Estimate complexity (low/medium/high)

## Report Format

For each finding:
```
location: core/path/to/file.py
function/class: SpecificClass or specific_function
current: CORE
should_be: PLUGIN
reason: Brief explanation
complexity: low|medium|high
dependencies: List any dependencies that would need to be resolved
```

## Areas to Audit

1. **LLM Services** (core/llm/) - What's essential vs pluggable?
2. **I/O System** (core/io/) - What's base infra vs feature?
3. **Commands** (core/commands/) - Registry is core, but are specific commands?
4. **UI** (core/ui/) - Base modal system vs specific widgets?
5. **Effects** (core/effects/) - Should any be core?
6. **Utils** (core/utils/) - Are there utils that should be plugins?
7. **Existing Plugins** (plugins/) - Verify they're correctly placed
