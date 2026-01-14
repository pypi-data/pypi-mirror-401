"""
Integration Tests for Dynamic Profile Environment Variables.

Tests follow the specification in docs/specs/DYNAMIC_PROFILE_ENV_VARS.md
Phase E: Testing - Tests 25-38

Tests:
- 25-30: Removal Verification (api_token_env field, global env vars, config keys)
- 31-32: Profile Rename Warning
- 33: Whitespace Handling (already in test_profile_env_vars.py)
- 34-35: get_env_var_hints()
- 36-37: APICommunicationService Init
- 38: from_dict() Forward Compatibility
"""

import inspect
import os
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path
from tempfile import TemporaryDirectory

from core.llm.profile_manager import LLMProfile, ProfileManager, EnvVarHint
from core.llm.api_communication_service import APICommunicationService


class TestRemovalVerification(unittest.TestCase):
    """Tests 25-30: Verify removed fields and global fallbacks are gone."""

    def test_25_api_token_env_field_removed(self):
        """Test 25: api_token_env field is fully removed from LLMProfile."""
        # Check LLMProfile dataclass fields
        profile_fields = {f.name for f in LLMProfile.__dataclass_fields__.values()}

        # api_token_env should NOT be in the fields
        self.assertNotIn("api_token_env", profile_fields)

        # Verify expected fields ARE present
        expected_fields = {
            "name", "api_url", "model", "temperature", "max_tokens",
            "tool_format", "timeout", "description", "extra_headers", "api_token"
        }
        for field in expected_fields:
            self.assertIn(field, profile_fields)

    def test_26_kollabor_api_token_removed(self):
        """Test 26: KOLLABOR_API_TOKEN global fallback is removed."""
        # Read APICommunicationService source
        source_path = Path(__file__).parent.parent / "core" / "llm" / "api_communication_service.py"
        source_code = source_path.read_text()

        # KOLLABOR_API_TOKEN should NOT appear in the source
        self.assertNotIn("KOLLABOR_API_TOKEN", source_code)

    def test_27_kollabor_api_key_removed(self):
        """Test 27: KOLLABOR_API_KEY global fallback is removed."""
        # Read APICommunicationService source
        source_path = Path(__file__).parent.parent / "core" / "llm" / "api_communication_service.py"
        source_code = source_path.read_text()

        # KOLLABOR_API_KEY should NOT appear in the source
        self.assertNotIn("KOLLABOR_API_KEY", source_code)

    def test_28_kollabor_api_temperature_removed(self):
        """Test 28: KOLLABOR_API_TEMPERATURE global fallback is removed."""
        # Read APICommunicationService source
        source_path = Path(__file__).parent.parent / "core" / "llm" / "api_communication_service.py"
        source_code = source_path.read_text()

        # KOLLABOR_API_TEMPERATURE should NOT appear in the source
        self.assertNotIn("KOLLABOR_API_TEMPERATURE", source_code)

    def test_29_kollabor_api_timeout_removed(self):
        """Test 29: KOLLABOR_API_TIMEOUT global fallback is removed."""
        # Read APICommunicationService source
        source_path = Path(__file__).parent.parent / "core" / "llm" / "api_communication_service.py"
        source_code = source_path.read_text()

        # KOLLABOR_API_TIMEOUT should NOT appear in the source
        self.assertNotIn("KOLLABOR_API_TIMEOUT", source_code)

    def test_30_core_llm_api_token_config_removed(self):
        """Test 30: core.llm.api_token config key is removed."""
        # Read APICommunicationService source
        source_path = Path(__file__).parent.parent / "core" / "llm" / "api_communication_service.py"
        source_code = source_path.read_text()

        # core.llm.api_token should NOT appear in the source
        self.assertNotIn('core.llm.api_token', source_code)
        self.assertNotIn('"core.llm.api_token"', source_code)
        self.assertNotIn("'core.llm.api_token'", source_code)


class TestProfileRenameWarning(unittest.TestCase):
    """Tests 31-32: Profile rename warning behavior."""

    def setUp(self):
        """Set up clean environment."""
        self.original_environ = os.environ.copy()
        os.environ.clear()
        self.manager = ProfileManager(config=None)
        # Clear all user profiles from config to start fresh
        from core.llm.profile_manager import ProfileManager as PM
        user_profile_names = [name for name in self.manager._profiles.keys()
                             if name not in PM.DEFAULT_PROFILES]
        for name in user_profile_names:
            del self.manager._profiles[name]

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    @patch('core.llm.profile_manager.logger')
    def test_31_rename_warns_about_env_var_change(self, mock_logger):
        """Test 31: Rename claude to anthropic logs warning about env var change."""
        # Use a custom profile since default profiles can't be created
        profile = self.manager.create_profile(
            name="my-claude-profile",
            save_to_config=False,
            api_url="https://api.anthropic.com",
            model="claude-sonnet-4-20250514",
        )
        self.assertIsNotNone(profile)

        # Clear any previous calls
        mock_logger.warning.reset_mock()

        # Rename to anthropic (different normalized name: MY_ANTHROPIC_PROFILE)
        result = self.manager.update_profile(
            original_name="my-claude-profile",
            new_name="my-anthropic-profile",
        )

        self.assertTrue(result)

        # Should log warning about env var change
        mock_logger.warning.assert_called()
        warning_msg = mock_logger.warning.call_args[0][0]
        self.assertIn("Profile renamed", warning_msg)
        self.assertIn("KOLLABOR_MY_CLAUDE_PROFILE", warning_msg)
        self.assertIn("KOLLABOR_MY_ANTHROPIC_PROFILE", warning_msg)
        self.assertIn("Update your environment variables", warning_msg)

    @patch('core.llm.profile_manager.logger')
    def test_32_rename_same_normalized_no_warning(self, mock_logger):
        """Test 32: Rename fast to FAST (same normalized) no warning logged."""
        # Use a custom profile since default profiles can't be created
        profile = self.manager.create_profile(
            name="my-fast-profile",
            api_url="http://localhost:1234",
            model="qwen/qwen3-0.6b",
            save_to_config=False,
        )
        self.assertIsNotNone(profile)

        # Clear any previous calls
        mock_logger.warning.reset_mock()

        # Rename to MY_FAST_PROFILE (same normalized name)
        result = self.manager.update_profile(
            original_name="my-fast-profile",
            new_name="MY_FAST_PROFILE",
        )

        self.assertTrue(result)

        # Should NOT log warning about env var change (normalized names are same)
        # Note: There may be other warnings, so we check specifically for the env var warning
        for call in mock_logger.warning.call_args_list:
            warning_msg = call[0][0] if call[0] else ""
            # Should not contain the env var change warning
            self.assertNotIn("env vars changed from KOLLABOR_MY_FAST_PROFILE", warning_msg)


class TestGetEnvVarHints(unittest.TestCase):
    """Tests 34-35: get_env_var_hints() functionality."""

    def setUp(self):
        """Set up clean environment."""
        self.original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_34_get_env_var_hints_returns_correct_structure(self):
        """Test 34: get_env_var_hints returns dict with name and is_set for each field."""
        profile = LLMProfile(
            name="claude",
            api_url="https://api.anthropic.com",
            model="claude-sonnet-4-20250514",
        )

        hints = profile.get_env_var_hints()

        # Verify it's a dict
        self.assertIsInstance(hints, dict)

        # Verify all expected fields are present
        expected_fields = ["endpoint", "token", "model", "max_tokens", "temperature", "timeout", "tool_format"]
        for field in expected_fields:
            self.assertIn(field, hints)

        # Verify each value is an EnvVarHint with name and is_set
        for field_name, hint in hints.items():
            self.assertIsInstance(hint, EnvVarHint)
            self.assertIsInstance(hint.name, str)
            self.assertIsInstance(hint.is_set, bool)
            # Name should be KOLLABOR_CLAUDE_{FIELD}
            self.assertTrue(hint.name.startswith("KOLLABOR_CLAUDE_"))

    def test_35_env_var_hints_is_set_reflects_env_state(self):
        """Test 35: Set KOLLABOR_CLAUDE_TOKEN, verify hints.token.is_set == True."""
        profile = LLMProfile(
            name="claude",
            api_url="https://api.anthropic.com",
            model="claude-sonnet-4-20250514",
        )

        # Initially not set
        hints = profile.get_env_var_hints()
        self.assertFalse(hints["token"].is_set)
        self.assertFalse(hints["endpoint"].is_set)
        self.assertFalse(hints["model"].is_set)

        # Set env var
        os.environ["KOLLABOR_CLAUDE_TOKEN"] = "sk-ant-xxx"
        os.environ["KOLLABOR_CLAUDE_ENDPOINT"] = "http://custom.example.com"
        os.environ["KOLLABOR_CLAUDE_MODEL"] = "custom-model"

        # Now should be set
        hints = profile.get_env_var_hints()
        self.assertTrue(hints["token"].is_set)
        self.assertTrue(hints["endpoint"].is_set)
        self.assertTrue(hints["model"].is_set)

        # Verify the name is correct
        self.assertEqual(hints["token"].name, "KOLLABOR_CLAUDE_TOKEN")
        self.assertEqual(hints["endpoint"].name, "KOLLABOR_CLAUDE_ENDPOINT")
        self.assertEqual(hints["model"].name, "KOLLABOR_CLAUDE_MODEL")


class TestAPICommunicationServiceInit(unittest.TestCase):
    """Tests 36-37: APICommunicationService initialization."""

    def test_36_requires_profile_parameter(self):
        """Test 36: APICommunicationService.__init__ requires profile parameter."""
        import inspect
        # Get the __init__ signature
        sig = inspect.signature(APICommunicationService.__init__)
        params = sig.parameters

        # Verify 'profile' is a required parameter
        self.assertIn("profile", params)

        # profile should not have a default value (required)
        # inspect.Parameter.empty means no default (required parameter)
        from inspect import Parameter
        self.assertEqual(params["profile"].default, Parameter.empty)
        self.assertEqual(params["config"].default, Parameter.empty)
        self.assertEqual(params["raw_conversations_dir"].default, Parameter.empty)

    def test_37_no_global_env_var_fallbacks(self):
        """Test 37: No global env var fallbacks in __init__ or update_from_profile."""
        # Read APICommunicationService source
        source_path = Path(__file__).parent.parent / "core" / "llm" / "api_communication_service.py"
        source_code = source_path.read_text()

        # Verify no global env var reads in __init__ or update_from_profile
        # These patterns should NOT appear:
        banned_patterns = [
            'os.environ.get("KOLLABOR_API_TOKEN',
            'os.environ.get("KOLLABOR_API_KEY',
            'os.environ.get("KOLLABOR_API_TEMPERATURE',
            'os.environ.get("KOLLABOR_API_TIMEOUT',
            "os.environ.get('KOLLABOR_API_TOKEN",
            "os.environ.get('KOLLABOR_API_KEY",
            "os.environ.get('KOLLABOR_API_TEMPERATURE",
            "os.environ.get('KOLLABOR_API_TIMEOUT",
        ]

        for pattern in banned_patterns:
            self.assertNotIn(pattern, source_code,
                           f"Found banned pattern: {pattern}")

    def test_37_uses_profile_getter_methods(self):
        """Test 37b: update_from_profile uses profile getter methods."""
        # Create a mock config
        config = MagicMock()
        config.get.side_effect = lambda key, default: {
            "core.llm.enable_streaming": False,
            "core.llm.http_connector_limit": 100,
            "core.llm.http_limit_per_host": 20,
            "core.llm.keepalive_timeout": 30,
            "core.llm.api_poll_delay": 0.01,
        }.get(key, default)

        # Create a temporary directory for raw conversations
        temp_dir = TemporaryDirectory()

        # Create a profile
        profile = LLMProfile(
            name="test",
            api_url="http://example.com",
            model="test-model",
            temperature=0.5,
            max_tokens=1000,
            timeout=10000,
            tool_format="openai",
        )

        # Set env vars to verify they're used via getter methods
        os.environ["KOLLABOR_TEST_ENDPOINT"] = "http://env-example.com"
        os.environ["KOLLABOR_TEST_MODEL"] = "env-model"
        os.environ["KOLLABOR_TEST_TEMPERATURE"] = "0.9"
        os.environ["KOLLABOR_TEST_MAX_TOKENS"] = "5000"
        os.environ["KOLLABOR_TEST_TIMEOUT"] = "60000"
        os.environ["KOLLABOR_TEST_TOKEN"] = "env-token"

        try:
            # Create service
            service = APICommunicationService(
                config=config,
                raw_conversations_dir=Path(temp_dir.name),
                profile=profile,
            )

            # Verify values from env vars (via profile getter methods)
            self.assertEqual(service.api_url, "http://env-example.com")
            self.assertEqual(service.model, "env-model")
            self.assertEqual(service.temperature, 0.9)
            self.assertEqual(service.max_tokens, 5000)
            self.assertEqual(service.timeout, 60000)
            self.assertEqual(service.api_token, "env-token")
        finally:
            temp_dir.cleanup()
            os.environ.clear()


class TestFromDictForwardCompatibility(unittest.TestCase):
    """Test 38: from_dict() forward compatibility with unknown fields."""

    def test_38_unknown_field_silently_ignored(self):
        """Test 38: Load profile with unknown field api_token_env, silently ignored."""
        # Profile data with old/unknown field
        data = {
            "api_url": "https://api.anthropic.com",
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.7,
            "max_tokens": 4096,
            "tool_format": "anthropic",
            "timeout": 30000,
            "description": "Test profile",
            "extra_headers": {},
            # Unknown/deprecated field - should be silently ignored
            "api_token_env": "ANTHROPIC_API_KEY",
            # Another unknown field for good measure
            "unknown_field": "some_value",
        }

        # Should not raise an error
        try:
            profile = LLMProfile.from_dict("test", data)
        except Exception as e:
            self.fail(f"from_dict() raised exception for unknown fields: {e}")

        # Verify profile was created correctly
        self.assertEqual(profile.name, "test")
        self.assertEqual(profile.api_url, "https://api.anthropic.com")
        self.assertEqual(profile.model, "claude-sonnet-4-20250514")
        self.assertEqual(profile.temperature, 0.7)
        self.assertEqual(profile.max_tokens, 4096)
        self.assertEqual(profile.tool_format, "anthropic")
        self.assertEqual(profile.timeout, 30000)

        # Verify unknown fields are NOT in the profile
        self.assertFalse(hasattr(profile, "api_token_env"))
        self.assertFalse(hasattr(profile, "unknown_field"))

        # Verify to_dict() doesn't include unknown fields
        profile_dict = profile.to_dict()
        self.assertNotIn("api_token_env", profile_dict)
        self.assertNotIn("unknown_field", profile_dict)


class TestWhitespaceHandlingIntegration(unittest.TestCase):
    """Test 33: Whitespace handling in profile names (integration)."""

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
        self.assertEqual(profile._get_env_key("MODEL"), "KOLLABOR_FAST_MODEL")

        # Verify ProfileManager also handles it correctly with a unique name
        # (can't use "  fast  " due to collision with default "fast" profile)
        manager = ProfileManager(config=None)
        # Clear user profiles to avoid conflicts
        from core.llm.profile_manager import ProfileManager as PM
        user_profile_names = [name for name in manager._profiles.keys()
                             if name not in PM.DEFAULT_PROFILES]
        for name in user_profile_names:
            del manager._profiles[name]

        profile2 = manager.create_profile(
            name="  my-fast  ",
            api_url="http://example.com",
            model="model",
            save_to_config=False,
        )
        self.assertIsNotNone(profile2)
        self.assertEqual(profile2._get_env_key("TOKEN"), "KOLLABOR_MY_FAST_TOKEN")


if __name__ == "__main__":
    unittest.main(verbosity=2)
