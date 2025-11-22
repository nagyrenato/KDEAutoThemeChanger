#!/usr/bin/env python3
"""
Configuration module for KDE Theme Auto-Changer

Contains default settings and configuration management.
"""

from pathlib import Path


class Config:
    """Configuration settings for theme changer"""

    # Default theme names
    DEFAULT_LIGHT_THEME = "org.kde.breeze.desktop"
    DEFAULT_DARK_THEME = "org.kde.breezedark.desktop"

    # Default location (New York)
    DEFAULT_LATITUDE = 40.7128
    DEFAULT_LONGITUDE = -74.0060
    DEFAULT_CITY = "New York"
    DEFAULT_REGION = "USA"
    DEFAULT_TIMEZONE = "America/New_York"

    # Daemon settings
    DEFAULT_CHECK_INTERVAL = 300  # 5 minutes in seconds

    # Logging settings
    LOG_FILE = Path.home() / ".kde_theme_changer.log"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    # API endpoints
    IP_GEOLOCATION_API = "http://ip-api.com/json/"
    GEOCODING_API = "https://nominatim.openstreetmap.org/search"

    # User agent for API requests
    USER_AGENT = "KDE-Theme-Changer/1.0"

    # API timeouts
    API_TIMEOUT = 10  # seconds

    # Notification settings
    NOTIFICATION_APP_NAME = "KDE Theme Changer"
    NOTIFICATION_ICON = "preferences-desktop-theme"
