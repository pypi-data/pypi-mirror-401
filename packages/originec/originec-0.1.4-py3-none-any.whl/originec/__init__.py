"""
OriginEC - Electrochemical data processing for OriginPro
"""

from .origin_UI import main as launch_ui

__version__ = "0.1.4"
__all__ = ["launch_ui", "launch"]

# Convenience function
def launch():
    """Launch the OriginEC GUI"""
    launch_ui()
