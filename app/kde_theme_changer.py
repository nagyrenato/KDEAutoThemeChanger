#!/usr/bin/env python3
"""
KDE Theme Auto-Changer based on Daylight

This script automatically changes KDE Plasma themes based on sunrise/sunset times.
It switches to a light theme during the day and a dark theme at night.

Requirements:
- KDE Plasma desktop environment
- Python packages: astral, requests (optional for location detection)

Usage:
    python kde_theme_changer.py [--latitude LAT] [--longitude LON] [--city CITY]

    Or run as a daemon:
    python kde_theme_changer.py --daemon

Author: Renato Nagy
"""

import argparse
import time
import logging

try:
    import requests
except ImportError:
    requests = None
    print("Warning: 'requests' package not found. Auto-location detection disabled.")

from .config import Config
from .location_manager import LocationManager
from .theme_manager import ThemeManager


class KDEThemeChanger:
    def __init__(
        self,
        latitude=None,
        longitude=None,
        city=None,
        light_theme=None,
        dark_theme=None,
    ):
        self.setup_logging()
        self.location_manager = LocationManager(latitude, longitude, city)
        self.theme_manager = ThemeManager(light_theme, dark_theme)

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format=Config.LOG_FORMAT,
            handlers=[logging.FileHandler(Config.LOG_FILE), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def update_theme(self):
        """Update theme based on current daylight status"""
        is_day = self.location_manager.is_daylight()
        target_theme = self.theme_manager.get_target_theme(is_day)
        current_theme = self.theme_manager.get_current_theme()

        sunrise, sunset = self.location_manager.get_sun_times()
        theme_status = "light (day)" if is_day else "dark (night)"

        if current_theme != target_theme:
            theme_type = "light" if is_day else "dark"
            self.logger.info(f"Switching to {theme_type} theme")

            if self.theme_manager.set_theme(target_theme):
                self.logger.info(
                    f"Theme changed successfully. Next change at: "
                    f"{'sunset' if is_day else 'sunrise'} "
                    f"({sunset.strftime('%H:%M') if is_day else sunrise.strftime('%H:%M')})"
                )
            else:
                self.logger.error("Failed to change theme")
        else:
            self.logger.info(
                f"Theme check: {theme_status}, current theme is correct. "
                f"Next change at: {'sunset' if is_day else 'sunrise'} "
                f"({sunset.strftime('%H:%M') if is_day else sunrise.strftime('%H:%M')})"
            )

    def run_once(self):
        """Run the theme update once"""
        self.logger.info("Running KDE theme changer")
        self.theme_manager._send_startup_notification(mode="manual")
        self.update_theme()

    def run_daemon(self, check_interval=Config.DEFAULT_CHECK_INTERVAL):
        """Run as a daemon, checking periodically"""
        self.logger.info(
            f"Starting KDE theme changer daemon (check interval: {check_interval}s)"
        )
        self.theme_manager._send_startup_notification(mode="daemon")

        try:
            while True:
                self.update_theme()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            self.logger.info("Daemon stopped by user")
        except Exception as e:
            self.logger.error(f"Daemon error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="KDE Theme Auto-Changer based on Daylight"
    )
    parser.add_argument("--latitude", type=float, help="Latitude for location")
    parser.add_argument("--longitude", type=float, help="Longitude for location")
    parser.add_argument("--city", help="City name for location")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument(
        "--interval",
        type=int,
        default=Config.DEFAULT_CHECK_INTERVAL,
        help="Check interval in seconds for daemon mode "
        f"(default: {Config.DEFAULT_CHECK_INTERVAL})",
    )
    parser.add_argument(
        "--light-theme",
        default=Config.DEFAULT_LIGHT_THEME,
        help="Light theme package name",
    )
    parser.add_argument(
        "--dark-theme",
        default=Config.DEFAULT_DARK_THEME,
        help="Dark theme package name",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create theme changer instance
    changer = KDEThemeChanger(
        args.latitude, args.longitude, args.city, args.light_theme, args.dark_theme
    )

    if args.daemon:
        changer.run_daemon(args.interval)
    else:
        changer.run_once()


if __name__ == "__main__":
    main()
