"""Configuration utilities for Kollabor."""

import os
import sys
from pathlib import Path
import logging
import shutil
from typing import Optional

logger = logging.getLogger(__name__)

# Platform check
IS_WINDOWS = sys.platform == "win32"


# ============================================================================
# Project Data Path Utilities
# ============================================================================

def encode_project_path(project_path: Path) -> str:
    """Encode a project path to a safe directory name.

    Replaces path separators (/ and \\) with underscores and strips
    leading underscores for use as a directory name.

    Args:
        project_path: Path to encode

    Returns:
        Encoded string safe for use as directory name

    Examples:
        >>> encode_project_path(Path("/Users/malmazan/dev/hello_world"))
        'Users_malmazan_dev_hello_world'
        >>> encode_project_path(Path("C:\\\\Users\\\\dev\\\\project"))
        'C_Users_dev_project'
    """
    path_str = str(project_path.resolve())
    # Replace path separators with underscores
    encoded = path_str.replace("/", "_").replace("\\", "_")
    # Remove leading underscore if present (from root /)
    while encoded.startswith("_"):
        encoded = encoded[1:]
    return encoded


def decode_project_path(encoded: str) -> Path:
    """Decode an encoded project path back to a Path.

    Reverses the encoding done by encode_project_path().

    Args:
        encoded: Encoded project path string

    Returns:
        Original Path object

    Examples:
        >>> decode_project_path("Users_malmazan_dev_hello_world")
        Path('/Users/malmazan/dev/hello_world')
        >>> decode_project_path("C_Users_dev_project")
        Path('C:\\\\Users\\\\dev\\\\project')
    """
    # Detect Windows paths (start with drive letter + underscore)
    if len(encoded) > 1 and encoded[1] == "_" and encoded[0].isalpha():
        # Windows: C_Users_... -> C:\Users\...
        path_str = encoded[0] + ":\\" + encoded[2:].replace("_", "\\")
    else:
        # Unix: Users_malmazan_... -> /Users/malmazan/...
        path_str = "/" + encoded.replace("_", "/")
    return Path(path_str)


def get_project_data_dir(project_path: Path = None) -> Path:
    """Get the centralized project data directory.

    Returns ~/.kollabor-cli/projects/<encoded-path>/ for the current
    or specified project.

    Args:
        project_path: Path to project directory. If None, uses Path.cwd()

    Returns:
        Path to project-specific data directory
    """
    if project_path is None:
        project_path = Path.cwd()

    encoded = encode_project_path(project_path)
    return Path.home() / ".kollabor-cli" / "projects" / encoded


def get_conversations_dir(project_path: Path = None) -> Path:
    """Get the conversations directory for a project.

    Args:
        project_path: Path to project directory. If None, uses Path.cwd()

    Returns:
        Path to project's conversations directory
    """
    return get_project_data_dir(project_path) / "conversations"


def get_logs_dir(project_path: Path = None) -> Path:
    """Get the logs directory for a project.

    Args:
        project_path: Path to project directory. If None, uses Path.cwd()

    Returns:
        Path to project's logs directory
    """
    return get_project_data_dir(project_path) / "logs"


def get_local_agents_dir() -> Path | None:
    """Get the local agents directory if it exists.

    Checks for .kollabor-cli/agents/ in the current working directory.

    Returns:
        Path to local agents directory if it exists, None otherwise
    """
    local_agents_dir = Path.cwd() / ".kollabor-cli" / "agents"
    if local_agents_dir.exists():
        return local_agents_dir
    return None


def get_local_agents_path() -> Path:
    """Get the local agents directory path (for creation purposes).

    Unlike get_local_agents_dir(), this returns the path even if it doesn't exist.
    Use this when you need to create the local agents directory.

    Returns:
        Path to .kollabor-cli/agents/ in the current working directory
    """
    return Path.cwd() / ".kollabor-cli" / "agents"


def get_global_agents_dir() -> Path:
    """Get the global agents directory.

    Returns:
        Path to ~/.kollabor-cli/agents/
    """
    return Path.home() / ".kollabor-cli" / "agents"

# CLI override for system prompt file (set via --system-prompt argument)
_cli_system_prompt_file: str | None = None


def set_cli_system_prompt_file(file_path: str | None) -> None:
    """Set the CLI override for system prompt file.

    Args:
        file_path: Path to the system prompt file, or None to clear
    """
    global _cli_system_prompt_file
    _cli_system_prompt_file = file_path
    if file_path:
        logger.info(f"CLI system prompt override set: {file_path}")


def _resolve_system_prompt_path(filename: str) -> Path | None:
    """Resolve a system prompt filename to a full path.

    Searches in order:
    1. As-is (if absolute path or exists in cwd)
    2. Local .kollabor-cli/agents/default/
    3. Global ~/.kollabor-cli/agents/default/

    Args:
        filename: The filename or path provided by the user

    Returns:
        Resolved Path if found, None otherwise
    """
    # Expand ~ in path
    expanded = Path(filename).expanduser()

    # 1. Check as-is (absolute path or relative from cwd)
    if expanded.exists():
        return expanded

    # If it's an absolute path that doesn't exist, don't search further
    if expanded.is_absolute():
        return None

    # Get just the filename for searching in directories
    name = expanded.name

    # Also try with .md extension if not present
    names_to_try = [name]
    if not name.endswith('.md'):
        names_to_try.append(f"{name}.md")

    # 2. Local .kollabor-cli/agents/default/
    local_agent_dir = Path.cwd() / ".kollabor-cli" / "agents" / "default"
    for n in names_to_try:
        candidate = local_agent_dir / n
        if candidate.exists():
            return candidate

    # 3. Global ~/.kollabor-cli/agents/default/
    global_agent_dir = Path.home() / ".kollabor-cli" / "agents" / "default"
    for n in names_to_try:
        candidate = global_agent_dir / n
        if candidate.exists():
            return candidate

    return None


def get_config_directory() -> Path:
    """Get the global Kollabor configuration directory.

    ALWAYS returns ~/.kollabor-cli/ regardless of current directory.
    Project-specific data is stored under ~/.kollabor-cli/projects/<encoded>/.

    Returns:
        Path to the global configuration directory (~/.kollabor-cli/)
    """
    return Path.home() / ".kollabor-cli"


def ensure_config_directory() -> Path:
    """Get and ensure the configuration directory exists.

    Creates both the global config directory and the project-specific
    data directory under ~/.kollabor-cli/projects/<encoded>/.

    Returns:
        Path to the global configuration directory
    """
    config_dir = get_config_directory()
    config_dir.mkdir(exist_ok=True)

    # Also ensure project data directory exists
    project_data_dir = get_project_data_dir()
    project_data_dir.mkdir(parents=True, exist_ok=True)

    return config_dir


def get_system_prompt_path() -> Path:
    """Get the system prompt file path, preferring env var over local/global.

    Resolution order:
    1. KOLLABOR_SYSTEM_PROMPT_FILE environment variable (custom file path)
    2. Local .kollabor-cli/agents/default/system_prompt.md (project-specific)
    3. Global ~/.kollabor-cli/agents/default/system_prompt.md (global default)

    Returns:
        Path to the system prompt file
    """
    # Check for environment variable override
    env_prompt_file = os.environ.get("KOLLABOR_SYSTEM_PROMPT_FILE")
    if env_prompt_file:
        env_path = Path(env_prompt_file).expanduser()
        if env_path.exists():
            logger.debug(f"Using system prompt from KOLLABOR_SYSTEM_PROMPT_FILE: {env_path}")
            return env_path
        else:
            logger.warning(f"KOLLABOR_SYSTEM_PROMPT_FILE points to non-existent file: {env_path}")

    local_config_dir = Path.cwd() / ".kollabor-cli"
    global_config_dir = Path.home() / ".kollabor-cli"

    # New agent-based paths
    local_agent_prompt = local_config_dir / "agents" / "default" / "system_prompt.md"
    global_agent_prompt = global_config_dir / "agents" / "default" / "system_prompt.md"

    # On Windows, prefer default_win.md if it exists (in agent directory)
    if IS_WINDOWS:
        local_win_prompt = local_config_dir / "agents" / "default" / "system_prompt_win.md"
        global_win_prompt = global_config_dir / "agents" / "default" / "system_prompt_win.md"

        if local_win_prompt.exists():
            logger.debug(f"Using Windows-specific system prompt: {local_win_prompt}")
            return local_win_prompt
        if global_win_prompt.exists():
            logger.debug(f"Using Windows-specific system prompt: {global_win_prompt}")
            return global_win_prompt

    # If local exists, use it (override)
    if local_agent_prompt.exists():
        return local_agent_prompt
    # Otherwise use global
    else:
        return global_agent_prompt


def get_system_prompt_content() -> str:
    """Get the system prompt content, checking CLI args, env vars, and files.

    Resolution order:
    1. CLI --system-prompt argument (highest priority)
    2. KOLLABOR_SYSTEM_PROMPT environment variable (direct string)
    3. KOLLABOR_SYSTEM_PROMPT_FILE environment variable (custom file path)
    4. Local .kollabor-cli/agents/default/system_prompt.md (project-specific override)
    5. Global ~/.kollabor-cli/agents/default/system_prompt.md (global default)
    6. Fallback to minimal default

    Returns:
        System prompt content as string
    """
    global _cli_system_prompt_file

    # Check for CLI override (highest priority)
    if _cli_system_prompt_file:
        cli_path = _resolve_system_prompt_path(_cli_system_prompt_file)
        if cli_path and cli_path.exists():
            try:
                content = cli_path.read_text(encoding='utf-8')
                logger.info(f"Loaded system prompt from CLI argument: {cli_path}")
                return content
            except Exception as e:
                logger.error(f"Failed to read CLI system prompt from {cli_path}: {e}")
        else:
            logger.error(f"CLI system prompt file not found: {_cli_system_prompt_file}")
            # Don't fall through - this is an explicit user request, so fail clearly
            return f"""[SYSTEM PROMPT LOAD FAILURE]

The system prompt file specified via --system-prompt was not found:
  {_cli_system_prompt_file}

Searched in:
  - Current directory
  - .kollabor-cli/system_prompt/
  - ~/.kollabor-cli/system_prompt/

Please check the file path and try again.

I'll do my best to help, but my responses may not follow the expected format.
"""

    # Check for direct environment variable string
    env_prompt = os.environ.get("KOLLABOR_SYSTEM_PROMPT")
    if env_prompt:
        logger.debug("Using system prompt from KOLLABOR_SYSTEM_PROMPT environment variable")
        return env_prompt

    # Otherwise read from file (respects KOLLABOR_SYSTEM_PROMPT_FILE via get_system_prompt_path)
    system_prompt_path = get_system_prompt_path()
    if system_prompt_path.exists():
        try:
            content = system_prompt_path.read_text(encoding='utf-8')
            logger.info(f"Loaded system prompt from: {system_prompt_path}")
            return content
        except Exception as e:
            logger.error(f"Failed to read system prompt from {system_prompt_path}: {e}")
            return get_default_system_prompt()
    else:
        logger.warning(f"System prompt file not found: {system_prompt_path}, using default")
        return get_default_system_prompt()


def get_default_system_prompt() -> str:
    """Get the default system prompt content when no file exists.

    Returns a minimal fallback that alerts the user about the missing prompt.

    Returns:
        Default system prompt string
    """
    # Emergency fallback - alert user that system prompt failed to load
    logger.warning("Using emergency fallback system prompt - this should not happen in production")
    return """[SYSTEM PROMPT LOAD FAILURE]

You are Kollabor, an AI coding assistant. However, your full system prompt
failed to load. This is a critical configuration issue.

IMPORTANT: Alert the user immediately about this problem:

"Warning: My system prompt failed to load properly. I'm operating in a limited
fallback mode. Please check your Kollabor installation:

1. Verify ~/.kollabor-cli/agents/default/system_prompt.md exists
2. Run 'kollab' to trigger automatic initialization
3. Review the logs at ~/.kollabor-cli/logs/kollabor.log for errors

I'll do my best to help, but my responses may not follow the expected format
until this is resolved."

Despite this issue, try to be helpful and assist the user with their request.
"""


def initialize_system_prompt() -> None:
    """Initialize agents from bundled seed folder.

    Copies ALL agents from bundled agents/ folder to global ~/.kollabor-cli/agents/
    on first install. Does NOT create local .kollabor-cli folders.

    Local .kollabor-cli/agents/ is only created when user explicitly creates
    a custom project-specific agent.

    Priority order:
    1. Migrate from old global ~/.kollabor-cli/system_prompt/default.md if it exists
    2. Copy ALL agents from seed folder to global ~/.kollabor-cli/agents/
    """
    try:
        global_config_dir = Path.home() / ".kollabor-cli"
        global_agents_dir = global_config_dir / "agents"

        # Old legacy directory (for migration)
        old_global_prompt_dir = global_config_dir / "system_prompt"

        # Ensure global agents directory has all seed agents
        _copy_seed_agents_to_global(global_agents_dir, old_global_prompt_dir)

    except Exception as e:
        logger.error(f"Failed to initialize system prompt: {e}")


def _copy_seed_agents_to_global(global_agents_dir: Path, old_global_prompt_dir: Path) -> None:
    """Copy all agents from bundled seed folder to global agents directory.

    Args:
        global_agents_dir: Target global agents directory (~/.kollabor-cli/agents/)
        old_global_prompt_dir: Old system_prompt dir for migration
    """
    # Find bundled seed agents folder
    package_dir = Path(__file__).parent.parent.parent
    seed_agents_dir = package_dir / "agents"

    if not seed_agents_dir.exists():
        # Fallback for development mode
        seed_agents_dir = Path.cwd() / "agents"

    if not seed_agents_dir.exists():
        logger.warning("No seed agents folder found")
        # Try migration from old location
        old_global_default = old_global_prompt_dir / "default.md"
        if old_global_default.exists():
            logger.info(f"Migrating global system prompt from old location: {old_global_default}")
            _migrate_old_prompt_to_agent(old_global_default, global_agents_dir / "default")
        return

    global_agents_dir.mkdir(parents=True, exist_ok=True)

    # Copy each agent from seed to global
    for agent_dir in seed_agents_dir.iterdir():
        if agent_dir.is_dir():
            target_agent_dir = global_agents_dir / agent_dir.name
            if not target_agent_dir.exists():
                target_agent_dir.mkdir(parents=True, exist_ok=True)
                for item in agent_dir.iterdir():
                    if item.is_file():
                        target_file = target_agent_dir / item.name
                        if not target_file.exists():
                            shutil.copy2(item, target_file)
                            logger.debug(f"Copied seed agent file: {agent_dir.name}/{item.name}")
                logger.info(f"Installed seed agent to global: {agent_dir.name}")


def _migrate_old_prompt_to_agent(old_prompt_file: Path, agent_dir: Path) -> None:
    """Migrate an old-style system prompt to new agent directory structure.

    Args:
        old_prompt_file: Path to old default.md file
        agent_dir: Target agent directory (e.g., .kollabor-cli/agents/default/)
    """
    agent_dir.mkdir(parents=True, exist_ok=True)

    new_prompt_file = agent_dir / "system_prompt.md"
    if not new_prompt_file.exists():
        shutil.copy2(old_prompt_file, new_prompt_file)
        logger.info(f"Migrated system prompt to: {new_prompt_file}")

        # Create agent.json with default config
        agent_json = agent_dir / "agent.json"
        if not agent_json.exists():
            import json
            agent_config = {
                "name": "default",
                "description": "Default agent with standard system prompt",
                "profile": None
            }
            agent_json.write_text(json.dumps(agent_config, indent=2), encoding='utf-8')
            logger.info(f"Created agent config: {agent_json}")


def _create_agent_from_defaults(agent_dir: Path) -> None:
    """Create default agent from bundled seed agents folder.

    Copies from bundled agents/<agent_name>/ to target directory.

    Args:
        agent_dir: Agent directory to create (e.g., ~/.kollabor-cli/agents/default/)
    """
    agent_name = agent_dir.name  # e.g., "default"

    # Find bundled seed agents folder
    package_dir = Path(__file__).parent.parent.parent  # Go up from core/utils/ to package root
    seed_agent_dir = package_dir / "agents" / agent_name

    if not seed_agent_dir.exists():
        # Fallback for development mode
        seed_agent_dir = Path.cwd() / "agents" / agent_name

    if seed_agent_dir.exists() and seed_agent_dir.is_dir():
        # Copy entire agent directory from seed
        agent_dir.mkdir(parents=True, exist_ok=True)
        for item in seed_agent_dir.iterdir():
            target = agent_dir / item.name
            if not target.exists():
                if item.is_file():
                    shutil.copy2(item, target)
                    logger.debug(f"Copied seed file: {item.name}")
        logger.info(f"Created agent from seed: {agent_dir}")
    else:
        # Fallback: create minimal agent
        agent_dir.mkdir(parents=True, exist_ok=True)

        prompt_file = agent_dir / "system_prompt.md"
        if not prompt_file.exists():
            prompt_file.write_text(get_default_system_prompt(), encoding='utf-8')
            logger.warning(f"Created fallback system prompt (seed not found): {prompt_file}")

        agent_json = agent_dir / "agent.json"
        if not agent_json.exists():
            import json
            agent_config = {
                "name": agent_name,
                "description": f"{agent_name} agent",
                "profile": None
            }
            agent_json.write_text(json.dumps(agent_config, indent=2), encoding='utf-8')
            logger.info(f"Created agent config: {agent_json}")


# Default LLM profiles - used for initial config creation
DEFAULT_LLM_PROFILES = {
    "default": {
        "api_url": "http://localhost:1234",
        "model": "qwen3-0.6b",
        "temperature": 0.7,
        "max_tokens": 32768,
        "tool_format": "openai",
        "native_tool_calling": False,
        "timeout": 30000,
        "description": "Local LLM for general use",
        "extra_headers": {},
        "api_token": "",
    },
    "fast": {
        "api_url": "http://localhost:1234",
        "model": "qwen3-0.6b",
        "temperature": 0.7,
        "max_tokens": 32768,
        "tool_format": "openai",
        "native_tool_calling": False,
        "timeout": 30000,
        "description": "Fast local model for quick queries",
        "extra_headers": {},
        "api_token": "",
    },
    "claude": {
        "api_url": "https://api.anthropic.com",
        "model": "claude-sonnet-4",
        "temperature": 0.7,
        "max_tokens": 32768,
        "tool_format": "anthropic",
        "native_tool_calling": False,
        "timeout": 60000,
        "description": "Anthropic Claude for complex tasks",
        "extra_headers": {},
        "api_token": "",
    },
    "openai": {
        "api_url": "https://api.openai.com",
        "model": "gpt-5",
        "temperature": 0.7,
        "max_tokens": 32768,
        "tool_format": "openai",
        "native_tool_calling": True,
        "timeout": 60000,
        "description": "OpenAI GPT-4 for general tasks",
        "extra_headers": {},
        "api_token": "",
    },
}


def initialize_config(force: bool = False) -> None:
    """Initialize config.json in global directory only.

    Does NOT create local .kollabor-cli folders. Local config is only
    created when user explicitly sets project-specific overrides.

    Flow:
    1. If global ~/.kollabor-cli/config.json doesn't exist (or force=True)
       -> create with defaults + profiles

    Args:
        force: If True, overwrite existing config file with defaults

    This ensures:
    - Users always have a discoverable config with example profiles
    - Existing config is never overwritten (unless force=True)
    """
    import json

    global_config_dir = Path.home() / ".kollabor-cli"
    global_config_path = global_config_dir / "config.json"

    try:
        # Step 1: Create global config if it doesn't exist or force=True
        if not global_config_path.exists() or force:
            if force:
                logger.info("Force resetting global config.json with defaults")
            else:
                logger.info("Creating global config.json with defaults")
            global_config_dir.mkdir(parents=True, exist_ok=True)

            # Build default config structure with profiles
            default_config = _get_minimal_default_config()
            default_config["core"] = default_config.get("core", {})
            default_config["core"]["llm"] = default_config["core"].get("llm", {})
            default_config["core"]["llm"]["profiles"] = DEFAULT_LLM_PROFILES.copy()
            default_config["core"]["llm"]["active_profile"] = "default"

            global_config_path.write_text(
                json.dumps(default_config, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            logger.info(f"Created global config: {global_config_path}")

    except Exception as e:
        logger.error(f"Failed to initialize config: {e}")


def get_default_agent() -> tuple[Optional[str], Optional[str]]:
    """
    Get the default agent from config.

    Returns:
        Tuple of (agent_name, level) where level is "project" or "global"
        Returns (None, None) if no default configured
    """
    import json

    # Check project-level first
    local_config_path = Path.cwd() / ".kollabor-cli" / "config.json"
    if local_config_path.exists():
        try:
            with open(local_config_path) as f:
                config = json.load(f)
                default = config.get("core", {}).get("llm", {}).get("default_agent")
                if default and default.get("level") == "project":
                    return (default.get("name"), "project")
        except Exception:
            pass

    # Check global-level
    global_config_path = Path.home() / ".kollabor-cli" / "config.json"
    if global_config_path.exists():
        try:
            with open(global_config_path) as f:
                config = json.load(f)
                default = config.get("core", {}).get("llm", {}).get("default_agent")
                if default and default.get("level") == "global":
                    return (default.get("name"), "global")
        except Exception:
            pass

    return (None, None)


def set_default_agent(agent_name: str, level: str) -> bool:
    """
    Set a default agent in config.

    Args:
        agent_name: Name of agent to set as default
        level: "project" or "global"

    Returns:
        True if saved successfully
    """
    import json

    if level == "project":
        config_path = Path.cwd() / ".kollabor-cli" / "config.json"
    else:
        config_path = Path.home() / ".kollabor-cli" / "config.json"

    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing config or create new
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {}

    # Ensure structure exists
    if "core" not in config:
        config["core"] = {}
    if "llm" not in config["core"]:
        config["core"]["llm"] = {}

    # Set default
    config["core"]["llm"]["default_agent"] = {
        "name": agent_name,
        "level": level
    }

    # Save
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    return True


def clear_default_agent(level: str) -> bool:
    """
    Clear the default agent from config.

    Args:
        level: "project" or "global"

    Returns:
        True if cleared successfully
    """
    import json

    if level == "project":
        config_path = Path.cwd() / ".kollabor-cli" / "config.json"
    else:
        config_path = Path.home() / ".kollabor-cli" / "config.json"

    if not config_path.exists():
        return True  # Nothing to clear

    with open(config_path) as f:
        config = json.load(f)

    # Remove default_agent entry
    if "core" in config and "llm" in config["core"]:
        config["core"]["llm"].pop("default_agent", None)

    # Save
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    return True


def get_all_default_agents() -> dict[str, str]:
    """
    Get all default agents from both config levels.

    Returns:
        Dict mapping level -> agent_name, e.g. {"project": "coder", "global": "research"}
        Only includes levels that have a default set
    """
    import json
    defaults = {}

    # Check project
    local_config_path = Path.cwd() / ".kollabor-cli" / "config.json"
    if local_config_path.exists():
        try:
            with open(local_config_path) as f:
                config = json.load(f)
                default = config.get("core", {}).get("llm", {}).get("default_agent")
                if default and default.get("level") == "project":
                    defaults["project"] = default.get("name")
        except Exception:
            pass

    # Check global
    global_config_path = Path.home() / ".kollabor-cli" / "config.json"
    if global_config_path.exists():
        try:
            with open(global_config_path) as f:
                config = json.load(f)
                default = config.get("core", {}).get("llm", {}).get("default_agent")
                if default and default.get("level") == "global":
                    defaults["global"] = default.get("name")
        except Exception:
            pass

    return defaults


def _get_minimal_default_config() -> dict:
    """Get minimal default config structure for initialization.

    This is a subset of the full base config - just enough to bootstrap.
    The full config with all defaults is loaded by ConfigLoader.

    Returns:
        Minimal config dictionary with core settings.
    """
    return {
        "application": {
            "name": "Kollabor CLI",
            "description": "AI Edition"
        },
        "core": {
            "llm": {
                "max_history": 90,
                "save_conversations": True,
                "conversation_format": "jsonl",
                "show_status": True,
            }
        }
    }
