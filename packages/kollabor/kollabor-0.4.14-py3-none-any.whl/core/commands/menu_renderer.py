"""Command menu renderer for interactive slash command display."""

import logging
from typing import List, Dict, Any, Optional, Tuple
from ..events.models import CommandCategory
from ..io.visual_effects import (
    AgnosterSegment, AgnosterColors, ColorPalette,
    make_bg_color, make_fg_color, Powerline,
    get_color_support, ColorSupport
)

logger = logging.getLogger(__name__)

# Basic ANSI codes
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = ColorPalette.RESET

# Powerline characters
PL_RIGHT = ""  # \ue0b0

# Menu symbols
ARROW_RIGHT = "▶"
ARROW_DOWN = "▼"
ARROW_UP = "▲"
DOT = "·"
GLOW = "◆"

# Category display order and icons (Unicode symbols)
CATEGORY_CONFIG = {
    "system": {"name": "SYS", "icon": "⚙", "full": "System"},
    "conversation": {"name": "CHAT", "icon": "⌘", "full": "Conversation"},
    "agent": {"name": "AGENT", "icon": "◈", "full": "Agent"},
    "development": {"name": "DEV", "icon": "⌥", "full": "Development"},
    "file": {"name": "FILE", "icon": "≡", "full": "Files"},
    "task": {"name": "TASK", "icon": "☰", "full": "Tasks"},
    "custom": {"name": "PLUG", "icon": "⊕", "full": "Plugins"},
}
CATEGORY_ORDER = ["system", "conversation", "agent", "development", "file", "task", "custom"]


def apply_bg_gradient(
    text: str,
    start_color: Tuple[int, int, int],
    end_color: Tuple[int, int, int],
) -> str:
    """Apply background color gradient to text.

    Args:
        text: Text to apply gradient background to.
        start_color: RGB tuple for start of gradient.
        end_color: RGB tuple for end of gradient.

    Returns:
        Text with gradient background applied.
    """
    if not text:
        return text

    result = []
    text_length = len(text)
    use_true_color = get_color_support() == ColorSupport.TRUE_COLOR

    for i, char in enumerate(text):
        position = i / max(1, text_length - 1)

        # Interpolate between start and end colors
        r = int(start_color[0] + (end_color[0] - start_color[0]) * position)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * position)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * position)

        if use_true_color:
            bg_code = f"\033[48;2;{r};{g};{b}m"
        else:
            # Fallback to 256-color approximation
            color_idx = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)
            bg_code = f"\033[48;5;{color_idx}m"

        result.append(f"{bg_code}{char}")

    result.append(RESET)
    return "".join(result)


class CommandMenuRenderer:
    """Renders interactive command menu overlay.

    Provides a command menu that appears when the user
    types '/' and allows filtering and selection of available commands.
    """

    def __init__(self, terminal_renderer, max_visible_items: int = 5) -> None:
        """Initialize the command menu renderer.

        Args:
            terminal_renderer: Terminal renderer for display operations.
            max_visible_items: Maximum number of menu items to show at once.
        """
        self.renderer = terminal_renderer
        self.logger = logger
        self.menu_active = False
        self.current_commands = []
        self.menu_items = []  # Flattened list: commands + subcommands as selectable items
        self.selected_index = 0
        self.filter_text = ""
        self.current_menu_lines = []  # Store menu content for event system
        self.max_visible_items = max_visible_items
        self.scroll_offset = 0  # First visible item index

    def _get_menu_width(self) -> int:
        """Get menu width to match input box width.

        Uses same calculation as enhanced_input plugin:
        terminal_width - 4, clamped between min_width and max_width from config.

        Returns:
            Menu width in characters.
        """
        import shutil
        try:
            terminal_width = shutil.get_terminal_size().columns
        except Exception:
            terminal_width = 80

        # Read constraints from same config as enhanced_input plugin
        config = getattr(self.renderer, '_app_config', None)
        if config and hasattr(config, 'get'):
            min_width = config.get("plugins.enhanced_input.min_width", 60)
            max_width = config.get("plugins.enhanced_input.max_width", 120)
        else:
            min_width = 60
            max_width = 120

        # Match input box: terminal_width - 4, with constraints
        proposed_width = terminal_width - 4
        return max(min_width, min(max_width, proposed_width))

    def show_command_menu(self, commands: List[Dict[str, Any]], filter_text: str = "") -> None:
        """Display command menu when user types '/'.

        Args:
            commands: List of available commands to display.
            filter_text: Current filter text (excluding the leading '/').
        """
        try:
            self.menu_active = True
            self.current_commands = self._sort_commands_by_category(commands)
            self.filter_text = filter_text
            self.selected_index = 0
            self.scroll_offset = 0  # Reset scroll when menu opens

            # Build flattened menu items (commands + subcommands)
            self.menu_items = self._build_menu_items()

            # Render the menu
            self._render_menu()

            self.logger.info(f"Command menu shown with {len(commands)} commands, {len(self.menu_items)} items")

        except Exception as e:
            self.logger.error(f"Error showing command menu: {e}")

    def set_selected_index(self, index: int) -> None:
        """Set the selected menu item index for navigation.

        Args:
            index: Index of the item to select (in menu_items list).
        """
        if 0 <= index < len(self.menu_items):
            self.selected_index = index
            self._ensure_selection_visible()
            # Note: No auto-render here - caller will trigger render to avoid duplicates
            logger.debug(f"Selected menu item index set to: {index}")

    def hide_menu(self) -> None:
        """Hide command menu and return to normal input."""
        try:
            if self.menu_active:
                self.menu_active = False
                self.current_commands = []
                self.selected_index = 0
                self.filter_text = ""
                self.scroll_offset = 0

                # Clear menu from display
                self._clear_menu()

                self.logger.info("Command menu hidden")

        except Exception as e:
            self.logger.error(f"Error hiding command menu: {e}")

    def filter_commands(self, commands: List[Dict[str, Any]], filter_text: str, reset_selection: bool = True) -> None:
        """Filter visible commands as user types.

        Args:
            commands: Filtered list of commands to display.
            filter_text: Current filter text.
            reset_selection: Whether to reset selection to top (True for typing, False for navigation).
        """
        try:
            if not self.menu_active:
                return

            self.current_commands = self._sort_commands_by_category(commands)
            self.filter_text = filter_text

            # Build flattened menu items (commands + subcommands)
            self.menu_items = self._build_menu_items()

            # Only reset selection when filtering by typing, not during navigation
            if reset_selection:
                self.selected_index = 0  # Reset selection to top
                self.scroll_offset = 0  # Reset scroll when filtering
            else:
                # Ensure selected index is still valid after filtering
                if self.selected_index >= len(self.menu_items):
                    self.selected_index = max(0, len(self.menu_items) - 1)
                # Adjust scroll if needed
                self._ensure_selection_visible()

            # Re-render with filtered commands
            self._render_menu()

            self.logger.debug(f"Filtered to {len(commands)} commands with '{filter_text}', reset_selection={reset_selection}")

        except Exception as e:
            self.logger.error(f"Error filtering commands: {e}")

    def navigate_selection(self, direction: str) -> bool:
        """Handle arrow key navigation in menu.

        Args:
            direction: Direction to navigate ("up" or "down").

        Returns:
            True if navigation was handled, False otherwise.
        """
        try:
            if not self.menu_active or not self.menu_items:
                return False

            if direction == "up":
                self.selected_index = max(0, self.selected_index - 1)
            elif direction == "down":
                self.selected_index = min(len(self.menu_items) - 1, self.selected_index + 1)
            else:
                return False

            # Adjust scroll to keep selection visible
            self._ensure_selection_visible()

            # Re-render with new selection
            self._render_menu()
            return True

        except Exception as e:
            self.logger.error(f"Error navigating menu: {e}")
            return False

    def _ensure_selection_visible(self) -> None:
        """Adjust scroll offset to keep selected item visible."""
        if not self.menu_items:
            return

        # If selection is above visible area, scroll up
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index

        # If selection is below visible area, scroll down
        elif self.selected_index >= self.scroll_offset + self.max_visible_items:
            self.scroll_offset = self.selected_index - self.max_visible_items + 1

        # Clamp scroll offset to valid range
        max_scroll = max(0, len(self.menu_items) - self.max_visible_items)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

    def get_selected_command(self) -> Optional[Dict[str, Any]]:
        """Get currently selected menu item (command or subcommand).

        Returns:
            Selected item dictionary with keys:
            - For commands: name, description, aliases, category, etc.
            - For subcommands: is_subcommand=True, parent_name, subcommand_name, subcommand_args
            Returns None if no selection.
        """
        if (self.menu_active and
            self.menu_items and
            0 <= self.selected_index < len(self.menu_items)):
            return self.menu_items[self.selected_index]
        return None

    def _build_menu_items(self) -> List[Dict[str, Any]]:
        """Build flattened list of menu items including subcommands.

        Creates a flat list where each command is followed by its subcommands.
        Subcommands only appear when filtered to a single command (not in main menu).

        Returns:
            List of menu item dicts, each with is_subcommand flag.
        """
        items = []
        # Only show subcommands when filtered to a single command
        show_subcommands = len(self.current_commands) == 1

        for i, cmd in enumerate(self.current_commands):
            # Add the command itself
            cmd_item = cmd.copy()
            cmd_item["is_subcommand"] = False
            cmd_item["_cmd_index"] = i
            items.append(cmd_item)

            # Add subcommands only when this is the only command showing
            if show_subcommands:
                subcommands = cmd.get("subcommands", [])
                if subcommands:
                    for sub in subcommands:
                        sub_item = {
                            "is_subcommand": True,
                            "parent_name": cmd["name"],
                            "parent_category": cmd.get("category", "custom"),
                            "subcommand_name": sub.get("name", ""),
                            "subcommand_args": sub.get("args", ""),
                            "subcommand_desc": sub.get("description", ""),
                            "_cmd_index": i,
                        }
                        items.append(sub_item)

        return items

    def _render_menu(self) -> None:
        """Render the command menu overlay."""
        try:
            if not self.menu_active:
                return

            # Create menu content
            menu_lines = self._create_menu_lines()

            # Display menu overlay
            self._display_menu_overlay(menu_lines)

        except Exception as e:
            self.logger.error(f"Error rendering menu: {e}")

    def _create_menu_lines(self) -> List[str]:
        """Create lines for menu display with category grouping and scroll support.

        Returns:
            List of formatted menu lines (limited to max_visible_items).
        """
        lines = []

        # If no items, show empty state
        if not self.menu_items:
            lines.append(self._make_empty_state())
            return lines

        total_items = len(self.menu_items)
        has_more_above = self.scroll_offset > 0
        has_more_below = self.scroll_offset + self.max_visible_items < total_items

        # Scroll up indicator
        if has_more_above:
            lines.append(self._make_scroll_indicator("up", self.scroll_offset))

        # Get visible items slice
        visible_start = self.scroll_offset
        visible_end = min(self.scroll_offset + self.max_visible_items, total_items)

        # Track current category for headers
        current_category = None

        # Render visible items (commands and subcommands)
        for i in range(visible_start, visible_end):
            item = self.menu_items[i]
            is_selected = (i == self.selected_index)

            if item.get("is_subcommand"):
                # Render subcommand item
                line = self._format_subcommand_item(item, is_selected)
                lines.append(line)
            else:
                # Render command item
                cmd_category = item.get("category", "custom")

                # Convert CommandCategory enum to string if needed
                if hasattr(cmd_category, 'value'):
                    cmd_category = cmd_category.value

                # Insert category header when category changes
                if cmd_category != current_category:
                    current_category = cmd_category
                    header = self._format_category_header(cmd_category)
                    lines.append(header)

                item["_is_selected"] = is_selected
                item["_index"] = i
                line = self._format_command_line(item, cmd_category)
                lines.append(line)

        # Scroll down indicator
        if has_more_below:
            remaining = total_items - visible_end
            lines.append(self._make_scroll_indicator("down", remaining))

        # Footer with keybind hints
        lines.extend(self._make_footer())

        return lines

    def _make_empty_state(self) -> str:
        """Create fancy empty state message."""
        seg = AgnosterSegment()
        seg.add_neutral(f" {GLOW} No matches ", "dark")
        return seg.render(separator="")

    def _make_scroll_indicator(self, direction: str, count: int) -> str:
        """Create scroll indicator with gradient background.

        Args:
            direction: "up" or "down"
            count: Number of items in that direction

        Returns:
            Formatted scroll indicator string with gradient.
        """
        arrow = ARROW_UP if direction == "up" else ARROW_DOWN
        line_width = self._get_menu_width()

        # Solid start portion with arrow and count
        cyan_bg = make_bg_color(*AgnosterColors.CYAN_DARK)
        text_light = make_fg_color(*AgnosterColors.TEXT_LIGHT)
        start_text = f" {arrow} {count} "

        # Gradient fade portion (remaining width)
        fade_width = line_width - len(start_text)
        fade_spaces = " " * fade_width

        # Apply gradient from cyan to near-black
        gradient_fade = apply_bg_gradient(
            fade_spaces,
            start_color=AgnosterColors.CYAN_DARK,
            end_color=(15, 25, 35),  # Dark blue-grey
        )

        line = (
            f"{cyan_bg}{text_light} {arrow} {BOLD}{count}{RESET}"
            f"{gradient_fade}"
        )
        return line

    def _make_footer(self) -> List[str]:
        """Create footer with keybind hints.

        Returns:
            List of formatted footer lines.
        """
        hint_text = "↑↓ navigate   ⏎ select   esc cancel"
        return [f" {DIM}   {hint_text}{RESET}"]

    def _format_subcommand_item(self, item: Dict[str, Any], is_selected: bool) -> str:
        """Format a single subcommand as a selectable menu item.

        Args:
            item: Subcommand item dict with subcommand_name, subcommand_args, subcommand_desc.
            is_selected: Whether this item is currently selected.

        Returns:
            Formatted subcommand line.
        """
        name = item.get("subcommand_name", "")
        args = item.get("subcommand_args", "")
        desc = item.get("subcommand_desc", "")

        # Format: "      new <name> <cmd>  Create session..."
        cmd_part = f"{name}"
        if args:
            cmd_part += f" {args}"

        # Pad command part to align descriptions
        cmd_padded = cmd_part.ljust(20)

        if is_selected:
            # Selected subcommand - highlighted
            cyan_bg = make_bg_color(*AgnosterColors.CYAN_DARK)
            cyan_fg = make_fg_color(*AgnosterColors.CYAN)
            lime_fg = make_fg_color(*AgnosterColors.LIME)
            text_light = make_fg_color(*AgnosterColors.TEXT_LIGHT)
            dark_bg = make_bg_color(*AgnosterColors.BG_MID)

            line = f"    {lime_fg}{GLOW}{RESET} {cyan_fg}{BOLD}{cmd_padded}{RESET} {text_light}{desc}{RESET}"
        else:
            # Unselected subcommand - dimmed
            cyan_fg = make_fg_color(*AgnosterColors.CYAN)
            line = f"      {cyan_fg}{cmd_padded}{RESET} {DIM}{desc}{RESET}"

        return line

    def _format_category_header(self, category: str) -> str:
        """Format a powerline-style category header.

        Args:
            category: Category identifier.

        Returns:
            Formatted category header string with powerline transitions.
        """
        config = CATEGORY_CONFIG.get(category, {"name": "???", "icon": "?", "full": category.title()})

        # Build powerline: icon segment -> name segment -> fade out
        lime_bg = make_bg_color(*AgnosterColors.LIME)
        lime_fg = make_fg_color(*AgnosterColors.LIME)
        dark_bg = make_bg_color(*AgnosterColors.BG_DARK)
        dark_fg = make_fg_color(*AgnosterColors.TEXT_DARK)
        light_fg = make_fg_color(*AgnosterColors.TEXT_LIGHT)

        # Icon in lime -> powerline separator -> name in dark
        line = (
            f"{lime_bg}{dark_fg}{BOLD} {config['icon']} {RESET}"
            f"{dark_bg}{lime_fg}{PL_RIGHT}{RESET}"
            f"{dark_bg}{light_fg} {config['full']} {RESET}"
            f"{lime_fg}{PL_RIGHT}{RESET}"
        )
        return line

    def _sort_commands_by_category(self, commands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort commands by category order for grouped display.

        Args:
            commands: List of command dictionaries.

        Returns:
            Sorted list of commands.
        """
        def get_category_order(cmd):
            category = cmd.get("category", "custom")
            # Handle CommandCategory enum
            if hasattr(category, 'value'):
                category = category.value
            try:
                return CATEGORY_ORDER.index(category)
            except ValueError:
                return len(CATEGORY_ORDER)  # Unknown categories go last

        return sorted(commands, key=get_category_order)

    def _group_commands_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """Group commands by category for organized display.

        Returns:
            Dictionary mapping category names to command lists.
        """
        categorized = {}

        for i, cmd in enumerate(self.current_commands):
            category = cmd.get("category", "custom")
            if category not in categorized:
                categorized[category] = []

            # Add selection info to command
            cmd_with_selection = cmd.copy()
            cmd_with_selection["_is_selected"] = (i == self.selected_index)
            cmd_with_selection["_index"] = i

            categorized[category].append(cmd_with_selection)

        return categorized

    def _format_category_name(self, category: str) -> str:
        """Format category name for display.

        Args:
            category: Category identifier.

        Returns:
            Formatted category name.
        """
        category_names = {
            "system": "Core System",
            "conversation": "Conversation Management",
            "agent": "Agent Management",
            "development": "Development Tools",
            "file": "File Management",
            "task": "Task Management",
            "custom": "Plugin Commands"
        }
        return category_names.get(category, category.title())

    def _format_command_line(self, cmd: Dict[str, Any], category: str = "custom") -> str:
        """Format a single command line with powerline style.

        Args:
            cmd: Command dictionary with display info.
            category: Category for color theming.

        Returns:
            Formatted command line string.
        """
        is_selected = cmd.get("_is_selected", False)
        name = cmd['name']
        description = cmd.get("description", "")
        aliases = cmd.get("aliases", [])
        line_width = self._get_menu_width()

        if is_selected:
            # SELECTED: Full powerline glow effect
            # [glow] [cyan: /name] [dark: description padded] [aliases]
            cyan_bg = make_bg_color(*AgnosterColors.CYAN)
            cyan_fg = make_fg_color(*AgnosterColors.CYAN)
            lime_bg = make_bg_color(*AgnosterColors.LIME)
            lime_fg = make_fg_color(*AgnosterColors.LIME)
            dark_bg = make_bg_color(*AgnosterColors.BG_MID)
            dark_fg = make_fg_color(*AgnosterColors.BG_MID)
            text_dark = make_fg_color(*AgnosterColors.TEXT_DARK)
            text_light = make_fg_color(*AgnosterColors.TEXT_LIGHT)

            # Calculate available space for description
            # Layout: " ◆ " (4) + /name + " " (varies) + description + padding
            name_part = f" /{name} "
            prefix_len = 4 + len(name_part) + 2  # glow + name + separators

            # Build alias hint if available
            alias_hint = ""
            alias_len = 0
            if aliases:
                alias_str = " ".join(f"/{a}" for a in aliases[:2])  # Max 2 aliases
                alias_hint = f" {DIM}also: {alias_str}{RESET}"
                alias_len = len(f" also: {alias_str}")

            # Available for description + padding
            desc_area = line_width - prefix_len - alias_len - 2
            if len(description) > desc_area:
                description = description[:desc_area-2] + ".."
            desc_padded = description.ljust(desc_area)

            line = (
                f"{lime_bg}{text_dark}{BOLD} {GLOW} {RESET}"
                f"{cyan_bg}{lime_fg}{PL_RIGHT}{RESET}"
                f"{cyan_bg}{text_dark}{BOLD} /{name} {RESET}"
                f"{dark_bg}{cyan_fg}{PL_RIGHT}{RESET}"
                f"{dark_bg}{text_light} {desc_padded}{RESET}"
                f"{dark_fg}{PL_RIGHT}{RESET}"
                f"{alias_hint}"
            )
            return line
        else:
            # NOT SELECTED: Subtle powerline with full-width description
            mid_bg = make_bg_color(*AgnosterColors.BG_DARK)
            mid_fg = make_fg_color(*AgnosterColors.BG_DARK)
            text_light = make_fg_color(*AgnosterColors.TEXT_LIGHT)
            cyan_fg = make_fg_color(*AgnosterColors.CYAN)

            # Dot leader between name and description
            name_str = f"/{name}"
            name_col_width = 14  # Fixed column for command name
            padding_len = name_col_width - len(name_str)
            dots = DOT * max(2, padding_len)

            # Calculate description area
            # Layout: "   " (3) + name_col + " " + dots + " " + description
            prefix_len = 3 + name_col_width + 4  # indent + name + powerline + spacing
            desc_area = line_width - prefix_len - 2
            if len(description) > desc_area:
                description = description[:desc_area-2] + ".."

            line = (
                f"   {mid_bg}{cyan_fg}{BOLD} {name_str} {RESET}"
                f"{mid_fg}{PL_RIGHT}{RESET}"
                f" {DIM}{dots} {description}{RESET}"
            )
            return line

    def _display_menu_overlay(self, menu_lines: List[str]) -> None:
        """Display menu as overlay on terminal.

        Args:
            menu_lines: Formatted menu lines to display.
        """
        try:
            # Store menu content for INPUT_RENDER event response
            self.current_menu_lines = menu_lines

            # Log menu for debugging
            self.logger.info("=== COMMAND MENU ===")
            for line in menu_lines:
                self.logger.info(line)
            self.logger.info("=== END MENU ===")

        except Exception as e:
            self.logger.error(f"Error preparing menu display: {e}")

    def _clear_menu(self) -> None:
        """Clear menu from display."""
        try:
            # Clear overlay if renderer supports it
            if hasattr(self.renderer, 'hide_overlay'):
                self.renderer.hide_overlay()
            elif hasattr(self.renderer, 'clear_menu'):
                self.renderer.clear_menu()
            else:
                # Fallback: log clear
                self.logger.info("Command menu cleared")

        except Exception as e:
            self.logger.error(f"Error clearing menu: {e}")

    def get_menu_stats(self) -> Dict[str, Any]:
        """Get menu statistics for debugging.

        Returns:
            Dictionary with menu statistics.
        """
        return {
            "active": self.menu_active,
            "command_count": len(self.current_commands),
            "selected_index": self.selected_index,
            "filter_text": self.filter_text,
            "selected_command": self.get_selected_command(),
            "scroll_offset": self.scroll_offset,
            "max_visible_items": self.max_visible_items,
            "visible_range": f"{self.scroll_offset}-{min(self.scroll_offset + self.max_visible_items, len(self.current_commands))}"
        }