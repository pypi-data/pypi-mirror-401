"""
Tests for LLMProfile environment variable resolution.

Tests follow the specification in docs/specs/DYNAMIC_PROFILE_ENV_VARS.md
Phase E: Testing - Tests 1-24
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from core.llm.profile_manager import LLMProfile, ProfileManager, EnvVarHint


class TestResolutionPriority(unittest.TestCase):
    """Tests 1-3: Resolution Priority - env var > config > default."""

    def setUp(self):
        """Set up clean environment for each test."""
        self.original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_1_env_var_takes_precedence(self):
        """Test 1: Env var takes precedence over config value."""
        profile = LLMProfile(
            name="test",
            api_url="http://config.example.com",
            model="config-model",
            temperature=0.5,
            max_tokens=1000,
            timeout=10000,
            tool_format="anthropic",
        )

        # Set env vars
        os.environ["KOLLABOR_TEST_ENDPOINT"] = "http://env.example.com"
        os.environ["KOLLABOR_TEST_MODEL"] = "env-model"
        os.environ["KOLLABOR_TEST_TEMPERATURE"] = "0.9"
        os.environ["KOLLABOR_TEST_MAX_TOKENS"] = "5000"
        os.environ["KOLLABOR_TEST_TIMEOUT"] = "60000"
        os.environ["KOLLABOR_TEST_TOOL_FORMAT"] = "openai"
        os.environ["KOLLABOR_TEST_TOKEN"] = "env-token"

        # Verify env vars take precedence
        self.assertEqual(profile.get_endpoint(), "http://env.example.com")
        self.assertEqual(profile.get_model(), "env-model")
        self.assertEqual(profile.get_temperature(), 0.9)
        self.assertEqual(profile.get_max_tokens(), 5000)
        self.assertEqual(profile.get_timeout(), 60000)
        self.assertEqual(profile.get_tool_format(), "openai")
        self.assertEqual(profile.get_token(), "env-token")

    def test_2_config_value_used_when_env_unset(self):
        """Test 2: Config value is used when env var is unset."""
        profile = LLMProfile(
            name="test",
            api_url="http://config.example.com",
            model="config-model",
            temperature=0.5,
            max_tokens=1000,
            timeout=10000,
            tool_format="anthropic",
            api_token="config-token",
        )

        # No env vars set - should use config values
        self.assertEqual(profile.get_endpoint(), "http://config.example.com")
        self.assertEqual(profile.get_model(), "config-model")
        self.assertEqual(profile.get_temperature(), 0.5)
        self.assertEqual(profile.get_max_tokens(), 1000)
        self.assertEqual(profile.get_timeout(), 10000)
        self.assertEqual(profile.get_tool_format(), "anthropic")
        self.assertEqual(profile.get_token(), "config-token")

    def test_3_default_used_when_both_unset(self):
        """Test 3: Default value used when both env var and config are unset."""
        # Create profile with None values for optional fields
        profile = LLMProfile(
            name="test",
            api_url="",  # Empty - required field
            model="",  # Empty - required field
            temperature=None,  # None - should default to 0.7
            max_tokens=None,  # None - should stay None (API default)
            timeout=None,  # None - should default to 30000
            tool_format="",  # Empty - should default to "openai"
        )

        # No env vars set - verify defaults for optional fields
        self.assertEqual(profile.get_temperature(), 0.7)
        self.assertIsNone(profile.get_max_tokens())
        self.assertEqual(profile.get_timeout(), 30000)
        self.assertEqual(profile.get_tool_format(), "openai")

        # Required fields return empty string when not configured
        self.assertEqual(profile.get_endpoint(), "")
        self.assertEqual(profile.get_model(), "")


class TestProfileNameNormalization(unittest.TestCase):
    """Tests 4-6: Profile name normalization for env var keys."""

    def setUp(self):
        """Set up clean environment."""
        self.original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_4_hyphen_to_underscore(self):
        """Test 4: my-llm -> KOLLABOR_MY_LLM_TOKEN."""
        profile = LLMProfile(
            name="my-llm",
            api_url="http://example.com",
            model="test-model",
        )

        self.assertEqual(profile._get_env_key("TOKEN"), "KOLLABOR_MY_LLM_TOKEN")
        self.assertEqual(profile._get_env_key("ENDPOINT"), "KOLLABOR_MY_LLM_ENDPOINT")
        self.assertEqual(profile._get_env_key("MODEL"), "KOLLABOR_MY_LLM_MODEL")

    def test_5_dot_to_underscore(self):
        """Test 5: my.profile -> KOLLABOR_MY_PROFILE_TOKEN."""
        profile = LLMProfile(
            name="my.profile",
            api_url="http://example.com",
            model="test-model",
        )

        self.assertEqual(profile._get_env_key("TOKEN"), "KOLLABOR_MY_PROFILE_TOKEN")
        self.assertEqual(profile._get_env_key("ENDPOINT"), "KOLLABOR_MY_PROFILE_ENDPOINT")

    def test_6_special_chars_to_underscore(self):
        """Test 6: My Profile! -> KOLLABOR_MY_PROFILE__TOKEN."""
        profile = LLMProfile(
            name="My Profile!",
            api_url="http://example.com",
            model="test-model",
        )

        # Space and ! both become underscores
        self.assertEqual(profile._get_env_key("TOKEN"), "KOLLABOR_MY_PROFILE__TOKEN")
        self.assertEqual(profile._get_env_key("ENDPOINT"), "KOLLABOR_MY_PROFILE__ENDPOINT")


class TestProfileNameCollisionPrevention(unittest.TestCase):
    """Tests 7-9: Profile name collision detection."""

    def setUp(self):
        """Set up profile manager."""
        self.original_environ = os.environ.copy()
        os.environ.clear()
        self.manager = ProfileManager(config=None)
        # Clear all user profiles from config to start fresh
        # Keep only built-in defaults (default, fast, claude, openai)
        from core.llm.profile_manager import ProfileManager as PM
        user_profile_names = [name for name in self.manager._profiles.keys()
                             if name not in PM.DEFAULT_PROFILES]
        for name in user_profile_names:
            del self.manager._profiles[name]

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_7_collision_on_create(self):
        """Test 7: Create my-profile, then create my_profile - should fail."""
        # First profile created successfully
        profile1 = self.manager.create_profile(
            name="my-profile",
            api_url="http://example.com",
            model="model1",
            save_to_config=False,  # Don't persist to config during test
        )
        self.assertIsNotNone(profile1)

        # Second profile with same normalized name should fail
        profile2 = self.manager.create_profile(
            name="my_profile",
            api_url="http://example.com",
            model="model2",
            save_to_config=False,  # Don't persist to config during test
        )
        self.assertIsNone(profile2)

    def test_8_collision_on_rename(self):
        """Test 8: Create my-profile, rename another to my.profile - should fail."""
        # Create two distinct profiles
        self.manager.create_profile(
            name="my-profile",
            api_url="http://example.com",
            model="model1",
            save_to_config=False,
        )
        self.manager.create_profile(
            name="other",
            api_url="http://example.com",
            model="model2",
            save_to_config=False,
        )

        # Renaming 'other' to 'my.profile' should collide with 'my-profile'
        result = self.manager.update_profile(
            original_name="other",
            new_name="my.profile",
        )
        self.assertFalse(result)

    def test_9_self_rename_same_normalized_allowed(self):
        """Test 9: Create my-profile, rename to my_profile (same normalized) - succeeds."""
        profile = self.manager.create_profile(
            name="my-profile",
            api_url="http://example.com",
            model="model1",
            save_to_config=False,
        )
        self.assertIsNotNone(profile)

        # Renaming to same normalized name should succeed
        result = self.manager.update_profile(
            original_name="my-profile",
            new_name="my_profile",
        )
        self.assertTrue(result)

        # Profile should exist under new name
        self.assertIsNotNone(self.manager.get_profile("my_profile"))
        self.assertIsNone(self.manager.get_profile("my-profile"))


class TestEmptyStringHandling(unittest.TestCase):
    """Tests 10-11: Empty string handling - should fall through without warning."""

    def setUp(self):
        """Set up clean environment."""
        self.original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_10_empty_string_falls_through_to_config(self):
        """Test 10: Empty string env var falls through to config (no warning)."""
        profile = LLMProfile(
            name="claude",
            api_url="http://config.example.com",
            model="config-model",
            temperature=0.5,
        )

        # Set env var to empty string
        os.environ["KOLLABOR_CLAUDE_MODEL"] = ""
        os.environ["KOLLABOR_CLAUDE_TEMPERATURE"] = ""

        # Should fall through to config values
        self.assertEqual(profile.get_model(), "config-model")
        self.assertEqual(profile.get_temperature(), 0.5)

    def test_11_empty_string_with_empty_config_uses_default(self):
        """Test 11: Empty string env var with empty config uses default (optional field)."""
        profile = LLMProfile(
            name="claude",
            api_url="http://example.com",
            model="model",
            temperature=None,  # Empty config
        )

        # Set env var to empty string
        os.environ["KOLLABOR_CLAUDE_TEMPERATURE"] = ""

        # Should fall through to default 0.7 (no warning for optional field)
        self.assertEqual(profile.get_temperature(), 0.7)


class TestZeroValueHandling(unittest.TestCase):
    """Tests 12-14: Zero value handling - 0 is valid, not treated as unset."""

    def setUp(self):
        """Set up clean environment."""
        self.original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_12_zero_max_tokens_preserved(self):
        """Test 12: MAX_TOKENS=0 returns 0 (not treated as unset)."""
        profile = LLMProfile(
            name="fast",
            api_url="http://example.com",
            model="model",
        )

        os.environ["KOLLABOR_FAST_MAX_TOKENS"] = "0"

        # Should return 0, not None or config value
        self.assertEqual(profile.get_max_tokens(), 0)

    def test_13_zero_temperature_preserved(self):
        """Test 13: TEMPERATURE=0 returns 0.0 (not treated as unset)."""
        profile = LLMProfile(
            name="fast",
            api_url="http://example.com",
            model="model",
            temperature=0.7,
        )

        os.environ["KOLLABOR_FAST_TEMPERATURE"] = "0"

        # Should return 0.0, not config value
        self.assertEqual(profile.get_temperature(), 0.0)

    def test_14_zero_timeout_preserved(self):
        """Test 14: TIMEOUT=0 returns 0 (not treated as unset)."""
        profile = LLMProfile(
            name="fast",
            api_url="http://example.com",
            model="model",
            timeout=30000,
        )

        os.environ["KOLLABOR_FAST_TIMEOUT"] = "0"

        # Should return 0 (meaning no timeout), not default 30000
        self.assertEqual(profile.get_timeout(), 0)


class TestInvalidValueWarnings(unittest.TestCase):
    """Tests 15-17: Invalid value warnings - log warning and fall back."""

    def setUp(self):
        """Set up clean environment."""
        self.original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    @patch('core.llm.profile_manager.logger')
    def test_15_invalid_max_tokens_warns(self, mock_logger):
        """Test 15: Invalid MAX_TOKENS logs warning and uses config value."""
        profile = LLMProfile(
            name="fast",
            api_url="http://example.com",
            model="model",
            max_tokens=1000,
        )

        os.environ["KOLLABOR_FAST_MAX_TOKENS"] = "abc"

        result = profile.get_max_tokens()

        # Should fall back to config value
        self.assertEqual(result, 1000)

        # Should log warning
        mock_logger.warning.assert_called()
        warning_msg = mock_logger.warning.call_args[0][0]
        self.assertIn("not a valid integer", warning_msg)
        self.assertIn("KOLLABOR_FAST_MAX_TOKENS", warning_msg)
        self.assertIn("abc", warning_msg)

    @patch('core.llm.profile_manager.logger')
    def test_16_invalid_temperature_warns(self, mock_logger):
        """Test 16: Invalid TEMPERATURE logs warning and falls back to 0.7."""
        profile = LLMProfile(
            name="fast",
            api_url="http://example.com",
            model="model",
            temperature=None,
        )

        os.environ["KOLLABOR_FAST_TEMPERATURE"] = "not-a-number"

        result = profile.get_temperature()

        # Should fall back to default 0.7
        self.assertEqual(result, 0.7)

        # Should log warning
        mock_logger.warning.assert_called()
        warning_msg = mock_logger.warning.call_args[0][0]
        self.assertIn("not a valid float", warning_msg)
        self.assertIn("KOLLABOR_FAST_TEMPERATURE", warning_msg)
        self.assertIn("not-a-number", warning_msg)

    @patch('core.llm.profile_manager.logger')
    def test_17_invalid_tool_format_warns(self, mock_logger):
        """Test 17: Invalid TOOL_FORMAT logs warning and falls back to config value."""
        profile = LLMProfile(
            name="fast",
            api_url="http://example.com",
            model="model",
            tool_format="anthropic",
        )

        os.environ["KOLLABOR_FAST_TOOL_FORMAT"] = "custom"

        result = profile.get_tool_format()

        # Should fall back to config value "anthropic"
        self.assertEqual(result, "anthropic")

        # Should log warning
        mock_logger.warning.assert_called()
        warning_msg = mock_logger.warning.call_args[0][0]
        self.assertIn("is invalid", warning_msg)
        self.assertIn("KOLLABOR_FAST_TOOL_FORMAT", warning_msg)
        self.assertIn("custom", warning_msg)

    @patch('core.llm.profile_manager.logger')
    def test_17b_invalid_tool_format_falls_back_to_openai(self, mock_logger):
        """Test 17b: Invalid TOOL_FORMAT with invalid config falls back to 'openai'."""
        profile = LLMProfile(
            name="fast",
            api_url="http://example.com",
            model="model",
            tool_format="",  # Empty/invalid config
        )

        os.environ["KOLLABOR_FAST_TOOL_FORMAT"] = "custom"

        result = profile.get_tool_format()

        # Should fall back to default "openai" when both env and config are invalid
        self.assertEqual(result, "openai")


class TestRequiredFieldWarnings(unittest.TestCase):
    """Tests 18-20: Required field warnings - warn when both env and config are empty."""

    def setUp(self):
        """Set up clean environment."""
        self.original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    @patch('core.llm.profile_manager.logger')
    def test_18_no_token_warns(self, mock_logger):
        """Test 18: No TOKEN in env or config logs warning."""
        profile = LLMProfile(
            name="test",
            api_url="http://example.com",
            model="model",
            api_token="",  # Empty config
        )

        # No env var set
        result = profile.get_token()

        # Should return None
        self.assertIsNone(result)

        # Should log warning
        mock_logger.warning.assert_called()
        warning_msg = mock_logger.warning.call_args[0][0]
        self.assertIn("No API token configured", warning_msg)
        self.assertIn("KOLLABOR_TEST_TOKEN", warning_msg)

    @patch('core.llm.profile_manager.logger')
    def test_19_no_endpoint_warns(self, mock_logger):
        """Test 19: No ENDPOINT in env or config logs warning."""
        profile = LLMProfile(
            name="test",
            api_url="",  # Empty config
            model="model",
        )

        # No env var set
        result = profile.get_endpoint()

        # Should return empty string
        self.assertEqual(result, "")

        # Should log warning
        mock_logger.warning.assert_called()
        warning_msg = mock_logger.warning.call_args[0][0]
        self.assertIn("No endpoint configured", warning_msg)
        self.assertIn("KOLLABOR_TEST_ENDPOINT", warning_msg)

    @patch('core.llm.profile_manager.logger')
    def test_20_no_model_warns(self, mock_logger):
        """Test 20: No MODEL in env or config logs warning."""
        profile = LLMProfile(
            name="test",
            api_url="http://example.com",
            model="",  # Empty config
        )

        # No env var set
        result = profile.get_model()

        # Should return empty string
        self.assertEqual(result, "")

        # Should log warning
        mock_logger.warning.assert_called()
        warning_msg = mock_logger.warning.call_args[0][0]
        self.assertIn("No model configured", warning_msg)
        self.assertIn("KOLLABOR_TEST_MODEL", warning_msg)


class TestOptionalFieldDefaults(unittest.TestCase):
    """Tests 21-24: Optional field defaults - sensible defaults when not configured."""

    def setUp(self):
        """Set up clean environment."""
        self.original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_21_no_max_tokens_returns_none(self):
        """Test 21: No MAX_TOKENS configured returns None (API default)."""
        profile = LLMProfile(
            name="test",
            api_url="http://example.com",
            model="model",
            max_tokens=None,  # Not configured
        )

        result = profile.get_max_tokens()

        # Should return None (uses API default)
        self.assertIsNone(result)

    def test_22_no_temperature_returns_default(self):
        """Test 22: No TEMPERATURE configured returns 0.7."""
        profile = LLMProfile(
            name="test",
            api_url="http://example.com",
            model="model",
            temperature=None,  # Not configured
        )

        result = profile.get_temperature()

        # Should return default 0.7
        self.assertEqual(result, 0.7)

    def test_23_no_timeout_returns_default(self):
        """Test 23: No TIMEOUT configured returns 30000."""
        profile = LLMProfile(
            name="test",
            api_url="http://example.com",
            model="model",
            timeout=None,  # Not configured
        )

        result = profile.get_timeout()

        # Should return default 30000
        self.assertEqual(result, 30000)

    def test_24_no_tool_format_returns_default(self):
        """Test 24: No TOOL_FORMAT configured returns 'openai'."""
        profile = LLMProfile(
            name="test",
            api_url="http://example.com",
            model="model",
            tool_format="",  # Not configured (empty string)
        )

        result = profile.get_tool_format()

        # Should return default "openai"
        self.assertEqual(result, "openai")


class TestEnvVarHints(unittest.TestCase):
    """Additional tests for get_env_var_hints() functionality."""

    def setUp(self):
        """Set up clean environment."""
        self.original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_env_var_hints_structure(self):
        """Test get_env_var_hints returns correct structure."""
        profile = LLMProfile(
            name="claude",
            api_url="https://api.anthropic.com",
            model="claude-sonnet-4-20250514",
        )

        hints = profile.get_env_var_hints()

        # Check structure
        self.assertIsInstance(hints, dict)
        self.assertIn("endpoint", hints)
        self.assertIn("token", hints)
        self.assertIn("model", hints)
        self.assertIn("max_tokens", hints)
        self.assertIn("temperature", hints)
        self.assertIn("timeout", hints)
        self.assertIn("tool_format", hints)

        # Check each hint is an EnvVarHint
        for hint in hints.values():
            self.assertIsInstance(hint, EnvVarHint)
            self.assertIsInstance(hint.name, str)
            self.assertIsInstance(hint.is_set, bool)

    def test_env_var_hints_names(self):
        """Test get_env_var_hints returns correct env var names."""
        profile = LLMProfile(
            name="my-local-llm",
            api_url="http://example.com",
            model="model",
        )

        hints = profile.get_env_var_hints()

        self.assertEqual(hints["endpoint"].name, "KOLLABOR_MY_LOCAL_LLM_ENDPOINT")
        self.assertEqual(hints["token"].name, "KOLLABOR_MY_LOCAL_LLM_TOKEN")
        self.assertEqual(hints["model"].name, "KOLLABOR_MY_LOCAL_LLM_MODEL")

    def test_env_var_hints_is_set(self):
        """Test get_env_var_hints is_set reflects actual env state."""
        profile = LLMProfile(
            name="claude",
            api_url="https://api.anthropic.com",
            model="claude-sonnet-4-20250514",
        )

        # Initially not set
        hints = profile.get_env_var_hints()
        self.assertFalse(hints["token"].is_set)

        # Set env var
        os.environ["KOLLABOR_CLAUDE_TOKEN"] = "sk-ant-xxx"
        hints = profile.get_env_var_hints()
        self.assertTrue(hints["token"].is_set)


class TestWhitespaceHandling(unittest.TestCase):
    """Test 33: Whitespace handling in profile names."""

    def test_33_whitespace_stripped_from_name(self):
        """Test 33: Profile name '  fast  ' normalizes to KOLLABOR_FAST_TOKEN."""
        profile = LLMProfile(
            name="  fast  ",
            api_url="http://example.com",
            model="model",
        )

        # Whitespace should be stripped, resulting in KOLLABOR_FAST_TOKEN
        self.assertEqual(profile._get_env_key("TOKEN"), "KOLLABOR_FAST_TOKEN")
        self.assertEqual(profile._get_env_key("ENDPOINT"), "KOLLABOR_FAST_ENDPOINT")


if __name__ == "__main__":
    unittest.main()
