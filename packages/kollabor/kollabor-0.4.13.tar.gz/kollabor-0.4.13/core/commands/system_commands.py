"""Core system commands for Kollabor CLI."""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..events.models import (
    CommandDefinition,
    CommandMode,
    CommandCategory,
    CommandResult,
    SlashCommand,
    UIConfig,
    EventType,
    Hook,
    Event,
)

logger = logging.getLogger(__name__)


class SystemCommandsPlugin:
    """Core system commands plugin.

    Provides essential system management commands like /help, /config, /status.
    These commands are automatically registered at application startup.
    """

    def __init__(
        self,
        command_registry,
        event_bus,
        config_manager,
        llm_service=None,
        profile_manager=None,
        agent_manager=None,
    ) -> None:
        """Initialize system commands plugin.

        Args:
            command_registry: Command registry for registration.
            event_bus: Event bus for system events.
            config_manager: Configuration manager for system settings.
            llm_service: LLM service for conversation management.
            profile_manager: LLM profile manager.
            agent_manager: Agent/skill manager.
        """
        self.name = "system"
        self.command_registry = command_registry
        self.event_bus = event_bus
        self.config_manager = config_manager
        self.llm_service = llm_service
        self.profile_manager = profile_manager
        self.agent_manager = agent_manager
        self.logger = logger

    def register_commands(self) -> None:
        """Register all system commands."""
        try:
            # Register /help command
            help_command = CommandDefinition(
                name="help",
                description="Show available commands and usage",
                handler=self.handle_help,
                plugin_name=self.name,
                category=CommandCategory.SYSTEM,
                mode=CommandMode.INSTANT,
                aliases=["h", "?"],
                icon="❓"
            )
            self.command_registry.register_command(help_command)

            # Register /config command
            config_command = CommandDefinition(
                name="config",
                description="Open system configuration panel",
                handler=self.handle_config,
                plugin_name=self.name,
                category=CommandCategory.SYSTEM,
                mode=CommandMode.STATUS_TAKEOVER,
                aliases=["settings", "preferences"],
                icon="[INFO]",
                ui_config=UIConfig(
                    type="tree",
                    navigation=["↑↓←→", "Enter", "Esc"],
                    height=15,
                    title="System Configuration",
                    footer="↑↓←→ navigate • Enter edit • Esc exit"
                )
            )
            self.command_registry.register_command(config_command)

            # Register /status command
            status_command = CommandDefinition(
                name="status",
                description="Show system status and diagnostics",
                handler=self.handle_status,
                plugin_name=self.name,
                category=CommandCategory.SYSTEM,
                mode=CommandMode.STATUS_TAKEOVER,
                aliases=["info", "diagnostics"],
                icon="[STATS]",
                ui_config=UIConfig(
                    type="table",
                    navigation=["↑↓", "Esc"],
                    height=12,
                    title="System Status",
                    footer="↑↓ navigate • Esc exit"
                )
            )
            self.command_registry.register_command(status_command)

            # Register /version command
            version_command = CommandDefinition(
                name="version",
                description="Show application version information",
                handler=self.handle_version,
                plugin_name=self.name,
                category=CommandCategory.SYSTEM,
                mode=CommandMode.INSTANT,
                aliases=["v", "ver"],
                icon="[INFO]"
            )
            self.command_registry.register_command(version_command)

            # Note: /resume command is handled by resume_conversation_plugin.py

            # Register /profile command
            profile_command = CommandDefinition(
                name="profile",
                description="Manage LLM API profiles",
                handler=self.handle_profile,
                plugin_name=self.name,
                category=CommandCategory.SYSTEM,
                mode=CommandMode.STATUS_TAKEOVER,
                aliases=["prof", "llm"],
                icon="[PROF]",
                ui_config=UIConfig(
                    type="modal",
                    navigation=["↑↓", "Enter", "Esc"],
                    height=15,
                    title="LLM Profiles",
                    footer="↑↓ navigate • Enter select • Esc exit"
                )
            )
            self.command_registry.register_command(profile_command)

            # Register /agent command
            agent_command = CommandDefinition(
                name="agent",
                description="Manage agents and their configurations",
                handler=self.handle_agent,
                plugin_name=self.name,
                category=CommandCategory.AGENT,
                mode=CommandMode.STATUS_TAKEOVER,
                aliases=["ag"],
                icon="[AGENT]",
                ui_config=UIConfig(
                    type="modal",
                    navigation=["↑↓", "Enter", "Esc"],
                    height=15,
                    title="Agents",
                    footer="↑↓ navigate • Enter select • Esc exit"
                )
            )
            self.command_registry.register_command(agent_command)

            # Register /skill command
            skill_command = CommandDefinition(
                name="skill",
                description="Load or unload agent skills",
                handler=self.handle_skill,
                plugin_name=self.name,
                category=CommandCategory.AGENT,
                mode=CommandMode.STATUS_TAKEOVER,
                aliases=["sk"],
                icon="[SKILL]",
                ui_config=UIConfig(
                    type="modal",
                    navigation=["↑↓", "Enter", "Esc"],
                    height=15,
                    title="Agent Skills",
                    footer="↑↓ navigate • Enter select • Esc exit"
                )
            )
            self.command_registry.register_command(skill_command)

            self.logger.info("System commands registered successfully")

        except Exception as e:
            self.logger.error(f"Error registering system commands: {e}")

    async def register_hooks(self) -> None:
        """Register event hooks for modal command handling."""
        try:
            hook = Hook(
                name="system_modal_command",
                plugin_name="system",
                event_type=EventType.MODAL_COMMAND_SELECTED,
                priority=10,
                callback=self._handle_modal_command
            )
            await self.event_bus.register_hook(hook)
            self.logger.info("System modal command hook registered")
        except Exception as e:
            self.logger.error(f"Error registering system hooks: {e}")

    async def _handle_modal_command(
        self, data: Dict[str, Any], event: Event
    ) -> Dict[str, Any]:
        """Handle modal command selection events for profile/agent/skill.

        Args:
            data: Event data containing command info.
            event: Event object.

        Returns:
            Modified data dict with display_messages key.
        """
        command = data.get("command", {})
        action = command.get("action")

        self.logger.info(f"System modal command received: action={action}")

        # Handle profile selection
        if action == "select_profile":
            profile_name = command.get("profile_name")
            if profile_name and self.profile_manager:
                if self.profile_manager.set_active_profile(profile_name):
                    profile = self.profile_manager.get_active_profile()
                    # Update the API service with new profile settings
                    if self.llm_service and hasattr(self.llm_service, 'api_service'):
                        self.llm_service.api_service.update_from_profile(profile)
                        # Reload native tools (profile may have different native_tool_calling setting)
                        import asyncio
                        asyncio.create_task(self.llm_service._load_native_tools())
                    tool_mode = "native" if profile.get_native_tool_calling() else "xml"
                    data["display_messages"] = [
                        ("system", f"[ok] Switched to profile: {profile_name}\n  Model: {profile.model}\n  API: {profile.api_url}\n  Tool format: {profile.tool_format}\n  Tool calling: {tool_mode}", {}),
                    ]
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Profile not found: {profile_name}", {}),
                    ]

        # Handle agent selection
        elif action == "select_agent":
            agent_name = command.get("agent_name")
            if agent_name and self.agent_manager:
                if self.agent_manager.set_active_agent(agent_name):
                    # Rebuild system prompt for the new agent
                    if self.llm_service:
                        self.llm_service.rebuild_system_prompt()
                    agent = self.agent_manager.get_active_agent()
                    skills = agent.list_skills() if agent else []
                    skill_info = f" ({len(skills)} skills)" if skills else ""
                    msg = f"[ok] Switched to agent: {agent_name}{skill_info}"
                    if agent and agent.profile:
                        msg += f"\n  Preferred profile: {agent.profile}"
                    data["display_messages"] = [("system", msg, {})]
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Agent not found: {agent_name}", {}),
                    ]

        # Handle agent clear
        elif action == "clear_agent":
            if self.agent_manager:
                self.agent_manager.clear_active_agent()
                # Rebuild system prompt without agent
                if self.llm_service:
                    self.llm_service.rebuild_system_prompt()
                data["display_messages"] = [
                    ("system", "[ok] Cleared active agent", {}),
                ]

        # Handle skill load
        elif action == "load_skill":
            skill_name = command.get("skill_name")
            if skill_name and self.agent_manager:
                agent = self.agent_manager.get_active_agent()
                skill = agent.get_skill(skill_name) if agent else None
                if skill and self.agent_manager.load_skill(skill_name):
                    # Inject skill content as user message instead of system prompt
                    if self.llm_service:
                        skill_message = f"## Skill: {skill_name}\n\n{skill.content}"
                        self.llm_service._add_conversation_message("user", skill_message)
                    data["display_messages"] = [
                        ("system", f"[ok] Loaded skill: {skill_name}", {}),
                    ]
                    # Reopen the skills modal (skip reload since memory is fresh)
                    modal_def = self._get_skills_modal_definition(skip_reload=True)
                    if modal_def:
                        data["show_modal"] = modal_def
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Skill not found: {skill_name}", {}),
                    ]

        # Handle skill unload
        elif action == "unload_skill":
            skill_name = command.get("skill_name")
            if skill_name and self.agent_manager:
                if self.agent_manager.unload_skill(skill_name):
                    # Add message indicating skill was unloaded
                    if self.llm_service:
                        self.llm_service._add_conversation_message(
                            "user",
                            f"[Skill '{skill_name}' has been unloaded - please disregard its instructions]"
                        )
                    data["display_messages"] = [
                        ("system", f"[ok] Unloaded skill: {skill_name}", {}),
                    ]
                    # Reopen the skills modal (skip reload since memory is fresh)
                    modal_def = self._get_skills_modal_definition(skip_reload=True)
                    if modal_def:
                        data["show_modal"] = modal_def
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Skill not loaded: {skill_name}", {}),
                    ]

        # Handle toggle default skill (project scope)
        elif action == "toggle_default_skill":
            skill_name = command.get("skill_name")
            if skill_name and self.agent_manager:
                success, is_default = self.agent_manager.toggle_default_skill(
                    skill_name, scope="project"
                )
                if success:
                    status = "added to" if is_default else "removed from"
                    data["display_messages"] = [
                        ("system", f"[ok] Skill '{skill_name}' {status} project defaults", {}),
                    ]
                    # Reopen the skills modal
                    modal_def = self._get_skills_modal_definition(skip_reload=True)
                    if modal_def:
                        data["show_modal"] = modal_def
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Failed to toggle project default for: {skill_name}", {}),
                    ]

        # Handle toggle global default skill
        elif action == "toggle_global_default_skill":
            skill_name = command.get("skill_name")
            if skill_name and self.agent_manager:
                success, is_default = self.agent_manager.toggle_default_skill(
                    skill_name, scope="global"
                )
                if success:
                    status = "added to" if is_default else "removed from"
                    data["display_messages"] = [
                        ("system", f"[ok] Skill '{skill_name}' {status} global defaults", {}),
                    ]
                    # Reopen the skills modal
                    modal_def = self._get_skills_modal_definition(skip_reload=True)
                    if modal_def:
                        data["show_modal"] = modal_def
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Failed to toggle global default for: {skill_name}", {}),
                    ]

        # Handle create skill - show form modal
        elif action == "create_skill_prompt":
            if self.agent_manager:
                active_agent = self.agent_manager.get_active_agent()
                if active_agent:
                    data["show_modal"] = self._get_create_skill_modal_definition(active_agent.name)
                else:
                    data["display_messages"] = [
                        ("error", "[err] No active agent", {}),
                    ]

        # Handle create skill form submission
        elif action == "create_skill_submit":
            form_data = command.get("form_data", {})
            name = form_data.get("name", "").strip()
            description = form_data.get("description", "").strip()

            if not name:
                data["display_messages"] = [
                    ("error", "[err] Skill name is required", {}),
                ]
            elif not description:
                data["display_messages"] = [
                    ("error", "[err] Description is required for AI generation", {}),
                ]
            elif self.agent_manager:
                active_agent = self.agent_manager.get_active_agent()
                if active_agent:
                    if self.llm_service:
                        # Build the generation prompt and send to LLM
                        generation_prompt = self._build_skill_generation_prompt(
                            agent_name=active_agent.name,
                            skill_name=name,
                            description=description,
                        )
                        # Send to LLM - it will use <create> tags to generate the file
                        await self.llm_service.process_user_input(generation_prompt)
                        # Close modal - LLM handles the rest with existing tool infrastructure
                        data["close_modal"] = True
                    else:
                        data["display_messages"] = [
                            ("error", "[err] LLM service not available", {}),
                        ]

        # Handle edit skill - show form modal
        elif action == "edit_skill_prompt":
            skill_name = command.get("skill_name")
            if skill_name and self.agent_manager:
                active_agent = self.agent_manager.get_active_agent()
                if active_agent:
                    modal_def = self._get_edit_skill_modal_definition(active_agent.name, skill_name)
                    if modal_def:
                        data["show_modal"] = modal_def
                    else:
                        data["display_messages"] = [
                            ("error", f"[err] Skill not found: {skill_name}", {}),
                        ]
            else:
                data["display_messages"] = [
                    ("error", "[err] Select a skill to edit", {}),
                ]

        # Handle edit skill form submission (rename only)
        elif action == "edit_skill_submit":
            form_data = command.get("form_data", {})
            original_name = command.get("edit_skill_name", "")
            new_name = form_data.get("name", "").strip()

            if not new_name:
                data["display_messages"] = [
                    ("error", "[err] Skill name is required", {}),
                ]
            elif self.agent_manager:
                active_agent = self.agent_manager.get_active_agent()
                if active_agent:
                    success = self._rename_skill_file(active_agent, original_name, new_name)
                    if success:
                        self.agent_manager.refresh()
                        msg = f"[ok] Updated skill: {new_name}"
                        if new_name != original_name:
                            msg += f"\n  Renamed from: {original_name}"
                        data["display_messages"] = [("system", msg, {})]
                        modal_def = self._get_skills_modal_definition(skip_reload=True)
                        if modal_def:
                            data["show_modal"] = modal_def
                    else:
                        data["display_messages"] = [
                            ("error", f"[err] Failed to rename skill", {}),
                        ]

        # Handle delete skill - show confirmation modal
        elif action == "delete_skill_prompt":
            skill_name = command.get("skill_name")
            if skill_name and self.agent_manager:
                active_agent = self.agent_manager.get_active_agent()
                if active_agent:
                    modal_def = self._get_delete_skill_confirm_modal(active_agent.name, skill_name)
                    if modal_def:
                        data["show_modal"] = modal_def
                    else:
                        data["display_messages"] = [
                            ("error", f"[err] Cannot delete skill: {skill_name}", {}),
                        ]
            else:
                data["display_messages"] = [
                    ("error", "[err] Select a skill to delete", {}),
                ]

        # Handle delete skill confirmation
        elif action == "delete_skill_confirm":
            skill_name = command.get("skill_name")
            if skill_name and self.agent_manager:
                active_agent = self.agent_manager.get_active_agent()
                if active_agent:
                    success = self._delete_skill_file(active_agent, skill_name)
                    if success:
                        self.agent_manager.refresh()
                        data["display_messages"] = [
                            ("system", f"[ok] Deleted skill: {skill_name}", {}),
                        ]
                        modal_def = self._get_skills_modal_definition(skip_reload=True)
                        if modal_def:
                            data["show_modal"] = modal_def
                    else:
                        data["display_messages"] = [
                            ("error", f"[err] Failed to delete skill: {skill_name}", {}),
                        ]

        # Handle save profile to config (profiles are global-only)
        elif action == "save_profile_to_config":
            if self.profile_manager:
                profile = self.profile_manager.get_active_profile()
                if profile:
                    result = self.profile_manager.save_profile_values_to_config(profile)

                    if result.get("global"):
                        # Reload profiles from config to pick up saved values
                        self.profile_manager.reload()
                        data["display_messages"] = [
                            ("system", f"[ok] Saved '{profile.name}' profile to global config (~/.kollabor-cli/)", {}),
                        ]
                    else:
                        data["display_messages"] = [
                            ("error", f"[err] Failed to save profile '{profile.name}'.", {}),
                        ]
                    # Reopen the profile modal (skip_reload since we just reloaded above)
                    data["show_modal"] = self._get_profiles_modal_definition(skip_reload=True)
                else:
                    data["display_messages"] = [
                        ("error", "[err] No active profile to save.", {}),
                    ]

        # Handle create profile - show form modal
        elif action == "create_profile_prompt":
            data["show_modal"] = self._get_create_profile_modal_definition()

        # Handle create profile form submission
        elif action == "create_profile_submit":
            form_data = command.get("form_data", {})
            name = form_data.get("name", "").strip()
            api_url = form_data.get("api_url", "").strip()
            model = form_data.get("model", "").strip()
            api_token = form_data.get("api_token", "").strip() or None
            temperature = float(form_data.get("temperature", 0.7))
            tool_format = form_data.get("tool_format", "openai")
            # Convert dropdown value to bool (native=True, xml=False)
            native_tool_calling = form_data.get("native_tool_calling", "native") == "native"
            description = form_data.get("description", "").strip()

            if not name or not api_url or not model:
                data["display_messages"] = [
                    ("error", "[err] Name, API URL, and Model are required", {}),
                ]
            elif self.profile_manager:
                profile = self.profile_manager.create_profile(
                    name=name,
                    api_url=api_url,
                    model=model,
                    api_token=api_token,
                    temperature=temperature,
                    tool_format=tool_format,
                    native_tool_calling=native_tool_calling,
                    description=description or f"Created via /profile",
                    save_to_config=True
                )
                if profile:
                    data["display_messages"] = [
                        ("system", f"[ok] Created profile: {name}\n  API: {api_url}\n  Model: {model}\n  Saved to config.json", {}),
                    ]
                    # Reopen the profile modal so user can see the new profile
                    data["show_modal"] = self._get_profiles_modal_definition(skip_reload=True)
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Failed. Profile '{name}' may already exist.", {}),
                    ]

        # Handle create agent - show form modal
        elif action == "create_agent_prompt":
            data["show_modal"] = self._get_create_agent_modal_definition()

        # Handle create agent form submission - AI generation
        elif action == "create_agent_submit":
            form_data = command.get("form_data", {})
            name = form_data.get("name", "").strip()
            description = form_data.get("description", "").strip()
            profile = form_data.get("profile", "").strip()
            source = form_data.get("source", "global").strip()

            if not name:
                data["display_messages"] = [
                    ("error", "[err] Agent name is required", {}),
                ]
            elif not description:
                data["display_messages"] = [
                    ("error", "[err] Description is required for AI generation", {}),
                ]
            elif self.llm_service:
                # Build the generation prompt and send to LLM
                generation_prompt = self._build_agent_generation_prompt(
                    name=name,
                    description=description,
                    profile=profile if profile and profile != "(none)" else None,
                    source=source,
                )
                # Send to LLM - it will use <create> tags to generate files
                await self.llm_service.process_user_input(generation_prompt)
                # Close modal - LLM handles the rest with existing tool infrastructure
                data["close_modal"] = True
            else:
                data["display_messages"] = [
                    ("error", "[err] LLM service not available", {}),
                ]

        # Handle edit profile - show form modal with profile data
        elif action == "edit_profile_prompt":
            profile_name = command.get("profile_name")
            if profile_name and self.profile_manager:
                modal_def = self._get_edit_profile_modal_definition(profile_name)
                if modal_def:
                    data["show_modal"] = modal_def
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Profile not found: {profile_name}", {}),
                    ]
            else:
                data["display_messages"] = [
                    ("error", "[err] Select a profile to edit", {}),
                ]

        # Handle edit profile form submission
        elif action == "edit_profile_submit":
            form_data = command.get("form_data", {})
            original_name = command.get("edit_profile_name", "")
            new_name = form_data.get("name", "").strip()
            api_url = form_data.get("api_url", "").strip()
            model = form_data.get("model", "").strip()
            api_token = form_data.get("api_token", "").strip() or None
            temperature = float(form_data.get("temperature", 0.7))
            tool_format = form_data.get("tool_format", "openai")
            # Convert dropdown value to bool (native=True, xml=False)
            native_tool_calling = form_data.get("native_tool_calling", "native") == "native"
            description = form_data.get("description", "").strip()

            if not new_name or not api_url or not model:
                data["display_messages"] = [
                    ("error", "[err] Name, API URL, and Model are required", {}),
                ]
            elif self.profile_manager:
                success = self.profile_manager.update_profile(
                    original_name=original_name,
                    new_name=new_name,
                    api_url=api_url,
                    model=model,
                    api_token=api_token,
                    temperature=temperature,
                    tool_format=tool_format,
                    native_tool_calling=native_tool_calling,
                    description=description,
                    save_to_config=True
                )
                if success:
                    # If this profile is active (check both original and new name), update the API service
                    is_active = (self.profile_manager.is_active(new_name) or
                                self.profile_manager.is_active(original_name))
                    if is_active and self.llm_service and hasattr(self.llm_service, 'api_service'):
                        profile = self.profile_manager.get_profile(new_name) or self.profile_manager.get_profile(original_name)
                        if profile:
                            self.llm_service.api_service.update_from_profile(profile)
                            # Reload native tools (tool calling mode may have changed)
                            import asyncio
                            asyncio.create_task(self.llm_service._load_native_tools())
                    tool_mode = "native" if native_tool_calling else "xml"
                    msg = f"[ok] Updated profile: {new_name}\n  API: {api_url}\n  Model: {model}\n  Tool format: {tool_format}\n  Tool calling: {tool_mode}"
                    if is_active:
                        msg += "\n  [reloaded - changes applied]"
                    data["display_messages"] = [("system", msg, {})]
                    # Reopen the profile modal
                    data["show_modal"] = self._get_profiles_modal_definition(skip_reload=True)
                else:
                    data["display_messages"] = [
                        ("error", "[err] Failed to update profile", {}),
                    ]

        # Handle delete profile prompt - show confirmation modal
        elif action == "delete_profile_prompt":
            profile_name = command.get("profile_name")
            if profile_name and self.profile_manager:
                modal_def = self._get_delete_profile_confirm_modal(profile_name)
                if modal_def:
                    data["show_modal"] = modal_def
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Cannot delete profile: {profile_name}", {}),
                    ]
            else:
                data["display_messages"] = [
                    ("error", "[err] Select a profile to delete", {}),
                ]

        # Handle delete profile confirmation
        elif action == "delete_profile_confirm":
            profile_name = command.get("profile_name")
            if profile_name and self.profile_manager:
                success = self.profile_manager.delete_profile(profile_name)
                if success:
                    data["display_messages"] = [
                        ("system", f"[ok] Deleted profile: {profile_name}", {}),
                    ]
                    # Reopen the profile modal so user can continue managing
                    # Skip reload since memory state is already updated
                    data["show_modal"] = self._get_profiles_modal_definition(skip_reload=True)
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Failed to delete profile: {profile_name}", {}),
                    ]

        # Handle delete agent prompt - show confirmation modal
        elif action == "delete_agent_prompt":
            agent_name = command.get("agent_name")
            if agent_name and self.agent_manager:
                modal_def = self._get_delete_agent_confirm_modal(agent_name)
                if modal_def:
                    data["show_modal"] = modal_def
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Cannot delete agent: {agent_name}", {}),
                    ]
            else:
                data["display_messages"] = [
                    ("error", "[err] Select an agent to delete", {}),
                ]

        # Handle delete agent confirmation
        elif action == "delete_agent_confirm":
            agent_name = command.get("agent_name")
            if agent_name and self.agent_manager:
                success = self.agent_manager.delete_agent(agent_name)
                if success:
                    data["display_messages"] = [
                        ("system", f"[ok] Deleted agent: {agent_name}", {}),
                    ]
                    # Reopen the agents modal so user can continue managing
                    # Skip reload since memory state is already updated
                    data["show_modal"] = self._get_agents_modal_definition(skip_reload=True)
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Failed to delete agent: {agent_name}", {}),
                    ]

        # Handle edit agent - show form modal with agent data
        elif action == "edit_agent_prompt":
            agent_name = command.get("agent_name")
            if agent_name and self.agent_manager:
                modal_def = self._get_edit_agent_modal_definition(agent_name)
                if modal_def:
                    data["show_modal"] = modal_def
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Agent not found: {agent_name}", {}),
                    ]
            else:
                data["display_messages"] = [
                    ("error", "[err] Select an agent to edit", {}),
                ]

        # Handle toggle project default
        elif action == "toggle_project_default":
            agent_name = command.get("agent_name")
            if agent_name and self.agent_manager:
                from ..utils.config_utils import get_all_default_agents, set_default_agent, clear_default_agent
                
                # Check if this agent is already project default
                defaults = get_all_default_agents()
                current_project_default = defaults.get("project")
                
                if current_project_default == agent_name:
                    # Clear it
                    if clear_default_agent("project"):
                        data["display_messages"] = [
                            ("system", f"[ok] Cleared project default agent", {}),
                        ]
                else:
                    # Set it
                    if set_default_agent(agent_name, "project"):
                        data["display_messages"] = [
                            ("system", f"[ok] Set '{agent_name}' as project default agent", {}),
                        ]
                    else:
                        data["display_messages"] = [
                            ("error", f"[err] Failed to set project default", {}),
                        ]
                
                # Reopen modal to show updated indicators
                modal_def = self._get_agents_modal_definition(skip_reload=True)
                if modal_def:
                    data["show_modal"] = modal_def

        # Handle toggle global default
        elif action == "toggle_global_default":
            agent_name = command.get("agent_name")
            if agent_name and self.agent_manager:
                from ..utils.config_utils import get_all_default_agents, set_default_agent, clear_default_agent
                
                # Check if this agent is already global default
                defaults = get_all_default_agents()
                current_global_default = defaults.get("global")
                
                if current_global_default == agent_name:
                    # Clear it
                    if clear_default_agent("global"):
                        data["display_messages"] = [
                            ("system", f"[ok] Cleared global default agent", {}),
                        ]
                else:
                    # Set it
                    if set_default_agent(agent_name, "global"):
                        data["display_messages"] = [
                            ("system", f"[ok] Set '{agent_name}' as global default agent", {}),
                        ]
                    else:
                        data["display_messages"] = [
                            ("error", f"[err] Failed to set global default", {}),
                        ]
                
                # Reopen modal to show updated indicators
                modal_def = self._get_agents_modal_definition(skip_reload=True)
                if modal_def:
                    data["show_modal"] = modal_def

        # Handle edit agent form submission
        elif action == "edit_agent_submit":
            form_data = command.get("form_data", {})
            original_name = command.get("edit_agent_name", "")
            new_name = form_data.get("name", "").strip()
            description = form_data.get("description", "").strip()
            profile = form_data.get("profile", "").strip()

            if not new_name:
                data["display_messages"] = [
                    ("error", "[err] Agent name is required", {}),
                ]
            elif self.agent_manager:
                success = self.agent_manager.update_agent(
                    original_name=original_name,
                    new_name=new_name,
                    description=description,
                    profile=profile if profile and profile != "(none)" else None,
                    system_prompt=None,  # Don't update system_prompt via modal
                )
                if success:
                    msg = f"[ok] Updated agent: {new_name}"
                    if new_name != original_name:
                        msg += f"\n  Renamed from: {original_name}"
                    if description:
                        msg += f"\n  Description: {description[:50]}..."
                    data["display_messages"] = [("system", msg, {})]
                    # Reopen the agents modal
                    data["show_modal"] = self._get_agents_modal_definition(skip_reload=True)
                else:
                    data["display_messages"] = [
                        ("error", f"[err] Failed to update agent", {}),
                    ]

        return data

    def _get_create_profile_modal_definition(self) -> Dict[str, Any]:
        """Get modal definition for creating a new profile."""
        return {
            "title": "Create New Profile",
            "footer": "Tab: next • Ctrl+S: create • Esc: cancel",
            "width": 82,
            "height": 26,
            "form_action": "create_profile_submit",
            "sections": [
                {
                    "title": "Profile Name (required)",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Name *",
                            "field": "name",
                            "placeholder": "my-llm, claude-prod, openai-dev, etc.",
                            "help": "Used for env vars: KOLLABOR_{NAME}_TOKEN"
                        },
                    ]
                },
                {
                    "title": "Connection (required)",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Endpoint *",
                            "field": "api_url",
                            "placeholder": "https://api.openai.com/v1/chat/completions",
                            "help": "API endpoint URL"
                        },
                        {
                            "type": "dropdown",
                            "label": "Provider",
                            "field": "tool_format",
                            "options": ["openai", "anthropic"],
                            "current_value": "openai",
                            "help": "API format (most use openai)"
                        },
                        {
                            "type": "dropdown",
                            "label": "Tool Calling",
                            "field": "native_tool_calling",
                            "options": ["native", "xml"],
                            "current_value": "native",
                            "help": "native=API tools, xml=XML tags only"
                        },
                    ]
                },
                {
                    "title": "Authentication (required)",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Token *",
                            "field": "api_token",
                            "placeholder": "sk-... or set env var KOLLABOR_{NAME}_TOKEN",
                            "password": True,
                            "help": "API key (or leave empty and set env var)"
                        },
                    ]
                },
                {
                    "title": "Model (required)",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Model *",
                            "field": "model",
                            "placeholder": "gpt-4-turbo, claude-sonnet-4-20250514, qwen/qwen3-4b",
                            "help": "Model identifier"
                        },
                    ]
                },
                {
                    "title": "Advanced (optional)",
                    "widgets": [
                        {
                            "type": "slider",
                            "label": "Temperature",
                            "field": "temperature",
                            "min_value": 0.0,
                            "max_value": 2.0,
                            "step": 0.1,
                            "current_value": 0.7,
                            "help": "0.0 = precise, 2.0 = creative"
                        },
                        {
                            "type": "text_input",
                            "label": "Description",
                            "field": "description",
                            "placeholder": "Optional description"
                        },
                    ]
                }
            ],
            "actions": [
                {"key": "Ctrl+S", "label": "[ Create ]", "action": "submit", "style": "primary"},
                {"key": "Escape", "label": "[ Cancel ]", "action": "cancel", "style": "secondary"}
            ]
        }

    def _get_edit_profile_modal_definition(self, profile_name: str) -> Dict[str, Any]:
        """Get modal definition for editing an existing profile.

        Args:
            profile_name: Name of the profile to edit.

        Returns:
            Modal definition dict with pre-populated values.
        """
        if not self.profile_manager:
            return {}

        profile = self.profile_manager.get_profile(profile_name)
        if not profile:
            return {}

        # Get env var hints for this profile
        env_hints = profile.get_env_var_hints()

        # Determine token status
        token_from_env = env_hints['token'].is_set
        token_in_config = bool(profile.api_token)
        if token_from_env:
            token_status = f"(using env: {env_hints['token'].name})"
            token_placeholder = "Leave empty to use env var"
        elif token_in_config:
            token_status = "(set in config)"
            token_placeholder = ""
        else:
            token_status = "[REQUIRED - not set]"
            token_placeholder = "Enter API key or set env var"

        # Determine overall status
        issues = []
        if not profile.api_url:
            issues.append("endpoint missing")
        if not profile.model:
            issues.append("model missing")
        if not token_from_env and not token_in_config:
            issues.append("token missing")

        if issues:
            status_line = f"[!] Fix {len(issues)} issue(s): {', '.join(issues)}"
        else:
            status_line = "[ok] Ready to use"

        return {
            "title": f"Edit Profile: {profile_name}",
            "footer": "Tab: next • Ctrl+S: save • Ctrl+T: test • Esc: cancel",
            "width": 82,
            "height": 26,
            "form_action": "edit_profile_submit",
            "edit_profile_name": profile_name,
            "sections": [
                {
                    "title": "Connection (required)",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Endpoint *",
                            "field": "api_url",
                            "value": profile.api_url,
                            "placeholder": "https://api.openai.com/v1/chat/completions",
                            "help": "API endpoint URL"
                        },
                        {
                            "type": "dropdown",
                            "label": "Provider",
                            "field": "tool_format",
                            "options": ["openai", "anthropic"],
                            "current_value": profile.tool_format,
                            "help": "API format (most use openai)"
                        },
                        {
                            "type": "dropdown",
                            "label": "Tool Calling",
                            "field": "native_tool_calling",
                            "options": ["native", "xml"],
                            "current_value": "native" if profile.native_tool_calling else "xml",
                            "help": "native=API tools, xml=XML tags only"
                        },
                    ]
                },
                {
                    "title": "Authentication (required)",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": f"Token * {token_status}",
                            "field": "api_token",
                            "value": profile.api_token or "",
                            "placeholder": token_placeholder,
                            "password": True
                        },
                    ]
                },
                {
                    "title": "Model (required)",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Model *",
                            "field": "model",
                            "value": profile.model,
                            "placeholder": "gpt-4-turbo, claude-sonnet-4-20250514, etc.",
                            "help": "Model identifier"
                        },
                    ]
                },
                {
                    "title": "Advanced (optional)",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Profile Name",
                            "field": "name",
                            "value": profile.name,
                            "placeholder": "my-profile",
                            "help": "Determines env var prefix: KOLLABOR_{NAME}_*"
                        },
                        {
                            "type": "slider",
                            "label": "Temperature",
                            "field": "temperature",
                            "min_value": 0.0,
                            "max_value": 2.0,
                            "step": 0.1,
                            "current_value": profile.temperature,
                            "help": "0.0 = precise, 2.0 = creative"
                        },
                        {
                            "type": "text_input",
                            "label": "Description",
                            "field": "description",
                            "value": profile.description or "",
                            "placeholder": "Optional description"
                        },
                    ]
                },
                {
                    "title": f"Status: {status_line}",
                    "widgets": [
                        {
                            "type": "label",
                            "label": "Env vars",
                            "value": f"{env_hints['token'].name}={'[set]' if token_from_env else '[not set]'}"
                        },
                    ]
                }
            ],
            "actions": [
                {"key": "Ctrl+S", "label": "[ Save ]", "action": "submit", "style": "primary"},
                {"key": "Ctrl+T", "label": "[ Test ]", "action": "test_connection", "style": "secondary"},
                {"key": "Escape", "label": "[ Cancel ]", "action": "cancel", "style": "secondary"}
            ]
        }

    def _get_delete_profile_confirm_modal(self, profile_name: str) -> Dict[str, Any]:
        """Get modal definition for delete profile confirmation.

        Args:
            profile_name: Name of the profile to delete.

        Returns:
            Modal definition dict for confirmation, or empty dict if cannot delete.
        """
        if not self.profile_manager:
            return {}

        profile = self.profile_manager.get_profile(profile_name)
        if not profile:
            return {}

        # Check if profile can be deleted
        if profile_name in self.profile_manager.DEFAULT_PROFILES:
            # Cannot delete built-in profiles
            return {}

        if self.profile_manager.is_active(profile_name):
            # Cannot delete active profile - but we can show a warning
            pass

        is_active = self.profile_manager.is_active(profile_name)
        warning_msg = ""
        if is_active:
            warning_msg = "\n\n[!] This is the currently active profile.\n    You must switch to another profile first."
            can_delete = False
        else:
            can_delete = True

        return {
            "title": f"Delete Profile: {profile_name}?",
            "footer": "Enter confirm • Esc cancel",
            "width": 60,
            "height": 12,
            "sections": [
                {
                    "title": "Confirm Deletion",
                    "commands": [
                        {
                            "name": f"Delete '{profile_name}'",
                            "description": f"Model: {profile.model} @ {profile.api_url}{warning_msg}",
                            "profile_name": profile_name,
                            "action": "delete_profile_confirm" if can_delete else "cancel"
                        },
                        {
                            "name": "Cancel",
                            "description": "Keep the profile",
                            "action": "cancel"
                        }
                    ]
                }
            ],
            "actions": [
                {"key": "Enter", "label": "Confirm", "action": "select"},
                {"key": "Escape", "label": "Cancel", "action": "cancel"}
            ]
        }

    def _get_create_agent_modal_definition(self) -> Dict[str, Any]:
        """Get modal definition for creating a new agent."""
        # Get available profiles for dropdown
        profile_options = ["(none)"]
        if self.profile_manager:
            profile_options.extend(self.profile_manager.get_profile_names())

        return {
            "title": "Create Agent",
            "footer": "Tab navigate • Enter confirm • Ctrl+S save • Esc cancel",
            "width": 70,
            "height": 20,
            "form_action": "create_agent_submit",
            "sections": [
                {
                    "title": "Agent Settings",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Agent Name",
                            "field": "name",
                            "placeholder": "my-agent",
                            "help": "Unique identifier (creates agents/<name>/ directory)"
                        },
                        {
                            "type": "text_input",
                            "label": "Description",
                            "field": "description",
                            "placeholder": "A Python web development specialist...",
                            "help": "Describe what this agent specializes in (AI generates from this)"
                        },
                        {
                            "type": "dropdown",
                            "label": "Source",
                            "field": "source",
                            "options": ["global", "local"],
                            "current_value": "global",
                            "help": "global=~/shared, local=project-specific"
                        },
                        {
                            "type": "dropdown",
                            "label": "Preferred Profile",
                            "field": "profile",
                            "options": profile_options,
                            "current_value": "(none)",
                            "help": "LLM profile to use with this agent"
                        },
                        {
                            "type": "label",
                            "label": "Generation",
                            "value": "AI will generate system prompt and 5-6 skills based on description"
                        },
                    ]
                }
            ],
            "actions": [
                {"key": "Ctrl+S", "label": "Generate", "action": "submit", "style": "primary"},
                {"key": "Escape", "label": "Cancel", "action": "cancel", "style": "secondary"}
            ]
        }

    def _build_agent_generation_prompt(
        self, name: str, description: str, profile: Optional[str] = None, source: str = "global"
    ) -> str:
        """Build prompt for LLM-powered agent generation.

        Args:
            name: Agent name (directory name).
            description: What the agent specializes in.
            profile: Optional preferred LLM profile.
            source: Agent source - "global" or "local".

        Returns:
            Prompt string for the LLM to generate agent files.
        """
        profile_value = f'"{profile}"' if profile else "null"

        # Determine the base path for the agent
        if source == "local":
            agents_path = ".kollabor-cli/agents"
        else:
            agents_path = "~/.kollabor-cli/agents"

        return f'''Create a new agent called "{name}" that specializes in: {description}

IMPORTANT: First, review the structure of the default agent to understand the format:
- Read ~/.kollabor-cli/agents/default/system_prompt.md (the main system prompt template)
- Read ~/.kollabor-cli/agents/default/agent.json (the configuration format)
- Read ~/.kollabor-cli/agents/default/debugging.md (an example skill file format)

After reviewing the templates, create the new agent with the SAME level of detail and quality.

Create these files using <create> tags:

1. system_prompt.md - Comprehensive system prompt (500+ lines) following the default template structure:
   - Header with agent name
   - Core philosophy and mission
   - Session context with <trender> tags for dynamic content
   - Tool execution guidelines
   - Response patterns and examples
   - Quality assurance checklist
   - Error handling guidance

2. agent.json - Configuration file:
   {{"description": "{description}", "profile": {profile_value}}}

3. Create 5-6 skill files (.md) relevant to this agent's specialty. Each skill should:
   - Start with HTML comment description: <!-- Skill name - brief purpose -->
   - Include PHASE 0: Environment verification
   - Include multiple phases with detailed guidance
   - End with Mandatory rules section
   - Be 500+ lines with comprehensive, actionable content

Use this exact format for each file:
<create>
  <file>{agents_path}/{name}/filename.md</file>
  <content>
[file content here - be comprehensive and detailed]
  </content>
</create>

Generate all files now. Match the quality and depth of the default agent templates.'''

    def _build_skill_generation_prompt(
        self, agent_name: str, skill_name: str, description: str
    ) -> str:
        """Build prompt for LLM-powered skill generation.

        Args:
            agent_name: Name of the agent this skill belongs to.
            skill_name: Skill name (filename without .md).
            description: What the skill helps with.

        Returns:
            Prompt string for the LLM to generate the skill file.
        """
        return f'''Create a new skill called "{skill_name}" for the "{agent_name}" agent.

The skill should help with: {description}

IMPORTANT: First, review existing skills in this agent to understand the format and style:
- Read .kollabor-cli/agents/{agent_name}/system_prompt.md (to understand the agent's purpose)
- Read any existing .md skill files in .kollabor-cli/agents/{agent_name}/ for format reference

After reviewing, create a comprehensive skill file that:
1. Starts with HTML comment description: <!-- {skill_name} - {description} -->
2. Has a clear header with skill name
3. Includes PHASE 0: Environment/context verification
4. Has multiple phases with detailed, actionable guidance
5. Includes examples and code snippets where relevant
6. Ends with a "Mandatory Rules" or "Quality Checklist" section
7. Is comprehensive (300+ lines) with real, actionable content

Use this exact format:
<create>
  <file>.kollabor-cli/agents/{agent_name}/{skill_name}.md</file>
  <content>
[comprehensive skill content here - be detailed and actionable]
  </content>
</create>

Generate the skill file now. Match the quality and depth of existing skills.'''

    def _get_delete_agent_confirm_modal(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get modal definition for delete agent confirmation.

        Args:
            agent_name: Name of the agent to delete.

        Returns:
            Modal definition dict for confirmation, or empty dict if cannot delete.
        """
        if not self.agent_manager:
            return {}

        agents = self.agent_manager.list_agents()
        agent = next((a for a in agents if a.name == agent_name), None)
        if not agent:
            return {}

        active_agent = self.agent_manager.get_active_agent()
        active_name = active_agent.name if active_agent else None
        is_active = agent_name == active_name

        warning_msg = ""
        if is_active:
            warning_msg = "\n\n[!] This is the currently active agent.\n    You must clear or switch to another agent first."
            can_delete = False
        else:
            can_delete = True

        skills = agent.list_skills()
        skill_info = f", {len(skills)} skills" if skills else ""

        return {
            "title": f"Delete Agent: {agent_name}?",
            "footer": "Enter confirm • Esc cancel",
            "width": 60,
            "height": 12,
            "sections": [
                {
                    "title": "Confirm Deletion",
                    "commands": [
                        {
                            "name": f"Delete '{agent_name}'",
                            "description": f"{agent.description or 'No description'}{skill_info}{warning_msg}",
                            "agent_name": agent_name,
                            "action": "delete_agent_confirm" if can_delete else "cancel"
                        },
                        {
                            "name": "Cancel",
                            "description": "Keep the agent",
                            "action": "cancel"
                        }
                    ]
                }
            ],
            "actions": [
                {"key": "Enter", "label": "Confirm", "action": "select"},
                {"key": "Escape", "label": "Cancel", "action": "cancel"}
            ]
        }

    def _get_edit_agent_modal_definition(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get modal definition for editing an existing agent.

        Args:
            agent_name: Name of the agent to edit.

        Returns:
            Modal definition dict with pre-populated values, or None if not found.
        """
        if not self.agent_manager:
            return None

        agent = self.agent_manager.get_agent(agent_name)
        if not agent:
            return None

        # Get available profiles for dropdown
        profile_options = ["(none)"]
        if self.profile_manager:
            profile_options.extend(self.profile_manager.get_profile_names())

        # Determine current profile value
        current_profile = agent.profile if agent.profile else "(none)"

        # Read system prompt from file
        system_prompt = agent.system_prompt

        # Get skill info for display
        skills = agent.list_skills()
        skill_info = f", {len(skills)} skills" if skills else ""

        # Determine if agent is protected (cannot be renamed to default name)
        is_protected = agent_name in self.agent_manager.list_agents() and agent_name == "default"

        # Show short path for system_prompt file
        short_path = f"agents/{agent_name}/system_prompt.md"

        return {
            "title": f"Edit Agent: {agent_name}",
            "footer": "Tab navigate • Ctrl+S save • Esc cancel",
            "width": 70,
            "height": 16,
            "form_action": "edit_agent_submit",
            "edit_agent_name": agent_name,  # Track original name for rename
            "sections": [
                {
                    "title": "Agent Settings",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Name",
                            "field": "name",
                            "value": agent.name,
                            "placeholder": "my-agent",
                            "help": "Renames agent directory"
                        },
                        {
                            "type": "text_input",
                            "label": "Desc",
                            "field": "description",
                            "value": agent.description or "",
                            "placeholder": "What this agent does",
                            "help": "Agent description"
                        },
                        {
                            "type": "dropdown",
                            "label": "Profile",
                            "field": "profile",
                            "options": profile_options,
                            "current_value": current_profile,
                            "help": "Preferred LLM profile"
                        },
                    ]
                },
                {
                    "title": f"Files{skill_info}",
                    "widgets": [
                        {
                            "type": "label",
                            "label": "Prompt",
                            "value": short_path,
                            "help": "nano or vim to edit"
                        },
                    ]
                }
            ],
            "actions": [
                {"key": "Ctrl+S", "label": "Save", "action": "submit", "style": "primary"},
                {"key": "Escape", "label": "Cancel", "action": "cancel", "style": "secondary"}
            ]
        }

    def _get_create_skill_modal_definition(self, agent_name: str) -> Dict[str, Any]:
        """Get modal definition for creating a new skill."""
        short_path = f"agents/{agent_name}/<name>.md"

        return {
            "title": f"Create Skill - {agent_name}",
            "footer": "Ctrl+S: create • Esc: cancel",
            "width": 70,
            "height": 18,
            "form_action": "create_skill_submit",
            "sections": [
                {
                    "title": "New Skill",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Name",
                            "field": "name",
                            "placeholder": "my-skill",
                            "help": "Creates <name>.md in agent directory"
                        },
                        {
                            "type": "text_input",
                            "label": "Description",
                            "field": "description",
                            "placeholder": "What this skill helps with...",
                            "help": "AI generates comprehensive skill from this"
                        },
                    ]
                },
                {
                    "title": "Info",
                    "widgets": [
                        {
                            "type": "label",
                            "label": "Location",
                            "value": short_path,
                            "help": "AI generates detailed skill content"
                        },
                    ]
                }
            ],
            "actions": [
                {"key": "Ctrl+S", "label": "Create", "action": "submit", "style": "primary"},
                {"key": "Escape", "label": "Cancel", "action": "cancel", "style": "secondary"}
            ]
        }

    def _get_edit_skill_modal_definition(self, agent_name: str, skill_name: str) -> Optional[Dict[str, Any]]:
        """Get modal definition for editing an existing skill."""
        if not self.agent_manager:
            return None

        active_agent = self.agent_manager.get_active_agent()
        if not active_agent or active_agent.name != agent_name:
            return None

        # Find the skill
        skill = None
        for s in active_agent.list_skills():
            if s.name == skill_name:
                skill = s
                break

        if not skill:
            return None

        # Short path for display
        short_path = f"agents/{agent_name}/{skill_name}.md"

        return {
            "title": f"Edit Skill: {skill_name}",
            "footer": "Tab navigate • Ctrl+S save • Esc cancel",
            "width": 70,
            "height": 14,
            "form_action": "edit_skill_submit",
            "edit_skill_name": skill_name,
            "sections": [
                {
                    "title": "Skill Settings",
                    "widgets": [
                        {
                            "type": "text_input",
                            "label": "Name",
                            "field": "name",
                            "value": skill_name,
                            "placeholder": "my-skill",
                            "help": "Rename the skill file"
                        },
                    ]
                },
                {
                    "title": "File",
                    "widgets": [
                        {
                            "type": "label",
                            "label": "Path",
                            "value": short_path,
                            "help": "nano or vim to edit"
                        },
                    ]
                }
            ],
            "actions": [
                {"key": "Ctrl+S", "label": "Save", "action": "submit", "style": "primary"},
                {"key": "Escape", "label": "Cancel", "action": "cancel", "style": "secondary"}
            ]
        }

    def _get_delete_skill_confirm_modal(self, agent_name: str, skill_name: str) -> Optional[Dict[str, Any]]:
        """Get modal definition for delete skill confirmation."""
        if not self.agent_manager:
            return None

        active_agent = self.agent_manager.get_active_agent()
        if not active_agent or active_agent.name != agent_name:
            return None

        # Find the skill
        skill = None
        for s in active_agent.list_skills():
            if s.name == skill_name:
                skill = s
                break

        if not skill:
            return None

        is_loaded = skill_name in active_agent.active_skills
        warning_msg = ""
        if is_loaded:
            warning_msg = "\n\n[!] This skill is currently loaded."

        return {
            "title": f"Delete Skill: {skill_name}?",
            "footer": "Enter confirm • Esc cancel",
            "width": 60,
            "height": 12,
            "sections": [
                {
                    "title": "Confirm Deletion",
                    "commands": [
                        {
                            "name": f"Delete '{skill_name}'",
                            "description": f"{skill.description or skill.file_path.name}{warning_msg}",
                            "skill_name": skill_name,
                            "action": "delete_skill_confirm"
                        },
                        {
                            "name": "Cancel",
                            "description": "Keep the skill",
                            "action": "cancel"
                        }
                    ]
                }
            ],
            "actions": [
                {"key": "Enter", "label": "Confirm", "action": "select"},
                {"key": "Escape", "label": "Cancel", "action": "cancel"}
            ]
        }

    def _create_skill_file(self, agent, name: str, content: str) -> bool:
        """Create a new skill file in the agent directory."""
        try:
            # Sanitize name - remove .md extension if present
            if name.endswith(".md"):
                name = name[:-3]

            skill_path = agent.directory / f"{name}.md"

            # Don't overwrite existing files
            if skill_path.exists():
                return False

            skill_path.write_text(content, encoding="utf-8")
            return True
        except Exception:
            return False

    def _rename_skill_file(self, agent, original_name: str, new_name: str) -> bool:
        """Rename a skill file."""
        try:
            # Sanitize names
            if original_name.endswith(".md"):
                original_name = original_name[:-3]
            if new_name.endswith(".md"):
                new_name = new_name[:-3]

            # Same name = no-op success
            if original_name == new_name:
                return True

            original_path = agent.directory / f"{original_name}.md"
            new_path = agent.directory / f"{new_name}.md"

            if not original_path.exists():
                return False

            # Check new name doesn't exist
            if new_path.exists():
                return False

            # Rename file
            original_path.rename(new_path)
            return True
        except Exception:
            return False

    def _delete_skill_file(self, agent, skill_name: str) -> bool:
        """Delete a skill file from the agent directory."""
        try:
            # Sanitize name
            if skill_name.endswith(".md"):
                skill_name = skill_name[:-3]

            # Don't delete system_prompt.md
            if skill_name == "system_prompt":
                return False

            skill_path = agent.directory / f"{skill_name}.md"

            if not skill_path.exists():
                return False

            skill_path.unlink()
            return True
        except Exception:
            return False

    async def handle_help(self, command: SlashCommand) -> CommandResult:
        """Handle /help command.

        Args:
            command: Parsed slash command.

        Returns:
            Command execution result.
        """
        try:
            if command.args:
                # Show help for specific command
                command_name = command.args[0]
                return await self._show_command_help(command_name)
            else:
                # Show all commands categorized by plugin
                return await self._show_all_commands()

        except Exception as e:
            self.logger.error(f"Error in help command: {e}")
            return CommandResult(
                success=False,
                message=f"Error displaying help: {str(e)}",
                display_type="error"
            )

    async def handle_config(self, command: SlashCommand) -> CommandResult:
        """Handle /config command.

        Args:
            command: Parsed slash command.

        Returns:
            Command execution result with status UI.
        """
        try:
            # Import the comprehensive config widget definitions
            from ..ui.config_widgets import ConfigWidgetDefinitions

            # Get the complete configuration modal definition
            modal_definition = ConfigWidgetDefinitions.get_config_modal_definition()

            return CommandResult(
                success=True,
                message="Configuration modal opened",
                ui_config=UIConfig(
                    type="modal",
                    title=modal_definition["title"],
                    width=modal_definition["width"],
                    modal_config=modal_definition
                ),
                display_type="modal"
            )

        except Exception as e:
            self.logger.error(f"Error in config command: {e}")
            return CommandResult(
                success=False,
                message=f"Error opening configuration: {str(e)}",
                display_type="error"
            )

    async def handle_status(self, command: SlashCommand) -> CommandResult:
        """Handle /status command.

        Args:
            command: Parsed slash command.

        Returns:
            Command execution result with status modal UI.
        """
        try:
            # Create status modal definition (similar to config modal)
            status_definition = self._get_status_modal_definition()

            return CommandResult(
                success=True,
                message="System status opened",
                ui_config=UIConfig(
                    type="modal",
                    title=status_definition["title"],
                    width=status_definition.get("width", 70),
                    modal_config=status_definition
                ),
                display_type="modal"
            )

        except Exception as e:
            self.logger.error(f"Error in status command: {e}")
            return CommandResult(
                success=False,
                message=f"Error showing status: {str(e)}",
                display_type="error"
            )

    def _get_status_modal_definition(self) -> Dict[str, Any]:
        """Get status modal definition with live system data.

        Returns:
            Modal definition dictionary for status display.
        """
        import platform
        import sys
        import os

        stats = self.command_registry.get_registry_stats()

        return {
            "title": "System Status",
            "footer": "Esc to close",
            "width": 70,
            "height": 18,
            "sections": [
                {
                    "title": "Commands",
                    "widgets": [
                        {"type": "label", "label": "Registered", "value": str(stats.get('total_commands', 0))},
                        {"type": "label", "label": "Enabled", "value": str(stats.get('enabled_commands', 0))},
                        {"type": "label", "label": "Categories", "value": str(stats.get('categories', 0))},
                    ]
                },
                {
                    "title": "Plugins",
                    "widgets": [
                        {"type": "label", "label": "Active", "value": str(stats.get('plugins', 0))},
                    ]
                },
                {
                    "title": "System",
                    "widgets": [
                        {"type": "label", "label": "Python", "value": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"},
                        {"type": "label", "label": "Platform", "value": platform.system()},
                        {"type": "label", "label": "Architecture", "value": platform.machine()},
                    ]
                },
                {
                    "title": "Services",
                    "widgets": [
                        {"type": "label", "label": "Event Bus", "value": "[ok] Active"},
                        {"type": "label", "label": "Input Handler", "value": "[ok] Running"},
                        {"type": "label", "label": "Terminal Renderer", "value": "[ok] Active"},
                    ]
                }
            ],
            "actions": [
                {"key": "Escape", "label": "Close", "action": "cancel", "style": "secondary"}
            ]
        }

    async def handle_version(self, command: SlashCommand) -> CommandResult:
        """Handle /version command.

        Args:
            command: Parsed slash command.

        Returns:
            Command execution result.
        """
        try:
            # Get version information
            version_info = self._get_version_info()

            message = f"""Kollabor CLI v{version_info['version']}
Built: {version_info['build_date']}
Python: {version_info['python_version']}
Platform: {version_info['platform']}"""

            return CommandResult(
                success=True,
                message=message,
                display_type="info",
                data=version_info
            )

        except Exception as e:
            self.logger.error(f"Error in version command: {e}")
            return CommandResult(
                success=False,
                message=f"Error getting version: {str(e)}",
                display_type="error"
            )

    async def handle_profile(self, command: SlashCommand) -> CommandResult:
        """Handle /profile command.

        Args:
            command: Parsed slash command.

        Returns:
            Command execution result.
        """
        try:
            if not self.profile_manager:
                return CommandResult(
                    success=False,
                    message="Profile manager not available",
                    display_type="error"
                )

            args = command.args or []

            if not args or args[0] in ("list", "ls"):
                # Show profile selection modal
                return await self._show_profiles_modal()
            elif args[0] == "create" and len(args) >= 4:
                # Create new profile: /profile create <name> <api_url> <model>
                name = args[1]
                api_url = args[2]
                model = args[3]
                temp = float(args[4]) if len(args) > 4 else 0.7
                return await self._create_profile(name, api_url, model, temp)
            else:
                # Switch to specified profile (direct command)
                profile_name = args[0]
                return await self._switch_profile(profile_name)

        except Exception as e:
            self.logger.error(f"Error in profile command: {e}")
            return CommandResult(
                success=False,
                message=f"Error managing profiles: {str(e)}",
                display_type="error"
            )

    def _get_profiles_modal_definition(self, skip_reload: bool = False) -> Dict[str, Any]:
        """Get modal definition for profile selection.

        Args:
            skip_reload: If True, don't reload from config (use current state).

        Returns:
            Modal definition dictionary.
        """
        # Reload profiles from config to pick up any changes
        # Skip reload when called immediately after delete (memory state is fresher)
        if not skip_reload:
            self.profile_manager.reload()

        profiles = self.profile_manager.list_profiles()
        active_name = self.profile_manager.active_profile_name

        # Build profile list for modal
        profile_items = []
        for profile in profiles:
            is_active = profile.name == active_name
            # Use getter methods to show resolved values (respects env vars)
            model = profile.get_model() or "unknown"
            api_url = profile.get_endpoint() or "unknown"
            profile_items.append({
                "name": f"{'[*] ' if is_active else '    '}{profile.name}",
                "description": f"{model} @ {api_url}",
                "profile_name": profile.name,
                "action": "select_profile"
            })

        # Add management options
        management_items = [
            {
                "name": "    [+] Save to Config",
                "description": "Save current profile settings (from env vars) to config.json",
                "action": "save_profile_to_config"
            },
            {
                "name": "    [+] Create New Profile",
                "description": "Create a new profile from scratch",
                "action": "create_profile_prompt"
            },
        ]

        # Env var help section (non-selectable info items)
        # Short label on left (name), env var on right (description)
        env_help_items = [
            {
                "name": "auto-create from env vars",
                "description": "python main.py --profile NAME --save",
                "action": "noop",
                "selectable": False
            },
            {
                "name": "API URL (required)",
                "description": "KOLLABOR_{NAME}_ENDPOINT",
                "action": "noop",
                "selectable": False
            },
            {
                "name": "API key",
                "description": "KOLLABOR_{NAME}_TOKEN",
                "action": "noop",
                "selectable": False
            },
            {
                "name": "model name",
                "description": "KOLLABOR_{NAME}_MODEL",
                "action": "noop",
                "selectable": False
            },
            {
                "name": "tool format",
                "description": "KOLLABOR_{NAME}_TOOL_FORMAT",
                "action": "noop",
                "selectable": False
            },
            {
                "name": "max tokens",
                "description": "KOLLABOR_{NAME}_MAX_TOKENS",
                "action": "noop",
                "selectable": False
            },
            {
                "name": "temperature",
                "description": "KOLLABOR_{NAME}_TEMPERATURE",
                "action": "noop",
                "selectable": False
            },
            {
                "name": "timeout (ms)",
                "description": "KOLLABOR_{NAME}_TIMEOUT",
                "action": "noop",
                "selectable": False
            },
        ]

        return {
            "title": "LLM Profiles",
            "footer": "↑↓ navigate • Enter select • e edit • d delete • Esc exit",
            "width": 75,
            "height": 28,
            "sections": [
                {
                    "title": f"Available Profiles (active: {active_name})",
                    "commands": profile_items
                },
                {
                    "title": "Management",
                    "commands": management_items
                },
                {
                    "title": "Create via Environment Variables",
                    "commands": env_help_items
                }
            ],
            "actions": [
                {"key": "Enter", "label": "Select", "action": "select"},
                {"key": "e", "label": "Edit", "action": "edit_profile_prompt"},
                {"key": "d", "label": "Delete", "action": "delete_profile_prompt"},
                {"key": "Escape", "label": "Close", "action": "cancel"}
            ]
        }

    async def _show_profiles_modal(self) -> CommandResult:
        """Show profile selection modal.

        Returns:
            Command result with modal UI.
        """
        modal_definition = self._get_profiles_modal_definition()

        return CommandResult(
            success=True,
            message="Select a profile",
            ui_config=UIConfig(
                type="modal",
                title=modal_definition["title"],
                width=modal_definition["width"],
                height=modal_definition["height"],
                modal_config=modal_definition
            ),
            display_type="modal"
        )

    async def _switch_profile(self, profile_name: str) -> CommandResult:
        """Switch to a different profile.

        Args:
            profile_name: Name of profile to switch to.

        Returns:
            Command result.
        """
        if self.profile_manager.set_active_profile(profile_name):
            profile = self.profile_manager.get_active_profile()
            # Update the API service with new profile settings
            if self.llm_service and hasattr(self.llm_service, 'api_service'):
                self.llm_service.api_service.update_from_profile(profile)
            return CommandResult(
                success=True,
                message=f"Switched to profile: {profile_name}\n  API: {profile.api_url}\n  Model: {profile.model}",
                display_type="success"
            )
        else:
            available = ", ".join(self.profile_manager.get_profile_names())
            return CommandResult(
                success=False,
                message=f"Profile not found: {profile_name}\nAvailable: {available}",
                display_type="error"
            )

    async def _create_profile(
        self, name: str, api_url: str, model: str, temperature: float = 0.7
    ) -> CommandResult:
        """Create a new profile.

        Args:
            name: Profile name.
            api_url: API endpoint URL.
            model: Model identifier.
            temperature: Sampling temperature.

        Returns:
            Command result.
        """
        profile = self.profile_manager.create_profile(
            name=name,
            api_url=api_url,
            model=model,
            temperature=temperature,
            description=f"Created via /profile create",
            save_to_config=True
        )
        if profile:
            return CommandResult(
                success=True,
                message=f"[ok] Created profile: {name}\n  API: {api_url}\n  Model: {model}\n  Saved to config.json",
                display_type="success"
            )
        else:
            return CommandResult(
                success=False,
                message=f"[err] Failed to create profile. '{name}' may already exist.",
                display_type="error"
            )

    async def handle_agent(self, command: SlashCommand) -> CommandResult:
        """Handle /agent command.

        Args:
            command: Parsed slash command.

        Returns:
            Command execution result.
        """
        try:
            if not self.agent_manager:
                return CommandResult(
                    success=False,
                    message="Agent manager not available",
                    display_type="error"
                )

            args = command.args or []

            if not args or args[0] in ("list", "ls"):
                # Show agent selection modal
                return await self._show_agents_modal()
            elif args[0] == "clear":
                # Clear active agent
                self.agent_manager.clear_active_agent()
                return CommandResult(
                    success=True,
                    message="Cleared active agent, using default behavior",
                    display_type="success"
                )
            else:
                # Switch to specified agent (direct command)
                agent_name = args[0]
                return await self._switch_agent(agent_name)

        except Exception as e:
            self.logger.error(f"Error in agent command: {e}")
            return CommandResult(
                success=False,
                message=f"Error managing agents: {str(e)}",
                display_type="error"
            )

    def _get_agents_modal_definition(self, skip_reload: bool = False) -> Optional[Dict[str, Any]]:
        """Get modal definition for agent selection with default indicators.

        Args:
            skip_reload: If True, don't reload from disk (use current state).

        Returns:
            Modal definition dictionary, or None if no agents found.
        """
        from ..utils.config_utils import get_all_default_agents
        
        # Get all default agents
        default_agents = get_all_default_agents()  # {"project": "coder", "global": "research"}
        project_default = default_agents.get("project")
        global_default = default_agents.get("global")
        
        # Refresh agents from directories to pick up any changes
        if not skip_reload:
            self.agent_manager.refresh()

        agents = self.agent_manager.list_agents()
        active_agent = self.agent_manager.get_active_agent()
        active_name = active_agent.name if active_agent else None

        if not agents:
            return None

        # Build agent list with indicators
        agent_items = []
        for agent in agents:
            is_active = agent.name == active_name
            is_project_default = agent.name == project_default
            is_global_default = agent.name == global_default

            # Build source indicator (L=local only, G=global only, *=both)
            if agent.source == "local" and agent.overrides_global:
                source_char = "*"
            elif agent.source == "local":
                source_char = "L"
            else:  # global
                source_char = "G"

            # Build default indicator
            default_parts = []
            if is_project_default:
                default_parts.append("D")
            if is_global_default:
                default_parts.append("g")
            default_str = "".join(default_parts) if default_parts else " "

            # Format: [active] source default - examples: [*G ] [ L] [ Gd]
            active_char = "*" if is_active else " "
            indicator = f"{active_char}{source_char}{default_str}"

            skills = agent.list_skills()
            skill_count = f" ({len(skills)} skills)" if skills else ""
            description = agent.description or "No description"

            agent_items.append({
                "name": f"[{indicator}] {agent.name}{skill_count}",
                "description": description,
                "agent_name": agent.name,
                "action": "select_agent",
                "is_active": is_active,
                "is_project_default": is_project_default,
                "is_global_default": is_global_default
            })

        # Add clear option
        agent_items.append({
            "name": "    [Clear Agent]",
            "description": "Use default system prompt behavior",
            "agent_name": None,
            "action": "clear_agent"
        })

        # Management options
        management_items = [
            {
                "name": "    [+] Create New Agent",
                "description": "Create a new agent with system prompt",
                "action": "create_agent_prompt"
            }
        ]

        return {
            "title": "Agents",
            "footer": "L=local G=global *=both | D=proj g=global | ↑↓ Enter",
            "width": 70,
            "height": 18,
            "sections": [
                {
                    "title": f"Available Agents (active: {active_name or 'none'})",
                    "commands": agent_items
                },
                {
                    "title": "Management",
                    "commands": management_items
                }
            ],
            "actions": [
                {"key": "Enter", "label": "Select", "action": "select"},
                {"key": "d", "label": "Project Default", "action": "toggle_project_default"},
                {"key": "g", "label": "Global Default", "action": "toggle_global_default"},
                {"key": "e", "label": "Edit", "action": "edit_agent_prompt"},
                {"key": "r", "label": "Delete", "action": "delete_agent_prompt"},
                {"key": "Escape", "label": "Close", "action": "cancel"}
            ]
        }

    async def _show_agents_modal(self) -> CommandResult:
        """Show agent selection modal.

        Returns:
            Command result with modal UI.
        """
        modal_definition = self._get_agents_modal_definition()

        if not modal_definition:
            return CommandResult(
                success=True,
                message="No agents found.\nCreate agents in .kollabor-cli/agents/<name>/system_prompt.md",
                display_type="info"
            )

        return CommandResult(
            success=True,
            message="Select an agent",
            ui_config=UIConfig(
                type="modal",
                title=modal_definition["title"],
                width=modal_definition["width"],
                height=modal_definition["height"],
                modal_config=modal_definition
            ),
            display_type="modal"
        )

    async def _switch_agent(self, agent_name: str) -> CommandResult:
        """Switch to a different agent.

        Args:
            agent_name: Name of agent to switch to.

        Returns:
            Command result.
        """
        if self.agent_manager.set_active_agent(agent_name):
            # Rebuild system prompt for the new agent
            if self.llm_service:
                self.llm_service.rebuild_system_prompt()

            agent = self.agent_manager.get_active_agent()
            skills = agent.list_skills()
            skill_info = f", {len(skills)} skills available" if skills else ""

            # If agent has a preferred profile, mention it
            profile_info = ""
            if agent.profile:
                profile_info = f"\n  Preferred profile: {agent.profile}"

            return CommandResult(
                success=True,
                message=f"Switched to agent: {agent_name}{skill_info}{profile_info}",
                display_type="success"
            )
        else:
            available = ", ".join(self.agent_manager.get_agent_names())
            return CommandResult(
                success=False,
                message=f"Agent not found: {agent_name}\nAvailable: {available}",
                display_type="error"
            )

    async def handle_skill(self, command: SlashCommand) -> CommandResult:
        """Handle /skill command.

        Args:
            command: Parsed slash command.

        Returns:
            Command execution result.
        """
        try:
            if not self.agent_manager:
                return CommandResult(
                    success=False,
                    message="Agent manager not available",
                    display_type="error"
                )

            active_agent = self.agent_manager.get_active_agent()
            if not active_agent:
                return CommandResult(
                    success=False,
                    message="No active agent. Use /agent <name> first.",
                    display_type="error"
                )

            args = command.args or []

            if not args:
                # Show skill selection modal
                return await self._show_skills_modal()
            elif args[0] in ("list", "ls"):
                # Show skill selection modal
                return await self._show_skills_modal()
            elif args[0] == "load" and len(args) > 1:
                # Load skill
                skill_name = args[1]
                return await self._load_skill(skill_name)
            elif args[0] == "unload" and len(args) > 1:
                # Unload skill
                skill_name = args[1]
                return await self._unload_skill(skill_name)
            else:
                # Try to load skill by name directly
                skill_name = args[0]
                return await self._load_skill(skill_name)

        except Exception as e:
            self.logger.error(f"Error in skill command: {e}")
            return CommandResult(
                success=False,
                message=f"Error managing skills: {str(e)}",
                display_type="error"
            )

    def _get_skills_modal_definition(self, skip_reload: bool = False) -> Optional[Dict[str, Any]]:
        """Get modal definition for skill selection.

        Args:
            skip_reload: If True, don't reload from disk (use current state).

        Returns:
            Modal definition dictionary, or None if no skills available.
        """
        active_agent = self.agent_manager.get_active_agent()
        if not active_agent:
            return None

        # Refresh agent from disk to pick up any changes (unless skipped)
        if not skip_reload:
            self.agent_manager.refresh()
            # Re-get active agent in case it was refreshed
            active_agent = self.agent_manager.get_active_agent()
            if not active_agent:
                return None

        skills = active_agent.list_skills()
        active_skills = active_agent.active_skills

        # Check project and global defaults
        from pathlib import Path
        import json

        local_config = (self.agent_manager.local_agents_dir / active_agent.name / "agent.json"
                        if self.agent_manager.local_agents_dir else None)
        global_config = self.agent_manager.global_agents_dir / active_agent.name / "agent.json"

        project_defaults = set()
        global_defaults = set()

        if local_config and local_config.exists():
            try:
                config_data = json.loads(local_config.read_text(encoding="utf-8"))
                project_defaults = set(config_data.get("default_skills", []))
            except Exception:
                pass

        if global_config.exists():
            try:
                config_data = json.loads(global_config.read_text(encoding="utf-8"))
                global_defaults = set(config_data.get("default_skills", []))
            except Exception:
                pass

        if not skills:
            return None

        # Build skill list for modal
        skill_items = []
        for skill in skills:
            is_loaded = skill.name in active_skills
            is_proj_default = skill.name in project_defaults
            is_global_default = skill.name in global_defaults

            # Show markers: [*] loaded, [d] proj default, [g] global default
            # Examples: [*dg] [*d ] [ g] [  ]
            loaded_char = "*" if is_loaded else " "
            proj_char = "d" if is_proj_default else " "
            global_char = "g" if is_global_default else " "
            marker = f"[{loaded_char}{proj_char}{global_char}]"

            action = "unload_skill" if is_loaded else "load_skill"
            description = skill.description or f"Skill file: {skill.file_path.name}"

            skill_items.append({
                "name": f"{marker} {skill.name}",
                "description": description,
                "skill_name": skill.name,
                "action": action,
                "loaded": is_loaded,
                "is_default": is_proj_default or is_global_default
            })

        loaded_count = len(active_skills)
        total_count = len(skills)
        default_count = len(project_defaults | global_defaults)

        # Management options
        management_items = [
            {
                "name": "    [+] Create New Skill",
                "description": "Create a new skill file for this agent",
                "action": "create_skill_prompt"
            }
        ]

        return {
            "title": f"Skills - {active_agent.name}",
            "footer": "*=loaded d=proj g=global | ↑↓ Enter | d/g dflt | e r",
            "width": 70,
            "height": 18,
            "sections": [
                {
                    "title": f"Available Skills ({loaded_count}/{total_count} loaded, {default_count} default)",
                    "commands": skill_items
                },
                {
                    "title": "Management",
                    "commands": management_items
                }
            ],
            "actions": [
                {"key": "Enter", "label": "Toggle", "action": "toggle"},
                {"key": "d", "label": "Project Default", "action": "toggle_default_skill"},
                {"key": "g", "label": "Global Default", "action": "toggle_global_default_skill"},
                {"key": "e", "label": "Edit", "action": "edit_skill_prompt"},
                {"key": "r", "label": "Delete", "action": "delete_skill_prompt"},
                {"key": "Escape", "label": "Close", "action": "cancel"}
            ]
        }

    async def _show_skills_modal(self) -> CommandResult:
        """Show skill selection modal for active agent.

        Returns:
            Command result with modal UI.
        """
        active_agent = self.agent_manager.get_active_agent()
        if not active_agent:
            return CommandResult(
                success=False,
                message="No active agent",
                display_type="error"
            )

        modal_definition = self._get_skills_modal_definition()
        if not modal_definition:
            return CommandResult(
                success=True,
                message=f"Agent '{active_agent.name}' has no skills defined.\nAdd .md files to the agent directory to create skills.",
                display_type="info"
            )

        return CommandResult(
            success=True,
            message="Select a skill to load/unload",
            ui_config=UIConfig(
                type="modal",
                title=modal_definition["title"],
                width=modal_definition["width"],
                height=modal_definition["height"],
                modal_config=modal_definition
            ),
            display_type="modal"
        )

    async def _load_skill(self, skill_name: str) -> CommandResult:
        """Load a skill into active agent.

        Args:
            skill_name: Name of skill to load.

        Returns:
            Command result.
        """
        agent = self.agent_manager.get_active_agent()
        skill = agent.get_skill(skill_name) if agent else None
        if skill and self.agent_manager.load_skill(skill_name):
            # Inject skill content as user message
            if self.llm_service:
                skill_message = f"## Skill: {skill_name}\n\n{skill.content}"
                self.llm_service._add_conversation_message("user", skill_message)
            return CommandResult(
                success=True,
                message=f"Loaded skill: {skill_name}",
                display_type="success"
            )
        else:
            active_agent = self.agent_manager.get_active_agent()
            available = ", ".join(s.name for s in active_agent.list_skills()) if active_agent else ""
            return CommandResult(
                success=False,
                message=f"Skill not found: {skill_name}\nAvailable: {available}",
                display_type="error"
            )

    async def _unload_skill(self, skill_name: str) -> CommandResult:
        """Unload a skill from active agent.

        Args:
            skill_name: Name of skill to unload.

        Returns:
            Command result.
        """
        if self.agent_manager.unload_skill(skill_name):
            # Add message indicating skill was unloaded
            if self.llm_service:
                self.llm_service._add_conversation_message(
                    "user",
                    f"[Skill '{skill_name}' has been unloaded - please disregard its instructions]"
                )
            return CommandResult(
                success=True,
                message=f"Unloaded skill: {skill_name}",
                display_type="success"
            )
        else:
            return CommandResult(
                success=False,
                message=f"Skill not loaded: {skill_name}",
                display_type="error"
            )

    async def _show_command_help(self, command_name: str) -> CommandResult:
        """Show help for a specific command.

        Args:
            command_name: Name of command to show help for.

        Returns:
            Command result with help information.
        """
        command_def = self.command_registry.get_command(command_name)
        if not command_def:
            return CommandResult(
                success=False,
                message=f"Unknown command: /{command_name}",
                display_type="error"
            )

        # Format detailed help for the command
        help_text = f"""Command: /{command_def.name}
Description: {command_def.description}
Plugin: {command_def.plugin_name}
Category: {command_def.category.value}
Mode: {command_def.mode.value}"""

        if command_def.aliases:
            help_text += f"\nAliases: {', '.join(command_def.aliases)}"

        if command_def.parameters:
            help_text += "\nParameters:"
            for param in command_def.parameters:
                required = " (required)" if param.required else ""
                help_text += f"\n  {param.name}: {param.description}{required}"

        return CommandResult(
            success=True,
            message=help_text,
            display_type="info"
        )

    async def _show_all_commands(self) -> CommandResult:
        """Show all available commands grouped by plugin in a status modal.

        Returns:
            Command result with status modal UI config.
        """
        # Get commands grouped by plugin
        plugin_categories = self.command_registry.get_plugin_categories()

        # Build command list for modal display
        command_sections = []

        for plugin_name in sorted(plugin_categories.keys()):
            commands = self.command_registry.get_commands_by_plugin(plugin_name)
            if not commands:
                continue

            # Create section for this plugin
            section_commands = []
            for cmd in sorted(commands, key=lambda c: c.name):
                aliases = f" ({', '.join(cmd.aliases)})" if cmd.aliases else ""
                section_commands.append({
                    "name": f"/{cmd.name}{aliases}",
                    "description": cmd.description
                })

            command_sections.append({
                "title": f"{plugin_name.title()} Commands",
                "commands": section_commands
            })

        return CommandResult(
            success=True,
            message="Help opened in status modal",
            ui_config=UIConfig(
                type="status_modal",
                title="Available Commands",
                height=15,
                width=80,
                modal_config={
                    "sections": command_sections,
                    "footer": "Esc/Enter close • /help <command> for details",
                    "scrollable": True
                }
            ),
            display_type="status_modal"
        )

    def _get_version_info(self) -> Dict[str, str]:
        """Get application version information.

        Returns:
            Dictionary with version details.
        """
        import sys
        import platform

        return {
            "version": "1.0.0-dev",
            "build_date": datetime.now().strftime("%Y-%m-%d"),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": platform.system(),
            "architecture": platform.machine()
        }


class SystemConfigUI:
    """UI component for system configuration."""

    def __init__(self, config_manager, event_bus) -> None:
        """Initialize config UI.

        Args:
            config_manager: Configuration manager.
            event_bus: Event bus for configuration events.
        """
        self.config_manager = config_manager
        self.event_bus = event_bus

    def render(self) -> List[str]:
        """Render configuration interface.

        Returns:
            List of lines for display.
        """
        # This would be implemented to show actual config options
        return [
            "╭─ System Configuration ─────────────────────────────────────╮",
            "│                                                             │",
            "│ ❯ Terminal Settings                                         │",
            "│   Input Configuration                                       │",
            "│   Display Options                                           │",
            "│   Performance Settings                                      │",
            "│                                                             │",
            "│ Plugin Settings                                             │",
            "│   Event Bus Configuration                                   │",
            "│   Logging Options                                           │",
            "│                                                             │",
            "╰─────────────────────────────────────────────────────────────╯",
            "   ↑↓←→ navigate • Enter edit • Esc exit"
        ]


class SystemStatusUI:
    """UI component for system status display."""

    def __init__(self, event_bus, command_registry) -> None:
        """Initialize status UI.

        Args:
            event_bus: Event bus for status information.
            command_registry: Command registry for statistics.
        """
        self.event_bus = event_bus
        self.command_registry = command_registry

    def render(self) -> List[str]:
        """Render status interface.

        Returns:
            List of lines for display.
        """
        stats = self.command_registry.get_registry_stats()

        return [
            "╭─ System Status ─────────────────────────────────────────────╮",
            "│                                                             │",
            f"│ Commands: {stats['total_commands']} registered, {stats['enabled_commands']} enabled              │",
            f"│ Plugins: {stats['plugins']} active                                    │",
            f"│ Categories: {stats['categories']} in use                               │",
            "│                                                             │",
            "│ Event Bus: [ok] Active                                        │",
            "│ Input Handler: [ok] Running                                   │",
            "│ Terminal Renderer: [ok] Active                                │",
            "│                                                             │",
            "│ Memory Usage: ~ 45MB                                        │",
            "│ Uptime: 00:15:32                                            │",
            "│                                                             │",
            "╰─────────────────────────────────────────────────────────────╯",
            "   ↑↓ navigate • Esc exit"
        ]
