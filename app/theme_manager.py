#!/usr/bin/env python3
"""
Theme management module for KDE Theme Auto-Changer

Handles KDE Plasma theme operations and system notifications.
"""

import logging
import subprocess

from .config import Config


class ThemeManager:
    """Manages KDE Plasma theme changes and notifications"""

    def __init__(self, light_theme=None, dark_theme=None):
        self.logger = logging.getLogger(__name__)
        self.light_theme = light_theme or Config.DEFAULT_LIGHT_THEME
        self.dark_theme = dark_theme or Config.DEFAULT_DARK_THEME

    def get_current_theme(self):
        """Get the currently active KDE theme"""
        try:
            result = subprocess.run(
                [
                    "kreadconfig5",
                    "--file",
                    "kdeglobals",
                    "--group",
                    "KDE",
                    "--key",
                    "LookAndFeelPackage",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            current_theme = result.stdout.strip()
            self.logger.debug(f"Current theme: {current_theme}")
            return current_theme
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting current theme: {e}")
            return None
        except FileNotFoundError:
            self.logger.error("kreadconfig5 not found. Are you running KDE Plasma?")
            return None

    def set_theme(self, theme_name):
        """Set the KDE theme"""
        try:
            # Change the look and feel package
            subprocess.run(
                [
                    "kwriteconfig5",
                    "--file",
                    "kdeglobals",
                    "--group",
                    "KDE",
                    "--key",
                    "LookAndFeelPackage",
                    theme_name,
                ],
                check=True,
            )

            # Apply the theme using lookandfeeltool
            subprocess.run(["lookandfeeltool", "--apply", theme_name], check=True)

            self.logger.info(f"Successfully changed theme to: {theme_name}")

            # Send system notification
            self._send_notification(theme_name)

            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error setting theme: {e}")
            return False
        except FileNotFoundError:
            self.logger.error("KDE tools not found. Are you running KDE Plasma?")
            return False

    def _send_notification(self, theme_name):
        """Send a system notification about theme change"""
        try:
            theme_type = "Light" if "breeze.desktop" in theme_name else "Dark"
            title = "KDE Theme Changed"
            message = f"Switched to {theme_type} theme"

            subprocess.run(
                [
                    "notify-send",
                    "-a",
                    Config.NOTIFICATION_APP_NAME,
                    "-i",
                    Config.NOTIFICATION_ICON,
                    title,
                    message,
                ],
                check=False,
                stderr=subprocess.DEVNULL,
            )  # Suppress libnotify portal messages
        except FileNotFoundError:
            self.logger.debug("notify-send not found, skipping notification")
        except Exception as e:
            self.logger.debug(f"Could not send notification: {e}")

    def _send_startup_notification(self, mode="manual"):
        """Send a system notification when the app starts"""
        try:
            title = "KDE Theme Changer Started"
            if mode == "daemon":
                message = "Running in daemon mode"
            else:
                message = "Theme update completed"

            subprocess.run(
                [
                    "notify-send",
                    "-a",
                    Config.NOTIFICATION_APP_NAME,
                    "-i",
                    Config.NOTIFICATION_ICON,
                    title,
                    message,
                ],
                check=False,
                stderr=subprocess.DEVNULL,
            )  # Suppress libnotify portal messages
        except FileNotFoundError:
            self.logger.debug("notify-send not found, skipping startup notification")
        except Exception as e:
            self.logger.debug(f"Could not send startup notification: {e}")

    def get_target_theme(self, is_daylight):
        """Get the target theme based on daylight status"""
        return self.light_theme if is_daylight else self.dark_theme
