#!/usr/bin/env python3
"""
Location management module for KDE Theme Auto-Changer

Handles location detection, geocoding, and sunrise/sunset calculations.
"""

import logging
from datetime import datetime, timezone

try:
    from astral import LocationInfo
    from astral.sun import sun
except ImportError:
    raise ImportError(
        "'astral' package is required. Install it with: pip install astral"
    )

try:
    import requests
except ImportError:
    requests = None

from .config import Config


class LocationManager:
    """Manages location data and sun time calculations"""

    def __init__(self, latitude=None, longitude=None, city=None):
        self.logger = logging.getLogger(__name__)
        self.location = self._setup_location(latitude, longitude, city)

    def _setup_location(self, latitude, longitude, city):
        """Setup location for sunrise/sunset calculations"""
        if latitude and longitude:
            location = LocationInfo("Custom", "Custom", "UTC", latitude, longitude)
            self.logger.info(f"Using custom coordinates: {latitude}, {longitude}")
            return location

        if city:
            location = self._geocode_city(city)
            if location:
                return location
            self.logger.warning(f"Could not find city '{city}', trying auto-detection")

        # Try to auto-detect location
        location = self._auto_detect_location()
        if location:
            return location

        # Default to configured location if everything else fails
        self.logger.warning(f"Using default location ({Config.DEFAULT_CITY})")
        return LocationInfo(
            Config.DEFAULT_CITY,
            Config.DEFAULT_REGION,
            Config.DEFAULT_TIMEZONE,
            Config.DEFAULT_LATITUDE,
            Config.DEFAULT_LONGITUDE,
        )

    def _geocode_city(self, city_name):
        """Geocode a city name to get coordinates"""
        if not requests:
            self.logger.error("'requests' package required for city lookup")
            return None

        try:
            params = {"q": city_name, "format": "json", "limit": 1}
            headers = {"User-Agent": Config.USER_AGENT}

            response = requests.get(
                Config.GEOCODING_API,
                params=params,
                headers=headers,
                timeout=Config.API_TIMEOUT,
            )
            data = response.json()

            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                display_name = data[0]["display_name"]

                location = LocationInfo(city_name, display_name, "UTC", lat, lon)
                self.logger.info(f"Found city: {display_name} ({lat:.4f}, {lon:.4f})")
                return location
            else:
                self.logger.warning(
                    f"City '{city_name}' not found in geocoding service"
                )
        except Exception as e:
            self.logger.warning(f"Error geocoding city '{city_name}': {e}")

        return None

    def _auto_detect_location(self):
        """Auto-detect location using IP geolocation"""
        if not requests:
            return None

        try:
            response = requests.get(
                Config.IP_GEOLOCATION_API, timeout=Config.API_TIMEOUT
            )
            data = response.json()
            if data["status"] == "success":
                lat = data["lat"]
                lon = data["lon"]
                city = data["city"]
                country = data["country"]

                location = LocationInfo(city, country, "UTC", lat, lon)
                self.logger.info(
                    f"Auto-detected location: {city}, {country} ({lat}, {lon})"
                )
                return location
        except Exception as e:
            self.logger.warning(f"Could not auto-detect location: {e}")

        return None

    def get_sun_times(self, date=None):
        """Get sunrise and sunset times for the given date"""
        if date is None:
            date = datetime.now().date()

        try:
            s = sun(self.location.observer, date=date)
            sunrise = s["sunrise"]
            sunset = s["sunset"]
            return sunrise, sunset
        except Exception as e:
            self.logger.error(f"Error calculating sun times: {e}")
            # Default fallback times (6 AM - 6 PM)
            from datetime import time as dt_time

            sunrise = datetime.combine(date, dt_time(hour=6)).replace(
                tzinfo=timezone.utc
            )
            sunset = datetime.combine(date, dt_time(hour=18)).replace(
                tzinfo=timezone.utc
            )
            return sunrise, sunset

    def is_daylight(self):
        """Check if it's currently daylight"""
        sunrise, sunset = self.get_sun_times()
        now = datetime.now(sunrise.tzinfo)

        self.logger.debug(f"Current time: {now}")
        self.logger.debug(f"Sunrise: {sunrise}")
        self.logger.debug(f"Sunset: {sunset}")

        return sunrise <= now <= sunset
