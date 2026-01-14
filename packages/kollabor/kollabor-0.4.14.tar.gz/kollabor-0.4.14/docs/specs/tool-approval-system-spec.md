
---
title: Tool Approval System Specification
description: Permission gates for terminal, file write, and delete operations
category: spec
created: 2026-01-10
status: draft
---

# Tool Approval System Specification

**Version**: 1.0
**Status**: Draft - Ready for Review
**Created**: 2026-01-10
**Updated**: 2026-01-10

---

## 1. Overview

Add permission gates for destructive operations (terminal commands, file writes, file deletes) similar to Claude Code CLI and Codex CLI workflows.

### Current Problem

LLM can execute destructive operations without user approval:
- Terminal commands can delete files, modify systems, install packages
- File operations can overwrite critical code
- No safety net for accidental changes
- Difficult to undo destructive operations

### Proposed Solution

Permission gate before destructive operations execute:
- Terminal commands: require approval (whitelist safe commands)
- File writes: require approval (whitelist safe paths)
- File deletes: require double-confirmation
- Auto-approve via `--yolo` flag or config settings

### Key Features

1. **--yolo Command-Line Flag**: Bypass all approval checks
2. **Config-Based Approval Rules**: Whitelist patterns, protected paths
3. **Interactive Prompts**: y/N/a/q responses (yes/no/all/quit)
4. **Batch Approval**: Apply decision to multiple operations
5. **Operation Categorization**:
   - Terminal: require approval (whitelist safe commands)
   - File write: require approval (whitelist safe paths)
   - File delete: require double-confirmation
   - File read: always allowed

---

## 2. Architecture

### 2.1 High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      ToolExecutor                              │
│  - execute_tool() - entry point for all tool operations       │
│  - execute_all_tools() - batch operations                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    [Permission Gate?]
                              │
              ┌───────────────┴───────────────┐
              │                               │
         [Yes]                            [No]
              │                               │
              ▼                               ▼
┌─────────────────────────────────┐   ┌────────────────────────────┐
│   PermissionManager            │   │   Execute Immediately     │
│  - check_permission()          │   │   (--yolo mode)          │
│  - request_approval()          │   └────────────────────────────┘
│  - update_stats()              │
└─────────────────────────────────┘
              │
              ▼
      [User Input Required]
              │
              ▼
┌─────────────────────────────────┐
│   InputHandler                 │
│  - handle_permission_prompt()  │
│  - y/N/a/q responses          │
└─────────────────────────────────┘
              │
              ▼
      [Approved/Denied]
              │
              ▼
┌─────────────────────────────────┐
│   Execute or Skip              │
│  - If approved: execute tool   │
│  - If denied: log and skip     │
│  - Batch: apply to all tools  │
└─────────────────────────────────┘
```

### 2.2 Detailed Sequence Diagram

```
User          ToolExecutor      PermissionManager    EventBus      InputHandler      ModalController   Future
 │                  │                    │              │               │                  │       │
 │─ tools ───────────>│                    │              │               │                  │       │
 │                  │                    │              │               │                  │       │
 │                  │── check_perm ──────>│              │               │                  │       │
 │                  │<── Permission ────────│              │               │                  │       │
 │                  │                    │              │               │                  │       │
 │                  │─ create Future ───>│              │               │                  │       │
 │                  │<─ future_id ──────────│              │               │                  │       │
 │                  │                    │              │               │                  │       │
 │                  │── emit(PERM_REQ) ──>│              │               │                  │       │
 │                  │                    │── emit ──────>│               │                  │       │
 │                  │                    │              │── handle ─────>│                  │       │
 │                  │                    │              │               │── show_modal ──>│       │
 │                  │                    │              │               │                  │       │
 │                  │                    │              │               │<─ ready ──────────│       │
 │                  │                    │              │               │                  │       │
 │                  │                    │              │               │                  │       │
 │                  │── await Future ────────────────────────────────────────────>│───┐       │
 │                  │                    │              │               │                  │       │       │
 │                  │                    │              │               │                  │       │       │
 │── types "y" ──────────────────────────────────────────────────────────────────────>│       │
 │                  │                    │              │               │                  │       │       │
 │                  │                    │              │               │── handle_key ────>│       │
 │                  │                    │              │               │                  │       │
 │                  │                    │              │               │<─ decision ────│       │
 │                  │                    │              │               │                  │       │
 │                  │                    │              │── route_resp ──>│                  │       │
 │                  │                    │              │               │                  │       │
 │                  │                    │              │               │                  │── set_result ───>│
 │                  │                    │              │               │                  │       │       │
 │                  │<── unblocks ────────────────────────────────────────────│<──────┘       │
 │                  │                    │              │               │                  │       │
 │                  │── execute_tool ────────────────────────────────────────────────────────>│
 │                  │                    │              │               │                  │       │
 │                  │<── result ──────────────────────────────────────────────────────────│
 │                  │                    │              │               │                  │       │
 │<─ done ──────────│                    │              │               │                  │       │
```

**Sequence Flow:**

1. **Tool Execution Starts**: User triggers tool execution (via LLM response or direct command)
2. **Permission Check**: ToolExecutor asks PermissionManager if approval needed
3. **Permission Decision**: PermissionManager checks rules, returns PermissionResult
4. **Future Creation**: If approval needed, ToolExecutor creates asyncio.Future
5. **Future Storage**: Future stored in PermissionManager._pending_approval
6. **Event Emission**: PERMISSION_REQUEST event emitted via EventBus
7. **Event Handling**: InputHandler receives event via hook system
8. **UI Display**: InputHandler determines UI type, shows modal or status takeover
9. **User Input**: User types y/N/a/q
10. **Key Routing**: KeyPressHandler routes input to approval handler
11. **Decision Routing**: InputHandler retrieves Future, calls set_result(decision)
12. **Future Resolution**: asyncio.Future unblocks ToolExecutor
13. **Tool Execution**: ToolExecutor executes or skips tool based on decision
14. **Result Return**: Tool result returned to caller

### 2.3 Component Reference Chain

```
Application
  ├── ToolExecutor
  │   ├── PermissionManager
  │   │   ├── _pending_approval: asyncio.Future
  │   │   ├── stats: Dict[str, Any]
  │   │   └── config: Dict[str, Any]
  │   ├── FileOperationsExecutor
  │   └── MCPIntegration
  │
  ├── InputHandler
  │   ├── _permission_manager: PermissionManager (reference)
  │   ├── _approval_mode_active: bool
  │   ├── _approval_future_id: int
  │   ├── _double_confirm_active: bool
  │   ├── KeyPressHandler
  │   ├── ModalController
  │   └── CommandModeHandler
  │
  └── EventBus
      ├── HookRegistry
      ├── HookExecutor
      └── EventProcessor
```

---

## 2.5. Async Communication Architecture

### 2.5.1 Approval Flow Overview

The permission system uses an event-driven async communication pattern:

```
ToolExecutor                 InputHandler              PermissionManager
     |                              |                             |
     |-- check_permission() -------->|                             |
     |<-- PermissionResult ---------|                             |
     |                              |                             |
     |-- create Future ------------>|                             |
     |                              |                             |
     |-- emit PERMISSION_REQUEST -->|                             |
     |                              |                             |
     |                              |-- show modal -------------->|
     |                              |                             |
     |                              |-- user types "y"          |
     |                              |                             |
     |<-- emit PERMISSION_GRANTED -----|                             |
     |                              |                             |
     |<-- Future.set_result() ------|                             |
     |                              |                             |
     |-- await Future ------------->|                             |
     |<-- ApprovalDecision ----------|                             |
     |                              |                             |
     |-- execute tool ------------->|                             |
```

### 2.5.2 Future-Based Approval Mechanism

ToolExecutor uses `asyncio.Future` to block until user responds:

**Key Components:**
- `PermissionManager._pending_approval`: Stores the active Future
- `ToolExecutor._request_user_approval()`: Creates and waits for Future
- `InputHandler._handle_permission_response()`: Sets Future result

**Flow:**
1. Tool executor creates `asyncio.Future()`
2. Future is stored in PermissionManager for access
3. PERMISSION_REQUEST event emitted with metadata
4. Input handler catches event, shows modal
5. User responds (y/N/a/q/v)
6. Input handler emits PERMISSION_GRANTED/PASSWORD_DENIED event
7. Input handler retrieves Future from PermissionManager
8. Input handler calls `future.set_result(decision)`
9. Tool executor unblocks from `await future`
10. Tool executor executes or skips tool

**Timeout Handling:**
```python
try:
    decision = await asyncio.wait_for(
        approval_future,
        timeout=self.permission_manager.approval_timeout
    )
    return decision
except asyncio.TimeoutError:
    return ApprovalDecision.TIMEOUT
```

**Error Handling:**
- If modal crashes before user responds
- If input handler receives unexpected keys
- If event bus fails to emit events

All errors result in `ApprovalDecision.DENY` (safe default).

### 2.5.3 Event Data Structure

**PERMISSION_REQUEST Event:**
```python
{
    "tool_data": {
        "type": "terminal",
        "id": "terminal_0",
        "command": "rm -rf node_modules"
    },
    "permission_result": {
        "decision": "approve",
        "approved": False,
        "message": "Requires approval",
        "auto_approved": False
    },
    "index": 1,
    "total": 3,
    "timeout": 30,
    "approval_future_id": 140234567890  # For debugging
}
```

**PERMISSION_GRANTED Event:**
```python
{
    "decision": "APPROVE",  # or DENY, APPROVE_ALL, QUIT, TIMEOUT
    "user_response": "y",
    "approval_future_id": 140234567890,
    "tool_id": "terminal_0"
}
```

**PERMISSION_DENIED Event:**
```python
{
    "decision": "DENY",
    "user_response": "N",
    "approval_future_id": 140234567890,
    "tool_id": "terminal_0"
}
```

---

## 3. Operation Categories

### 3.1 Terminal Commands

**Requires Approval**: Yes (unless whitelisted)

**Safe Commands** (auto-approved):
```python
SAFE_TERMINAL_COMMANDS = [
    "ls", "ll", "la",
    "pwd", "cd",
    "cat", "head", "tail",
    "grep", "find",
    "git log", "git status", "git diff",
    "echo", "printf"
]
```

**Dangerous Commands** (always require confirmation):
```python
DANGEROUS_TERMINAL_PATTERNS = [
    r"rm\s+.*(-rf|--recursive)",
    r"mkfs\.",
    r"dd\s+.*of=/dev",
    r"chmod\s+.*777",
    r":\(\)\s*{\s*:\|:&\s*}",  # fork bomb
    r"rm\s+-rf\s+(/|~|\.git)",
]
```

**Approval Prompt**:
```
Execute terminal command?
  Command: rm -rf node_modules
  CWD: /Users/malmazan/dev/kollabor-cli
  Timeout: 30s

[y]es, [N]o, [a]pprove all, [q]uit
```

---

### 3.2 File Operations

| Operation | Requires Approval | Default Action |
|-----------|------------------|----------------|
| `file_edit` | Yes (unless whitelisted path) | Prompt |
| `file_create` | Yes (unless whitelisted path) | Prompt |
| `file_create_overwrite` | Yes (always - destructive) | Prompt |
| `file_delete` | Yes (always - destructive) | Double-confirm |
| `file_move` | Yes | Prompt |
| `file_copy` | No | Auto-approve |
| `file_append` | Yes (unless whitelisted path) | Prompt |
| `file_insert_after` | Yes (unless whitelisted path) | Prompt |
| `file_insert_before` | Yes (unless whitelisted path) | Prompt |
| `file_mkdir` | No | Auto-approve |
| `file_rmdir` | Yes | Prompt |
| `file_read` | No | Auto-approve |
| `file_grep` | No | Auto-approve |

**Safe Paths** (auto-approved file operations):
```python
SAFE_FILE_PATHS = [
    "*.md",           # Markdown files
    "*.txt",          # Text files
    "*.json",         # Config files (user)
    "tests/**/*.py",  # Test files
    "docs/**/*",      # Documentation
    "*.log",          # Log files
]
```

**Protected Paths** (always require confirmation, never auto-approve):
```python
PROTECTED_PATHS = [
    "core/application.py",
    "main.py",
    "core/llm/llm_service.py",
    "core/llm/api_communication_service.py",
    ".env",
    ".git/**",
    "venv/**",
    ".venv/**"
]
```

**File Write Approval Prompt**:
```
Modify file?
  Operation: edit
  File: core/config/service.py
  Changes: Replace 1 occurrence at line 42
  Backup: core/config/service.py.bak

[y]es, [N]o, [a]pprove all, [q]uit, [v]iew diff
```

**File Delete Approval Prompt**:
```
Delete file?
  File: plugins/old_plugin.py
  Backup: plugins/old_plugin.py.deleted

THIS CANNOT BE UNDONE

Confirm delete? [y/N]
```

---

### 3.3 MCP Tools

**Requires Approval**: Yes (always - unknown execution)

MCP tools are third-party and their behavior is unknown, so they always require approval.

**Approval Prompt**:
```
Execute MCP tool?
  Tool: filesystem.write_file
  Server: local-filesystem
  Arguments: {"path": "config.json", "content": "..."}

[y]es, [N]o, [a]pprove all, [q]uit
```

---

## 4. User Responses

### Interactive Prompt Options

| Response | Meaning | Behavior |
|----------|---------|----------|
| `y` / `yes` | Approve this operation | Execute and continue |
| `N` / `no` | Deny this operation | Skip and continue |
| `a` / `all` | Approve all remaining operations | Execute remaining tools |
| `q` / `quit` | Stop all operations | Cancel entire batch |
| `v` / `view` | View details (for file operations) | Show diff/details, then re-prompt |

### Default Behavior

- **Default response**: `N` (deny) - require explicit approval
- **Timeout behavior**: Default to `N` after 30 seconds
- **Batch operations**: Ask for each operation unless `a` selected

---

## 5. Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `core/llm/permission_manager.py` | CREATE | Permission checking logic |
| `core/llm/tool_executor.py` | MODIFY | Add permission gate before execution |
| `core/cli.py` | MODIFY | Add `--yolo` flag |
| `core/config/loader.py` | MODIFY | Add permissions config schema |
| `core/io/input_handler.py` | MODIFY | Handle permission prompt responses |
| `core/events/models.py` | MODIFY | Add permission event types |

---

## 6. Implementation

### 6.1 Core Infrastructure: PermissionManager

File: `core/llm/permission_manager.py`

```python
"""Permission management for tool execution.

Provides safety gates for destructive operations with user approval
workflow similar to Claude Code CLI and Codex CLI.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import re

logger = logging.getLogger(__name__)


class ApprovalDecision(Enum):
    """User approval decision."""
    APPROVE = "approve"
    DENY = "deny"
    APPROVE_ALL = "approve_all"
    QUIT = "quit"
    VIEW_DETAILS = "view_details"
    TIMEOUT = "timeout"


class OperationCategory(Enum):
    """Operation categories for permission rules."""
    TERMINAL = "terminal"
    FILE_WRITE = "file_write"
    FILE_DELETE = "file_delete"
    FILE_READ = "file_read"
    MCP_TOOL = "mcp_tool"
    SAFE = "safe"


@dataclass
class PermissionRequest:
    """Request for user approval."""
    tool_type: str
    tool_id: str
    category: OperationCategory
    operation_data: Dict[str, Any]
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    can_auto_approve: bool = False
    requires_double_confirm: bool = False


@dataclass
class PermissionResult:
    """Result of permission request."""
    decision: ApprovalDecision
    approved: bool
    message: str = ""
    auto_approved: bool = False
    user_response: Optional[str] = None


class PermissionManager:
    """Manage tool execution permissions with user approval workflow."""

    # Safe terminal commands (auto-approved)
    SAFE_TERMINAL_COMMANDS = {
        "ls", "ll", "la",
        "pwd", "cd",
        "cat", "head", "tail",
        "grep", "find", "wc",
        "echo", "printf",
        "date", "whoami",
        "git log", "git status", "git diff", "git show",
    }

    # Dangerous terminal patterns (always require confirmation)
    DANGEROUS_TERMINAL_PATTERNS = [
        r"rm\s+.*(-rf|--recursive)",
        r"mkfs\.",
        r"dd\s+.*of=/dev",
        r"chmod\s+.*777",
        r":\(\)\s*{\s*:\|:&\s*}",
        r"rm\s+-rf\s+(/|~|\.git)",
        r">\s*/dev/sd",
        r"format\s+.*:",
    ]

    # Safe file patterns (auto-approved operations)
    SAFE_FILE_PATTERNS = [
        r"\.md$",
        r"\.txt$",
        r"\.json$",
        r"tests/.*\.py$",
        r"docs/.*",
        r"\.log$",
        r"\.bak$",
    ]

    # Protected paths (always require confirmation)
    PROTECTED_PATHS = {
        "core/application.py",
        "main.py",
        "core/llm/llm_service.py",
        "core/llm/api_communication_service.py",
        ".env",
        ".git",
        "venv",
        ".venv",
    }

    def __init__(self, config=None):
        """Initialize permission manager.

        Args:
            config: Configuration manager
        """
        self.config = config
        self._approved_all = False
        self._approval_cache: Dict[str, ApprovalDecision] = {}

        # Load config settings
        self._load_config()

        # Statistics
        self.stats = {
            "total_requests": 0,
            "approved": 0,
            "denied": 0,
            "auto_approved": 0,
            "double_confirmed": 0,
            "quit_requested": 0,
        }

        logger.info("Permission manager initialized")

    def _load_config(self):
        """Load configuration settings."""
        if not self.config:
            self.enabled = True
            self.yolo_mode = False
            self.safe_commands_only = False
            self.approval_timeout = 30
            self.auto_approve_safe_commands = True
            self.auto_approve_safe_paths = True
            return

        self.enabled = self.config.get("permissions.enabled", True)
        self.yolo_mode = self.config.get("permissions.yolo_mode", False)
        self.safe_commands_only = self.config.get("permissions.safe_commands_only", False)
        self.approval_timeout = self.config.get("permissions.approval_timeout", 30)
        self.auto_approve_safe_commands = self.config.get(
            "permissions.auto_approve_safe_commands", True
        )
        self.auto_approve_safe_paths = self.config.get(
            "permissions.auto_approve_safe_paths", True
        )

        # Load custom safe commands from config
        custom_safe_commands = self.config.get("permissions.safe_commands", [])
        if custom_safe_commands:
            self.SAFE_TERMINAL_COMMANDS.update(set(custom_safe_commands))

        # Load custom safe patterns from config
        custom_safe_patterns = self.config.get("permissions.safe_file_patterns", [])
        if custom_safe_patterns:
            self.SAFE_FILE_PATTERNS.extend(custom_safe_patterns)

    def reset_batch(self):
        """Reset batch approval state (for new request batches)."""
        self._approved_all = False
        self._approval_cache.clear()

    async def check_permission(
        self,
        tool_type: str,
        tool_id: str,
        operation_data: Dict[str, Any]
    ) -> PermissionResult:
        """Check if operation requires approval.

        Args:
            tool_type: Type of tool (terminal, file_edit, etc.)
            tool_id: Unique tool identifier
            operation_data: Operation-specific data

        Returns:
            PermissionResult with decision
        """
        # Check if permissions disabled
        if not self.enabled or self.yolo_mode:
            return PermissionResult(
                decision=ApprovalDecision.APPROVE,
                approved=True,
                auto_approved=True,
                message="Permissions disabled (--yolo mode)"
            )

        # Check batch approval
        if self._approved_all:
            return PermissionResult(
                decision=ApprovalDecision.APPROVE,
                approved=True,
                auto_approved=True,
                message="Auto-approved (approve all mode)"
            )

        # Determine operation category
        category = self._categorize_operation(tool_type, operation_data)

        # Create permission request
        request = PermissionRequest(
            tool_type=tool_type,
            tool_id=tool_id,
            category=category,
            operation_data=operation_data,
            description=self._build_description(tool_type, operation_data),
            details=self._build_details(tool_type, operation_data),
            can_auto_approve=self._can_auto_approve(category, operation_data),
            requires_double_confirm=category == OperationCategory.FILE_DELETE
        )

        # Update stats
        self.stats["total_requests"] += 1

        # Check for auto-approval
        if request.can_auto_approve:
            self.stats["auto_approved"] += 1
            logger.debug(f"Auto-approved {tool_type}:{tool_id}")
            return PermissionResult(
                decision=ApprovalDecision.APPROVE,
                approved=True,
                auto_approved=True,
                message=f"Auto-approved ({category.value})"
            )

        # Require user approval
        logger.info(f"Requesting approval for {tool_type}:{tool_id}")
        return PermissionResult(
            decision=ApprovalDecision.APPROVE,  # Placeholder
            approved=False,  # Will be set after user response
            message=f"Requires approval: {request.description}"
        )

    def _categorize_operation(
        self,
        tool_type: str,
        operation_data: Dict[str, Any]
    ) -> OperationCategory:
        """Categorize operation for permission rules.

        Args:
            tool_type: Tool type
            operation_data: Operation data

        Returns:
            OperationCategory
        """
        # Terminal commands
        if tool_type == "terminal":
            command = operation_data.get("command", "")
            if self._is_safe_terminal_command(command):
                return OperationCategory.SAFE
            elif self._is_dangerous_terminal_command(command):
                return OperationCategory.FILE_DELETE  # Treat as high-risk
            else:
                return OperationCategory.TERMINAL

        # MCP tools
        elif tool_type == "mcp_tool":
            return OperationCategory.MCP_TOOL

        # File operations
        elif tool_type.startswith("file_"):
            filepath = operation_data.get("file", "")

            # Safe operations
            if tool_type in ("file_read", "file_grep"):
                return OperationCategory.SAFE

            # Delete operations
            elif tool_type in ("file_delete", "file_rmdir"):
                return OperationCategory.FILE_DELETE

            # Write operations
            elif tool_type in (
                "file_edit", "file_create", "file_create_overwrite",
                "file_append", "file_insert_after", "file_insert_before"
            ):
                if self._is_safe_file_path(filepath):
                    return OperationCategory.SAFE
                elif self._is_protected_path(filepath):
                    return OperationCategory.FILE_DELETE  # High risk
                else:
                    return OperationCategory.FILE_WRITE

        # Default to safe
        return OperationCategory.SAFE

    def _is_safe_terminal_command(self, command: str) -> bool:
        """Check if terminal command is safe.

        Args:
            command: Command string

        Returns:
            True if safe
        """
        if not self.auto_approve_safe_commands:
            return False

        # Extract base command
        base_cmd = command.strip().split()[0] if command.strip().split() else ""

        # Check against safe commands
        if base_cmd in self.SAFE_TERMINAL_COMMANDS:
            return True

        return False

    def _is_dangerous_terminal_command(self, command: str) -> bool:
        """Check if terminal command is dangerous.

        Args:
            command: Command string

        Returns:
            True if dangerous
        """
        for pattern in self.DANGEROUS_TERMINAL_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False

    def _is_safe_file_path(self, filepath: str) -> bool:
        """Check if file path is safe for auto-approval.

        Args:
            filepath: File path

        Returns:
            True if safe
        """
        if not self.auto_approve_safe_paths:
            return False

        if not filepath:
            return False

        # Check against safe patterns
        for pattern in self.SAFE_FILE_PATTERNS:
            if re.search(pattern, filepath, re.IGNORECASE):
                return True

        return False

    def _is_protected_path(self, filepath: str) -> bool:
        """Check if file path is protected.

        Args:
            filepath: File path

        Returns:
            True if protected
        """
        if not filepath:
            return False

        # Check exact matches
        if filepath in self.PROTECTED_PATHS:
            return True

        # Check prefix matches
        for protected in self.PROTECTED_PATHS:
            if filepath.startswith(protected + "/"):
                return True

        return False

    def _can_auto_approve(
        self,
        category: OperationCategory,
        operation_data: Dict[str, Any]
    ) -> bool:
        """Check if operation can be auto-approved.

        Args:
            category: Operation category
            operation_data: Operation data

        Returns:
            True if can auto-approve
        """
        # Safe category always auto-approves
        if category == OperationCategory.SAFE:
            return True

        # Protected paths never auto-approve
        filepath = operation_data.get("file", "")
        if self._is_protected_path(filepath):
            return False

        return False

    def _build_description(
        self,
        tool_type: str,
        operation_data: Dict[str, Any]
    ) -> str:
        """Build human-readable description for approval prompt.

        Args:
            tool_type: Tool type
            operation_data: Operation data

        Returns:
            Description string
        """
        if tool_type == "terminal":
            command = operation_data.get("command", "")
            cwd = operation_data.get("cwd", str(Path.cwd()))
            timeout = operation_data.get("timeout", 30)
            return f"Execute terminal command: '{command}' (cwd: {cwd}, timeout: {timeout}s)"

        elif tool_type == "mcp_tool":
            tool_name = operation_data.get("name", "")
            server = operation_data.get("server", "unknown")
            return f"Execute MCP tool: {tool_name} (server: {server})"

        elif tool_type.startswith("file_"):
            filepath = operation_data.get("file", "")

            if tool_type == "file_edit":
                return f"Edit file: {filepath}"
            elif tool_type == "file_create":
                return f"Create file: {filepath}"
            elif tool_type == "file_delete":
                return f"Delete file: {filepath}"
            elif tool_type == "file_move":
                return f"Move file: {filepath}"
            elif tool_type == "file_copy":
                return f"Copy file: {filepath}"
            elif tool_type == "file_append":
                return f"Append to file: {filepath}"
            elif tool_type == "file_insert_after":
                return f"Insert into file: {filepath}"
            else:
                return f"File operation ({tool_type}): {filepath}"

        return f"Tool operation: {tool_type}"

    def _build_details(
        self,
        tool_type: str,
        operation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build details dict for approval prompt.

        Args:
            tool_type: Tool type
            operation_data: Operation data

        Returns:
            Details dictionary
        """
        details = {
            "tool_type": tool_type,
            "operation_data": operation_data.copy()
        }

        # Add tool-specific details
        if tool_type == "terminal":
            details["command"] = operation_data.get("command", "")
            details["cwd"] = str(Path.cwd())

        elif tool_type.startswith("file_"):
            filepath = operation_data.get("file", "")
            details["file"] = filepath
            details["exists"] = Path(filepath).exists() if filepath else False

            if tool_type == "file_edit":
                details["find"] = operation_data.get("find", "")[:100] + "..."
                details["replace"] = operation_data.get("replace", "")[:100] + "..."

        return details

    def set_approved_all(self, approved: bool):
        """Set batch approval state.

        Args:
            approved: True to approve all remaining operations
        """
        self._approved_all = approved
        logger.info(f"Batch approval mode: {'enabled' if approved else 'disabled'}")

    def get_stats(self) -> Dict[str, Any]:
        """Get permission statistics.

        Returns:
            Statistics dictionary
        """
        return self.stats.copy()

    def _update_stats(self, decision: ApprovalDecision, was_auto: bool = False):
        """Update permission statistics after decision.

        Args:
            decision: The approval decision made
            was_auto: Whether this was auto-approved
        """
        if was_auto:
            self.stats["auto_approved"] += 1
        else:
            self.stats["total_requests"] += 1

        if decision == ApprovalDecision.APPROVE:
            self.stats["approved"] += 1
        elif decision == ApprovalDecision.DENY:
            self.stats["denied"] += 1
        elif decision == ApprovalDecision.APPROVE_ALL:
            # Approve all doesn't increment individual approvals
            self.stats["approved"] += 1
        elif decision == ApprovalDecision.QUIT:
            self.stats["quit_requested"] += 1
        elif decision == ApprovalDecision.TIMEOUT:
            self.stats["denied"] += 1

    def reset_stats(self):
        """Reset permission statistics."""
        self.stats = {
            "total_requests": 0,
            "approved": 0,
            "denied": 0,
            "auto_approved": 0,
            "double_confirmed": 0,
            "quit_requested": 0,
        }
```

---

### 6.2 Tool Executor Integration

File: `core/llm/tool_executor.py`

```python
# Add import at top
from .permission_manager import PermissionManager, ApprovalDecision

class ToolExecutor:
    def __init__(self, mcp_integration: MCPIntegration, event_bus,
                 terminal_timeout: int = 90, mcp_timeout: int = 180, config=None):
        # ... existing initialization ...

        # NEW: Permission manager
        self.permission_manager = PermissionManager(config)

        # File operations executor
        self.file_ops_executor = FileOperationsExecutor(config=config)

    async def execute_tool(self, tool_data: Dict[str, Any]) -> ToolExecutionResult:
        """Execute a single tool with permission gate.

        Args:
            tool_data: Tool information from ResponseParser

        Returns:
            Tool execution result
        """
        tool_type = tool_data.get("type", "unknown")
        tool_id = tool_data.get("id", "unknown")

        start_time = time.time()

        try:
            # NEW: Check permission before execution
            permission_result = await self.permission_manager.check_permission(
                tool_type=tool_type,
                tool_id=tool_id,
                operation_data=tool_data
            )

            # If permission denied, return early
            if not permission_result.approved:
                logger.info(f"Operation denied: {tool_id}")
                self.permission_manager.stats["denied"] += 1

                return ToolExecutionResult(
                    tool_id=tool_id,
                    tool_type=tool_type,
                    success=False,
                    error=f"Operation requires approval: {permission_result.message}"
                )

            # Emit pre-execution hook
            await self.event_bus.emit_with_hooks(
                EventType.TOOL_CALL_PRE,
                {"tool_data": tool_data, "approved": True},
                "tool_executor"
            )

            # Execute based on tool type
            try:
                logger.debug(f"Executing tool {tool_id} of type {tool_type}")
                if tool_type == "terminal":
                    result = await self._execute_terminal_command(tool_data)
                elif tool_type == "mcp_tool":
                    result = await self._execute_mcp_tool(tool_data)
                elif tool_type.startswith("file_"):
                    result = await self._execute_file_operation(tool_data)
                else:
                    result = ToolExecutionResult(
                        tool_id=tool_id,
                        tool_type=tool_type,
                        success=False,
                        error=f"Unknown tool type: {tool_type}"
                    )
            except Exception as inner_e:
                import traceback
                inner_trace = traceback.format_exc()
                logger.error(f"Inner execution error for {tool_id}: {str(inner_e)}")
                raise

            # Update execution time
            result.execution_time = time.time() - start_time

            # Emit post-execution hook
            await self.event_bus.emit_with_hooks(
                EventType.TOOL_CALL_POST,
                {
                    "tool_data": tool_data,
                    "result": result.to_dict(),
                    "auto_approved": permission_result.auto_approved
                },
                "tool_executor"
            )

            # Update statistics
            if result.success:
                self.permission_manager.stats["approved"] += 1

            self._update_stats(result)
            logger.info(f"Tool execution completed: {result}")
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            error_result = ToolExecutionResult(
                tool_id=tool_id,
                tool_type=tool_type,
                success=False,
                error=f"Execution error: {str(e)}",
                execution_time=execution_time
            )

            self._update_stats(error_result)
            self.permission_manager.stats["denied"] += 1
            logger.error(f"Tool execution failed: {e}")
            return error_result

    async def execute_all_tools(self, tools: List[Dict[str, Any]]) -> List[ToolExecutionResult]:
        """Execute multiple tools with interactive approval.

        Args:
            tools: List of tool data from ResponseParser

        Returns:
            List of execution results
        """
        if not tools:
            return []

        logger.info(f"Executing {len(tools)} tools with permission checks")
        results = []

        # NEW: Reset batch state before new batch
        self.permission_manager.reset_batch()

        for i, tool_data in enumerate(tools):
            tool_id = tool_data.get("id", "unknown")

            # NEW: Check permission for each tool
            permission_result = await self.permission_manager.check_permission(
                tool_type=tool_data.get("type", "unknown"),
                tool_id=tool_id,
                operation_data=tool_data
            )

            # If not auto-approved, request user input
            if not permission_result.approved:
                user_decision = await self._request_user_approval(
                    tool_data=tool_data,
                    permission_result=permission_result,
                    index=i + 1,
                    total=len(tools)
                )

                # Handle user decision
                if user_decision == ApprovalDecision.DENY:
                    # Skip this tool
                    results.append(ToolExecutionResult(
                        tool_id=tool_id,
                        tool_type=tool_data.get("type", "unknown"),
                        success=False,
                        error="Operation denied by user"
                    ))
                    continue

                elif user_decision == ApprovalDecision.QUIT:
                    # Stop all remaining operations
                    logger.info(f"User quit batch at tool {i+1}/{len(tools)}")
                    self.permission_manager.stats["quit_requested"] += 1
                    break

                elif user_decision == ApprovalDecision.APPROVE_ALL:
                    # Approve all remaining operations
                    self.permission_manager.set_approved_all(True)
                    logger.info("User approved all remaining operations")

                elif user_decision == ApprovalDecision.TIMEOUT:
                    # Default to deny on timeout
                    results.append(ToolExecutionResult(
                        tool_id=tool_id,
                        tool_type=tool_data.get("type", "unknown"),
                        success=False,
                        error="Operation timed out awaiting approval"
                    ))
                    continue

            # Execute tool (approved or auto-approved)
            result = await self.execute_tool(tool_data)
            results.append(result)

            # Log intermediate result
            if result.success:
                logger.debug(f"Tool {i+1} succeeded")
            else:
                logger.warning(f"Tool {i+1} failed: {result.error}")

        logger.info(f"Tool execution batch completed: "
                   f"{sum(1 for r in results if r.success)}/{len(results)} successful")

        return results

    async def _request_user_approval(
        self,
        tool_data: Dict[str, Any],
        permission_result: PermissionResult,
        index: int,
        total: int
    ) -> ApprovalDecision:
        """Request user approval for operation.

        Uses asyncio.Future to wait for user input via event system.

        Args:
            tool_data: Tool data
            permission_result: Permission check result
            index: Tool index in batch
            total: Total number of tools

        Returns:
            User approval decision
        """
        # Create a Future to wait for user response
        approval_future = asyncio.Future()

        # Store the future in permission manager for lookup by input handler
        self.permission_manager._pending_approval = approval_future

        # Emit approval request event with future reference
        await self.event_bus.emit_with_hooks(
            EventType.PERMISSION_REQUEST,
            {
                "tool_data": tool_data,
                "permission_result": permission_result,
                "index": index,
                "total": total,
                "timeout": self.permission_manager.approval_timeout,
                "approval_future_id": id(approval_future)  # For debugging
            },
            "tool_executor"
        )

        try:
            # Wait for user response with timeout
            decision = await asyncio.wait_for(
                approval_future,
                timeout=self.permission_manager.approval_timeout
            )
            return decision
        except asyncio.TimeoutError:
            logger.warning(f"Approval request timed out for tool {tool_data.get('id')}")
            return ApprovalDecision.TIMEOUT
        finally:
            # Clean up future reference
            self.permission_manager._pending_approval = None
```

---

### 6.3 Command-Line Flag (--yolo)

File: `core/cli.py`

Add the --yolo argument to the existing parser:

```python
def parse_arguments():
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Kollab - Terminal-based LLM chat interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  kollab                                    # Start interactive mode
  kollab "what is 1+1?"                     # Pipe mode with query
  kollab --yolo                              # YOLO mode (bypass all approvals)
  kollab --yolo "install packages"           # YOLO mode with query
        """,
    )

    # ... existing arguments ...

    # NEW: --yolo flag
    parser.add_argument(
        "--yolo",
        action="store_true",
        default=False,
        help="YOLO mode: bypass all permission checks (dangerous!)"
    )

    return parser.parse_args()
```

Update `async_main()` to pass the flag:

```python
async def async_main() -> None:
    """Main async entry point for the application with proper error handling."""
    # Setup bootstrap logging before application starts
    setup_bootstrap_logging()
    logger = logging.getLogger(__name__)

    args = parse_arguments()

    # NEW: Pass --yolo flag to application
    yolo_mode = getattr(args, 'yolo', False)

    if yolo_mode:
        logger.warning("YOLO mode enabled - all permission checks bypassed!")
        print("[warn] YOLO mode enabled - all tool operations will execute without approval")

    # Get piped input if present
    piped_input = None

    # ... rest of existing main ...

    # Create application with yolo_mode
    app = None
    try:
        logger.info("Creating application instance...")
        app = TerminalLLMChat(
            system_prompt_file=args.system_prompt,
            agent_name=args.agent,
            profile_name=args.profile,
            save_profile=args.save,
            skill_names=args.skill,
            yolo_mode=yolo_mode  # NEW parameter
        )
```

---

### 6.4 Configuration Integration

File: `core/config/loader.py`

Add permissions section to existing `get_base_config()` method. Locate the method and insert the permissions section after the existing configuration sections.

**Find this line in `get_base_config()`:**
```python
return {
    # ... existing config sections ...
}
```

**Insert this permissions section:**
```python
def get_base_config(self) -> Dict[str, Any]:
    """Get the base application configuration with defaults.

    Returns:
        Base configuration dictionary with application defaults.
    """
    # Load system prompt from file
    system_prompt = self._load_system_prompt()

    return {
        # ... existing config sections ...

        # NEW: Permissions section
        "permissions": {
            "enabled": True,
            "yolo_mode": False,
            "safe_commands_only": False,
            "approval_timeout": 30,
            "auto_approve_safe_commands": True,
            "auto_approve_safe_paths": True,
            "safe_commands": [
                "ls", "ll", "la",
                "pwd", "cd",
                "cat", "head", "tail",
                "grep", "find", "wc",
                "echo", "printf",
                "date", "whoami",
                "git log", "git status", "git diff", "git show",
            ],
            "safe_file_patterns": [
                r"\.md$",
                r"\.txt$",
                r"\.json$",
                r"tests/.*\.py$",
                r"docs/.*",
                r"\.log$",
                r"\.bak$",
            ],
            "protected_paths": [
                "core/application.py",
                "main.py",
                "core/llm/llm_service.py",
                "core/llm/api_communication_service.py",
                ".env",
                ".git",
                "venv",
                ".venv",
            ],
            "double_confirm_deletes": True,
            "show_approval_stats": True
        },
        # ... rest of existing config ...
    }
```

**Update Application to Pass YOLO Mode:**

In `core/application.py`, update the `__init__()` to accept and pass yolo_mode:

```python
def __init__(self,
             system_prompt_file: Optional[str] = None,
             agent_name: Optional[str] = None,
             profile_name: Optional[str] = None,
             save_profile: bool = False,
             skill_names: Optional[List[str]] = None,
             yolo_mode: bool = False):  # NEW parameter
    """Initialize the application.

    Args:
        system_prompt_file: Optional custom system prompt file.
        agent_name: Optional agent name to use.
        profile_name: Optional profile name to use.
        save_profile: Whether to save auto-created profile.
        skill_names: Optional list of skills to load.
        yolo_mode: Whether to enable YOLO mode (bypass approvals).  # NEW
    """
    # ... existing init ...

    # Pass yolo_mode to ToolExecutor via config
    if yolo_mode:
        # Temporarily set yolo_mode in config
        self.config["permissions"]["yolo_mode"] = True
        logger.warning("YOLO mode enabled - bypassing all permission checks")
```

---

### 6.5 Event Types

File: `core/events/models.py`

Add to `EventType` enum (after the `MODAL_HIDE` event, before `FULLSCREEN_INPUT`):

```python
class EventType(Enum):
    """Event types for the hook system."""

    # ... existing event types ...

    # Modal events
    MODAL_TRIGGER = "modal_trigger"
    STATUS_MODAL_TRIGGER = "status_modal_trigger"
    STATUS_MODAL_RENDER = "status_modal_render"
    LIVE_MODAL_TRIGGER = "live_modal_trigger"
    MODAL_COMMAND_SELECTED = "modal_command_selected"

    # Rendering control events
    PAUSE_RENDERING = "pause_rendering"
    RESUME_RENDERING = "resume_rendering"
    MODAL_SHOW = "modal_show"
    MODAL_HIDE = "modal_hide"
    MODAL_SAVE = "modal_save"
    FULLSCREEN_INPUT = "fullscreen_input"
    COMMAND_MENU_ACTIVATE = "command_menu_activate"

    # Status area takeover events
    STATUS_TAKEOVER_START = "status_takeover_start"
    STATUS_TAKEOVER_NAVIGATE = "status_takeover_navigate"
    STATUS_TAKEOVER_ACTION = "status_takeover_action"
    STATUS_TAKEOVER_END = "status_takeover_end"

    # NEW: Permission events (inserted here for approval workflow)
    PERMISSION_REQUEST = "permission_request"           # Request user approval
    PERMISSION_GRANTED = "permission_granted"           # User approved
    PERMISSION_DENIED = "permission_denied"             # User denied
    PERMISSION_TIMEOUT = "permission_timeout"           # Approval timed out
    PERMISSION_APPROVE_ALL = "permission_approve_all"   # Approve all remaining
    PERMISSION_QUIT = "permission_quit"                 # Quit batch
```

**Integration Note:**
These events are inserted between existing events to maintain the enum ordering.
The event bus will automatically handle them via the hook system.

---

### 6.6 Input Handler Integration

File: `core/io/input_handler.py`

The InputHandler needs to handle permission requests and route user responses back to PermissionManager.

#### 6.6.1 Add Permission State to InputHandler

Add new attributes to `InputHandler.__init__()`:

```python
# Permission handling state
self._approval_mode_active = False
self._approval_future_id = None
self._permission_manager = None  # Passed from Application
```

#### 6.6.2 Register Permission Request Handler

Register a hook to handle PERMISSION_REQUEST events. This is done in HookRegistrar:

```python
# In HookRegistrar.register_all_hooks(), add:
await self.event_bus.register_hook(
    Hook(
        name="handle_permission_request",
        plugin_name="input_handler",
        event_type=EventType.PERMISSION_REQUEST,
        priority=HookPriority.DISPLAY,
        callback=self._handle_permission_request,
        enabled=True
    )
)
```

#### 6.6.3 Handle Permission Request

Add method to `InputHandler`:

```python
async def _handle_permission_request(
    self, event_data: Dict[str, Any], context: str = None
) -> Dict[str, Any]:
    """Handle permission request events by showing approval prompt.

    Args:
        event_data: Event data containing permission request info.
        context: Hook execution context.

    Returns:
        Dictionary with handling result.
    """
    try:
        tool_data = event_data.get("tool_data", {})
        permission_result = event_data.get("permission_result", {})
        index = event_data.get("index", 1)
        total = event_data.get("total", 1)

        # Store future ID for response correlation
        self._approval_future_id = event_data.get("approval_future_id")

        # Determine UI type (modal vs status takeover)
        ui_type = self._determine_approval_ui_type(tool_data)

        if ui_type == "modal":
            # Show modal for destructive operations
            await self._show_approval_modal(tool_data, permission_result, index, total)
        else:
            # Show status takeover for quick approvals
            await self._show_approval_status_takeover(tool_data, index, total)

        # Mark approval mode as active
        self._approval_mode_active = True

        return {"success": True, "ui_type": ui_type}

    except Exception as e:
        logger.error(f"Error handling permission request: {e}")
        return {"success": False, "error": str(e)}


def _determine_approval_ui_type(self, tool_data: Dict[str, Any]) -> str:
    """Determine whether to show modal or status takeover.

    Args:
        tool_data: Tool data to check

    Returns:
        "modal" or "status_takeover"
    """
    tool_type = tool_data.get("type", "")

    # Modal for destructive operations
    if tool_type in ("file_delete", "file_create_overwrite"):
        return "modal"

    if tool_type == "terminal":
        command = tool_data.get("command", "")
        # Modal for dangerous commands
        dangerous_patterns = [
            r"rm\s+.*(-rf|--recursive)",
            r"mkfs\.",
            r"dd\s+.*of=/dev",
        ]
        import re
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return "modal"

    # Status takeover for quick approvals
    return "status_takeover"


async def _show_approval_modal(self, tool_data, permission_result, index, total):
    """Show approval modal overlay.

    Args:
        tool_data: Tool data
        permission_result: Permission check result
        index: Tool index
        total: Total tools
    """
    from ...events.models import UIConfig

    ui_config = UIConfig(
        type="modal",
        title="Tool Execution Approval Required",
        modal_config={
            "sections": [
                {
                    "title": f"Operation {index} of {total}",
                    "commands": [
                        {
                            "name": self._format_tool_description(tool_data),
                            "description": permission_result.get("message", ""),
                            "action": "show_approval_details",
                            "exit_mode": "minimal",
                            "metadata": tool_data
                        }
                    ]
                },
                {
                    "title": "Options",
                    "commands": [
                        {"name": "[y]es", "description": "Execute this operation", "action": "approve"},
                        {"name": "[N]o", "description": "Skip this operation", "action": "deny"},
                        {"name": "[a]pprove all", "description": "Approve all remaining", "action": "approve_all"},
                        {"name": "[q]uit", "description": "Stop all operations", "action": "quit"},
                    ]
                }
            ]
        }
    )

    await self.event_bus.emit_with_hooks(
        EventType.MODAL_TRIGGER,
        {"ui_config": ui_config},
        "input_handler"
    )


async def _show_approval_status_takeover(self, tool_data, index, total):
    """Show approval prompt in status area.

    Args:
        tool_data: Tool data
        index: Tool index
        total: Total tools
    """
    from ...events.models import UIConfig

    ui_config = UIConfig(
        type="status_takeover",
        title=f"Approve: {tool_data.get('command', 'operation')}",
        modal_config={
            "sections": [
                {
                    "commands": [
                        {
                            "name": f"[{index}/{total}]",
                            "description": self._format_tool_description(tool_data),
                            "action": "show_details"
                        }
                    ]
                }
            ]
        }
    }

    await self.event_bus.emit_with_hooks(
        EventType.STATUS_TAKEOVER_START,
        {"ui_config": ui_config},
        "input_handler"
    )


def _format_tool_description(self, tool_data: Dict[str, Any]) -> str:
    """Format tool data for display.

    Args:
        tool_data: Tool data

    Returns:
        Formatted description string
    """
    tool_type = tool_data.get("type", "")

    if tool_type == "terminal":
        command = tool_data.get("command", "")
        return f"Terminal: {command[:50]}..."
    elif tool_type.startswith("file_"):
        filepath = tool_data.get("file", "")
        operation = tool_type.replace("file_", "").replace("_", " ").title()
        return f"{operation}: {filepath}"
    elif tool_type == "mcp_tool":
        tool_name = tool_data.get("name", "")
        return f"MCP Tool: {tool_name}"
    else:
        return f"{tool_type}: unknown operation"
```

#### 6.6.4 Handle Permission Response

Add method to route user decision back to PermissionManager:

```python
def _route_permission_response(self, decision: ApprovalDecision, user_response: str):
    """Route user's approval decision back to PermissionManager.

    Args:
        decision: User's decision (APPROVE, DENY, APPROVE_ALL, QUIT)
        user_response: Raw user input (e.g., "y", "N", "a", "q")
    """
    try:
        # Get pending Future from PermissionManager
        permission_manager = self._permission_manager

        if permission_manager and permission_manager._pending_approval:
            future = permission_manager._pending_approval

            # Check if future is not already done
            if not future.done():
                future.set_result(decision)
                logger.info(f"Permission decision routed: {decision.value} from '{user_response}'")

            # Handle APPROVE_ALL: set flag in PermissionManager
            if decision == ApprovalDecision.APPROVE_ALL:
                permission_manager.set_approved_all(True)

        # Clear approval mode
        self._approval_mode_active = False
        self._approval_future_id = None

    except Exception as e:
        logger.error(f"Error routing permission response: {e}")
        # On error, default to DENY (safe default)
        if permission_manager and permission_manager._pending_approval:
            try:
                if not permission_manager._pending_approval.done():
                    permission_manager._pending_approval.set_result(ApprovalDecision.DENY)
            except:
                pass
```

#### 6.6.5 Integrate with KeyPressHandler

Modify `KeyPressHandler` to check for approval mode:

```python
# In KeyPressHandler._handle_key_press(), add at the top:

# Check if we're in approval mode
if (hasattr(self, '_approval_mode_active') and
    hasattr(self, '_route_permission_response') and
    self._approval_mode_active):
    return await self._handle_approval_keypress(key_press)


async def _handle_approval_keypress(self, key_press: KeyPress) -> bool:
    """Handle keypress during approval prompt.

    Args:
        key_press: Parsed key press

    Returns:
        True if key was handled
    """
    from ...llm.permission_manager import ApprovalDecision

    # Map keys to decisions
    key_mapping = {
        'y': ApprovalDecision.APPROVE,
        'Y': ApprovalDecision.APPROVE,
        'n': ApprovalDecision.DENY,
        'N': ApprovalDecision.DENY,
        'a': ApprovalDecision.APPROVE_ALL,
        'A': ApprovalDecision.APPROVE_ALL,
        'q': ApprovalDecision.QUIT,
        'Q': ApprovalDecision.QUIT,
        '\r': ApprovalDecision.APPROVE,  # Enter key
    }

    # Get decision from key
    if key_press.char:
        decision = key_mapping.get(key_press.char)
    elif key_press.name == "Enter":
        decision = ApprovalDecision.APPROVE
    else:
        decision = None

    if decision:
        # Route decision to PermissionManager
        self._route_permission_response(decision, key_press.char or key_press.name)

        # Close modal or status takeover
        if self.command_mode == CommandMode.MODAL:
            # ModalController handles exit
            await self._modal_controller._exit_modal_mode()
        elif self.command_mode == CommandMode.STATUS_TAKEOVER:
            # CommandModeHandler handles exit
            await self._command_mode_handler.exit_command_mode()

        return True

    return False
```

#### 6.6.6 Permission State Management

The PermissionManager stores the pending approval Future. Here's how it's accessed:

**In Application Initialization:**
```python
# In Application.__init__(), after creating ToolExecutor:
self.tool_executor = ToolExecutor(mcp_integration, event_bus, config)
self.permission_manager = self.tool_executor.permission_manager

# Pass to InputHandler
self.input_handler = InputHandler(
    event_bus,
    renderer,
    config,
    permission_manager=self.permission_manager  # NEW
)
```

**In PermissionManager:**
```python
def __init__(self, config=None):
    """Initialize permission manager.

    Args:
        config: Configuration manager
    """
    # ... existing init ...
    self._pending_approval: Optional[asyncio.Future] = None
```

**In InputHandler:**
```python
def __init__(self, event_bus, renderer, config, permission_manager=None):
    """Initialize the input handler.

    Args:
        event_bus: Event bus for emitting input events.
        renderer: Terminal renderer for updating input display.
        config: Configuration manager for input settings.
        permission_manager: PermissionManager for approval routing (NEW)
    """
    # ... existing init ...
    self._permission_manager = permission_manager
```

This creates a clean reference chain:
```
Application
  ├── ToolExecutor
  │   └── PermissionManager (_pending_approval Future)
  └── InputHandler (stores PermissionManager reference)
          └── KeyPressHandler (routes decisions back)
```

#### 6.6.7 Double-Confirmation Flow for Deletes

File delete operations require two confirmations:

```python
async def _handle_approval_keypress(self, key_press: KeyPress) -> bool:
    """Handle keypress during approval prompt.

    Args:
        key_press: Parsed key press

    Returns:
        True if key was handled
    """
    from ...llm.permission_manager import ApprovalDecision

    # Check for delete double-confirmation
    if (hasattr(self, '_double_confirm_active') and
        self._double_confirm_active):

        key_mapping = {
            'y': ApprovalDecision.APPROVE,
            'Y': ApprovalDecision.APPROVE,
        }

        if key_press.char in ('y', 'Y'):
            # Second confirmation received
            decision = ApprovalDecision.APPROVE
            self._double_confirm_active = False
        else:
            # Any other key cancels delete
            decision = ApprovalDecision.DENY
            self._double_confirm_active = False

        self._route_permission_response(decision, key_press.char or key_press.name)

        # Exit modal
        await self._modal_controller._exit_modal_mode()
        return True

    # Normal approval handling
    # ... existing code ...

    # For delete operations, enter double-confirm mode
    tool_data = event_data.get("tool_data", {})
    if tool_data.get("type") == "file_delete":
        # Show first confirmation (existing modal)
        await self._show_approval_modal(tool_data, permission_result, index, total)

        # Set flag for second confirmation
        self._double_confirm_active = True

        return {"success": True, "ui_type": "double_confirm"}
```

---

## 7. Configuration

### Complete Schema

```json
{
  "permissions": {
    "enabled": true,
    "yolo_mode": false,
    "safe_commands_only": false,
    "approval_timeout": 30,
    "auto_approve_safe_commands": true,
    "auto_approve_safe_paths": true,
    "safe_commands": [
      "ls", "ll", "la",
      "pwd", "cd",
      "cat", "head", "tail",
      "grep", "find", "wc",
      "echo", "printf",
      "date", "whoami",
      "git log", "git status", "git diff", "git show"
    ],
    "safe_file_patterns": [
      "\\.md$",
      "\\.txt$",
      "\\.json$",
      "tests/.*\\.py$",
      "docs/.*",
      "\\.log$",
      "\\.bak$"
    ],
    "protected_paths": [
      "core/application.py",
      "main.py",
      "core/llm/llm_service.py",
      "core/llm/api_communication_service.py",
      ".env",
      ".git",
      "venv",
      ".venv"
    ],
    "double_confirm_deletes": true,
    "show_approval_stats": true
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | bool | `true` | Enable permission checks |
| `yolo_mode` | bool | `false` | Bypass all approvals (CLI --yolo sets this) |
| `safe_commands_only` | bool | `false` | Only allow safe commands (experimental) |
| `approval_timeout` | int | `30` | Seconds to wait for user response |
| `auto_approve_safe_commands` | bool | `true` | Auto-approve whitelisted terminal commands |
| `auto_approve_safe_paths` | bool | `true` | Auto-approve operations on safe file patterns |
| `safe_commands` | list | `[...]` | Whitelisted terminal commands |
| `safe_file_patterns` | list | `[...]` | Regex patterns for safe file paths |
| `protected_paths` | list | `[...]` | Paths that always require confirmation |
| `double_confirm_deletes` | bool | `true` | Require double confirmation for delete operations |
| `show_approval_stats` | bool | `true` | Show approval statistics in logs |

---

## 8. Security Considerations

### 8.1 Default Deny

- **Default behavior**: All operations require approval unless explicitly whitelisted
- **Protected paths**: Always require confirmation, never auto-approve
- **Dangerous commands**: Always require double confirmation

### 8.2 Protected Paths

Cannot be auto-approved even if they match safe patterns:
- Core application files
- Main entry point
- LLM service
- Configuration with secrets (.env)
- Git directory
- Virtual environments

### 8.3 Audit Trail

All permission decisions logged:
```json
{
  "timestamp": "2026-01-10T15:30:00Z",
  "tool_type": "terminal",
  "tool_id": "terminal_0",
  "operation": "rm -rf node_modules",
  "decision": "approved",
  "auto_approved": false,
  "user_response": "y",
  "execution_time_ms": 2450
}
```

### 8.4 Timeout Behavior

- Default timeout: 30 seconds
- On timeout: Operation denied (safe default)
- Configurable per environment

### 8.5 Escape Hatch

--yolo flag provides emergency bypass:
- Only works from CLI (not via config)
- Logged as warning
- Requires explicit action each session

---

## 9. User Experience

### 9.1 UI Integration Points

Permission prompts display through existing modal infrastructure:

**Two Modal Types**:

1. **Modal Overlay** (for complex approval decisions)
   - Uses `ModalOverlayRenderer` (centered overlay)
   - Triggered via `MODAL_TRIGGER` event
   - Blocks other UI interaction
   - Good for: file operations with diffs, dangerous commands

2. **Status Takeover** (for quick prompts)
   - Uses status area (bottom 4 lines)
   - Triggered via `STATUS_TAKEOVER_START` event
   - Allows conversation to continue visible
   - Good for: simple terminal commands, reads

**Event Flow**:
```
ToolExecutor._request_user_approval()
    ↓
emit event: PERMISSION_REQUEST
    ↓
ModalController catches event
    ↓
Calls modal_renderer.show_modal(ui_config) OR
    status takeover via command_mode_handler
    ↓
User sees prompt and responds
    ↓
InputHandler routes response back to ToolExecutor
```

**UI State Management**:
```
Current UI States:
  - CommandMode.NORMAL (conversation active)
  - CommandMode.MODAL (modal overlay active)
  - CommandMode.STATUS_TAKEOVER (status area active)

Approval Prompt State:
  - InputHandler in "approval_prompt" mode
  - PermissionManager stores pending approval
  - ModalController manages prompt display
```

---

### 9.2 Approval Prompt Format

```
╭───────────────────────────────────────────────╮
│  Tool Execution Approval Required             │
├───────────────────────────────────────────────┤
│  Operation 1 of 3                          │
│                                              │
│  Type: Terminal Command                      │
│  Command: rm -rf node_modules               │
│  CWD: /Users/malmazan/dev/kollabor-cli      │
│  Timeout: 30s                               │
│                                              │
│  ⚠️  This operation is destructive          │
╰───────────────────────────────────────────────╯

[y]es  Execute this operation
[N]o   Skip this operation
[a]ll  Approve all remaining operations
[q]uit Stop all operations

Your choice:
```

### 9.2 File Operation Prompt

```
╭───────────────────────────────────────────────╮
│  File Operation Approval Required             │
├───────────────────────────────────────────────┤
│  Operation 2 of 3                          │
│                                              │
│  Type: Edit File                            │
│  File: core/config/service.py                │
│  Line: 42                                   │
│                                              │
│  Changes:                                    │
│  - Replace "enabled = True"                   │
│  + With "enabled = False"                    │
│                                              │
│  Backup: core/config/service.py.bak           │
╰───────────────────────────────────────────────╯

[y]es, [N]o, [a]ll, [q]uit, [v]iew diff
```

### 9.3 Delete Confirmation Prompt

```
╭───────────────────────────────────────────────╮
│  ⚠️  DELETE CONFIRMATION                   │
├───────────────────────────────────────────────┤
│                                              │
│  You are about to delete:                   │
│  plugins/old_plugin.py                      │
│                                              │
│  Backup will be created:                     │
│  plugins/old_plugin.py.deleted               │
│                                              │
│  THIS CANNOT BE UNDONE                      │
╰───────────────────────────────────────────────╯

Confirm delete? [y/N]
```

### 9.4 Batch Approval

When user selects `a`pprove all:
```
✓ Approved 3 remaining operations
Executing: terminal_0...
Executing: file_edit_1...
Executing: file_create_2...
```

### 9.5 Quit Behavior

When user selects `q`uit:
```
User requested to stop execution
Cancelled 2 remaining operations
Completed: 1/3 operations
```


---

## 10. UI Integration Details

### 10.1 Where Approval Prompts Appear

Approval prompts display through **two existing UI systems**:

#### Option A: Modal Overlay (Recommended for Destructive Operations)

**When to Use**:
- File edits/creates/overwrites (destructive operations)
- Dangerous terminal commands
- MCP tool executions
- Double-confirmation for deletes

**How It Works**:
1. `ToolExecutor._request_user_approval()` emits `MODAL_TRIGGER` event
2. `ModalController._handle_modal_trigger()` receives event
3. `ModalRenderer.show_modal()` displays centered overlay
4. Input is routed to modal (blocks other UI interaction)
5. User responds (y/N/a/q), modal closes, decision returned

**Visual Example**:
```
┌────────────────────────────────────────────┐
│  Tool Execution Approval Required          │
├────────────────────────────────────────────┤
│  Operation 2 of 5                     │
│                                        │
│  Type: Edit File                       │
│  File: core/config/service.py           │
│                                        │
│  Changes:                               │
│  - Replace "enabled = True"            │
│  + With "enabled = False"             │
│                                        │
│  Backup: core/config/service.py.bak    │
├────────────────────────────────────────────┤
│  [y]es  [N]o  [a]pprove all  [q]uit │
└────────────────────────────────────────────┘
```

**Key Features**:
- Blocks other UI interaction (user must respond)
- Centered overlay on terminal
- Can show detailed information (diffs, file paths)
- Clean focus on decision

---

#### Option B: Status Takeover (Recommended for Quick Prompts)

**When to Use**:
- Simple terminal commands (ls, cat, grep)
- File read operations
- Non-destructive operations
- When you want conversation to remain visible

**How It Works**:
1. `ToolExecutor._request_user_approval()` emits `STATUS_TAKEOVER_START` event
2. `CommandModeHandler.handle_status_takeover_keypress()` catches event
3. Status area (bottom 4 lines) shows prompt
4. Conversation remains visible above
5. User responds (y/N/a/q), takeover ends, decision returned

**Visual Example**:
```
... existing conversation visible above ...

┌─────────────────────────────────────────┐
│  Execute: ls -la  [2/5]                │
│  y/N/a/q?                              │
└─────────────────────────────────────────┘
```

**Key Features**:
- Conversation remains visible (context preserved)
- Quick single-line prompts
- Less disruptive for operations like `ls`, `cat`
- Status area shows current tool index (e.g., "2/5")

---

### 10.2 Event Flow Architecture

```
ToolExecutor
    │
    ├─> check_permission()
    │       │
    │       └─> PermissionManager (check if auto-approved)
    │               │
    │               └─> (If not auto-approved)
    │                       │
    │                       └─> emit: PERMISSION_REQUEST
    │                               │
    │                               ▼
    │                       InputHandler._handle_permission_request()
    │                               │
    │                               └─> _approval_prompt_active = True
    │                                       │
    │                                       ├─> emit: MODAL_TRIGGER  (if modal)
    │                                       │       │
    │                                       │       └─> ModalController
    │                                       │               │
    │                                       │               └─> ModalRenderer
    │                                       │                       │
    │                                       │                       └─> SHOW OVERLAY
    │                                       │
    │                                       └─> OR emit: STATUS_TAKEOVER_START (if status)
    │                                               │
    │                                               └─> CommandModeHandler
    │                                                       │
    │                                                       └─> SHOW STATUS PROMPT
    │
    ├─> (User types: "y" + Enter)
    │
    ├─> KeyPressHandler.handle_keypress()
    │       │
    │       └─> _check: _approval_prompt_active?
    │               │
    │               └─> YES → _handle_approval_input()
    │                       │
    │                       └─> emit: PERMISSION_DECISION {user_input: "y"}
    │
    └─> InputHandler receives PERMISSION_DECISION
            │
            ├─> _approval_prompt_active = False
            │
            └─> emit: MODAL_HIDE  or  STATUS_TAKEOVER_END
                    │
                    └─> ToolExecutor receives decision
                            │
                            └─> Execute tool or skip
```

---

### 10.3 Modal vs Status Takeover Decision Matrix

| Operation Type | Recommended UI | Reason |
|---------------|-----------------|---------|
| `file_delete` | Modal Overlay | Destructive, needs confirmation |
| `file_create_overwrite` | Modal Overlay | Destructive, overwrites files |
| `file_edit` (protected path) | Modal Overlay | High-risk operation |
| `file_edit` (safe path) | Status Takeover | Quick approval, low risk |
| `terminal` (dangerous) | Modal Overlay | Destructive command |
| `terminal` (safe: ls, cat) | Status Takeover | Quick approval, informational |
| `mcp_tool` | Modal Overlay | Unknown behavior, risky |
| `file_read` | None | Auto-approved, no prompt |

---



---

## 11. Testing

### 11.1 Unit Tests

```python
# tests/unit/test_permission_manager.py

class TestPermissionManager:
    def test_safe_terminal_command_auto_approves(self):
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="terminal",
            tool_id="terminal_0",
            operation_data={"command": "ls -la"}
        ))
        assert result.approved
        assert result.auto_approved

    def test_dangerous_command_requires_approval(self):
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="terminal",
            tool_id="terminal_0",
            operation_data={"command": "rm -rf node_modules"}
        ))
        assert not result.approved

    def test_protected_path_never_auto_approves(self):
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="file_edit",
            tool_id="file_edit_0",
            operation_data={"file": "core/application.py"}
        ))
        assert not result.approved

    def test_safe_file_pattern_auto_approves(self):
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="file_edit",
            tool_id="file_edit_0",
            operation_data={"file": "docs/README.md"}
        ))
        assert result.approved
        assert result.auto_approved

    def test_yolo_mode_bypasses_all_checks(self):
        pm = PermissionManager(config={"yolo_mode": True})
        result = asyncio.run(pm.check_permission(
            tool_type="terminal",
            tool_id="terminal_0",
            operation_data={"command": "rm -rf /"}
        ))
        assert result.approved
        assert result.auto_approved

    def test_batch_approval_state(self):
        pm = PermissionManager()
        pm.set_approved_all(True)

        result = asyncio.run(pm.check_permission(
            tool_type="terminal",
            tool_id="terminal_0",
            operation_data={"command": "rm -rf node_modules"}
        ))
        assert result.approved
        assert result.auto_approved

    def test_delete_requires_double_confirm(self):
        pm = PermissionManager()
        request = pm._categorize_operation(
            tool_type="file_delete",
            operation_data={"file": "old_file.py"}
        )
        assert request == OperationCategory.FILE_DELETE

    def test_read_operation_always_safe(self):
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="file_read",
            tool_id="file_read_0",
            operation_data={"file": "any_file.py"}
        ))
        assert result.approved
        assert result.auto_approved
```

---

### 10.2 Integration Tests

```python
# tests/integration/test_permission_system.py

class TestPermissionSystemIntegration:
    async def test_terminal_command_approval_flow(self):
        # Create tool executor with permission manager
        executor = ToolExecutor(mcp_integration, event_bus, config)

        # Try to execute dangerous command
        tools = [
            {
                "type": "terminal",
                "id": "terminal_0",
                "command": "rm -rf node_modules"
            }
        ]

        # Mock user approval
        # ... setup mock for permission request ...

        results = await executor.execute_all_tools(tools)

        # Verify approval was requested
        # Verify execution only after approval

    async def test_file_operation_batch_approval(self):
        # Test batch approval workflow
        tools = [
            {"type": "file_edit", "id": "edit_0", "file": "test.py", "find": "old", "replace": "new"},
            {"type": "file_create", "id": "create_0", "file": "new.py", "content": "..."},
            {"type": "file_delete", "id": "delete_0", "file": "old.py"}
        ]

        # User approves all after first
        # ... setup mock user responses ...

        results = await executor.execute_all_tools(tools)

        # Verify all 3 executed
        assert len(results) == 3
        assert all(r.success for r in results)

    async def test_quit_during_batch(self):
        tools = [
            {"type": "file_edit", "id": "edit_0", "file": "test.py", "find": "old", "replace": "new"},
            {"type": "file_edit", "id": "edit_1", "file": "test.py", "find": "old", "replace": "new"},
            {"type": "file_edit", "id": "edit_2", "file": "test.py", "find": "old", "replace": "new"},
        ]

        # User quits after second operation
        # ... setup mock user responses ...

        results = await executor.execute_all_tools(tools)

        # Verify only first 2 executed
        assert len(results) == 2

    async def test_yolo_flag_bypass(self):
        # Start with --yolo flag
        args = parse_args(["--yolo"])

        # Verify permission manager has yolo_mode=True
        # Verify all operations execute without prompts
```

---

## 12. Error Recovery and Edge Cases

### 12.1 Timeout Handling

Timeouts are enforced using `asyncio.wait_for()`:

```python
# In ToolExecutor._request_user_approval():
try:
    decision = await asyncio.wait_for(
        approval_future,
        timeout=self.permission_manager.approval_timeout
    )
    return decision
except asyncio.TimeoutError:
    logger.warning(f"Approval timed out for tool {tool_id}")
    return ApprovalDecision.TIMEOUT
```

**Timeout Behavior:**
- Default: 30 seconds (configurable via `permissions.approval_timeout`)
- On timeout: Tool is skipped (safe default)
- User can press `q` to quit immediately

### 12.2 Modal Crash Recovery

If the modal system crashes during approval:

```python
# In ToolExecutor, wrap approval request:
try:
    decision = await self._request_user_approval(...)
except Exception as e:
    logger.error(f"Approval request failed: {e}")
    return ApprovalDecision.DENY  # Safe default
```

**Recovery Steps:**
1. Catch exception in `_request_user_approval()`
2. Log error with full traceback
3. Return `ApprovalDecision.DENY` (safe default)
4. Continue to next tool in batch

### 12.3 Event Bus Failure

If event bus fails to emit events:

```python
# In ToolExecutor._request_user_approval():
try:
    await self.event_bus.emit_with_hooks(...)
except Exception as e:
    logger.error(f"Failed to emit PERMISSION_REQUEST: {e}")
    return ApprovalDecision.DENY
```

**Fallback Behavior:**
- If event emission fails, tool is denied
- No user prompt is shown
- Error is logged for debugging

### 12.4 User Input Validation

Invalid user responses are handled:

```python
# In KeyPressHandler._handle_approval_keypress():
# Only valid keys: y, N, a, q, Enter
# All other keys are ignored during approval mode

# Mapping ensures only valid decisions:
key_mapping = {
    'y': ApprovalDecision.APPROVE,
    'N': ApprovalDecision.DENY,
    'a': ApprovalDecision.APPROVE_ALL,
    'q': ApprovalDecision.QUIT,
}

# Invalid keys return None, decision is not routed
```

### 12.5 Future Completion Errors

If Future is already done when setting result:

```python
# In InputHandler._route_permission_response():
if future and not future.done():
    future.set_result(decision)
else:
    logger.warning("Attempted to set result on already-done Future")
```

### 12.6 Cleanup on Quit

When user quits during batch:

```python
# In ToolExecutor.execute_all_tools():
elif user_decision == ApprovalDecision.QUIT:
    # Stop all remaining operations
    logger.info(f"User quit at tool {i+1}/{len(tools)}")
    self.permission_manager.stats["quit_requested"] += 1
    break

# Clean up pending future
self.permission_manager._pending_approval = None
```

---

## 13. Testing Strategy

### 13.1 Unit Tests

File: `tests/unit/test_permission_manager.py`

```python
"""Unit tests for PermissionManager."""

import pytest
import asyncio
from core.llm.permission_manager import (
    PermissionManager,
    ApprovalDecision,
    OperationCategory
)


class TestPermissionManager:
    """Test permission manager functionality."""

    def test_init_default_config(self):
        """Test default initialization."""
        pm = PermissionManager()
        assert pm.enabled is True
        assert pm.yolo_mode is False
        assert pm.approval_timeout == 30

    def test_safe_terminal_command_auto_approves(self):
        """Test safe commands auto-approve."""
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="terminal",
            tool_id="terminal_0",
            operation_data={"command": "ls -la"}
        ))
        assert result.approved is True
        assert result.auto_approved is True

    def test_dangerous_command_requires_approval(self):
        """Test dangerous commands require approval."""
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="terminal",
            tool_id="terminal_0",
            operation_data={"command": "rm -rf node_modules"}
        ))
        assert result.approved is False
        assert result.auto_approved is False

    def test_protected_path_never_auto_approves(self):
        """Test protected paths require approval."""
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="file_edit",
            tool_id="file_edit_0",
            operation_data={"file": "core/application.py"}
        ))
        assert result.approved is False
        assert result.auto_approved is False

    def test_safe_file_pattern_auto_approves(self):
        """Test safe patterns auto-approve."""
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="file_edit",
            tool_id="file_edit_0",
            operation_data={"file": "docs/README.md"}
        ))
        assert result.approved is True
        assert result.auto_approved is True

    def test_yolo_mode_bypasses_all_checks(self):
        """Test YOLO mode bypasses all checks."""
        pm = PermissionManager(config={"permissions": {"yolo_mode": True}})
        result = asyncio.run(pm.check_permission(
            tool_type="terminal",
            tool_id="terminal_0",
            operation_data={"command": "rm -rf /"}
        ))
        assert result.approved is True
        assert result.auto_approved is True

    def test_batch_approval_state(self):
        """Test approve-all state."""
        pm = PermissionManager()
        pm.set_approved_all(True)

        result = asyncio.run(pm.check_permission(
            tool_type="terminal",
            tool_id="terminal_0",
            operation_data={"command": "rm -rf node_modules"}
        ))
        assert result.approved is True
        assert result.auto_approved is True

    def test_delete_requires_double_confirm(self):
        """Test delete categorization."""
        pm = PermissionManager()
        category = pm._categorize_operation(
            tool_type="file_delete",
            operation_data={"file": "old_file.py"}
        )
        assert category == OperationCategory.FILE_DELETE

    def test_read_operation_always_safe(self):
        """Test read operations are always safe."""
        pm = PermissionManager()
        result = asyncio.run(pm.check_permission(
            tool_type="file_read",
            tool_id="file_read_0",
            operation_data={"file": "any_file.py"}
        ))
        assert result.approved is True
        assert result.auto_approved is True

    def test_stats_tracking(self):
        """Test statistics are tracked."""
        pm = PermissionManager()
        pm.get_stats()["total_requests"]  # Access stats
        assert "total_requests" in pm.stats
        assert "approved" in pm.stats

    def test_reset_batch(self):
        """Test batch state reset."""
        pm = PermissionManager()
        pm.set_approved_all(True)
        pm.reset_batch()
        # Check internal state (would need to expose for test)
        # For now, just verify method doesn't crash
```

### 13.2 Integration Tests

File: `tests/integration/test_permission_system.py`

```python
"""Integration tests for permission system."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from core.llm.tool_executor import ToolExecutor
from core.llm.permission_manager import ApprovalDecision


class TestPermissionSystemIntegration:
    """Test permission system integration with tool execution."""

    @pytest.fixture
    async def setup_executor(self):
        """Setup tool executor with mocks."""
        mcp_integration = Mock()
        event_bus = Mock()
        event_bus.emit_with_hooks = AsyncMock(return_value={})

        config = {"permissions": {"enabled": True}}
        executor = ToolExecutor(mcp_integration, event_bus, config=config)

        return executor

    async def test_approval_future_creation(self, setup_executor):
        """Test approval future is created correctly."""
        executor = setup_executor
        pm = executor.permission_manager

        # Mock event bus emit
        with patch.object(executor.event_bus, 'emit_with_hooks', new_callable=AsyncMock()):
            try:
                # This should create a future
                await executor._request_user_approval(
                    tool_data={"type": "terminal", "id": "test"},
                    permission_result=Mock(approved=False),
                    index=1,
                    total=1
                )
            except asyncio.TimeoutError:
                # Expected - we didn't set the future result
                pass

        # Verify future was created and stored
        assert pm._pending_approval is not None
        assert isinstance(pm._pending_approval, asyncio.Future)

    async def test_approval_timeout(self, setup_executor):
        """Test approval times out correctly."""
        executor = setup_executor
        pm = executor.permission_manager

        with patch.object(executor.event_bus, 'emit_with_hooks', new_callable=AsyncMock()):
            decision = await executor._request_user_approval(
                tool_data={"type": "terminal", "id": "test"},
                permission_result=Mock(approved=False),
                index=1,
                total=1
            )

        # Should timeout since we didn't respond
        assert decision == ApprovalDecision.TIMEOUT

    async def test_manual_approval_response(self, setup_executor):
        """Test manual approval response works."""
        executor = setup_executor
        pm = executor.permission_manager

        async def mock_emit(*args, **kwargs):
            # Simulate user approving by setting future result
            if pm._pending_approval and not pm._pending_approval.done():
                pm._pending_approval.set_result(ApprovalDecision.APPROVE)

        with patch.object(executor.event_bus, 'emit_with_hooks', new_callable=mock_emit):
            decision = await executor._request_user_approval(
                tool_data={"type": "terminal", "id": "test"},
                permission_result=Mock(approved=False),
                index=1,
                total=1
            )

        assert decision == ApprovalDecision.APPROVE

    async def test_approve_all_sets_flag(self, setup_executor):
        """Test approve-all sets batch flag."""
        executor = setup_executor
        pm = executor.permission_manager

        async def mock_emit(*args, **kwargs):
            if pm._pending_approval and not pm._pending_approval.done():
                pm._pending_approval.set_result(ApprovalDecision.APPROVE_ALL)

        with patch.object(executor.event_bus, 'emit_with_hooks', new_callable=mock_emit):
            await executor._request_user_approval(
                tool_data={"type": "terminal", "id": "test"},
                permission_result=Mock(approved=False),
                index=1,
                total=3
            )

        # Verify flag was set
        # Note: This would require exposing internal state
        # For now, test that method doesn't crash
```

### 13.3 Mock User Input for Tests

To test approval flow without actual user input, use mocks:

```python
# Helper function for tests
async def simulate_user_approval(executor, decision: ApprovalDecision):
    """Simulate user approving a request.

    Args:
        executor: ToolExecutor instance
        decision: Decision to simulate
    """
    pm = executor.permission_manager

    async def mock_emit(*args, **kwargs):
        # Wait a tiny bit to simulate user thinking
        await asyncio.sleep(0.01)
        if pm._pending_approval and not pm._pending_approval.done():
            pm._pending_approval.set_result(decision)

    with patch.object(executor.event_bus, 'emit_with_hooks', new_callable=mock_emit):
        return await executor._request_user_approval(
            tool_data={"type": "terminal", "id": "test"},
            permission_result=Mock(approved=False),
            index=1,
            total=1
        )
```

**Usage in tests:**
```python
async def test_user_approves(self, setup_executor):
    """Test user approves operation."""
    executor = setup_executor
    decision = await simulate_user_approval(executor, ApprovalDecision.APPROVE)
    assert decision == ApprovalDecision.APPROVE

async def test_user_denies(self, setup_executor):
    """Test user denies operation."""
    executor = setup_executor
    decision = await simulate_user_approval(executor, ApprovalDecision.DENY)
    assert decision == ApprovalDecision.DENY
```

---

## 14. Implementation Checklist

### Phase 1: Core Infrastructure
- [ ] Create `core/llm/permission_manager.py`
- [ ] Implement `PermissionManager` class
- [ ] Implement operation categorization
- [ ] Implement safe/protected path detection
- [ ] Implement permission check logic
- [ ] Add `_pending_approval` Future storage attribute
- [ ] Add unit tests for `PermissionManager`

### Phase 2: Tool Executor Integration
- [ ] Modify `ToolExecutor.__init__()` to create `PermissionManager`
- [ ] Add permission gate to `execute_tool()`
- [ ] Modify `execute_all_tools()` for interactive approval
- [ ] Implement `_request_user_approval()` with Future-based async wait
- [ ] Implement `asyncio.wait_for()` timeout handling
- [ ] Add permission stats tracking
- [ ] Add integration tests

### Phase 3: Command-Line Flag
- [ ] Add `--yolo` argument to `argparse` in `core/cli.py`
- [ ] Pass `--yolo` flag to `Application.__init__()`
- [ ] Set `permissions.yolo_mode` in config when flag present
- [ ] Test yolo mode functionality

### Phase 4: Configuration Integration
- [ ] Add permissions section to `get_base_config()` in `core/config/loader.py`
- [ ] Implement config loading in `PermissionManager._load_config()`
- [ ] Add validation for permission settings
- [ ] Test config-based approval rules

### Phase 5: Event System
- [ ] Add permission event types to `EventType` enum in `core/events/models.py`
  - PERMISSION_REQUEST
  - PERMISSION_GRANTED
  - PERMISSION_DENIED
  - PERMISSION_TIMEOUT
  - PERMISSION_APPROVE_ALL
  - PERMISSION_QUIT
- [ ] Emit permission request events from ToolExecutor
- [ ] Emit permission decision events from InputHandler
- [ ] Test plugin hooks for permission events

### Phase 6: Input Handler Integration
- [ ] Add permission state attributes to `InputHandler`
  - `_approval_mode_active`
  - `_approval_future_id`
  - `_permission_manager` reference
- [ ] Implement `_handle_permission_request()` hook method
- [ ] Implement `_determine_approval_ui_type()` method
- [ ] Implement `_show_approval_modal()` for destructive operations
- [ ] Implement `_show_approval_status_takeover()` for quick approvals
- [ ] Implement `_route_permission_response()` method
- [ ] Implement double-confirmation logic for deletes
  - `_double_confirm_active` flag
  - Two-stage prompt flow
- [ ] Add approval mode to `KeyPressHandler`
- [ ] Implement `_handle_approval_keypress()` method
- [ ] Map y/N/a/q keys to ApprovalDecision
- [ ] Register permission request hook in `HookRegistrar`
- [ ] Test user interaction flow (both modal and status takeover)
- [ ] Test approval decision routing back to PermissionManager
- [ ] Test timeout scenarios

### Phase 7: Application Integration
- [ ] Pass `permission_manager` to `InputHandler.__init__()`
- [ ] Pass `yolo_mode` to `Application.__init__()`
- [ ] Update config with yolo_mode flag when set
- [ ] Verify reference chain: Application -> ToolExecutor -> PermissionManager
- [ ] Verify reference chain: Application -> InputHandler -> PermissionManager

### Phase 8: Documentation
- [ ] Update system prompt with permission info
- [ ] Add user documentation for --yolo flag
- [ ] Document configuration options
- [ ] Create troubleshooting guide
- [ ] Add sequence diagrams to spec

### Phase 9: Testing
- [ ] Unit tests for PermissionManager
  - Safe command auto-approval
  - Dangerous command requires approval
  - Protected path never auto-approves
  - YOLO mode bypass
  - Batch approval state
  - Stats tracking
- [ ] Integration tests for approval flow
  - Approval Future creation and resolution
  - Timeout handling
  - Manual approval response
  - Approve-all flag
  - Quit behavior
- [ ] Edge case tests
  - Protected paths
  - Dangerous commands
  - Double-confirmation for deletes
- [ ] Security tests
  - YOLO bypass
  - Protected files
  - Config override attempts
- [ ] Mock user input scenarios in tests

---

## 15. Migration Notes

### 15.1 Backwards Compatibility

No breaking changes - permissions are opt-in via config.

**Default Behavior:**
- `permissions.enabled: true` (safe by default)
- Existing tools continue to work (with approval prompts)
- Users can disable via config or use --yolo

**Migration Path:**
1. Update to new version
2. Permissions enabled by default
3. Users see approval prompts for first time
4. Can disable in config if desired
5. Or use --yolo for development

### 15.2 Rollback Plan

If issues arise:
1. Set `permissions.enabled: false` in config
2. Use --yolo flag temporarily
3. Revert to previous version
4. Check logs for permission-related errors

---

## 16. Summary of Fixes Applied

### 16.1 Async Flow
- [x] Added `asyncio.Future` based approval mechanism
- [x] Implemented `asyncio.wait_for()` timeout handling
- [x] Defined Future storage in `PermissionManager._pending_approval`
- [x] Implemented `_route_permission_response()` to set Future result
- [x] Added complete async communication architecture section

### 16.2 Event System
- [x] Added 6 permission event types to EventType enum
- [x] Defined event data structures for all permission events
- [x] Specified event emission points in ToolExecutor and InputHandler
- [x] Added event integration details to spec

### 16.3 Input Handler Integration
- [x] Defined permission state attributes
- [x] Implemented `_handle_permission_request()` hook method
- [x] Implemented UI type determination logic
- [x] Implemented modal and status takeover display methods
- [x] Implemented approval response routing
- [x] Added double-confirmation flow for deletes
- [x] Integrated with KeyPressHandler for key handling
- [x] Defined reference chain between components

### 16.4 Configuration
- [x] Added --yolo flag to CLI argument parser
- [x] Added permissions section to get_base_config()
- [x] Documented config schema with all options
- [x] Added Application initialization with yolo_mode parameter

### 16.5 Error Handling
- [x] Added timeout handling section
- [x] Added modal crash recovery
- [x] Added event bus failure handling
- [x] Added user input validation
- [x] Added Future completion error handling
- [x] Added cleanup on quit

### 16.6 Testing
- [x] Added comprehensive unit test strategy
- [x] Added integration test scenarios
- [x] Added mock user input helper
- [x] Defined test coverage goals

---

**END OF SPEC - READY FOR IMPLEMENTATION (UPDATED)**

### Phase 1: Core Infrastructure
- [ ] Create `core/llm/permission_manager.py`
- [ ] Implement `PermissionManager` class
- [ ] Implement operation categorization
- [ ] Implement safe/protected path detection
- [ ] Implement permission check logic
- [ ] Add unit tests for `PermissionManager`

### Phase 2: Tool Executor Integration
- [ ] Modify `ToolExecutor.__init__()` to create `PermissionManager`
- [ ] Add permission gate to `execute_tool()`
- [ ] Modify `execute_all_tools()` for interactive approval
- [ ] Implement `_request_user_approval()` method
- [ ] Add permission stats tracking
- [ ] Add integration tests

### Phase 3: Command-Line Flag
- [ ] Add `--yolo` argument to `argparse`
- [ ] Pass `--yolo` flag to application
- [ ] Test yolo mode functionality

### Phase 4: Configuration Integration
- [ ] Add permissions section to `get_base_config()`
- [ ] Implement config loading in `PermissionManager`
- [ ] Add validation for permission settings
- [ ] Test config-based approval rules

### Phase 6: Input Handler Integration
- [ ] Implement permission prompt display (modal overlay + status takeover)
- [ ] Handle user input (y/N/a/q/v) via key press handler
- [ ] Implement double-confirmation for deletes
- [ ] Implement timeout handling with async futures
- [ ] Add approval mode to InputHandler and KeyPressHandler
- [ ] Integrate with ModalController for modal overlays
- [ ] Test user interaction flow (both modal and status takeover)

### Phase 7: Event System
- [ ] Add permission event types to `EventType` enum
- [ ] Emit permission request events
- [ ] Emit permission decision events
- [ ] Test plugin hooks for permission events

### Phase 8: Documentation
- [ ] Update system prompt with permission info
- [ ] Add user documentation for --yolo flag
- [ ] Document configuration options
- [ ] Create troubleshooting guide

### Phase 8: Testing
- [ ] Unit tests for all components
- [ ] Integration tests for approval flow
- [ ] Edge case tests (protected paths, dangerous commands)
- [ ] Security tests (yolo bypass, protected files)
- [ ] Performance tests (batch operations)

---

## 12. Migration

### From Current System

1. No breaking changes - permissions are opt-in via config
2. Default: `enabled: true` (safe by default)
3. Existing tools continue to work (with approval prompts)
4. Users can disable via config or use --yolo

### Rollback Plan

If issues arise:
1. Set `permissions.enabled: false` in config
2. Use --yolo flag temporarily
3. Revert to previous version

---

## 13. Future Enhancements

### Potential Features

1. **Whitelist Mode**: Only allow explicitly approved operations
2. **Blacklist Mode**: Allow all except explicitly denied
3. **Time-based Approval**: Approve operations for N minutes
4. **Persistent Approvals**: Remember user decisions across sessions
5. **Plugin-defined Rules**: Plugins can add custom approval rules
6. **Approval History**: View past approval decisions
7. **Dry Run Mode**: Show what would happen without executing
8. **Multi-user Support**: Different approval rules per user

---

## 14. Questions Requiring Decisions

### DECISION 1: Default Enabled State

Should permissions be enabled by default?

**Option A**: Yes (`enabled: true`) - Safe by default, requires explicit disable
**Option B**: No (`enabled: false`) - Current behavior, opt-in safety

**Recommendation**: Option A (safe by default)

---

### DECISION 2: Approval Timeout

What should default approval timeout be?

**Option A**: 30 seconds
**Option B**: 60 seconds
**Option C**: No timeout (wait indefinitely)

**Recommendation**: Option A (30 seconds - balance of safety and usability)

---

### DECISION 3: Batch Approval Behavior

Should "approve all" apply to delete operations?

**Option A**: Yes - User explicitly said "all"
**Option B**: No - Still require confirmation for deletes

**Recommendation**: Option B (safer - deletes always require confirmation)

---

### DECISION 4: MCP Tool Handling

How to handle MCP tools (third-party, unknown behavior)?

**Option A**: Always require approval (most conservative)
**Option B**: Allow whitelist of trusted MCP servers
**Option C**: Auto-approve read-only MCP tools

**Recommendation**: Option A (always approve - MCP tools are black box)

---

### DECISION 5: Permission Persistence

Should user approval decisions be remembered?

**Option A**: Yes - Remember decisions per session
**Option B**: Yes - Remember decisions persistently across sessions
**Option C**: No - Always ask (most secure)

**Recommendation**: Option A (session-only persistence - balance of security and UX)

---

## 15. Estimated Implementation

**Total Complexity**: Medium-High
**Estimated Time**: 12-16 hours
**Files Created**: 1
**Files Modified**: 5
**Risk Level**: Medium (new feature, integrates deeply with tool execution)

**Breakdown**:
- Phase 1 (Core Infrastructure): 4 hours
- Phase 2 (Tool Executor Integration): 3 hours
- Phase 3 (Command-Line Flag): 1 hour
- Phase 4 (Configuration Integration): 2 hours
- Phase 5 (Event System): 1 hour
- Phase 6 (Input Handler Integration): 3 hours
- Phase 7 (Documentation): 1 hour
- Phase 8 (Testing): 3 hours

---

**END OF SPEC - READY FOR IMPLEMENTATION**
