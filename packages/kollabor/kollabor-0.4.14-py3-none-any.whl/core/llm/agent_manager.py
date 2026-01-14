"""
Agent and Skill Manager.

Manages agents defined in .kollabor-cli/agents/ directories:
- Each agent has a system_prompt.md and optional skill files
- Skills are loaded dynamically and appended to system prompt
- Supports both local (project) and global (user) agent directories

Directory structure:
    .kollabor-cli/agents/
        default/
            system_prompt.md
        lint-editor/
            system_prompt.md
            agent.json          # Optional config
            create-tasks.md     # Skill file
            fix-file.md         # Another skill
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.utils.config_utils import get_global_agents_dir, get_local_agents_dir, get_local_agents_path

logger = logging.getLogger(__name__)


@dataclass
class Skill:
    """
    A skill that can be loaded into an agent's context.

    Skills are markdown files containing instructions or context
    that can be dynamically loaded during a session.

    Attributes:
        name: Skill identifier (filename without extension)
        content: Full content of the skill file
        file_path: Path to the skill file
        description: Optional description extracted from file header
    """

    name: str
    content: str
    file_path: Path
    description: str = ""

    @classmethod
    def from_file(cls, file_path: Path) -> Optional["Skill"]:
        """
        Load skill from a markdown file.

        Extracts description from HTML comment at start of file:
        <!-- Description text here -->

        Args:
            file_path: Path to the .md file

        Returns:
            Skill instance or None on error
        """
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to read skill file {file_path}: {e}")
            return None

        # Extract description from HTML comment at start
        description = ""
        lines = content.split("\n")
        if lines and lines[0].strip().startswith("<!--"):
            comment_lines = []
            for line in lines:
                comment_lines.append(line)
                if "-->" in line:
                    break
            comment_text = "\n".join(comment_lines)
            description = (
                comment_text.replace("<!--", "")
                .replace("-->", "")
                .strip()
            )

        return cls(
            name=file_path.stem,
            content=content,
            file_path=file_path,
            description=description,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "file_path": str(self.file_path),
        }


@dataclass
class Agent:
    """
    An agent configuration with system prompt and available skills.

    Agents are loaded from directories containing:
    - system_prompt.md (required)
    - agent.json (optional config)
    - *.md files (skills)

    Attributes:
        name: Agent identifier (directory name)
        directory: Path to agent directory
        system_prompt: Base system prompt content
        skills: Available skills (name -> Skill)
        active_skills: Currently loaded skill names
        profile: Optional preferred LLM profile
        description: Human-readable description
        default_skills: Skills to auto-load when agent is activated
        source: 'local' or 'global' - where the agent was loaded from
        overrides_global: True if local agent overrides a global agent with same name
    """

    name: str
    directory: Path
    system_prompt: str
    skills: Dict[str, Skill] = field(default_factory=dict)
    active_skills: List[str] = field(default_factory=list)
    profile: Optional[str] = None
    description: str = ""
    default_skills: List[str] = field(default_factory=list)
    source: str = "global"
    overrides_global: bool = False

    @classmethod
    def from_directory(
        cls,
        agent_dir: Path,
        source: str = "global",
        overrides_global: bool = False,
    ) -> Optional["Agent"]:
        """
        Load agent from a directory.

        Args:
            agent_dir: Path to agent directory
            source: 'local' or 'global' - where the agent was loaded from
            overrides_global: True if local agent overrides a global agent

        Returns:
            Agent instance or None if invalid
        """
        if not agent_dir.is_dir():
            return None

        # Load system prompt (required)
        system_prompt_file = agent_dir / "system_prompt.md"
        if not system_prompt_file.exists():
            logger.warning(f"Agent {agent_dir.name} missing system_prompt.md")
            return None

        try:
            system_prompt = system_prompt_file.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to read system prompt for {agent_dir.name}: {e}")
            return None

        # Load skills (all .md files except system_prompt.md)
        skills: Dict[str, Skill] = {}
        for md_file in agent_dir.glob("*.md"):
            if md_file.name != "system_prompt.md":
                skill = Skill.from_file(md_file)
                if skill:
                    skills[skill.name] = skill

        # Load optional config
        profile = None
        description = ""
        default_skills: List[str] = []
        config_file = agent_dir / "agent.json"
        if config_file.exists():
            try:
                config = json.loads(config_file.read_text(encoding="utf-8"))
                profile = config.get("profile")
                description = config.get("description", "")
                default_skills = config.get("default_skills", [])
            except Exception as e:
                logger.warning(f"Failed to load agent config for {agent_dir.name}: {e}")

        return cls(
            name=agent_dir.name,
            directory=agent_dir,
            system_prompt=system_prompt,
            skills=skills,
            profile=profile,
            description=description,
            default_skills=default_skills,
            source=source,
            overrides_global=overrides_global,
        )

    def get_full_system_prompt(self) -> str:
        """
        Get system prompt with active skills appended.

        Skills are added under "## Skill: {name}" headers.

        Returns:
            Combined system prompt string
        """
        parts = [self.system_prompt]

        for skill_name in self.active_skills:
            if skill_name in self.skills:
                skill = self.skills[skill_name]
                parts.append(f"\n\n## Skill: {skill_name}\n\n{skill.content}")

        return "\n".join(parts)

    def load_skill(self, skill_name: str) -> bool:
        """
        Load a skill into active context.

        Args:
            skill_name: Name of skill to load

        Returns:
            True if loaded, False if not found
        """
        if skill_name not in self.skills:
            logger.error(f"Skill not found: {skill_name}")
            return False

        if skill_name not in self.active_skills:
            self.active_skills.append(skill_name)
            logger.info(f"Loaded skill: {skill_name}")
        return True

    def unload_skill(self, skill_name: str) -> bool:
        """
        Unload a skill from active context.

        Args:
            skill_name: Name of skill to unload

        Returns:
            True if unloaded, False if not loaded
        """
        if skill_name in self.active_skills:
            self.active_skills.remove(skill_name)
            logger.info(f"Unloaded skill: {skill_name}")
            return True
        return False

    def list_skills(self) -> List[Skill]:
        """Get list of available skills."""
        return list(self.skills.values())

    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a specific skill by name."""
        return self.skills.get(name)

    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary representation."""
        return {
            "name": self.name,
            "directory": str(self.directory),
            "description": self.description,
            "profile": self.profile,
            "skills": [s.to_dict() for s in self.skills.values()],
            "active_skills": self.active_skills,
            "source": self.source,
            "overrides_global": self.overrides_global,
        }


class AgentManager:
    """
    Manages agent discovery, loading, and skill management.

    Searches for agents in:
    1. Local: .kollabor-cli/agents/ (project-specific, higher priority)
    2. Global: ~/.kollabor-cli/agents/ (user defaults)

    Local agents override global agents with the same name.
    """

    def __init__(self, config=None):
        """
        Initialize agent manager.

        Args:
            config: Configuration object (optional)
        """
        self.config = config
        self._agents: Dict[str, Agent] = {}
        self._active_agent_name: Optional[str] = None

        # Agent directories (in discovery order, lowest to highest priority)
        # 1. Global: ~/.kollabor-cli/agents/ (user defaults)
        # 2. Local: .kollabor-cli/agents/ (project-specific, where agents are created)
        self.global_agents_dir = get_global_agents_dir()
        self.local_agents_dir = get_local_agents_dir()

        self._discover_agents()

    def _discover_agents(self) -> None:
        """Discover all available agents from directories."""
        # Skip these directory names during discovery
        skip_dirs = {"__pycache__", ".git", ".svn", "node_modules"}

        # Load from global first (lowest priority)
        if self.global_agents_dir:
            for agent_dir in self.global_agents_dir.iterdir():
                if agent_dir.is_dir() and agent_dir.name not in skip_dirs and not agent_dir.name.startswith("."):
                    agent = Agent.from_directory(agent_dir, source="global", overrides_global=False)
                    if agent:
                        self._agents[agent.name] = agent
                        logger.debug(f"Discovered global agent: {agent.name}")

        # Load from local (higher priority, overrides global)
        if self.local_agents_dir:
            for agent_dir in self.local_agents_dir.iterdir():
                if agent_dir.is_dir() and agent_dir.name not in skip_dirs and not agent_dir.name.startswith("."):
                    # Check if this local agent overrides a global one
                    overrides = agent_dir.name in self._agents
                    agent = Agent.from_directory(agent_dir, source="local", overrides_global=overrides)
                    if agent:
                        self._agents[agent.name] = agent
                        override_msg = " (overrides global)" if overrides else ""
                        logger.debug(f"Discovered local agent: {agent.name}{override_msg}")

        logger.info(f"Discovered {len(self._agents)} agents")

    def get_agent(self, name: str) -> Optional[Agent]:
        """
        Get agent by name.

        Args:
            name: Agent name

        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(name)

    def get_active_agent(self) -> Optional[Agent]:
        """
        Get the currently active agent.

        Returns:
            Active Agent or "default" agent or None
        """
        if self._active_agent_name:
            agent = self._agents.get(self._active_agent_name)
            if agent:
                return agent

        # Fall back to "default" agent
        return self._agents.get("default")

    def set_active_agent(self, name: str, load_defaults: bool = True) -> bool:
        """
        Set the active agent.

        Args:
            name: Agent name to activate
            load_defaults: If True, auto-load the agent's default skills

        Returns:
            True if successful, False if agent not found
        """
        if name not in self._agents:
            logger.error(f"Agent not found: {name}")
            return False

        old_agent = self._active_agent_name
        self._active_agent_name = name

        # Auto-load default skills if configured
        agent = self._agents[name]
        if load_defaults and agent.default_skills:
            for skill_name in agent.default_skills:
                if skill_name in agent.skills and skill_name not in agent.active_skills:
                    agent.load_skill(skill_name)
                    logger.debug(f"Auto-loaded default skill: {skill_name}")

        logger.info(f"Activated agent: {old_agent} -> {name}")
        return True

    def clear_active_agent(self) -> None:
        """Clear the active agent (use default or no agent)."""
        self._active_agent_name = None
        logger.info("Cleared active agent")

    def list_agents(self) -> List[Agent]:
        """
        List all available agents.

        Returns:
            List of Agent instances
        """
        return list(self._agents.values())

    def get_agent_names(self) -> List[str]:
        """
        Get list of agent names.

        Returns:
            List of agent name strings
        """
        return list(self._agents.keys())

    def has_agent(self, name: str) -> bool:
        """Check if an agent exists."""
        return name in self._agents

    def list_skills(self, agent_name: Optional[str] = None) -> List[Skill]:
        """
        List skills for an agent.

        Args:
            agent_name: Agent name (default: active agent)

        Returns:
            List of Skill instances
        """
        agent = self._agents.get(agent_name) if agent_name else self.get_active_agent()
        if not agent:
            return []
        return agent.list_skills()

    def load_skill(
        self, skill_name: str, agent_name: Optional[str] = None
    ) -> bool:
        """
        Load a skill into an agent's active context.

        Args:
            skill_name: Name of skill to load
            agent_name: Agent name (default: active agent)

        Returns:
            True if loaded, False otherwise
        """
        agent = self._agents.get(agent_name) if agent_name else self.get_active_agent()
        if not agent:
            logger.error("No agent available to load skill")
            return False

        return agent.load_skill(skill_name)

    def unload_skill(
        self, skill_name: str, agent_name: Optional[str] = None
    ) -> bool:
        """
        Unload a skill from an agent's active context.

        Args:
            skill_name: Name of skill to unload
            agent_name: Agent name (default: active agent)

        Returns:
            True if unloaded, False otherwise
        """
        agent = self._agents.get(agent_name) if agent_name else self.get_active_agent()
        if not agent:
            return False

        return agent.unload_skill(skill_name)

    def toggle_default_skill(
        self, skill_name: str, agent_name: Optional[str] = None, scope: str = "project"
    ) -> tuple[bool, bool]:
        """
        Toggle a skill as default (auto-loaded when agent is activated).

        Args:
            skill_name: Name of skill to toggle
            agent_name: Agent name (default: active agent)
            scope: "project" for .kollabor-cli or "global" for ~/.kollabor-cli

        Returns:
            Tuple of (success, is_now_default)
        """
        agent = self._agents.get(agent_name) if agent_name else self.get_active_agent()
        if not agent:
            return (False, False)

        # Check if skill exists
        if skill_name not in agent.skills:
            logger.error(f"Skill not found: {skill_name}")
            return (False, False)

        # Determine target directory based on scope
        if scope == "global":
            target_dir = self.global_agents_dir / agent.name
        else:
            # Use get_local_agents_path() for creation (creates dir if needed)
            target_dir = get_local_agents_path() / agent.name

        # Ensure directory exists
        target_dir.mkdir(parents=True, exist_ok=True)

        # Load existing config from target scope
        config_file = target_dir / "agent.json"
        current_defaults = []
        if config_file.exists():
            try:
                config_data = json.loads(config_file.read_text(encoding="utf-8"))
                current_defaults = config_data.get("default_skills", [])
            except Exception as e:
                logger.error(f"Failed to read {scope} agent.json: {e}")

        # Toggle default status
        if skill_name in current_defaults:
            current_defaults.remove(skill_name)
            is_default = False
            logger.info(f"Removed skill from {scope} defaults: {skill_name}")
        else:
            current_defaults.append(skill_name)
            is_default = True
            logger.info(f"Added skill to {scope} defaults: {skill_name}")

        # Save to target scope
        self._save_agent_config_to_path(target_dir, current_defaults, agent)

        # Reload agent to reflect changes
        self._reload_agent(agent.name)

        return (True, is_default)

    def _save_agent_config(self, agent: Agent) -> bool:
        """
        Save agent configuration to agent.json.

        Args:
            agent: Agent to save config for

        Returns:
            True if saved, False otherwise
        """
        try:
            config_file = agent.directory / "agent.json"

            # Build config dict
            agent_json: Dict[str, Any] = {}
            if agent.description:
                agent_json["description"] = agent.description
            if agent.profile:
                agent_json["profile"] = agent.profile
            if agent.default_skills:
                agent_json["default_skills"] = agent.default_skills

            if agent_json:
                config_file.write_text(
                    json.dumps(agent_json, indent=4, ensure_ascii=False),
                    encoding="utf-8"
                )
            elif config_file.exists():
                # Remove agent.json if empty
                config_file.unlink()

            return True
        except Exception as e:
            logger.error(f"Failed to save agent config for {agent.name}: {e}")
            return False

    def _save_agent_config_to_path(
        self, target_dir: Path, default_skills: List[str], agent: Agent
    ) -> bool:
        """
        Save agent configuration to a specific directory.

        Args:
            target_dir: Directory to save to
            default_skills: List of default skill names
            agent: Agent instance for reference data

        Returns:
            True if saved, False otherwise
        """
        try:
            config_file = target_dir / "agent.json"

            # Load existing config to preserve other fields
            agent_json: Dict[str, Any] = {}
            if config_file.exists():
                try:
                    agent_json = json.loads(config_file.read_text(encoding="utf-8"))
                except Exception:
                    pass

            # Update default_skills
            if default_skills:
                agent_json["default_skills"] = default_skills
            elif "default_skills" in agent_json:
                del agent_json["default_skills"]

            if agent_json:
                config_file.write_text(
                    json.dumps(agent_json, indent=4, ensure_ascii=False),
                    encoding="utf-8"
                )
            elif config_file.exists():
                config_file.unlink()

            return True
        except Exception as e:
            logger.error(f"Failed to save agent config to {target_dir}: {e}")
            return False

    def _reload_agent(self, agent_name: str) -> None:
        """
        Reload an agent from disk to pick up configuration changes.

        Args:
            agent_name: Name of agent to reload
        """
        # Store active skills before reload
        active_skills = []
        if agent_name in self._agents:
            active_skills = self._agents[agent_name].active_skills.copy()

        # Reload from disk (local overrides global)
        local_path = self.local_agents_dir / agent_name if self.local_agents_dir else None
        global_path = self.global_agents_dir / agent_name if self.global_agents_dir else None

        if local_path and local_path.exists():
            # Check if this overrides a global agent
            overrides = global_path and global_path.exists()
            agent = Agent.from_directory(local_path, source="local", overrides_global=overrides)
            if agent:
                self._agents[agent_name] = agent
        elif global_path and global_path.exists():
            agent = Agent.from_directory(global_path, source="global", overrides_global=False)
            if agent:
                self._agents[agent_name] = agent

        # Restore active skills
        if agent_name in self._agents and active_skills:
            for skill_name in active_skills:
                if skill_name in self._agents[agent_name].skills:
                    self._agents[agent_name].load_skill(skill_name)

    def get_system_prompt(self) -> Optional[str]:
        """
        Get the full system prompt for the active agent.

        Includes base system prompt and active skills.

        Returns:
            System prompt string or None if no agent
        """
        agent = self.get_active_agent()
        if agent:
            return agent.get_full_system_prompt()
        return None

    def get_preferred_profile(self) -> Optional[str]:
        """
        Get the preferred LLM profile for the active agent.

        Returns:
            Profile name or None
        """
        agent = self.get_active_agent()
        if agent:
            return agent.profile
        return None

    @property
    def active_agent_name(self) -> Optional[str]:
        """Get the name of the active agent."""
        return self._active_agent_name

    def is_active(self, name: str) -> bool:
        """Check if an agent is the active one."""
        return name == self._active_agent_name

    def get_agent_summary(self, name: Optional[str] = None) -> str:
        """
        Get a human-readable summary of an agent.

        Args:
            name: Agent name (default: active agent)

        Returns:
            Formatted summary string
        """
        agent = self._agents.get(name) if name else self.get_active_agent()
        if not agent:
            return f"Agent '{name}' not found" if name else "No active agent"

        lines = [
            f"Agent: {agent.name}",
            f"  Directory: {agent.directory}",
        ]
        if agent.description:
            lines.append(f"  Description: {agent.description}")
        if agent.profile:
            lines.append(f"  Preferred Profile: {agent.profile}")

        skills = agent.list_skills()
        if skills:
            lines.append(f"  Skills ({len(skills)}):")
            for skill in skills:
                active = "*" if skill.name in agent.active_skills else " "
                desc = f" - {skill.description[:40]}..." if skill.description else ""
                lines.append(f"    [{active}] {skill.name}{desc}")
        else:
            lines.append("  Skills: none")

        return "\n".join(lines)

    def refresh(self) -> None:
        """Re-discover agents from directories, preserving active skills."""
        # Preserve active skills state before refresh
        active_skills_backup: Dict[str, List[str]] = {}
        for name, agent in self._agents.items():
            if agent.active_skills:
                active_skills_backup[name] = list(agent.active_skills)

        self._agents.clear()
        self._discover_agents()

        # Restore active skills after refresh
        for name, skills in active_skills_backup.items():
            if name in self._agents:
                self._agents[name].active_skills = skills

    def create_agent(
        self,
        name: str,
        description: str = "",
        profile: Optional[str] = None,
        system_prompt: str = "",
        default_skills: Optional[List[str]] = None,
    ) -> Optional[Agent]:
        """
        Create a new agent with directory structure.

        Creates .kollabor-cli/agents/<name>/ directory with:
        - system_prompt.md
        - agent.json (if profile, description, or default_skills specified)

        Args:
            name: Agent name (becomes directory name)
            description: Agent description
            profile: Preferred LLM profile name
            system_prompt: Base system prompt content
            default_skills: List of skill names to auto-load when agent is activated

        Returns:
            Created Agent or None on failure
        """
        import json

        # Check if agent already exists
        if name in self._agents:
            logger.warning(f"Agent already exists: {name}")
            return None

        # Create in .kollabor-cli/agents/ directory (creates local dir if needed)
        local_path = get_local_agents_path()
        agent_dir = local_path / name

        if agent_dir.exists():
            logger.warning(f"Agent directory already exists: {agent_dir}")
            return None

        try:
            # Create directory structure
            agent_dir.mkdir(parents=True, exist_ok=True)

            # Create system_prompt.md
            default_prompt = system_prompt or f"""# {name.replace('-', ' ').title()} Agent

You are a specialized assistant.

## Your Mission

{description or 'Help users with their tasks.'}

## Approach

1. Analyze the user's request
2. Provide clear, actionable guidance
3. Follow best practices
"""
            prompt_file = agent_dir / "system_prompt.md"
            prompt_file.write_text(default_prompt, encoding="utf-8")

            # Create agent.json if profile, description, or default_skills specified
            if profile or description or default_skills:
                agent_json: Dict[str, Any] = {
                    "description": description or f"Agent: {name}",
                }
                if profile and profile != "(none)":
                    agent_json["profile"] = profile
                if default_skills:
                    agent_json["default_skills"] = default_skills

                json_file = agent_dir / "agent.json"
                json_file.write_text(
                    json.dumps(agent_json, indent=4, ensure_ascii=False),
                    encoding="utf-8"
                )

            # Update local_agents_dir since we just created the local directory
            self.local_agents_dir = get_local_agents_dir()

            # Load the newly created agent
            # Check if it overrides a global agent
            overrides = (
                self.global_agents_dir is not None
                and (self.global_agents_dir / name).exists()
            )
            agent = Agent.from_directory(agent_dir, source="local", overrides_global=overrides)
            if agent:
                self._agents[name] = agent
                logger.info(f"Created agent: {name} at {agent_dir}")
                return agent

            return None

        except Exception as e:
            logger.error(f"Failed to create agent {name}: {e}")
            # Clean up on failure
            if agent_dir.exists():
                import shutil
                shutil.rmtree(agent_dir, ignore_errors=True)
            return None

    def delete_agent(self, name: str) -> bool:
        """
        Delete an agent by removing its directory.

        Cannot delete the active agent or protected agents like "default".

        Args:
            name: Agent name to delete

        Returns:
            True if deleted, False if cannot delete
        """
        import shutil

        # Protected agents that cannot be deleted
        protected_agents = {"default"}

        # Check if agent exists
        if name not in self._agents:
            logger.warning(f"Agent not found: {name}")
            return False

        # Check if protected
        if name in protected_agents:
            logger.warning(f"Cannot delete protected agent: {name}")
            return False

        # Check if active
        if self.is_active(name):
            logger.warning(f"Cannot delete active agent: {name}")
            return False

        agent = self._agents[name]
        agent_dir = agent.directory

        # Only delete from local directory (never delete global agents)
        if not agent_dir.is_relative_to(self.local_agents_dir):
            logger.warning(f"Cannot delete agent from global directory: {name}")
            return False

        try:
            # Remove the directory
            shutil.rmtree(agent_dir)
            # Remove from internal dict
            del self._agents[name]
            logger.info(f"Deleted agent: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete agent {name}: {e}")
            return False

    def load_default_agent(self, cli_agent_name: Optional[str] = None) -> Optional[str]:
        """
        Load the appropriate default agent based on priority.
        
        Priority:
        1. CLI agent name (highest, one-time override)
        2. Project default (.kollabor-cli/config.json)
        3. Global default (~/.kollabor-cli/config.json)
        4. Fallback to "default" agent
        
        Args:
            cli_agent_name: Agent name from CLI --agent argument
            
        Returns:
            Name of agent that was activated, or None if failed
        """
        from ..utils.config_utils import get_default_agent
        
        # Priority 1: CLI argument (one-time override)
        if cli_agent_name:
            if self.set_active_agent(cli_agent_name):
                logger.info(f"Loaded agent from CLI argument: {cli_agent_name}")
                return cli_agent_name
            else:
                logger.warning(f"CLI agent '{cli_agent_name}' not found, trying defaults")
        
        # Priority 2: Project default
        project_agent, level = get_default_agent()
        if level == "project" and project_agent:
            if self.set_active_agent(project_agent):
                logger.info(f"Loaded project default agent: {project_agent}")
                return project_agent
            else:
                logger.warning(f"Project default agent '{project_agent}' not found, trying next level")
        
        # Priority 3: Global default
        global_agent, level = get_default_agent()
        if level == "global" and global_agent:
            if self.set_active_agent(global_agent):
                logger.info(f"Loaded global default agent: {global_agent}")
                return global_agent
            else:
                logger.warning(f"Global default agent '{global_agent}' not found, trying fallback")
        
        # Priority 4: Fallback to "default" agent
        if self.set_active_agent("default", load_defaults=True):
            logger.info("Loaded fallback default agent")
            return "default"
        
        logger.error("Failed to load any agent")
        return None

    def update_agent(
        self,
        original_name: str,
        new_name: str,
        description: str = "",
        profile: Optional[str] = None,
        system_prompt: str = "",
        default_skills: Optional[List[str]] = None,
    ) -> bool:
        """
        Update an existing agent's configuration.

        Can rename the agent (rename directory), update description,
        profile, system prompt, and default skills. Only works for agents in the
        local directory (.kollabor-cli/agents/).

        Args:
            original_name: Current name of the agent to update.
            new_name: New name for the agent (can be same as original).
            description: New description.
            profile: New preferred LLM profile name.
            system_prompt: New system prompt content.
            default_skills: List of skill names to auto-load when agent is activated.

        Returns:
            True if updated successfully, False otherwise.
        """
        import shutil

        # Check if agent exists
        if original_name not in self._agents:
            logger.warning(f"Agent not found for update: {original_name}")
            return False

        agent = self._agents[original_name]
        agent_dir = agent.directory

        # Only update local agents (not global)
        local_path = get_local_agents_path()
        if not self.local_agents_dir or not agent_dir.is_relative_to(self.local_agents_dir):
            logger.warning(f"Cannot edit agent from global directory: {original_name}")
            return False

        try:
            # If renaming, we need to move the directory
            if new_name != original_name:
                # Check if new name already exists
                if new_name in self._agents:
                    logger.warning(f"Agent already exists with new name: {new_name}")
                    return False

                new_agent_dir = local_path / new_name

                # Check if target directory already exists
                if new_agent_dir.exists():
                    logger.warning(f"Target directory already exists: {new_agent_dir}")
                    return False

                # Rename directory
                shutil.move(str(agent_dir), str(new_agent_dir))
                agent_dir = new_agent_dir
                logger.info(f"Renamed agent directory: {original_name} -> {new_name}")

            # Update system_prompt.md
            prompt_file = agent_dir / "system_prompt.md"
            if system_prompt:
                prompt_file.write_text(system_prompt, encoding="utf-8")
                logger.info(f"Updated system prompt for agent: {new_name}")

            # Update or create agent.json for description, profile, and default_skills
            agent_json: Dict[str, Any] = {}
            if description or profile or default_skills:
                agent_json["description"] = description or f"Agent: {new_name}"
                if profile:
                    agent_json["profile"] = profile
                if default_skills:
                    agent_json["default_skills"] = default_skills

            if agent_json:
                json_file = agent_dir / "agent.json"
                json_file.write_text(
                    json.dumps(agent_json, indent=4, ensure_ascii=False),
                    encoding="utf-8"
                )
                logger.info(f"Updated agent.json for agent: {new_name}")
            elif (agent_dir / "agent.json").exists():
                # Remove agent.json if no description or profile
                (agent_dir / "agent.json").unlink()

            # If renamed, remove old entry from dict
            if new_name != original_name:
                del self._agents[original_name]

            # Reload the agent from directory
            # Check if it overrides a global agent
            overrides = (
                self.global_agents_dir is not None
                and (self.global_agents_dir / new_name).exists()
            )
            updated_agent = Agent.from_directory(agent_dir, source="local", overrides_global=overrides)
            if updated_agent:
                self._agents[new_name] = updated_agent

                # If this was the active agent, update the active name
                if self._active_agent_name == original_name:
                    self._active_agent_name = new_name

                logger.info(f"Updated agent: {new_name}")
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to update agent {original_name}: {e}")
            # If rename failed, try to revert
            if new_name != original_name:
                original_dir = local_path / original_name
                new_dir = local_path / new_name
                if not original_dir.exists() and new_dir.exists():
                    try:
                        shutil.move(str(new_dir), str(original_dir))
                    except:
                        pass
            return False
