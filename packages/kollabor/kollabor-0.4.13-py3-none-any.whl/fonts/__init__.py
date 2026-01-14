"""Bundled Nerd Fonts for terminal icon rendering.

This package includes Nerd Fonts Symbols Only, which provides the Powerline
and icon glyphs used in the Kollabor CLI status bar.

Usage with agg (asciinema gif generator):
    agg --font-dir $(kollab --font-dir) recording.cast output.gif
"""

from pathlib import Path


def get_font_dir() -> Path:
    """Get the path to the bundled fonts directory.

    Returns:
        Path to the fonts directory containing Nerd Font TTF files.
    """
    return Path(__file__).parent


def get_font_path(font_name: str = "SymbolsNerdFontMono-Regular.ttf") -> Path:
    """Get the path to a specific bundled font file.

    Args:
        font_name: Name of the font file. Defaults to SymbolsNerdFontMono-Regular.ttf

    Returns:
        Path to the font file.

    Raises:
        FileNotFoundError: If the font file doesn't exist.
    """
    font_path = get_font_dir() / font_name
    if not font_path.exists():
        raise FileNotFoundError(f"Font not found: {font_path}")
    return font_path


# Available fonts
AVAILABLE_FONTS = [
    "SymbolsNerdFont-Regular.ttf",
    "SymbolsNerdFontMono-Regular.ttf",
]
