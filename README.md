# KDE Theme Auto-Changer

A Python script that automatically changes your KDE Plasma theme based on daylight hours. It switches to a light theme during the day and a dark theme at night, calculated from sunrise and sunset times for your location.

## Features

- Automatic theme switching based on sunrise/sunset
- Auto-location detection using IP geolocation
- Manual location configuration (city name or coordinates)
- Customizable theme selection
- Daemon mode for continuous monitoring
- System notifications on theme changes
- Comprehensive logging
- Modular architecture for easy maintenance

## Project Structure

```
AutoThemeChanger/
├── app/                    # Main application package
│   ├── __init__.py        # Package initialization and exports
│   ├── config.py          # Configuration and constants
│   ├── location_manager.py # Location detection and sun time calculations
│   ├── theme_manager.py   # KDE theme operations and notifications
│   └── kde_theme_changer.py # Main orchestrator script
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_config.py     # Tests for configuration module
│   └── test_theme_manager.py # Tests for theme management
├── .vscode/               # VS Code configuration
│   ├── launch.json        # Debug launch configurations
│   ├── settings.json      # Workspace settings
│   └── tasks.json         # Build and test tasks
├── main.py               # Entry point script
├── run_tests.py          # Test runner script
├── requirements.txt      # Runtime Python dependencies
├── requirements-dev.txt  # Development dependencies
├── .gitignore           # Git ignore rules
├── .flake8             # Flake8 linting configuration
└── README.md            # This file
```

### Module Overview

- **app/__init__.py**: Package initialization and exports
- **app/config.py**: Contains all configuration constants and default settings
- **app/location_manager.py**: Handles location detection (geocoding, IP-based), and calculates sunrise/sunset times
- **app/theme_manager.py**: Manages KDE theme switching and system notifications
- **app/kde_theme_changer.py**: Main entry point that orchestrates the components
- **main.py**: Simple wrapper script that launches the application
- **run_tests.py**: Test runner script for easy testing
- **tests/**: Unit tests covering core functionality
- **.vscode/**: VS Code configuration for development
- **requirements-dev.txt**: Development tools (pytest, flake8, black)

## Requirements

- KDE Plasma desktop environment
- Python 3.6+
- Required Python packages (see `requirements.txt` and `requirements-dev.txt`)

## Installation & Setup

1. Install runtime dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. For development (optional - includes testing and linting tools):
   ```bash
   pip install -r requirements-dev.txt
   ```

## Usage

### Basic Usage

Run once to update theme based on current time:
```bash
python3 main.py
```

### Daemon Mode

Run continuously in the background:
```bash
python3 main.py --daemon
```

### Location Configuration

Auto-detect location (default):
```bash
python3 main.py
```

Specify city:
```bash
python3 main.py --city "London"
```

Specify coordinates:
```bash
python3 main.py --latitude 40.7128 --longitude -74.0060
```

### Custom Themes

Use different themes:
```bash
python3 main.py \
  --light-theme "org.kde.breeze.desktop" \
  --dark-theme "org.kde.breezedark.desktop"
```

### Advanced Options

```bash
python3 main.py \
  --daemon \
  --interval 600 \
  --city "Tokyo" \
  --verbose
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--daemon` | Run as background daemon | False |
| `--interval SECONDS` | Check interval for daemon mode | 300 |
| `--city CITY` | City name for location | Auto-detect |
| `--latitude LAT` | Latitude coordinate | Auto-detect |
| `--longitude LON` | Longitude coordinate | Auto-detect |
| `--light-theme THEME` | Light theme package name | org.kde.breeze.desktop |
| `--dark-theme THEME` | Dark theme package name | org.kde.breezedark.desktop |
| `--verbose, -v` | Enable verbose logging | False |

## Available KDE Themes

Common KDE theme packages:
- `org.kde.breeze.desktop` (Light)
- `org.kde.breezedark.desktop` (Dark)
- `org.kde.breezetwilight.desktop` (Twilight)

To list available themes on your system:
```bash
ls /usr/share/plasma/look-and-feel/
```

## Troubleshooting

### Common Issues

1. **Script not working**: Make sure you're running KDE Plasma
   ```bash
   echo $XDG_CURRENT_DESKTOP
   # Should show "KDE"
   ```

2. **Permission errors**: Ensure the script has proper permissions
   ```bash
   chmod +x kde_theme_changer.py
   ```

3. **Theme not changing**: Check if the theme packages are installed
   ```bash
   ls /usr/share/plasma/look-and-feel/ | grep breeze
   ```

4. **Location detection fails**: Manually specify your location
   ```bash
   python3 main.py --city "Your City"
   ```

### Logs

The script logs to `~/.kde_theme_changer.log`. Check this file for detailed information about what's happening:
```bash
tail -f ~/.kde_theme_changer.log
```

## Configuration

### Custom Themes

You can use any installed KDE look-and-feel package. To find available themes:
```bash
# List all look-and-feel packages
ls /usr/share/plasma/look-and-feel/

# Or use plasmashell
kreadconfig5 --file kdeglobals --group KDE --key LookAndFeelPackage
```

### Time Zones

The script automatically handles time zones using the system's local time zone and UTC calculations for sunrise/sunset.

## Development

### VS Code Configuration

The project includes VS Code configuration files (`.vscode/`) with:

- **Launch configurations** for debugging different run modes
- **Tasks** for running the application and tests
- **Settings** for Python development (linting, formatting, testing)

Available debug configurations:
- Manual run mode
- Daemon mode (with shorter interval for testing)
- Verbose logging mode
- Custom city/location testing
- Test execution and debugging

### Code Quality

The project uses automated code quality tools:

- **Black**: Code formatting (100-character line length)
- **Flake8**: Linting and style checking
- **Pytest**: Unit testing framework

### Development Setup

1. Install all dependencies:
   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   ```

2. Run code quality checks:
   ```bash
   python3 -m flake8 app/ tests/ main.py
   ```

3. Format code:
   ```bash
   python3 -m black app/ tests/ main.py
   ```

### Running Tests

Run the test suite:
```bash
python3 run_tests.py
```

Or run tests directly with pytest:
```bash
python3 -m pytest tests/ -v
```

Run specific tests:
```bash
python3 -m pytest tests/test_config.py -v
```

### VS Code Tasks

Available tasks (Ctrl+Shift+P → "Tasks: Run Task"):
- **Run KDE Theme Changer**: Execute the application
- **Run Tests**: Run the test suite
- **Install Dependencies**: Install all required packages
- **Check Code Quality**: Run flake8 linting

## Changelog

### v2.0.0 (Current)
- **Project Structure**: Reorganized into `app/` and `tests/` folders
- **VS Code Integration**: Added comprehensive debug configurations and tasks
- **Code Quality**: Implemented Black formatting and Flake8 linting
- **Testing**: Added unit tests with pytest
- **Dependencies**: Separated runtime and development dependencies
- **Startup Notifications**: Added notifications when app starts
- **Daemon Mode**: Focused on daemon functionality only

### v1.0.0
- Initial release
- Basic daylight detection
- KDE theme switching
- Auto-location detection
- Daemon mode
- System notifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is released under the MIT License. See the LICENSE file for details.

## Author

Created by Renato Nagy
