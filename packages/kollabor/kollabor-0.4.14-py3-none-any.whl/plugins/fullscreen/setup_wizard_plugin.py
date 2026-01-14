"""Setup wizard plugin for first-time user onboarding."""

import asyncio
import os
import re
from core.fullscreen import FullScreenPlugin
from core.fullscreen.plugin import PluginMetadata
from core.fullscreen.components.drawing import DrawingPrimitives
from core.fullscreen.components.animation import AnimationFramework
from core.io.visual_effects import ColorPalette, GradientRenderer
from core.io.key_parser import KeyPress


class SetupWizardPlugin(FullScreenPlugin):
    """Interactive setup wizard for new users.

    Single-screen wizard that shows:
    - LLM connection configuration
    - Keyboard shortcuts reference
    - Slash commands reference
    """

    # Kollabor ASCII banner (same as main app)
    KOLLABOR_LOGO = [
        "╭──────────────────────────────────────────────────╮",
        "│ ▄█─●─●─█▄  █ ▄▀ █▀▀█ █   █   █▀▀█ █▀▀▄ █▀▀█ █▀▀█ │",
        "│ ●──███──●  █▀▄  █  █ █   █   █▄▄█ █▀▀▄ █  █ █▄▄▀ │",
        "│ ▀█─●─●─█▀  █  █ █▄▄█ █▄▄ █▄▄ █  █ █▄▄▀ █▄▄█ █ █▄ │",
        "╰──────────────────────────────────────────────────╯",
    ]

    def __init__(self):
        """Initialize the setup wizard plugin."""
        metadata = PluginMetadata(
            name="setup",
            description="Interactive setup wizard for first-time configuration",
            version="1.0.0",
            author="Kollabor",
            category="config",
            icon="*",
            aliases=["wizard", "onboarding"]
        )
        super().__init__(metadata)

        # Lower FPS for static form (reduces CPU and eliminates unnecessary redraws)
        self.target_fps = 3.0

        # Form state - all fields on one screen
        self.fields = ["profile_name", "api_url", "model", "token", "temperature", "tool_format"]
        self.current_field_index = 0
        self.field_values = {
            "profile_name": "local",
            "api_url": "http://localhost:1234",
            "model": "qwen3-4b",
            "token": "",  # Can be entered here or via env var
            "temperature": "0.7",
            "tool_format": "openai",
        }
        self.cursor_positions = {field: len(self.field_values.get(field, "")) for field in self.fields}

        # Tool format options
        self.tool_formats = ["openai", "anthropic"]
        self.tool_format_index = 0

        # Page state: 0 = form, 1 = tips (shown when height too small)
        self.current_page = 0

        # Animation
        self.animation_framework = AnimationFramework()
        self.frame_count = 0

        # Wizard completion flag
        self.completed = False
        self.skipped = False

        # Config and profile manager references (set during initialize)
        self._config = None
        self._profile_manager = None

        # State tracking to skip unnecessary redraws
        self._last_render_state = None

    async def initialize(self, renderer) -> bool:
        """Initialize the setup wizard."""
        if not await super().initialize(renderer):
            return False

        # Reset render state to force initial render
        self._last_render_state = None

        # Setup animations
        current_time = asyncio.get_event_loop().time()
        self.demo_animations = {
            'title_fade': self.animation_framework.fade_in(1.5, current_time),
            'bounce': self.animation_framework.bounce_in(1.0, current_time + 0.3)
        }

        return True

    def set_managers(self, config, profile_manager):
        """Set config and profile managers for saving configuration.

        Args:
            config: ConfigService instance for setup completion flag
            profile_manager: ProfileManager instance for creating profiles
        """
        self._config = config
        self._profile_manager = profile_manager

        # Load values from active profile if available
        if profile_manager:
            try:
                profile = profile_manager.get_active_profile()
                if profile:
                    self.field_values["profile_name"] = profile.name or "local"
                    self.field_values["api_url"] = profile.api_url or "http://localhost:1234"
                    self.field_values["model"] = profile.model or "qwen3-4b"
                    self.field_values["token"] = profile.api_token or ""  # From config
                    self.field_values["temperature"] = str(profile.temperature) if profile.temperature else "0.7"
                    self.field_values["tool_format"] = profile.tool_format or "openai"

                    # Update cursor positions to end of values
                    for field in self.fields:
                        self.cursor_positions[field] = len(self.field_values.get(field, ""))

                    # Update tool format index
                    if profile.tool_format in self.tool_formats:
                        self.tool_format_index = self.tool_formats.index(profile.tool_format)
            except Exception:
                pass  # Use defaults if profile loading fails

    async def render_frame(self, delta_time: float) -> bool:
        """Render the wizard screen."""
        if not self.renderer:
            return False

        width, height = self.renderer.get_terminal_size()

        # Build state hash to detect changes
        current_state = (
            self.current_field_index,
            tuple(sorted(self.field_values.items())),
            tuple(sorted(self.cursor_positions.items())),
            self.current_page,
            self.tool_format_index,
            width,
            height
        )

        # Skip render if nothing changed (static form optimization)
        if current_state == self._last_render_state:
            return True

        self._last_render_state = current_state
        self.frame_count += 1

        # Now do the actual render (buffered by session's begin_frame/end_frame)
        self.renderer.clear_screen()

        # Minimum height check
        if height < 18:
            DrawingPrimitives.draw_text_centered(
                self.renderer, height // 2,
                f"Terminal too small (need 18 rows, have {height})",
                ColorPalette.YELLOW
            )
            return True

        # Track if we need a tips page
        self._tips_on_separate_page = height < 30

        if self.current_page == 0:
            self._render_main_screen(width, height)
        else:
            self._render_tips_screen(width, height)

        return True

    def _render_main_screen(self, width: int, height: int):
        """Render the single-screen setup wizard."""
        y = 1

        # Calculate available space for optional sections
        # Required: logo(5) + header(2) + fields(6) + status(2) + footer(1) = 16 lines minimum
        # Optional: separator(2) + shortcuts(6) + commands(7) = 15 lines
        show_shortcuts = height >= 30
        show_commands = height >= 37

        # --- Logo ---
        for i, line in enumerate(self.KOLLABOR_LOGO):
            gradient_line = GradientRenderer.apply_dim_scheme_gradient(line)
            x = 4
            self.renderer.write_at(x, y + i, gradient_line)
        y += len(self.KOLLABOR_LOGO) + 1

        # --- Welcome header ---
        self.renderer.write_at(4, y, ">> Welcome to Kollabor!", ColorPalette.WHITE)
        y += 1
        self.renderer.write_at(4, y, "// SETUP LLM CONNECTION", ColorPalette.DIM_GREY)
        y += 1

        # Generate env var prefix based on profile name
        profile_name = self.field_values.get("profile_name", "local")
        normalized_name = re.sub(r'[^a-zA-Z0-9]', '_', profile_name.strip()).upper()
        env_prefix = f"KOLLABOR_{normalized_name}"
        env_token = f"{env_prefix}_TOKEN"

        # Get token from env
        token_value = os.environ.get(env_token, "")

        # --- Form fields (inline style) ---
        label_x = 4
        value_x = 14

        # Profile
        self._render_inline_field(y, "profile_name", "profile:", label_x, value_x, width)
        y += 1

        # Endpoint
        self._render_inline_field(y, "api_url", "endpoint:", label_x, value_x, width)
        y += 1

        # Model
        self._render_inline_field(y, "model", "model:", label_x, value_x, width)
        y += 1

        # Token (editable, masked display)
        self._render_token_field(y, "token", "token:", label_x, value_x, width, env_token, token_value)
        y += 1

        # Temperature
        self._render_inline_field(y, "temperature", "temp:", label_x, value_x, width)
        y += 1

        # Format (checkbox style)
        self._render_format_field(y, label_x, value_x)
        y += 2

        # --- Status line ---
        form_token = self.field_values.get("token", "")
        has_token = bool(form_token or token_value)

        issues = []
        if not self.field_values.get("api_url"):
            issues.append("endpoint")
        if not self.field_values.get("model"):
            issues.append("model")
        if not has_token:
            issues.append("token")

        if issues:
            self.renderer.write_at(4, y, f"STATUS: [!] Missing: {', '.join(issues)}", ColorPalette.YELLOW)
        else:
            self.renderer.write_at(4, y, "STATUS: [ok] Ready to connect", ColorPalette.BRIGHT_GREEN)
        y += 1

        # --- Optional sections based on height ---
        if show_shortcuts or show_commands:
            # Separator
            separator = "─" * (width - 8)
            self.renderer.write_at(4, y, separator, ColorPalette.DIM_GREY)
            y += 2

        if show_shortcuts:
            # --- Keyboard Shortcuts ---
            self.renderer.write_at(4, y, "// Keyboard Shortcuts", ColorPalette.DIM_GREY)
            y += 1

            shortcuts = [
                ("Esc", "Cancel / close modals"),
                ("Enter", "Submit / confirm"),
                ("Up / Down", "Navigate prompt history"),
                ("Ctrl+C", "Exit application"),
            ]
            for key, desc in shortcuts:
                self.renderer.write_at(4, y, key.ljust(12), ColorPalette.WHITE)
                self.renderer.write_at(16, y, desc, ColorPalette.DIM_GREY)
                y += 1
            y += 1

        if show_commands:
            # --- Slash Commands ---
            self.renderer.write_at(4, y, "// Slash commands", ColorPalette.DIM_GREY)
            y += 1

            commands = [
                ("/help", "Show all available commands"),
                ("/profile", "Manage LLM API profiles"),
                ("/terminal", "Tmux session management"),
                ("/save", "Save conversation to file"),
                ("/resume", "Resume conversations"),
            ]
            for cmd, desc in commands:
                self.renderer.write_at(4, y, cmd.ljust(12), ColorPalette.BRIGHT_GREEN)
                self.renderer.write_at(16, y, f"- {desc}", ColorPalette.DIM_GREY)
                y += 1

        # --- Footer navigation ---
        footer_y = height - 1
        if self._tips_on_separate_page:
            self.renderer.write_at(4, footer_y, "Tab: next field  |  Enter: continue  |  Esc: cancel", ColorPalette.DIM_GREY)
        else:
            self.renderer.write_at(4, footer_y, "Tab: next field  |  Enter: save & start  |  Esc: cancel", ColorPalette.DIM_GREY)

    def _render_tips_screen(self, width: int, height: int):
        """Render the tips/shortcuts screen."""
        y = 2

        # Header
        self.renderer.write_at(4, y, "// Keyboard Shortcuts", ColorPalette.CYAN)
        y += 2

        shortcuts = [
            ("Esc", "Cancel / close modals"),
            ("Enter", "Submit / confirm"),
            ("Up / Down", "Navigate prompt history"),
            ("Ctrl+C", "Exit application"),
        ]
        for key, desc in shortcuts:
            self.renderer.write_at(4, y, key.ljust(14), ColorPalette.WHITE)
            self.renderer.write_at(18, y, desc, ColorPalette.DIM_GREY)
            y += 1
        y += 2

        # --- Slash Commands ---
        self.renderer.write_at(4, y, "// Slash commands", ColorPalette.CYAN)
        y += 2

        commands = [
            ("/help", "Show all available commands"),
            ("/profile", "Manage LLM API profiles"),
            ("/terminal", "Tmux session management"),
            ("/save", "Save conversation to file"),
            ("/resume", "Resume conversations"),
        ]
        for cmd, desc in commands:
            self.renderer.write_at(4, y, cmd.ljust(14), ColorPalette.BRIGHT_GREEN)
            self.renderer.write_at(18, y, f"- {desc}", ColorPalette.DIM_GREY)
            y += 1

        # Footer
        footer_y = height - 1
        self.renderer.write_at(4, footer_y, "Press any key to save & start", ColorPalette.DIM_GREY)

    def _render_inline_field(self, y: int, field: str, label: str, label_x: int, value_x: int, width: int):
        """Render an inline form field (label: value on same line)."""
        field_index = self.fields.index(field) if field in self.fields else -1
        is_active = field_index == self.current_field_index

        # Label
        label_color = ColorPalette.BRIGHT_GREEN if is_active else ColorPalette.DIM_GREY
        self.renderer.write_at(label_x, y, label, label_color)

        # Value with cursor if active
        value = self.field_values.get(field, "")
        cursor_pos = self.cursor_positions.get(field, len(value))
        max_width = width - value_x - 4

        if is_active:
            before = value[:cursor_pos]
            after = value[cursor_pos:]
            display = before + "_" + after
            value_color = ColorPalette.BRIGHT_YELLOW
        else:
            display = value
            value_color = ColorPalette.WHITE

        # Truncate if needed
        if len(display) > max_width:
            display = display[:max_width - 3] + "..."

        self.renderer.write_at(value_x, y, display, value_color)

    def _render_token_field(self, y: int, field: str, label: str, label_x: int, value_x: int, width: int, env_var: str, env_value: str):
        """Render the token field with masking."""
        field_index = self.fields.index(field) if field in self.fields else -1
        is_active = field_index == self.current_field_index

        # Label
        label_color = ColorPalette.BRIGHT_GREEN if is_active else ColorPalette.DIM_GREY
        self.renderer.write_at(label_x, y, label, label_color)

        # Get token value (form value takes precedence, then env var)
        form_value = self.field_values.get(field, "")

        if is_active:
            # When editing, show masked with cursor
            cursor_pos = self.cursor_positions.get(field, len(form_value))
            if form_value:
                # Show asterisks with cursor position
                masked = "*" * cursor_pos + "_" + "*" * (len(form_value) - cursor_pos)
            else:
                masked = "_"
            self.renderer.write_at(value_x, y, masked, ColorPalette.BRIGHT_YELLOW)
        else:
            # When not editing, show status
            if form_value:
                # Has form value - show masked
                masked = form_value[:3] + "*" * (len(form_value) - 5) + form_value[-2:] if len(form_value) > 8 else "****"
                self.renderer.write_at(value_x, y, masked, ColorPalette.WHITE)
            elif env_value:
                # Has env value - show env var name
                self.renderer.write_at(value_x, y, f"({env_var})", ColorPalette.BRIGHT_GREEN)
            else:
                # Neither - show env var hint
                self.renderer.write_at(value_x, y, env_var, ColorPalette.YELLOW)

    def _render_format_field(self, y: int, label_x: int, value_x: int):
        """Render the format field as checkboxes."""
        field_index = self.fields.index("tool_format")
        is_active = field_index == self.current_field_index

        # Label
        label_color = ColorPalette.BRIGHT_GREEN if is_active else ColorPalette.DIM_GREY
        self.renderer.write_at(label_x, y, "format:", label_color)

        # Checkbox options
        current_format = self.field_values["tool_format"]
        x = value_x

        for fmt in self.tool_formats:
            if fmt == current_format:
                checkbox = f"[x] {fmt}"
                color = ColorPalette.BRIGHT_YELLOW if is_active else ColorPalette.WHITE
            else:
                checkbox = f"[ ] {fmt}"
                color = ColorPalette.DIM_GREY

            self.renderer.write_at(x, y, checkbox, color)
            x += len(checkbox) + 2

    async def handle_input(self, key_press: KeyPress) -> bool:
        """Handle user input."""
        # Tips page - any key saves and exits
        if self.current_page == 1:
            await self._save_configuration()
            self.completed = True
            return True

        # Escape to skip wizard
        if key_press.name == "Escape":
            self.skipped = True
            return True

        # Enter - if tips on separate page, show tips first; otherwise save and exit
        if key_press.name == "Enter" or key_press.char == '\n' or key_press.char == '\r':
            if getattr(self, '_tips_on_separate_page', False):
                self.current_page = 1
                return False
            else:
                await self._save_configuration()
                self.completed = True
                return True

        # Tab navigation between fields
        if key_press.name == "Tab" or key_press.char == '\t':
            self.current_field_index = (self.current_field_index + 1) % len(self.fields)
            return False

        # Shift+Tab
        if key_press.name == "Shift+Tab":
            self.current_field_index = (self.current_field_index - 1) % len(self.fields)
            return False

        # Arrow up/down for field navigation
        if key_press.name == "ArrowUp":
            self.current_field_index = (self.current_field_index - 1) % len(self.fields)
            return False
        if key_press.name == "ArrowDown":
            self.current_field_index = (self.current_field_index + 1) % len(self.fields)
            return False

        # Get current field
        current_field = self.fields[self.current_field_index]

        # Tool format - use arrow left/right or space to toggle
        if current_field == "tool_format":
            if key_press.name in ("ArrowRight", "ArrowLeft") or key_press.char == ' ':
                self.tool_format_index = (self.tool_format_index + 1) % len(self.tool_formats)
                self.field_values["tool_format"] = self.tool_formats[self.tool_format_index]
            return False

        # Text input handling for other fields
        return self._handle_text_input(key_press, current_field)

    def _handle_text_input(self, key_press: KeyPress, field: str) -> bool:
        """Handle text input for a field."""
        value = self.field_values.get(field, "")
        cursor_pos = self.cursor_positions.get(field, len(value))

        # Backspace
        if key_press.name == "Backspace" or key_press.char == '\x7f' or key_press.char == '\x08':
            if cursor_pos > 0:
                value = value[:cursor_pos - 1] + value[cursor_pos:]
                cursor_pos -= 1
                self.field_values[field] = value
                self.cursor_positions[field] = cursor_pos
            return False

        # Delete
        if key_press.name == "Delete":
            if cursor_pos < len(value):
                value = value[:cursor_pos] + value[cursor_pos + 1:]
                self.field_values[field] = value
            return False

        # Cursor movement
        if key_press.name == "ArrowLeft":
            if cursor_pos > 0:
                self.cursor_positions[field] = cursor_pos - 1
            return False

        if key_press.name == "ArrowRight":
            if cursor_pos < len(value):
                self.cursor_positions[field] = cursor_pos + 1
            return False

        # Home/End
        if key_press.name == "Home":
            self.cursor_positions[field] = 0
            return False

        if key_press.name == "End":
            self.cursor_positions[field] = len(value)
            return False

        # Printable character
        if key_press.char and key_press.char.isprintable() and len(key_press.char) == 1:
            value = value[:cursor_pos] + key_press.char + value[cursor_pos:]
            cursor_pos += 1
            self.field_values[field] = value
            self.cursor_positions[field] = cursor_pos
            return False

        return False

    async def _save_configuration(self):
        """Save the configuration to profile manager."""
        if self._profile_manager:
            try:
                # Parse temperature
                temp = float(self.field_values.get("temperature", "0.7"))
            except ValueError:
                temp = 0.7

            try:
                # Get token and profile name
                token = self.field_values.get("token", "")
                profile_name = self.field_values["profile_name"]

                # Check if profile exists
                existing = self._profile_manager.get_profile(profile_name)
                if existing:
                    # Update existing profile
                    self._profile_manager.update_profile(
                        original_name=profile_name,
                        api_url=self.field_values["api_url"],
                        model=self.field_values["model"],
                        temperature=temp,
                        tool_format=self.field_values["tool_format"],
                        api_token=token if token else None,
                        description="Updated via setup wizard",
                        save_to_config=True
                    )
                else:
                    # Create new profile
                    self._profile_manager.create_profile(
                        name=profile_name,
                        api_url=self.field_values["api_url"],
                        model=self.field_values["model"],
                        temperature=temp,
                        tool_format=self.field_values["tool_format"],
                        api_token=token if token else None,
                        description="Created via setup wizard",
                        save_to_config=True
                    )

                # Set as active profile
                self._profile_manager.set_active_profile(profile_name)
            except Exception as e:
                # Log error but don't fail
                import logging
                logging.getLogger(__name__).error(f"Failed to save profile: {e}")

        # Mark setup as completed
        if self._config:
            self._config.set("application.setup_completed", True)

    async def cleanup(self):
        """Clean up wizard resources."""
        self.animation_framework.clear_all()
        await super().cleanup()
