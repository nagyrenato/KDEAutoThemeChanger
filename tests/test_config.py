#!/usr/bin/env python3
"""
Tests for config module
"""

import unittest
from app.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class"""

    def test_default_themes(self):
        """Test default theme constants"""
        self.assertEqual(Config.DEFAULT_LIGHT_THEME, "org.kde.breeze.desktop")
        self.assertEqual(Config.DEFAULT_DARK_THEME, "org.kde.breezedark.desktop")

    def test_default_location(self):
        """Test default location constants"""
        self.assertEqual(Config.DEFAULT_CITY, "New York")
        self.assertAlmostEqual(Config.DEFAULT_LATITUDE, 40.7128)
        self.assertAlmostEqual(Config.DEFAULT_LONGITUDE, -74.0060)

    def test_daemon_settings(self):
        """Test daemon-related constants"""
        self.assertEqual(Config.DEFAULT_CHECK_INTERVAL, 300)


if __name__ == "__main__":
    unittest.main()
