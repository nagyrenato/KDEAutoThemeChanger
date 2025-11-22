#!/usr/bin/env python3
"""
Test runner script for KDE Theme Auto-Changer
"""

import subprocess
import sys

def run_tests():
    """Run all tests"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short"
        ], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == "__main__":
    print("Running KDE Theme Auto-Changer tests...")
    success = run_tests()
    sys.exit(0 if success else 1)