---
title: Unified Logging Configuration System Specification
description: Granular configuration for conversation logging, raw API logging, and conversation management
category: spec
created: 2026-01-10
status: draft
---

# Unified Logging Configuration System Specification

**Version**: 1.0
**Status**: Draft - Ready for Review
**Created**: 2026-01-10
**Updated**: 2026-01-10

---

## 1. Overview

Comprehensive, granular configuration system for all conversation logging subsystems in Kollabor CLI.

### Current Problem

Three separate logging systems operate with hard-coded values and inconsistent configuration:

1. **KollaborConversationLogger** (JSONL): Rich structured logging with intelligence
   - Always enabled (no disable option)
   - One file per session: `.kollabor-cli/conversations/YYMMDDHHMM-name.jsonl`
   - No configuration beyond directory location

2. **Raw API Logger** (JSONL): Raw request/response logging
   - Always enabled (no disable option)
   - Multiple files per session: `.kollabor-cli/conversations_raw/YYMMDDHHMM-name_raw_HHMMSS.jsonl`
   - Creates new file for every API call (not configurable)

3. **ConversationManager** (JSON): Conversation snapshots
   - Boolean enable/disable only: `core.llm.save_conversations`
   - Hard-coded auto-save interval: every 10 messages (line 119-120)
   - One file per save: `.kollabor-cli/conversations/conversation_26011015_YYYYMMDD_HHMMSS.json`

**Issues:**
- Cannot disable expensive logging in production
- Cannot tune performance vs completeness tradeoffs
- Hard-coded values require code changes
- No privacy controls (API keys, sensitive data logged)
- No retention policies (unbounded disk usage)
- No compression or rotation
- Inconsistent configuration patterns

### Proposed Solution

Unified, hierarchical configuration system with:
- Independent enable/disable per subsystem
- Granular control over content, performance, and file management
- Privacy and security controls
- Retention and cleanup policies
- Environment variable overrides
- Backward compatibility with existing configs

### Key Features

1. **Hierarchical Configuration**: Global → per-logger → per-feature
2. **Privacy Controls**: Redaction, anonymization, encryption
3. **Performance Tuning**: Async writes, batching, buffering
4. **File Management**: Rotation, compression, retention
5. **Content Filtering**: Selective message types, size limits
6. **Debugging**: Performance metrics, tracing, verbose errors
7. **Environment Overrides**: Runtime configuration via env vars
8. **Backward Compatibility**: Existing configs continue to work

---

## 2. Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                   Logging Configuration System                   │
│                                                                  │
│  config.get("core.llm.logging.*")                               │
│  Environment variables: KOLLABOR_LOG_*                          │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                 [Load Configuration Hierarchy]
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Conversation    │  │ Raw API         │  │ Conversation    │
│ Logger Config   │  │ Logger Config   │  │ Manager Config  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ - enabled       │  │ - enabled       │  │ - enabled       │
│ - output_dir    │  │ - output_dir    │  │ - output_dir    │
│ - content       │  │ - content       │  │ - auto_save     │
│ - performance   │  │ - file_strategy │  │ - triggers      │
│ - rotation      │  │ - performance   │  │ - content       │
│ - intelligence  │  │ - filtering     │  │ - versioning    │
│ - metadata      │  │ - privacy       │  │ - compression   │
└─────────────────┘  └─────────────────┘  └─────────────────┘
          │                   │                   │
          └───────────────────┴───────────────────┘
                              │
                              ▼
                    [Apply Global Settings]
                              │
                              ▼
                    ┌───────────────────┐
                    │ - privacy         │
                    │ - retention       │
                    │ - compression     │
                    │ - debugging       │
                    │ - advanced        │
                    └───────────────────┘
```

---

## 3. Configuration Schema

### 3.1 Global Settings

```json
{
  "core": {
    "llm": {
      "logging": {
        "global": {
          "enabled": true,
          "base_dir": ".kollabor-cli",
          "async_logging": true,
          "buffer_size": 1000,
          "flush_interval": 5.0,
          "compression": "none",
          "compression_level": 6,
          "file_permissions": "0600",

          "privacy": {
            "redact_api_keys": true,
            "redact_tokens": true,
            "redact_patterns": ["password", "secret", "api_key"],
            "anonymize_paths": false,
            "hash_user_content": false
          },

          "retention": {
            "max_age_days": 30,
            "max_total_size_mb": 500,
            "cleanup_schedule": "daily",
            "cleanup_time": "03:00"
          }
        }
      }
    }
  }
}
```

**Global Settings Reference:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | `true` | Master switch for all logging |
| `base_dir` | string | `.kollabor-cli` | Base directory for all log files |
| `async_logging` | boolean | `true` | Use async I/O for logging |
| `buffer_size` | integer | `1000` | Number of log entries to buffer |
| `flush_interval` | float | `5.0` | Seconds between buffer flushes |
| `compression` | string | `"none"` | Compression algorithm: `none`, `gzip`, `bz2`, `lzma` |
| `compression_level` | integer | `6` | Compression level (1-9) |
| `file_permissions` | string | `"0600"` | Unix file permissions for log files |

**Privacy Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `redact_api_keys` | boolean | `true` | Replace API keys with `[REDACTED]` |
| `redact_tokens` | boolean | `true` | Replace auth tokens with `[REDACTED]` |
| `redact_patterns` | array | `["password", "secret", "api_key"]` | Regex patterns to redact |
| `anonymize_paths` | boolean | `false` | Replace absolute paths with relative |
| `hash_user_content` | boolean | `false` | SHA256 hash user messages |

**Retention Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `max_age_days` | integer | `30` | Delete logs older than N days (0=unlimited) |
| `max_total_size_mb` | integer | `500` | Delete oldest logs if total exceeds N MB (0=unlimited) |
| `cleanup_schedule` | string | `"daily"` | Cleanup frequency: `never`, `startup`, `hourly`, `daily`, `weekly` |
| `cleanup_time` | string | `"03:00"` | Time for daily cleanup (HH:MM) |

---

### 3.2 Conversation Logger Settings

```json
{
  "core": {
    "llm": {
      "logging": {
        "conversation_logger": {
          "enabled": true,
          "output_dir": "conversations",
          "format": "jsonl",

          "content": {
            "include_intelligence": true,
            "include_user_patterns": true,
            "include_project_context": true,
            "include_session_context": true,
            "log_system_messages": true,
            "log_tool_calls": true,
            "log_thinking_tags": false,
            "max_content_length": 0,
            "truncate_long_messages": false
          },

          "performance": {
            "async_writes": true,
            "batch_size": 10,
            "batch_timeout": 2.0,
            "queue_max_size": 1000
          },

          "rotation": {
            "enabled": false,
            "max_size_mb": 10,
            "max_files": 5,
            "rotate_on_startup": false
          },

          "intelligence": {
            "analyze_user_context": true,
            "analyze_assistant_response": true,
            "detect_intent": true,
            "track_file_mentions": true,
            "track_technologies": true,
            "learn_patterns": true,
            "pattern_deduplication": true
          },

          "metadata": {
            "include_git_branch": true,
            "include_cwd": true,
            "include_timestamps": true,
            "include_session_id": true,
            "include_parent_uuid": true,
            "custom_fields": {}
          }
        }
      }
    }
  }
}
```

**Conversation Logger Reference:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable conversation logger |
| `output_dir` | string | `"conversations"` | Directory relative to `base_dir` |
| `format` | string | `"jsonl"` | File format: `jsonl`, `json` |

**Content Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `include_intelligence` | boolean | `true` | Include Kollabor intelligence features |
| `include_user_patterns` | boolean | `true` | Include learned user patterns |
| `include_project_context` | boolean | `true` | Include project awareness data |
| `include_session_context` | boolean | `true` | Include session phase/themes |
| `log_system_messages` | boolean | `true` | Log system messages |
| `log_tool_calls` | boolean | `true` | Log tool execution |
| `log_thinking_tags` | boolean | `false` | Include thinking tag content |
| `max_content_length` | integer | `0` | Truncate content longer than N chars (0=unlimited) |
| `truncate_long_messages` | boolean | `false` | Truncate instead of error on large messages |

**Performance Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `async_writes` | boolean | `true` | Use async file writes |
| `batch_size` | integer | `10` | Number of entries per batch write |
| `batch_timeout` | float | `2.0` | Max seconds to wait for batch |
| `queue_max_size` | integer | `1000` | Max queue size before blocking |

**Intelligence Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `analyze_user_context` | boolean | `true` | Analyze user message patterns |
| `analyze_assistant_response` | boolean | `true` | Analyze assistant solutions |
| `detect_intent` | boolean | `true` | Detect user intent (debugging, feature dev, etc.) |
| `track_file_mentions` | boolean | `true` | Track file paths mentioned in conversation |
| `track_technologies` | boolean | `true` | Track technologies mentioned |
| `learn_patterns` | boolean | `true` | Learn from user communication patterns |
| `pattern_deduplication` | boolean | `true` | Deduplicate learned patterns |

---

### 3.3 Raw API Logger Settings

```json
{
  "core": {
    "llm": {
      "logging": {
        "raw_api_logger": {
          "enabled": true,
          "output_dir": "conversations_raw",
          "format": "jsonl",

          "content": {
            "log_request_payload": true,
            "log_response_payload": true,
            "log_response_headers": false,
            "log_request_headers": false,
            "log_errors": true,
            "log_cancelled_requests": true,
            "log_token_usage": true,
            "log_timing": true,
            "max_payload_size": 0,
            "truncate_large_payloads": false
          },

          "file_strategy": {
            "one_file_per_request": true,
            "one_file_per_session": false,
            "one_file_per_day": false,
            "append_to_single_file": false
          },

          "performance": {
            "async_writes": true,
            "buffer_writes": false,
            "immediate_flush": false
          },

          "rotation": {
            "enabled": false,
            "max_size_mb": 5,
            "max_files_per_session": 100
          },

          "filtering": {
            "log_streaming_chunks": false,
            "log_duplicate_requests": true,
            "exclude_models": [],
            "include_models": [],
            "min_response_time_ms": 0
          },

          "privacy": {
            "redact_messages": false,
            "hash_content": false,
            "strip_system_prompts": false
          }
        }
      }
    }
  }
}
```

**Raw API Logger Reference:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable raw API logger |
| `output_dir` | string | `"conversations_raw"` | Directory relative to `base_dir` |
| `format` | string | `"jsonl"` | File format: `jsonl`, `json` |

**Content Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `log_request_payload` | boolean | `true` | Log request payload to API |
| `log_response_payload` | boolean | `true` | Log response payload from API |
| `log_response_headers` | boolean | `false` | Log HTTP response headers |
| `log_request_headers` | boolean | `false` | Log HTTP request headers |
| `log_errors` | boolean | `true` | Log error responses |
| `log_cancelled_requests` | boolean | `true` | Log cancelled requests |
| `log_token_usage` | boolean | `true` | Log token usage stats |
| `log_timing` | boolean | `true` | Log request/response timing |
| `max_payload_size` | integer | `0` | Max payload size to log (0=unlimited) |
| `truncate_large_payloads` | boolean | `false` | Truncate vs skip large payloads |

**File Strategy Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `one_file_per_request` | boolean | `true` | Create new file for each API call |
| `one_file_per_session` | boolean | `false` | One file per conversation session |
| `one_file_per_day` | boolean | `false` | One file per day (rotated) |
| `append_to_single_file` | boolean | `false` | Single file for all requests |

**Filtering Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `log_streaming_chunks` | boolean | `false` | Log streaming response chunks |
| `log_duplicate_requests` | boolean | `true` | Log duplicate/retry requests |
| `exclude_models` | array | `[]` | Don't log requests to these models |
| `include_models` | array | `[]` | Only log requests to these models (empty=all) |
| `min_response_time_ms` | integer | `0` | Only log requests slower than N ms |

---

### 3.4 Conversation Manager Settings

```json
{
  "core": {
    "llm": {
      "logging": {
        "conversation_manager": {
          "enabled": true,
          "output_dir": "conversations",
          "format": "json",

          "auto_save": {
            "enabled": true,
            "interval": 10,
            "interval_type": "messages",
            "time_interval_seconds": 0,
            "save_on_user_message": false,
            "save_on_assistant_message": false,
            "save_on_error": true,
            "debounce_delay": 0
          },

          "triggers": {
            "save_on_clear": true,
            "save_on_shutdown": true,
            "save_on_context_switch": true,
            "save_on_branch_change": false
          },

          "content": {
            "include_metadata": true,
            "include_summary": true,
            "include_all_messages": true,
            "include_system_prompt": false,
            "max_messages": 0,
            "include_timestamps": true
          },

          "performance": {
            "async_writes": true,
            "pretty_print": true,
            "indent": 2,
            "ensure_ascii": false,
            "validate_json": true
          },

          "versioning": {
            "enabled": false,
            "keep_versions": 5,
            "version_on_save": false,
            "diff_tracking": false
          },

          "compression": {
            "enabled": false,
            "algorithm": "gzip",
            "level": 6,
            "compress_after_save": false
          }
        }
      }
    }
  }
}
```

**Conversation Manager Reference:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable conversation manager snapshots |
| `output_dir` | string | `"conversations"` | Directory relative to `base_dir` |
| `format` | string | `"json"` | File format: `json`, `jsonl` |

**Auto-Save Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable auto-save |
| `interval` | integer | `10` | Save every N messages/seconds |
| `interval_type` | string | `"messages"` | Interval type: `messages`, `time`, `both` |
| `time_interval_seconds` | integer | `0` | Save every N seconds (if interval_type includes time) |
| `save_on_user_message` | boolean | `false` | Save after every user message |
| `save_on_assistant_message` | boolean | `false` | Save after every assistant message |
| `save_on_error` | boolean | `true` | Save when error occurs |
| `debounce_delay` | float | `0` | Delay before save (avoid rapid saves) |

**Trigger Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `save_on_clear` | boolean | `true` | Save when conversation cleared |
| `save_on_shutdown` | boolean | `true` | Save on application shutdown |
| `save_on_context_switch` | boolean | `true` | Save when switching contexts |
| `save_on_branch_change` | boolean | `false` | Save when git branch changes |

**Content Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `include_metadata` | boolean | `true` | Include conversation metadata |
| `include_summary` | boolean | `true` | Include conversation summary |
| `include_all_messages` | boolean | `true` | Include all messages |
| `include_system_prompt` | boolean | `false` | Include system prompt in snapshot |
| `max_messages` | integer | `0` | Max messages to include (0=all) |
| `include_timestamps` | boolean | `true` | Include message timestamps |

**Versioning Settings:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable versioning |
| `keep_versions` | integer | `5` | Number of versions to keep |
| `version_on_save` | boolean | `false` | Create version on every save |
| `diff_tracking` | boolean | `false` | Track diffs between versions |

---

### 3.5 Export Settings

```json
{
  "core": {
    "llm": {
      "logging": {
        "export": {
          "default_format": "transcript",
          "available_formats": ["transcript", "markdown", "jsonl", "raw", "html", "pdf"],
          "auto_export": false,
          "export_on_shutdown": false,
          "export_formats": [],
          "output_dir": "exports"
        }
      }
    }
  }
}
```

---

### 3.6 Debugging Settings

```json
{
  "core": {
    "llm": {
      "logging": {
        "debugging": {
          "log_performance_metrics": false,
          "log_memory_usage": false,
          "log_file_operations": false,
          "trace_message_flow": false,
          "sample_rate": 1.0,
          "verbose_errors": true
        }
      }
    }
  }
}
```

**Debugging Reference:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `log_performance_metrics` | boolean | `false` | Log timing, throughput metrics |
| `log_memory_usage` | boolean | `false` | Log memory consumption |
| `log_file_operations` | boolean | `false` | Log all file I/O operations |
| `trace_message_flow` | boolean | `false` | Trace message flow through system |
| `sample_rate` | float | `1.0` | Fraction of events to log (0.0-1.0) |
| `verbose_errors` | boolean | `true` | Include stack traces in errors |

---

### 3.7 Advanced Settings

```json
{
  "core": {
    "llm": {
      "logging": {
        "advanced": {
          "use_memory_buffer": false,
          "memory_buffer_size_mb": 10,
          "sync_to_disk_interval": 10.0,
          "use_write_ahead_log": false,
          "enable_crash_recovery": false,
          "lock_files": false,
          "fsync_on_write": false
        }
      }
    }
  }
}
```

**Advanced Reference:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `use_memory_buffer` | boolean | `false` | Buffer logs in memory before disk |
| `memory_buffer_size_mb` | integer | `10` | Size of memory buffer |
| `sync_to_disk_interval` | float | `10.0` | Seconds between disk syncs |
| `use_write_ahead_log` | boolean | `false` | Use WAL for durability |
| `enable_crash_recovery` | boolean | `false` | Enable crash recovery |
| `lock_files` | boolean | `false` | Lock log files during writes |
| `fsync_on_write` | boolean | `false` | Force sync after every write |

---

## 4. Environment Variable Overrides

All configuration settings can be overridden via environment variables using the pattern:

```
KOLLABOR_LOG_<SECTION>_<SUBSECTION>_<SETTING>=<value>
```

### Examples:

```bash
# Global settings
export KOLLABOR_LOG_ENABLED=false
export KOLLABOR_LOG_COMPRESSION=gzip
export KOLLABOR_LOG_PRIVACY_REDACT_API_KEYS=true

# Conversation logger
export KOLLABOR_LOG_CONVERSATION_ENABLED=true
export KOLLABOR_LOG_CONVERSATION_CONTENT_INCLUDE_INTELLIGENCE=false
export KOLLABOR_LOG_CONVERSATION_PERFORMANCE_BATCH_SIZE=20

# Raw API logger
export KOLLABOR_LOG_RAW_API_ENABLED=false
export KOLLABOR_LOG_RAW_API_FILE_STRATEGY_ONE_FILE_PER_REQUEST=false
export KOLLABOR_LOG_RAW_API_FILE_STRATEGY_ONE_FILE_PER_SESSION=true

# Conversation manager
export KOLLABOR_LOG_MANAGER_AUTO_SAVE_ENABLED=true
export KOLLABOR_LOG_MANAGER_AUTO_SAVE_INTERVAL=20
export KOLLABOR_LOG_MANAGER_COMPRESSION_ENABLED=true

# Debugging
export KOLLABOR_LOG_DEBUG_PERFORMANCE_METRICS=true
export KOLLABOR_LOG_DEBUG_TRACE_MESSAGE_FLOW=true
```

**Precedence Order:**
1. Environment variables (highest priority)
2. User config file (`.kollabor-cli/config.json`)
3. Project config file (local `.kollabor-cli/config.json`)
4. Default configuration (lowest priority)

---

## 5. Implementation Plan

### Phase 1: Foundation (Week 1)

**Goal:** Establish configuration infrastructure without breaking existing behavior

**Tasks:**
1. Create configuration schema in `core/config/logging_config.py`
2. Add config validation and type checking
3. Implement environment variable parsing
4. Add backward compatibility layer
5. Update default config in `core/config/loader.py`

**Files Modified:**
- `core/config/loader.py` - Add logging config defaults
- `core/config/logging_config.py` - New file for config schema
- `core/config/env_parser.py` - New file for env var parsing

**Deliverables:**
- [ ] Configuration schema defined
- [ ] Environment variable parsing working
- [ ] Backward compatibility tests passing
- [ ] Default config loads without errors

---

### Phase 2: Conversation Logger (Week 2)

**Goal:** Apply configuration to KollaborConversationLogger

**Tasks:**
1. Refactor `KollaborConversationLogger.__init__()` to accept config
2. Implement enable/disable check
3. Add content filtering based on config
4. Implement performance settings (async, batching)
5. Add rotation support
6. Implement privacy controls (redaction)

**Files Modified:**
- `core/llm/conversation_logger.py`
- `core/llm/llm_service.py` - Pass config to logger

**Deliverables:**
- [ ] Logger respects `enabled` flag
- [ ] Content filtering works
- [ ] Batch writes implemented
- [ ] Redaction working
- [ ] Tests for all new features

---

### Phase 3: Raw API Logger (Week 3)

**Goal:** Apply configuration to APICommunicationService raw logger

**Tasks:**
1. Refactor `_log_raw_interaction()` to check config
2. Implement file strategy selection
3. Add content filtering
4. Add performance optimizations
5. Implement filtering (models, response time)
6. Add privacy controls

**Files Modified:**
- `core/llm/api_communication_service.py`

**Deliverables:**
- [ ] File strategy configurable
- [ ] One-file-per-session mode works
- [ ] Content filtering works
- [ ] Model filtering works
- [ ] Tests passing

---

### Phase 4: Conversation Manager (Week 4)

**Goal:** Apply configuration to ConversationManager

**Tasks:**
1. Make auto-save interval configurable
2. Implement interval types (messages, time, both)
3. Add trigger configuration
4. Implement debouncing
5. Add versioning support
6. Add compression support

**Files Modified:**
- `core/llm/conversation_manager.py`

**Deliverables:**
- [ ] Auto-save interval parameterized
- [ ] Time-based auto-save works
- [ ] Triggers configurable
- [ ] Versioning implemented
- [ ] Compression working
- [ ] Tests passing

---

### Phase 5: Global Features (Week 5)

**Goal:** Implement cross-cutting features

**Tasks:**
1. Implement global retention policy
2. Add cleanup scheduler
3. Implement global compression
4. Add debugging features
5. Implement advanced features (WAL, crash recovery)
6. Add performance monitoring

**Files Modified:**
- `core/llm/logging/retention_manager.py` - New file
- `core/llm/logging/cleanup_scheduler.py` - New file
- `core/llm/logging/performance_monitor.py` - New file

**Deliverables:**
- [ ] Retention cleanup working
- [ ] Scheduled cleanup runs
- [ ] Global compression works
- [ ] Performance metrics collected
- [ ] Tests passing

---

### Phase 6: Testing & Documentation (Week 6)

**Goal:** Comprehensive testing and documentation

**Tasks:**
1. Write unit tests for all configuration options
2. Write integration tests
3. Write migration guide
4. Update user documentation
5. Create example configurations
6. Performance benchmarking

**Files Created:**
- `tests/unit/test_logging_config.py`
- `tests/integration/test_logging_system.py`
- `docs/guides/logging-configuration.md`
- `docs/guides/logging-migration.md`
- `docs/examples/logging-configs/`

**Deliverables:**
- [ ] 90%+ test coverage
- [ ] All example configs tested
- [ ] Migration guide complete
- [ ] User documentation updated
- [ ] Performance benchmarks documented

---

## 6. Backward Compatibility

### Legacy Configuration Support

Old configuration will continue to work:

```json
{
  "core": {
    "llm": {
      "save_conversations": true,
      "conversation_format": "jsonl"
    }
  }
}
```

**Migration Strategy:**
1. Detect legacy config keys
2. Map to new config structure
3. Log deprecation warning
4. Provide migration tool: `kollab config migrate`

**Deprecated Keys:**
- `core.llm.save_conversations` → `core.llm.logging.conversation_manager.enabled`
- `core.llm.conversation_format` → `core.llm.logging.conversation_manager.format`

---

## 7. Configuration Examples

### Example 1: Minimal Logging (Production)

```json
{
  "core": {
    "llm": {
      "logging": {
        "global": {
          "enabled": true,
          "compression": "gzip",
          "retention": {
            "max_age_days": 7,
            "max_total_size_mb": 100
          }
        },
        "conversation_logger": {
          "enabled": true,
          "content": {
            "include_intelligence": false,
            "include_user_patterns": false
          }
        },
        "raw_api_logger": {
          "enabled": false
        },
        "conversation_manager": {
          "enabled": true,
          "auto_save": {
            "interval": 50
          }
        }
      }
    }
  }
}
```

---

### Example 2: Maximum Logging (Debugging)

```json
{
  "core": {
    "llm": {
      "logging": {
        "global": {
          "enabled": true,
          "compression": "none"
        },
        "conversation_logger": {
          "enabled": true,
          "content": {
            "include_intelligence": true,
            "log_thinking_tags": true
          }
        },
        "raw_api_logger": {
          "enabled": true,
          "content": {
            "log_request_headers": true,
            "log_response_headers": true
          },
          "file_strategy": {
            "one_file_per_request": true
          }
        },
        "conversation_manager": {
          "enabled": true,
          "auto_save": {
            "interval": 5
          },
          "versioning": {
            "enabled": true,
            "keep_versions": 10
          }
        },
        "debugging": {
          "log_performance_metrics": true,
          "log_memory_usage": true,
          "trace_message_flow": true
        }
      }
    }
  }
}
```

---

### Example 3: Privacy-Focused

```json
{
  "core": {
    "llm": {
      "logging": {
        "global": {
          "enabled": true,
          "privacy": {
            "redact_api_keys": true,
            "redact_tokens": true,
            "anonymize_paths": true,
            "hash_user_content": true
          },
          "file_permissions": "0600"
        },
        "conversation_logger": {
          "enabled": true
        },
        "raw_api_logger": {
          "enabled": false
        },
        "conversation_manager": {
          "enabled": true,
          "compression": {
            "enabled": true,
            "algorithm": "gzip"
          }
        }
      }
    }
  }
}
```

---

### Example 4: Performance-Optimized

```json
{
  "core": {
    "llm": {
      "logging": {
        "global": {
          "enabled": true,
          "async_logging": true,
          "buffer_size": 5000
        },
        "conversation_logger": {
          "enabled": true,
          "performance": {
            "async_writes": true,
            "batch_size": 50,
            "batch_timeout": 5.0
          }
        },
        "raw_api_logger": {
          "enabled": true,
          "file_strategy": {
            "one_file_per_session": true
          },
          "performance": {
            "buffer_writes": true
          }
        },
        "conversation_manager": {
          "enabled": true,
          "auto_save": {
            "debounce_delay": 2.0
          }
        }
      }
    }
  }
}
```

---

## 8. Use Cases

### Use Case 1: Development

**Requirements:**
- Full logging for debugging
- No privacy concerns
- Fast iteration

**Configuration:**
```bash
export KOLLABOR_LOG_DEBUG_TRACE_MESSAGE_FLOW=true
export KOLLABOR_LOG_DEBUG_PERFORMANCE_METRICS=true
export KOLLABOR_LOG_RAW_API_ENABLED=true
```

---

### Use Case 2: Production

**Requirements:**
- Minimal logging overhead
- Privacy compliance
- Disk space management

**Configuration:**
```bash
export KOLLABOR_LOG_COMPRESSION=gzip
export KOLLABOR_LOG_RETENTION_MAX_AGE_DAYS=7
export KOLLABOR_LOG_RETENTION_MAX_TOTAL_SIZE_MB=50
export KOLLABOR_LOG_PRIVACY_REDACT_API_KEYS=true
export KOLLABOR_LOG_RAW_API_ENABLED=false
```

---

### Use Case 3: Compliance Audit

**Requirements:**
- Complete audit trail
- Immutable logs
- Long retention

**Configuration:**
```json
{
  "core": {
    "llm": {
      "logging": {
        "global": {
          "retention": {
            "max_age_days": 365,
            "cleanup_schedule": "never"
          }
        },
        "conversation_logger": {
          "enabled": true,
          "content": {
            "include_intelligence": true
          }
        },
        "raw_api_logger": {
          "enabled": true
        },
        "conversation_manager": {
          "versioning": {
            "enabled": true,
            "keep_versions": 100
          }
        },
        "advanced": {
          "use_write_ahead_log": true,
          "lock_files": true
        }
      }
    }
  }
}
```

---

## 9. Performance Considerations

### Memory Usage

**Default Configuration:**
- Conversation logger queue: ~1000 entries × 1KB = 1MB
- Raw API logger: minimal (immediate write)
- Conversation manager: minimal (saves to disk)
- **Total: ~2-5MB**

**High-Performance Configuration:**
- Buffer size: 5000 entries × 1KB = 5MB
- Batch writes enabled
- Compression disabled
- **Total: ~10-15MB**

### Disk Usage

**Per Conversation (defaults):**
- Conversation logger: 50-200KB JSONL
- Raw API logger: 10-50KB per request × N requests
- Conversation manager: 20-100KB JSON
- **Total: ~100KB-1MB per conversation**

**With Compression:**
- GZIP compression: ~70% reduction
- LZMA compression: ~80% reduction
- **Total: ~20KB-300KB per conversation**

### CPU Usage

**Default Configuration:**
- Async writes: minimal CPU overhead
- No compression: <1% CPU
- Intelligence features: <2% CPU

**With Compression:**
- GZIP: +5-10% CPU during writes
- LZMA: +10-20% CPU during writes

---

## 10. Security Considerations

### Privacy Controls

1. **API Key Redaction**: Replace API keys with `[REDACTED]` in logs
2. **Token Redaction**: Remove auth tokens from headers
3. **Content Hashing**: SHA256 hash sensitive user content
4. **Path Anonymization**: Replace absolute paths with relative

### File Permissions

- Default: `0600` (owner read/write only)
- Configurable per environment
- Respects umask settings

### Secure Deletion

When retention cleanup runs:
1. Overwrite file with random data
2. Delete file
3. Sync filesystem
4. Verify deletion

---

## 11. Migration Guide

### Step 1: Backup Current Logs

```bash
cp -r .kollabor-cli/conversations .kollabor-cli/conversations.backup
cp -r .kollabor-cli/conversations_raw .kollabor-cli/conversations_raw.backup
```

### Step 2: Update Configuration

```bash
# Use migration tool
kollab config migrate

# Or manually update config.json
vim .kollabor-cli/config.json
```

### Step 3: Test New Configuration

```bash
# Dry run
kollab config validate

# Test with single conversation
kollab --config-test
```

### Step 4: Apply Changes

```bash
# No action needed - config takes effect immediately
```

---

## 12. Testing Strategy

### Unit Tests

- [ ] Configuration loading and validation
- [ ] Environment variable parsing
- [ ] Backward compatibility mapping
- [ ] Privacy controls (redaction, hashing)
- [ ] Retention cleanup logic
- [ ] Compression/decompression
- [ ] File rotation logic

### Integration Tests

- [ ] Full logging pipeline with all three systems
- [ ] Configuration changes at runtime
- [ ] Environment variable overrides
- [ ] Migration from legacy config
- [ ] Cleanup scheduler execution
- [ ] Performance under load

### Performance Tests

- [ ] Logging throughput (messages/second)
- [ ] Memory usage under various configs
- [ ] Disk I/O performance
- [ ] Compression performance
- [ ] Batch write performance

---

## 13. Open Questions

1. **Encryption at Rest**: Should we support encrypted log files?
2. **Remote Logging**: Support for remote log aggregation services?
3. **Log Streaming**: Real-time log streaming to external systems?
4. **Structured Query**: SQL-like queries over conversation history?
5. **Machine Learning**: Use logged data to improve intelligence features?

---

## 14. Future Enhancements

### Version 2.0

- Log encryption at rest
- Remote log shipping (syslog, Kafka, etc.)
- Real-time log analytics dashboard
- Machine learning on conversation patterns
- SQL query interface for conversation history
- Automated anomaly detection
- Multi-tenant logging support

---

## 15. References

- [Anthropic Claude API Documentation](https://docs.anthropic.com/claude/reference)
- [JSONL Format Specification](http://jsonlines.org/)
- [Python Logging Best Practices](https://docs.python.org/3/howto/logging.html)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

---

## Appendix A: Complete Default Configuration

See separate file: `docs/examples/logging-configs/default-logging-config.json`

## Appendix B: Environment Variable Reference

See separate file: `docs/reference/logging-env-vars.md`

## Appendix C: Performance Benchmarks

See separate file: `docs/benchmarks/logging-performance.md`

---

**End of Specification**
