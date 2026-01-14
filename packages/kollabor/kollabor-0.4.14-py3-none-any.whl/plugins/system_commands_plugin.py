"""System commands plugin - provides status view for core system commands."""

import logging
from typing import Dict, Any, List

from core.io.visual_effects import AgnosterSegment

logger = logging.getLogger(__name__)


class SystemCommandsPlugin:
    """Plugin that provides status view for system commands.

    Note: System commands (/help, /config, /status, etc.) are registered
    by core application in _initialize_slash_commands(). This plugin
    only provides the status view display.
    """

    def __init__(self, name: str = "system_commands",
                 event_bus=None, renderer=None, config=None) -> None:
        """Initialize the system commands plugin.

        Args:
            name: Plugin name.
            event_bus: Event bus (unused).
            renderer: Terminal renderer.
            config: Configuration manager (unused).
        """
        self.name = name
        self.version = "1.0.0"
        self.description = "Status view for core system commands"
        self.enabled = True
        self.renderer = renderer
        self.logger = logger

    async def initialize(self, event_bus, config, **kwargs) -> None:
        """Initialize the plugin."""
        try:
            self.renderer = kwargs.get('renderer')
            await self._register_status_view()
            self.logger.info("System commands plugin initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing system commands plugin: {e}")
            raise

    async def _register_status_view(self) -> None:
        """Register system commands status view."""
        try:
            if (self.renderer and
                hasattr(self.renderer, 'status_renderer') and
                self.renderer.status_renderer and
                hasattr(self.renderer.status_renderer, 'status_registry') and
                self.renderer.status_renderer.status_registry):

                from core.io.status_renderer import StatusViewConfig, BlockConfig

                view = StatusViewConfig(
                    name="System Commands",
                    plugin_source="system_commands",
                    priority=400,
                    blocks=[BlockConfig(
                        width_fraction=1.0,
                        content_provider=self._get_status_content,
                        title="System Commands",
                        priority=100
                    )],
                )

                registry = self.renderer.status_renderer.status_registry
                registry.register_status_view("system_commands", view)
                self.logger.info("Registered 'System Commands' status view")

        except Exception as e:
            self.logger.error(f"Failed to register status view: {e}")

    def _get_status_content(self) -> List[str]:
        """Get system commands status (agnoster style)."""
        try:
            seg = AgnosterSegment()
            seg.add_lime("Commands", "dark")
            seg.add_cyan("Active", "dark")
            seg.add_neutral("/help /config /status", "mid")
            return [seg.render()]
        except Exception as e:
            self.logger.error(f"Error getting status content: {e}")
            seg = AgnosterSegment()
            seg.add_neutral("Commands: Error", "dark")
            return [seg.render()]

    async def shutdown(self) -> None:
        """Shutdown the plugin."""
        self.logger.info("System commands plugin shutdown completed")

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "plugins": {
                "system_commands": {
                    "enabled": True
                }
            }
        }

    async def register_hooks(self) -> None:
        """Register event hooks (none needed)."""
        pass
