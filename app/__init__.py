"""
KDE Theme Auto-Changer

A modular Python application that automatically changes KDE Plasma themes
based on sunrise and sunset times.
"""

__version__ = "2.0.0"
__author__ = "Renato Nagy"

from .config import Config
from .location_manager import LocationManager
from .theme_manager import ThemeManager

__all__ = ["Config", "LocationManager", "ThemeManager"]
