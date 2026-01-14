"""Full-screen plugins directory."""

from .matrix_plugin import MatrixRainPlugin
from .example_plugin import EnhancedExamplePlugin
from .setup_wizard_plugin import SetupWizardPlugin
from .space_shooter_plugin import SpaceShooterPlugin

__all__ = [
    "MatrixRainPlugin",
    "EnhancedExamplePlugin",
    "SetupWizardPlugin",
    "SpaceShooterPlugin"
]