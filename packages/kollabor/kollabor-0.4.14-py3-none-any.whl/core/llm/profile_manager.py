"""
LLM Profile Manager.

Manages named LLM configuration profiles that define:
- API endpoint URL
- Model name
- Temperature and other parameters
- Tool calling format (OpenAI vs Anthropic)
- API token environment variable

Profiles can be defined in config.json under core.llm.profiles
or use built-in defaults.
"""

import json
import os
import re
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .api_adapters import BaseAPIAdapter, OpenAIAdapter, AnthropicAdapter

logger = logging.getLogger(__name__)


@dataclass
class EnvVarHint:
    """Information about a profile's env var."""
    name: str       # e.g., "KOLLABOR_CLAUDE_TOKEN"
    is_set: bool    # True if env var exists and is non-empty


@dataclass
class LLMProfile:
    """
    Configuration profile for LLM settings.

    Attributes:
        name: Profile identifier
        api_url: Base URL for the LLM API
        model: Model name/identifier
        temperature: Sampling temperature (0.0-1.0)
        max_tokens: Maximum tokens to generate (None = no limit)
        tool_format: Tool calling format ("openai" or "anthropic")
        native_tool_calling: Enable native API tool calling (True) or XML-only mode (False)
        timeout: Request timeout in milliseconds (0 = no timeout)
        description: Human-readable description
        extra_headers: Additional HTTP headers to include

    API tokens are now resolved via environment variables using the pattern:
    KOLLABOR_{PROFILE_NAME}_TOKEN (e.g., KOLLABOR_CLAUDE_TOKEN)
    """

    name: str
    api_url: str
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    tool_format: str = "openai"
    native_tool_calling: bool = True  # True = native API tools, False = XML tags only
    timeout: int = 0
    description: str = ""
    extra_headers: Dict[str, str] = field(default_factory=dict)
    # Internal storage for API token from config (not from env var)
    api_token: str = field(default="", repr=False)

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

    def get_native_tool_calling(self) -> bool:
        """Get native_tool_calling, checking env var first. OPTIONAL field (default: True).

        When True, tools are passed to the API for native function calling.
        When False, the LLM uses XML tags (<terminal>, <tool>, etc.) instead.
        """
        env_val = self._get_env_value("NATIVE_TOOL_CALLING")
        if env_val is not None:
            # Accept common truthy/falsy values
            return env_val.lower() in ("true", "1", "yes", "on")
        return self.native_tool_calling

    def get_env_var_hints(self) -> Dict[str, EnvVarHint]:
        """Get env var names and status for this profile."""
        fields = ["ENDPOINT", "TOKEN", "MODEL", "MAX_TOKENS", "TEMPERATURE", "TIMEOUT", "TOOL_FORMAT", "NATIVE_TOOL_CALLING"]
        return {
            field.lower(): EnvVarHint(
                name=self._get_env_key(field),
                is_set=self._get_env_value(field) is not None
            )
            for field in fields
        }

    def get_api_token(self) -> Optional[str]:
        """
        Get API token from environment variable.

        DEPRECATED: Use get_token() instead. Tokens are now resolved via
        KOLLABOR_{PROFILE_NAME}_TOKEN environment variables.

        Returns:
            None (deprecated method, use get_token() instead)
        """
        # Deprecated - use get_token() which follows the new env var pattern
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary representation."""
        result = {
            "name": self.name,
            "api_url": self.api_url,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "tool_format": self.tool_format,
            "native_tool_calling": self.native_tool_calling,
            "timeout": self.timeout,
            "description": self.description,
            "extra_headers": self.extra_headers,
        }
        # Only include api_token if set (to avoid empty string in config)
        if self.api_token:
            result["api_token"] = self.api_token
        return result

    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> "LLMProfile":
        """
        Create profile from dictionary.

        Silently ignores unknown fields for forward compatibility.

        Args:
            name: Profile name
            data: Profile configuration dictionary

        Returns:
            LLMProfile instance
        """
        return cls(
            name=name,
            api_url=data.get("api_url", "http://localhost:1234"),
            model=data.get("model", "default"),
            temperature=data.get("temperature", 0.7),
            max_tokens=data.get("max_tokens"),
            tool_format=data.get("tool_format", "openai"),
            native_tool_calling=data.get("native_tool_calling", True),
            timeout=data.get("timeout", 0),
            description=data.get("description", ""),
            extra_headers=data.get("extra_headers", {}),
            api_token=data.get("api_token", ""),
        )


class ProfileManager:
    """
    Manages LLM configuration profiles.

    Features:
    - Built-in default profiles (default, fast, claude, openai)
    - User-defined profiles from config.json
    - Active profile switching
    - Adapter instantiation for profiles
    """

    # Built-in default profiles
    DEFAULT_PROFILES: Dict[str, Dict[str, Any]] = {
        "default": {
            "api_url": "http://localhost:1234",
            "model": "qwen/qwen3-4b",
            "temperature": 0.7,
            "tool_format": "openai",
            "description": "Local LLM for general use",
        },
        "fast": {
            "api_url": "http://localhost:1234",
            "model": "qwen/qwen3-0.6b",
            "temperature": 0.3,
            "tool_format": "openai",
            "description": "Fast local model for quick queries",
        },
        "claude": {
            "api_url": "https://api.anthropic.com",
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.7,
            "max_tokens": 4096,
            "tool_format": "anthropic",
            "description": "Anthropic Claude for complex tasks",
        },
        "openai": {
            "api_url": "https://api.openai.com",
            "model": "gpt-4-turbo",
            "temperature": 0.7,
            "max_tokens": 4096,
            "tool_format": "openai",
            "description": "OpenAI GPT-4 for general tasks",
        },
    }

    def __init__(self, config=None):
        """
        Initialize profile manager.

        Args:
            config: Configuration object with get() method
        """
        self.config = config
        self._profiles: Dict[str, LLMProfile] = {}
        self._active_profile_name: str = "default"
        self._load_profiles()
        # Note: Default profile initialization is now handled by config_utils.initialize_config()
        # which runs earlier in app startup and creates global/local config with profiles

    def _load_profiles(self) -> None:
        """Load profiles from defaults and config file.

        Reads directly from config FILE (not cached config object) to ensure
        we always get the latest saved values.
        """
        # Start with built-in defaults
        for name, data in self.DEFAULT_PROFILES.items():
            self._profiles[name] = LLMProfile.from_dict(name, data)

        # Read profiles directly from config file (not cached config object)
        # This ensures we get the latest saved values after save_profile_values_to_config
        user_profiles, active_profile, default_profile = self._read_profiles_from_file()

        if user_profiles:
            for name, data in user_profiles.items():
                if isinstance(data, dict):
                    self._profiles[name] = LLMProfile.from_dict(name, data)
                    logger.debug(f"Loaded user profile: {name}")

        # Load active profile (last used) - takes priority
        if active_profile and active_profile in self._profiles:
            self._active_profile_name = active_profile
        elif default_profile and default_profile in self._profiles:
            self._active_profile_name = default_profile

        logger.info(
            f"Loaded {len(self._profiles)} profiles, active: {self._active_profile_name}"
        )

    def _read_profiles_from_file(self) -> tuple:
        """Read profiles directly from global config file.

        Profiles are user-level settings and only stored globally.

        Returns:
            Tuple of (profiles_dict, active_profile, default_profile)
        """
        global_config = Path.home() / ".kollabor-cli" / "config.json"

        if global_config.exists():
            try:
                config_data = json.loads(global_config.read_text(encoding="utf-8"))
                llm_config = config_data.get("core", {}).get("llm", {})
                profiles = llm_config.get("profiles", {})
                active = llm_config.get("active_profile")
                default = llm_config.get("default_profile", "default")

                if profiles:
                    logger.debug(f"Loaded profiles from: {global_config}")
                    return profiles, active, default
            except Exception as e:
                logger.warning(f"Failed to read profiles from {global_config}: {e}")

        # Fallback to config object if file read fails
        if self.config:
            return (
                self.config.get("core.llm.profiles", {}),
                self.config.get("core.llm.active_profile"),
                self.config.get("core.llm.default_profile", "default")
            )

        return {}, None, "default"

    def get_profile(self, name: str) -> Optional[LLMProfile]:
        """
        Get a profile by name.

        Args:
            name: Profile name

        Returns:
            LLMProfile or None if not found
        """
        return self._profiles.get(name)

    def get_active_profile(self) -> LLMProfile:
        """
        Get the currently active profile.

        Returns:
            Active LLMProfile (falls back to "default" if needed)
        """
        profile = self._profiles.get(self._active_profile_name)
        if not profile:
            logger.warning(
                f"Active profile '{self._active_profile_name}' not found, "
                "falling back to 'default'"
            )
            profile = self._profiles.get("default")
            if not profile:
                # Create minimal default profile
                profile = LLMProfile(
                    name="default",
                    api_url="http://localhost:1234",
                    model="default",
                )
        return profile

    def set_active_profile(self, name: str, persist: bool = True) -> bool:
        """
        Set the active profile.

        If profile doesn't exist but env vars are set (KOLLABOR_{NAME}_ENDPOINT
        and KOLLABOR_{NAME}_TOKEN), auto-creates the profile from env vars.

        Args:
            name: Profile name to activate
            persist: If True, save the selection to config for next startup

        Returns:
            True if successful, False if profile not found and can't be created
        """
        if name not in self._profiles:
            # Try to auto-create from env vars
            if self._try_create_profile_from_env(name):
                logger.info(f"Auto-created profile '{name}' from environment variables")
            else:
                logger.error(f"Profile not found: {name}")
                return False

        old_profile = self._active_profile_name
        self._active_profile_name = name
        logger.info(f"Switched profile: {old_profile} -> {name}")

        # Persist to config so it survives restart
        if persist:
            self._save_active_profile_to_config(name)

        return True

    def _try_create_profile_from_env(self, name: str) -> bool:
        """
        Try to create a profile from environment variables.

        Checks for KOLLABOR_{NAME}_ENDPOINT and KOLLABOR_{NAME}_TOKEN.
        If both are set, creates a minimal profile that will read all
        values from env vars at runtime.

        Args:
            name: Profile name to create

        Returns:
            True if profile was created, False if required env vars missing
        """
        # Normalize name for env var lookup (same logic as LLMProfile._get_env_key)
        name_normalized = re.sub(r'[^a-zA-Z0-9]', '_', name.strip()).upper()
        endpoint_key = f"KOLLABOR_{name_normalized}_ENDPOINT"
        token_key = f"KOLLABOR_{name_normalized}_TOKEN"

        endpoint = os.environ.get(endpoint_key, "").strip()
        token = os.environ.get(token_key, "").strip()

        # Require at least endpoint to create profile
        if not endpoint:
            logger.debug(f"Cannot auto-create profile '{name}': {endpoint_key} not set")
            return False

        # Create minimal profile - it will read all values from env vars at runtime
        profile = LLMProfile(
            name=name,
            api_url=endpoint,  # Fallback if env var unset later
            model="",  # Will be read from env var
            description=f"Auto-created from environment variables",
        )

        self._profiles[name] = profile
        logger.info(f"Created profile '{name}' from env vars ({endpoint_key})")
        return True

    def _save_active_profile_to_config(self, name: str) -> bool:
        """
        Save the active profile name to global config.json.

        Profiles are user-wide settings, so they're saved to global config
        (~/.kollabor-cli/config.json) to be available across all projects.

        Args:
            name: Profile name to save as active

        Returns:
            True if saved successfully
        """
        try:
            # Profiles are user-wide, always save to global config
            config_path = Path.home() / ".kollabor-cli" / "config.json"

            if not config_path.exists():
                logger.warning(f"Config file not found: {config_path}")
                return False

            config_data = json.loads(config_path.read_text(encoding="utf-8"))

            # Ensure core.llm exists
            if "core" not in config_data:
                config_data["core"] = {}
            if "llm" not in config_data["core"]:
                config_data["core"]["llm"] = {}

            # Save active profile
            config_data["core"]["llm"]["active_profile"] = name

            config_path.write_text(
                json.dumps(config_data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            logger.debug(f"Saved active profile to config: {name}")
            return True

        except Exception as e:
            logger.error(f"Failed to save active profile to config: {e}")
            return False

    def list_profiles(self) -> List[LLMProfile]:
        """
        List all available profiles.

        Returns:
            List of LLMProfile instances
        """
        return list(self._profiles.values())

    def get_profile_names(self) -> List[str]:
        """
        Get list of profile names.

        Returns:
            List of profile name strings
        """
        return list(self._profiles.keys())

    def add_profile(self, profile: LLMProfile) -> bool:
        """
        Add a new profile.

        Args:
            profile: LLMProfile to add

        Returns:
            True if added, False if name already exists
        """
        if profile.name in self._profiles:
            logger.warning(f"Profile already exists: {profile.name}")
            return False

        self._profiles[profile.name] = profile
        logger.info(f"Added profile: {profile.name}")
        return True

    def remove_profile(self, name: str) -> bool:
        """
        Remove a profile.

        Cannot remove built-in profiles or the current active profile.

        Args:
            name: Profile name to remove

        Returns:
            True if removed, False if protected or not found
        """
        if name in self.DEFAULT_PROFILES:
            logger.error(f"Cannot remove built-in profile: {name}")
            return False

        if name == self._active_profile_name:
            logger.error(f"Cannot remove active profile: {name}")
            return False

        if name not in self._profiles:
            logger.error(f"Profile not found: {name}")
            return False

        del self._profiles[name]
        logger.info(f"Removed profile: {name}")
        return True

    def delete_profile(self, name: str) -> bool:
        """
        Delete a profile from memory and config file.

        Cannot delete built-in profiles or the current active profile.

        Args:
            name: Profile name to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        if name in self.DEFAULT_PROFILES:
            logger.error(f"Cannot delete built-in profile: {name}")
            return False

        if name == self._active_profile_name:
            logger.error(f"Cannot delete active profile: {name}")
            return False

        if name not in self._profiles:
            logger.error(f"Profile not found: {name}")
            return False

        # Remove from memory
        del self._profiles[name]

        # Remove from config file
        self._delete_profile_from_config(name)

        logger.info(f"Deleted profile: {name}")
        return True

    def _delete_profile_from_config(self, name: str) -> bool:
        """
        Delete a profile from global config.json.

        Profiles are user-wide settings, so they're deleted from global config
        (~/.kollabor-cli/config.json).

        Args:
            name: Profile name to delete

        Returns:
            True if deleted successfully from config
        """
        try:
            # Profiles are user-wide, always use global config
            config_path = Path.home() / ".kollabor-cli" / "config.json"

            if not config_path.exists():
                logger.warning(f"Config file not found: {config_path}")
                return True  # No config file, nothing to delete

            # Load current config
            config_data = json.loads(config_path.read_text(encoding="utf-8"))

            # Check if profile exists in config
            profiles = config_data.get("core", {}).get("llm", {}).get("profiles", {})
            if name not in profiles:
                logger.debug(f"Profile '{name}' not in config file")
                return True  # Not in config, nothing to delete

            # Remove profile from config
            del config_data["core"]["llm"]["profiles"][name]

            # Write back
            config_path.write_text(
                json.dumps(config_data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            logger.info(f"Deleted profile from config: {name}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete profile from config: {e}")
            return False

    def get_adapter_for_profile(
        self, profile: Optional[LLMProfile] = None
    ) -> BaseAPIAdapter:
        """
        Get the appropriate API adapter for a profile.

        Args:
            profile: Profile to get adapter for (default: active profile)

        Returns:
            Configured API adapter instance
        """
        if profile is None:
            profile = self.get_active_profile()

        if profile.tool_format == "anthropic":
            return AnthropicAdapter(base_url=profile.api_url)
        else:
            return OpenAIAdapter(base_url=profile.api_url)

    def get_active_adapter(self) -> BaseAPIAdapter:
        """
        Get adapter for the active profile.

        Returns:
            Configured API adapter instance
        """
        return self.get_adapter_for_profile(self.get_active_profile())

    def is_active(self, name: str) -> bool:
        """
        Check if a profile is the active one.

        Args:
            name: Profile name

        Returns:
            True if this is the active profile
        """
        return name == self._active_profile_name

    @property
    def active_profile_name(self) -> str:
        """Get the name of the active profile."""
        return self._active_profile_name

    def _get_normalized_name(self, name: str) -> str:
        """Get normalized profile name for env var prefix.

        Strips whitespace and replaces all non-alphanumeric characters with
        underscores, then uppercases the result.

        Args:
            name: The profile name to normalize

        Returns:
            Normalized name suitable for env var prefix

        Examples:
            "my-profile" -> "MY_PROFILE"
            "my.profile" -> "MY_PROFILE"
            "My Profile!" -> "MY_PROFILE_"
            "  fast  " -> "FAST"
        """
        return re.sub(r'[^a-zA-Z0-9]', '_', name.strip()).upper()

    def _check_name_collision(self, new_name: str, exclude_name: Optional[str] = None) -> Optional[str]:
        """Check if new profile name would collide with existing profiles.

        Two profile names collide if they normalize to the same env var prefix,
        which would cause them to share the same environment variables.

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

    def get_profile_summary(self, name: Optional[str] = None) -> str:
        """
        Get a human-readable summary of a profile.

        Args:
            name: Profile name (default: active profile)

        Returns:
            Formatted summary string
        """
        profile = self._profiles.get(name) if name else self.get_active_profile()
        if not profile:
            return f"Profile '{name}' not found"

        hints = profile.get_env_var_hints()
        token_status = "[set]" if hints["token"].is_set else "[not set]"

        native_mode = "native" if profile.get_native_tool_calling() else "xml"
        lines = [
            f"Profile: {profile.name}",
            f"  Endpoint: {profile.get_endpoint() or '(not configured)'}",
            f"  Model: {profile.get_model() or '(not configured)'}",
            f"  Token: {hints['token'].name} {token_status}",
            f"  Temperature: {profile.get_temperature()}",
            f"  Max Tokens: {profile.get_max_tokens() or '(API default)'}",
            f"  Timeout: {profile.get_timeout()}ms",
            f"  Tool Format: {profile.get_tool_format()}",
            f"  Tool Calling: {native_mode}",
        ]
        if profile.description:
            lines.append(f"  Description: {profile.description}")

        return "\n".join(lines)

    def create_profile(
        self,
        name: str,
        api_url: str,
        model: str,
        api_token: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tool_format: str = "openai",
        native_tool_calling: bool = True,
        timeout: int = 0,
        description: str = "",
        save_to_config: bool = True,
    ) -> Optional[LLMProfile]:
        """
        Create a new profile and optionally save to config.

        Args:
            name: Profile name
            api_url: API endpoint URL
            model: Model identifier
            api_token: API token (optional, can use env var instead)
            temperature: Sampling temperature
            max_tokens: Max tokens (None for unlimited)
            tool_format: Tool calling format (openai/anthropic)
            native_tool_calling: Enable native API tool calling (True) or XML mode (False)
            timeout: Request timeout
            description: Human-readable description
            save_to_config: Whether to persist to config.json

        Returns:
            Created LLMProfile or None on failure
        """
        if name in self._profiles:
            logger.warning(f"Profile already exists: {name}")
            return None

        # Check for env var prefix collision
        collision = self._check_name_collision(name)
        if collision:
            logger.error(f"Cannot create profile '{name}': env var prefix collides with "
                         f"existing profile '{collision}' (both normalize to "
                         f"KOLLABOR_{self._get_normalized_name(name)}_*)")
            return None

        profile = LLMProfile(
            name=name,
            api_url=api_url,
            model=model,
            api_token=api_token,
            temperature=temperature,
            max_tokens=max_tokens,
            tool_format=tool_format,
            native_tool_calling=native_tool_calling,
            timeout=timeout,
            description=description,
        )

        self._profiles[name] = profile
        logger.info(f"Created profile: {name}")

        if save_to_config:
            self._save_profile_to_config(profile)

        return profile

    def _save_profile_to_config(self, profile: LLMProfile) -> bool:
        """
        Save a profile to global config.json.

        Profiles are user-wide settings, so they're saved to global config
        (~/.kollabor-cli/config.json) to be available across all projects.

        Args:
            profile: Profile to save

        Returns:
            True if saved successfully
        """
        try:
            # Profiles are user-wide, always save to global config
            config_path = Path.home() / ".kollabor-cli" / "config.json"

            if not config_path.exists():
                logger.error(f"Config file not found: {config_path}")
                return False

            # Load current config
            config_data = json.loads(config_path.read_text(encoding="utf-8"))

            # Ensure core.llm.profiles exists
            if "core" not in config_data:
                config_data["core"] = {}
            if "llm" not in config_data["core"]:
                config_data["core"]["llm"] = {}
            if "profiles" not in config_data["core"]["llm"]:
                config_data["core"]["llm"]["profiles"] = {}

            # Add profile (without name field, as it's the key)
            profile_data = profile.to_dict()
            del profile_data["name"]  # Name is the key
            config_data["core"]["llm"]["profiles"][profile.name] = profile_data

            # Write back
            config_path.write_text(
                json.dumps(config_data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            logger.info(f"Saved profile to config: {profile.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to save profile to config: {e}")
            return False

    def save_profile_values_to_config(self, profile: LLMProfile) -> Dict[str, bool]:
        """
        Save a profile's RESOLVED values (from env vars) to global config.

        Profiles are user-level settings and stored globally only.
        This reads current values using the profile's getter methods
        (which resolve env vars first) and saves them to config.

        Args:
            profile: Profile whose resolved values to save

        Returns:
            Dict with "global" key indicating success
        """
        # Build profile data from resolved getters (reads env vars)
        profile_data = {
            "api_url": profile.get_endpoint(),
            "model": profile.get_model(),
            "temperature": profile.get_temperature(),
            "max_tokens": profile.get_max_tokens(),
            "timeout": profile.get_timeout(),
            "tool_format": profile.get_tool_format(),
            "native_tool_calling": profile.get_native_tool_calling(),
        }

        # Only include token if it's set (don't save None)
        token = profile.get_token()
        if token:
            profile_data["api_token"] = token

        # Include description if set
        if profile.description:
            profile_data["description"] = profile.description

        # Include extra_headers if set
        if profile.extra_headers:
            profile_data["extra_headers"] = profile.extra_headers

        # Profiles are user-level settings, always save to global
        global_config = Path.home() / ".kollabor-cli" / "config.json"

        result = {"global": False, "local": False}
        result["global"] = self._save_profile_data_to_file(
            global_config, profile.name, profile_data
        )

        if result["global"]:
            logger.info(f"Saved profile '{profile.name}' to global config")
        else:
            logger.error(f"Failed to save profile '{profile.name}' to config")

        return result

    def _save_profile_data_to_file(self, config_path: Path, profile_name: str,
                                    profile_data: Dict[str, Any]) -> bool:
        """
        Save profile data to a specific config file.

        Args:
            config_path: Path to config.json file
            profile_name: Name of the profile (used as key)
            profile_data: Profile data dictionary to save

        Returns:
            True if saved successfully
        """
        try:
            if not config_path.exists():
                logger.debug(f"Config file not found, skipping: {config_path}")
                return False

            config_data = json.loads(config_path.read_text(encoding="utf-8"))

            # Ensure core.llm.profiles exists
            if "core" not in config_data:
                config_data["core"] = {}
            if "llm" not in config_data["core"]:
                config_data["core"]["llm"] = {}
            if "profiles" not in config_data["core"]["llm"]:
                config_data["core"]["llm"]["profiles"] = {}

            config_data["core"]["llm"]["profiles"][profile_name] = profile_data

            config_path.write_text(
                json.dumps(config_data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            logger.debug(f"Saved profile to: {config_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save profile to {config_path}: {e}")
            return False

    def reload(self) -> None:
        """Reload profiles from config file, preserving current active profile."""
        # Preserve current active profile name
        current_active = self._active_profile_name
        self._profiles.clear()
        self._load_profiles()
        # Restore active profile if it still exists, otherwise keep what _load_profiles set
        if current_active in self._profiles:
            self._active_profile_name = current_active
        logger.debug(f"Reloaded {len(self._profiles)} profiles, active: {self._active_profile_name}")

    def update_profile(
        self,
        original_name: str,
        new_name: str = None,
        api_url: str = None,
        model: str = None,
        api_token: str = None,
        temperature: float = None,
        max_tokens: Optional[int] = None,
        tool_format: str = None,
        native_tool_calling: bool = None,
        timeout: int = None,
        description: str = None,
        save_to_config: bool = True,
    ) -> bool:
        """
        Update an existing profile.

        Args:
            original_name: Current name of the profile to update
            new_name: New name for the profile (optional, for renaming)
            api_url: New API endpoint URL
            model: New model identifier
            api_token: New API token
            temperature: New sampling temperature
            max_tokens: New max tokens
            tool_format: New tool calling format
            native_tool_calling: Enable native API tool calling (True) or XML mode (False)
            timeout: New request timeout
            description: New description
            save_to_config: Whether to persist to config.json

        Returns:
            True if updated successfully, False otherwise
        """
        if original_name not in self._profiles:
            logger.error(f"Profile not found: {original_name}")
            return False

        profile = self._profiles[original_name]
        target_name = new_name or original_name

        # If renaming, check for collision and warn about env var change
        if new_name and new_name != original_name:
            collision = self._check_name_collision(new_name, exclude_name=original_name)
            if collision:
                logger.error(f"Cannot rename to '{new_name}': env var prefix collides with "
                             f"existing profile '{collision}'")
                return False

            # Warn user about env var change
            old_prefix = self._get_normalized_name(original_name)
            new_prefix = self._get_normalized_name(new_name)
            if old_prefix != new_prefix:
                logger.warning(f"Profile renamed: env vars changed from KOLLABOR_{old_prefix}_* "
                               f"to KOLLABOR_{new_prefix}_*. Update your environment variables.")

        # Update profile fields
        if api_url is not None:
            profile.api_url = api_url
        if model is not None:
            profile.model = model
        if api_token is not None:
            profile.api_token = api_token
        if temperature is not None:
            profile.temperature = temperature
        if max_tokens is not None:
            profile.max_tokens = max_tokens
        if tool_format is not None:
            profile.tool_format = tool_format
        if native_tool_calling is not None:
            profile.native_tool_calling = native_tool_calling
        if timeout is not None:
            profile.timeout = timeout
        if description is not None:
            profile.description = description

        # Handle renaming
        if new_name and new_name != original_name:
            profile.name = new_name
            del self._profiles[original_name]
            self._profiles[new_name] = profile

            # Update active profile name if this was the active one
            if self._active_profile_name == original_name:
                self._active_profile_name = new_name

            logger.info(f"Renamed profile: {original_name} -> {new_name}")

        logger.info(f"Updated profile: {target_name}")

        if save_to_config:
            self._update_profile_in_config(original_name, profile)

        return True

    def _update_profile_in_config(self, original_name: str, profile: LLMProfile) -> bool:
        """
        Update a profile in global config.json.

        Profiles are user-wide settings, so they're saved to global config
        (~/.kollabor-cli/config.json) to be available across all projects.

        Args:
            original_name: Original profile name (for removal if renamed)
            profile: Updated profile to save

        Returns:
            True if saved successfully
        """
        try:
            # Profiles are user-wide, always save to global config
            config_path = Path.home() / ".kollabor-cli" / "config.json"

            if not config_path.exists():
                logger.error(f"Config file not found: {config_path}")
                return False

            # Load current config
            config_data = json.loads(config_path.read_text(encoding="utf-8"))

            # Ensure core.llm.profiles exists
            if "core" not in config_data:
                config_data["core"] = {}
            if "llm" not in config_data["core"]:
                config_data["core"]["llm"] = {}
            if "profiles" not in config_data["core"]["llm"]:
                config_data["core"]["llm"]["profiles"] = {}

            # Remove old profile if it was renamed
            if original_name != profile.name and original_name in config_data["core"]["llm"]["profiles"]:
                del config_data["core"]["llm"]["profiles"][original_name]

            # Add/update profile (without name field, as it's the key)
            profile_data = profile.to_dict()
            del profile_data["name"]  # Name is the key
            config_data["core"]["llm"]["profiles"][profile.name] = profile_data

            # Write back
            config_path.write_text(
                json.dumps(config_data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            logger.info(f"Updated profile in config: {profile.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to update profile in config: {e}")
            return False
