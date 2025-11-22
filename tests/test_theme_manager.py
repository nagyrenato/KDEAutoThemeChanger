#!/usr/bin/env python3
"""
Tests for theme_manager module
"""

import unittest
from unittest.mock import Mock, patch
from app.theme_manager import ThemeManager
from app.config import Config


class TestThemeManager(unittest.TestCase):
    """Test cases for ThemeManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.theme_manager = ThemeManager()

    def test_initialization(self):
        """Test ThemeManager initialization with default themes"""
        self.assertEqual(self.theme_manager.light_theme, Config.DEFAULT_LIGHT_THEME)
        self.assertEqual(self.theme_manager.dark_theme, Config.DEFAULT_DARK_THEME)

    def test_custom_themes(self):
        """Test ThemeManager with custom themes"""
        custom_light = "custom.light.theme"
        custom_dark = "custom.dark.theme"
        tm = ThemeManager(custom_light, custom_dark)
        self.assertEqual(tm.light_theme, custom_light)
        self.assertEqual(tm.dark_theme, custom_dark)

    def test_get_target_theme(self):
        """Test getting target theme based on daylight"""
        # Test daylight (should return light theme)
        self.assertEqual(
            self.theme_manager.get_target_theme(True), Config.DEFAULT_LIGHT_THEME
        )

        # Test nighttime (should return dark theme)
        self.assertEqual(
            self.theme_manager.get_target_theme(False), Config.DEFAULT_DARK_THEME
        )

    @patch("app.theme_manager.subprocess.run")
    def test_send_startup_notification_daemon(self, mock_subprocess):
        """Test sending startup notification for daemon mode"""
        mock_subprocess.return_value = Mock()
        self.theme_manager._send_startup_notification(mode="daemon")

        # Verify notify-send was called with correct arguments
        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]
        self.assertEqual(args[0], "notify-send")
        self.assertEqual(args[1], "-a")
        self.assertEqual(args[2], Config.NOTIFICATION_APP_NAME)
        self.assertIn("Running in daemon mode", args)

    @patch("app.theme_manager.subprocess.run")
    def test_send_startup_notification_manual(self, mock_subprocess):
        """Test sending startup notification for manual mode"""
        mock_subprocess.return_value = Mock()
        self.theme_manager._send_startup_notification(mode="manual")

        # Verify notify-send was called with correct arguments
        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]
        self.assertEqual(args[0], "notify-send")
        self.assertEqual(args[1], "-a")
        self.assertEqual(args[2], Config.NOTIFICATION_APP_NAME)
        self.assertIn("Theme update completed", args)


if __name__ == "__main__":
    unittest.main()
