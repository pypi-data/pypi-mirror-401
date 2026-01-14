# Dynamic Profile Environment Variables

## Overview

Enable profiles to resolve configuration from environment variables using a predictable naming convention:
```
KOLLABOR_{PROFILE_NAME}_{FIELD}
```

## Problem

Current system has inconsistent env var handling:
- Global fallback: `KOLLABOR_API_TOKEN` / `KOLLABOR_API_KEY` (confusing, not profile-aware)
- Profile-specific: `api_token_env` field pointing to arbitrary env var names (inconsistent)
- No env var support for other profile fields (endpoint, model, etc.)

## Design Decisions

| Decision | Resolution |
|----------|------------|
| Breaking changes | Clean break, no deprecation period (new app) |
| Empty string handling | Treat as "not configured", fall through to config value |
| Missing value warning | Only warn if BOTH env var and config are empty/missing |
| Invalid value handling | Warn user, fall back to config or default |
| Profile name normalization | All non-alphanumeric chars become underscore (`my.profile` -> `MY_PROFILE`) |
| Profile name collision | Reject creation of profiles that would normalize to same env var prefix |
| Env var caching | None - re-read from env on every access |
| Invalid tool_format | Warn user, fallback to `openai` |
| timeout=0 meaning | 0 = no timeout (infinity), not a fallback value |
| core.llm.api_token config | Remove - all tokens must go through profile env vars |
| extra_headers env var | Not supported - Dict too complex for env var format |
| api_token_env param removal | Remove entirely from signatures, no deprecation |
| from_dict() stale fields | Silently ignore unknown fields (forward compatible) |
| get_profile_summary() display | Show `KOLLABOR_{PROFILE}_TOKEN: [set/not set]` |
| Temperature range validation | No clamping - pass through to API, let API reject |
| get_env_var_hints() check set | Yes, include `is_set: bool` for each env var |
| Profile rename warning | Yes, warn user their old env vars won't work |
| Return type "" vs None | Keep as-is: "" for required (usable), None for token (nullable) |
| APICommunicationService init | Require active profile at init, no fallback state |
| Thread safety (env reads) | Acceptable risk - env vars rarely change at runtime |
| Two layers of defaults | Keep both - from_dict for load, getter for runtime |
| Profile name whitespace | Strip whitespace before normalization |

### Required vs Optional Fields

**Required** (warn if missing from both env and config):
- `TOKEN` - cannot make API calls without authentication
- `ENDPOINT` - must know where to send requests
- `MODEL` - must know which model to use

**Optional** (have sensible defaults, no warning):
- `MAX_TOKENS` - default: null (API default)
- `TEMPERATURE` - default: 0.7
- `TIMEOUT` - default: 30000ms
- `TOOL_FORMAT` - default: openai

## What Gets Removed

- `KOLLABOR_API_TOKEN` global fallback in APICommunicationService
- `KOLLABOR_API_KEY` global fallback in APICommunicationService
- `KOLLABOR_API_TEMPERATURE` global fallback in APICommunicationService
- `KOLLABOR_API_TIMEOUT` global fallback in APICommunicationService
- `api_token_env` field from LLMProfile
- `core.llm.api_token` config key (tokens must use profile env vars)
- All references to `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` in code and docs
- No global env var fallbacks - all config must go through profile-specific env vars

### Default Profile Changes

Before:
```python
"claude": {
    "api_token_env": "ANTHROPIC_API_KEY",  # REMOVED
    ...
}
"openai": {
    "api_token_env": "OPENAI_API_KEY",  # REMOVED
    ...
}
```

After: Users must set:
```bash
export KOLLABOR_CLAUDE_TOKEN="sk-ant-..."
export KOLLABOR_OPENAI_TOKEN="sk-..."
```

## Solution

Standardized env var pattern per profile. For a profile named `fast`:

```bash
KOLLABOR_FAST_ENDPOINT=http://localhost:1234
KOLLABOR_FAST_TOKEN=sk-xxx
KOLLABOR_FAST_MODEL=qwen/qwen3-0.6b
KOLLABOR_FAST_MAX_TOKENS=4096
KOLLABOR_FAST_TEMPERATURE=0.3
KOLLABOR_FAST_TIMEOUT=30000
KOLLABOR_FAST_TOOL_FORMAT=openai
```

## Field Mapping

| Env Var Suffix | Profile Field | Type | Example |
|----------------|---------------|------|---------|
| `_ENDPOINT` | `api_url` | string | `https://api.anthropic.com` |
| `_TOKEN` | (api token) | string | `sk-ant-xxx` |
| `_MODEL` | `model` | string | `claude-sonnet-4-20250514` |
| `_MAX_TOKENS` | `max_tokens` | int | `4096` |
| `_TEMPERATURE` | `temperature` | float | `0.7` |
| `_TIMEOUT` | `timeout` | int (ms) | `30000` |
| `_TOOL_FORMAT` | `tool_format` | string | `openai` or `anthropic` |

## Resolution Priority

For each field, resolution order:
1. Environment variable `KOLLABOR_{PROFILE_NAME}_{FIELD}`
2. Config file value (`config.json`)
3. Default value

## Implementation

### 1. Update LLMProfile class

Add helper method for env var key generation:

```python
import re
import logging

logger = logging.getLogger(__name__)

def _get_env_key(self, field: str) -> str:
    """Generate env var key for this profile and field.

    Normalizes profile name: strip whitespace, all non-alphanumeric chars become underscore.
    Examples:
        my-local-llm -> KOLLABOR_MY_LOCAL_LLM_{FIELD}
        my.profile   -> KOLLABOR_MY_PROFILE_{FIELD}
        My Profile!  -> KOLLABOR_MY_PROFILE__{FIELD}
        "  fast  "   -> KOLLABOR_FAST_{FIELD}
    """
    # Strip whitespace, replace all non-alphanumeric with underscore, then uppercase
    name_stripped = self.name.strip()
    name_normalized = re.sub(r'[^a-zA-Z0-9]', '_', name_stripped).upper()
    return f"KOLLABOR_{name_normalized}_{field}"
```

Add getter methods that check env vars first:

```python
def _get_env_value(self, field: str) -> Optional[str]:
    """Get env var value, treating empty/whitespace-only as unset.

    Returns:
        The env var value if set and non-empty, None otherwise.
        Note: "0" is a valid value and will be returned (not treated as falsy).
    """
    env_key = self._get_env_key(field)
    env_val = os.environ.get(env_key)
    # Check for None (unset) or empty/whitespace-only
    if env_val is None or not env_val.strip():
        return None
    return env_val

def get_endpoint(self) -> str:
    """Get API endpoint, checking env var first. REQUIRED field."""
    env_val = self._get_env_value("ENDPOINT")
    if env_val:
        return env_val
    if self.api_url:
        return self.api_url
    # Both sources empty - warn user
    logger.warning(f"Profile '{self.name}': No endpoint configured. "
                   f"Set {self._get_env_key('ENDPOINT')} or configure in config.json")
    return ""

def get_token(self) -> Optional[str]:
    """Get API token from env var or config. REQUIRED field."""
    env_val = self._get_env_value("TOKEN")
    if env_val:
        return env_val
    if self.api_token:
        return self.api_token
    # Both sources empty - warn user
    logger.warning(f"Profile '{self.name}': No API token configured. "
                   f"Set {self._get_env_key('TOKEN')} in your environment")
    return None

def get_model(self) -> str:
    """Get model, checking env var first. REQUIRED field."""
    env_val = self._get_env_value("MODEL")
    if env_val:
        return env_val
    if self.model:
        return self.model
    # Both sources empty - warn user
    logger.warning(f"Profile '{self.name}': No model configured. "
                   f"Set {self._get_env_key('MODEL')} or configure in config.json")
    return ""

def get_max_tokens(self) -> Optional[int]:
    """Get max tokens, checking env var first. OPTIONAL field."""
    env_key = self._get_env_key("MAX_TOKENS")
    env_val = self._get_env_value("MAX_TOKENS")
    if env_val:
        try:
            return int(env_val)
        except ValueError:
            logger.warning(f"Profile '{self.name}': {env_key}='{env_val}' is not a valid integer, "
                           f"using config value")
    return self.max_tokens  # Returns None if not configured (uses API default)

def get_temperature(self) -> float:
    """Get temperature, checking env var first. OPTIONAL field (default: 0.7)."""
    env_key = self._get_env_key("TEMPERATURE")
    env_val = self._get_env_value("TEMPERATURE")
    if env_val:
        try:
            return float(env_val)
        except ValueError:
            logger.warning(f"Profile '{self.name}': {env_key}='{env_val}' is not a valid float, "
                           f"using config value")
    return self.temperature if self.temperature is not None else 0.7

def get_timeout(self) -> int:
    """Get timeout, checking env var first. OPTIONAL field (default: 30000ms).

    Note: 0 means no timeout (infinity), not a fallback value.
    """
    env_key = self._get_env_key("TIMEOUT")
    env_val = self._get_env_value("TIMEOUT")
    if env_val is not None:
        try:
            return int(env_val)
        except ValueError:
            logger.warning(f"Profile '{self.name}': {env_key}='{env_val}' is not a valid integer, "
                           f"using config value")
    # 0 is valid (no timeout), only use default if truly None
    if self.timeout is not None:
        return self.timeout
    return 30000

def get_tool_format(self) -> str:
    """Get tool format, checking env var first. OPTIONAL field (default: openai)."""
    env_key = self._get_env_key("TOOL_FORMAT")
    env_val = self._get_env_value("TOOL_FORMAT")
    valid_formats = ("openai", "anthropic")
    if env_val:
        if env_val in valid_formats:
            return env_val
        logger.warning(f"Profile '{self.name}': {env_key}='{env_val}' is invalid "
                       f"(must be one of {valid_formats}), using 'openai'")
    config_val = self.tool_format
    if config_val and config_val in valid_formats:
        return config_val
    return "openai"
```

### 2. Update callers to use getter methods

Files to update:
- `core/llm/api_communication_service.py` - `update_from_profile()`
- `core/commands/system_commands.py` - profile display/switching
- `core/llm/profile_manager.py` - `get_profile_summary()`

### 3. Fix update_from_profile() and require profile at init

Current signature is missing max_tokens and timeout, causing stale values when switching profiles.
Also, APICommunicationService should require an active profile at init (no fallback state):

```python
# BEFORE (incomplete, with global fallbacks):
def __init__(self, ...):
    self.api_token = os.environ.get("KOLLABOR_API_TOKEN") or os.environ.get("KOLLABOR_API_KEY")
    # ... other global fallbacks

def update_from_profile(self, api_url: str, model: str, temperature: float, tool_format: str):
    self.base_url = api_url
    self.model = model
    self.temperature = temperature
    self.tool_format = tool_format

# AFTER (profile-driven):
def __init__(self, profile: LLMProfile, ...):
    """Initialize with a profile. No global fallbacks."""
    self.update_from_profile(profile)

def update_from_profile(self, profile: LLMProfile):
    """Update service configuration from a profile.

    Uses profile getter methods to resolve env var -> config -> default.
    """
    self.base_url = profile.get_endpoint()
    self.model = profile.get_model()
    self.temperature = profile.get_temperature()
    self.tool_format = profile.get_tool_format()
    self.max_tokens = profile.get_max_tokens()
    self.timeout = profile.get_timeout()
    self.api_token = profile.get_token()
```

This also simplifies the call sites - instead of extracting individual fields, just pass the profile object.

### 4. Add profile name collision validation

Prevent creating profiles that would share the same env var prefix:

```python
def _get_normalized_name(self, name: str) -> str:
    """Get normalized profile name for env var prefix."""
    return re.sub(r'[^a-zA-Z0-9]', '_', name).upper()

def _check_name_collision(self, new_name: str, exclude_name: Optional[str] = None) -> Optional[str]:
    """Check if new profile name would collide with existing profiles.

    Args:
        new_name: The proposed profile name
        exclude_name: Profile name to exclude from check (for renames)

    Returns:
        Name of colliding profile if collision found, None otherwise.
    """
    new_normalized = self._get_normalized_name(new_name)
    for existing_name in self._profiles:
        if existing_name == exclude_name:
            continue
        if self._get_normalized_name(existing_name) == new_normalized:
            return existing_name
    return None

def create_profile(self, name: str, ...) -> bool:
    # Check for collision before creating
    collision = self._check_name_collision(name)
    if collision:
        logger.error(f"Cannot create profile '{name}': env var prefix collides with "
                     f"existing profile '{collision}' (both normalize to "
                     f"KOLLABOR_{self._get_normalized_name(name)}_*)")
        return False
    # ... rest of creation logic

def update_profile(self, name: str, new_name: Optional[str] = None, ...) -> bool:
    # If renaming, check for collision and warn about env var change
    if new_name and new_name != name:
        collision = self._check_name_collision(new_name, exclude_name=name)
        if collision:
            logger.error(f"Cannot rename to '{new_name}': env var prefix collides with "
                         f"existing profile '{collision}'")
            return False

        # Warn user about env var change
        old_prefix = self._get_normalized_name(name)
        new_prefix = self._get_normalized_name(new_name)
        if old_prefix != new_prefix:
            logger.warning(f"Profile renamed: env vars changed from KOLLABOR_{old_prefix}_* "
                           f"to KOLLABOR_{new_prefix}_*. Update your environment variables.")
    # ... rest of update logic
```

### 5. Remove api_token_env field

- Remove `api_token_env` field from `LLMProfile` dataclass
- Remove from `to_dict()` and `from_dict()` methods
- Remove from `DEFAULT_PROFILES` (claude, openai profiles)
- Remove from `create_profile()` and `update_profile()` signatures
- Update `get_profile_summary()` to show new env var pattern instead

### 6. Update setup wizard

- Remove `api_token_env` field from form
- Show env var convention on token page:
  ```
  Set your API token in your shell:

    export KOLLABOR_MY_LLM_TOKEN='sk-...'

  The env var name is based on your profile name.
  ```
- Update ready page to show expected env var name

### 7. Update get_profile_summary() display

```python
def get_profile_summary(self) -> str:
    """Get a summary of the profile for display."""
    hints = self.get_env_var_hints()
    token_status = "[set]" if hints["token"].is_set else "[not set]"

    return f"""Profile: {self.name}
  Endpoint: {self.get_endpoint() or '(not configured)'}
  Model: {self.get_model() or '(not configured)'}
  Token: {hints["token"].name} {token_status}
  Temperature: {self.get_temperature()}
  Max Tokens: {self.get_max_tokens() or '(API default)'}
  Timeout: {self.get_timeout()}ms
  Tool Format: {self.get_tool_format()}"""
```

### 8. Add helper method for env var display

```python
@dataclass
class EnvVarHint:
    """Information about a profile's env var."""
    name: str       # e.g., "KOLLABOR_CLAUDE_TOKEN"
    is_set: bool    # True if env var exists and is non-empty

def get_env_var_hints(self) -> Dict[str, EnvVarHint]:
    """Get env var names and status for this profile."""
    fields = ["ENDPOINT", "TOKEN", "MODEL", "MAX_TOKENS", "TEMPERATURE", "TIMEOUT", "TOOL_FORMAT"]
    return {
        field.lower(): EnvVarHint(
            name=self._get_env_key(field),
            is_set=self._get_env_value(field) is not None
        )
        for field in fields
    }
```

## Example Usage

### Profile: claude

```bash
# In ~/.bashrc or ~/.zshrc
export KOLLABOR_CLAUDE_TOKEN="sk-ant-api03-xxx"

# Optional overrides
export KOLLABOR_CLAUDE_MODEL="claude-opus-4-20250514"
export KOLLABOR_CLAUDE_MAX_TOKENS="8192"
```

### Profile: my-local-llm

```bash
# Profile name "my-local-llm" becomes "MY_LOCAL_LLM"
export KOLLABOR_MY_LOCAL_LLM_ENDPOINT="http://192.168.1.100:8080"
export KOLLABOR_MY_LOCAL_LLM_MODEL="llama3"
```

## Migration

1. Remove `api_token_env` field entirely
2. Remove global `KOLLABOR_API_TOKEN` / `KOLLABOR_API_KEY` fallback
3. Users must update their env vars to new profile-specific pattern
4. Setup wizard uses new pattern
5. Documentation updated with new pattern

## Files to Modify

| File | Changes |
|------|---------|
| `core/llm/profile_manager.py` | Add getter methods to LLMProfile, remove `api_token_env` field, update DEFAULT_PROFILES |
| `core/llm/api_communication_service.py` | Remove `KOLLABOR_API_TOKEN`/`KOLLABOR_API_KEY` fallback, use profile.get_*() methods |
| `core/commands/system_commands.py` | Update profile display, remove api_token_env from forms, update placeholder text |
| `plugins/fullscreen/setup_wizard_plugin.py` | Update to show env var convention, remove api_token_env field, remove ANTHROPIC/OPENAI refs |
| `docs/reference/troubleshooting-guide.md` | Update env var examples to use KOLLABOR_*_TOKEN pattern |
| `docs/reference/technology-stack.md` | Update env var examples to use KOLLABOR_*_TOKEN pattern |

## Testing

### Resolution Priority
1. Create profile, set env vars, verify env var takes precedence
2. Unset env var, verify config value is used
3. Unset both, verify default is used (for optional fields)

### Profile Name Normalization
4. `my-llm` -> `KOLLABOR_MY_LLM_TOKEN`
5. `my.profile` -> `KOLLABOR_MY_PROFILE_TOKEN`
6. `My Profile!` -> `KOLLABOR_MY_PROFILE__TOKEN`

### Profile Name Collision Prevention
7. Create `my-profile`, then try to create `my_profile` - should fail with collision error
8. Create `my-profile`, then try to rename another profile to `my.profile` - should fail
9. Create `my-profile`, rename it to `my_profile` (same normalized) - should succeed (self-rename allowed)

### Empty String Handling
10. Set `KOLLABOR_CLAUDE_MODEL=""` with valid config, verify falls through to config value (no warning)
11. Set `KOLLABOR_CLAUDE_TEMPERATURE=""` with empty config, verify falls through to default 0.7 (no warning, optional field)

### Zero Value Handling
12. Set `KOLLABOR_FAST_MAX_TOKENS=0`, verify returns 0 (not treated as unset)
13. Set `KOLLABOR_FAST_TEMPERATURE=0`, verify returns 0.0 (not treated as unset)
14. Set `KOLLABOR_FAST_TIMEOUT=0`, verify returns 0 (not treated as unset)

### Invalid Value Warnings
15. Set `KOLLABOR_FAST_MAX_TOKENS="abc"`, verify warning logged and config value used
16. Set `KOLLABOR_FAST_TEMPERATURE="not-a-number"`, verify warning and fallback to 0.7
17. Set `KOLLABOR_FAST_TOOL_FORMAT="custom"`, verify warning and fallback to "openai"

### Required Field Warnings
18. Profile with no TOKEN in env or config, verify warning when `get_token()` called
19. Profile with no ENDPOINT in env or config, verify warning when `get_endpoint()` called
20. Profile with no MODEL in env or config, verify warning when `get_model()` called

### Optional Field Defaults
21. No MAX_TOKENS configured anywhere, verify returns None (API default)
22. No TEMPERATURE configured anywhere, verify returns 0.7
23. No TIMEOUT configured anywhere, verify returns 30000
24. No TOOL_FORMAT configured anywhere, verify returns "openai"

### Removal Verification
25. Verify `api_token_env` field is fully removed from LLMProfile
26. Verify `KOLLABOR_API_TOKEN` global fallback is removed
27. Verify `KOLLABOR_API_KEY` global fallback is removed
28. Verify `KOLLABOR_API_TEMPERATURE` global fallback is removed
29. Verify `KOLLABOR_API_TIMEOUT` global fallback is removed
30. Verify `core.llm.api_token` config key is removed

### Profile Rename Warning
31. Rename `claude` to `anthropic`, verify warning about env var change logged
32. Rename `fast` to `FAST` (same normalized), verify no warning (no change)

### Whitespace Handling
33. Profile name `"  fast  "` normalizes to `KOLLABOR_FAST_TOKEN` (stripped)

### get_env_var_hints()
34. Call get_env_var_hints(), verify returns dict with name and is_set for each field
35. Set KOLLABOR_CLAUDE_TOKEN, verify hints.token.is_set == True

### APICommunicationService Init
36. Verify APICommunicationService.__init__ requires profile parameter
37. Verify no global env var fallbacks in __init__

### from_dict() Forward Compatibility
38. Load profile with unknown field `api_token_env`, verify silently ignored (no error)
