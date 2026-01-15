"""
Platform detection utility for Windows systems.
"""

import platform


def check_is_platform_windows() -> bool:
    """
    Check if the current platform is Windows.

    Returns:
        bool: True if running on Windows, False otherwise
    """
    return (
        platform.system() == "Windows"
    )
