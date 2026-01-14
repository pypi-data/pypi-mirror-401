"""
OriginEC - Electrochemical data processing for OriginPro
"""

from originec.origin_UI import main as launch_ui

__version__ = "0.1.3"
__all__ = ["launch_ui"]

# Convenience function
def launch():
    """Launch the OriginEC GUI"""
    launch_ui()
