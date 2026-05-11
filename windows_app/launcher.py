#!/usr/bin/env python3
"""
PhishGuard Pro Windows App Launcher

This script launches the PhishGuard Pro Windows desktop application
and handles any necessary setup or configuration.
"""

import sys
import os
import json
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import tkinter
        import requests
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install requests")
        return False

def load_config():
    """Load application configuration"""
    config_path = Path(__file__).parent / "config" / "app_config.json"
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "api": {"base_url": "http://localhost:8000"},
            "ui": {"window_width": 1200, "window_height": 800}
        }

def main():
    """Main launcher function"""
    print("🛡️ PhishGuard Pro Windows App Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        input("Press Enter to exit...")
        return 1
    
    # Load configuration
    config = load_config()
    print(f"Configuration loaded: {config['app']['name']} v{config['app']['version']}")
    
    # Add src directory to path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    try:
        # Import and run the main application
        from phishguard_windows import main as run_app
        print("Starting PhishGuard Pro Windows App...")
        run_app()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())