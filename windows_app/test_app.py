#!/usr/bin/env python3
"""
Test script for PhishGuard Pro Windows Application

This script tests the application components without requiring tkinter.
"""

import sys
import json
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import requests
        print("✅ requests module available")
    except ImportError:
        print("❌ requests module not available")
        return False
    
    try:
        import tkinter
        print("✅ tkinter module available")
    except ImportError:
        print("❌ tkinter module not available (expected on Linux)")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    config_path = Path(__file__).parent / "config" / "app_config.json"
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print("✅ Configuration loaded successfully")
            print(f"   App: {config['app']['name']} v{config['app']['version']}")
            print(f"   API URL: {config['api']['base_url']}")
            return True
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return False
    else:
        print("❌ Configuration file not found")
        return False

def test_file_structure():
    """Test file structure"""
    print("\nTesting file structure...")
    
    required_files = [
        "src/phishguard_windows.py",
        "config/app_config.json",
        "launcher.py",
        "build_windows.py",
        "README.md",
        "requirements.txt"
    ]
    
    all_present = True
    for file_path in required_files:
        full_path = Path(__file__).parent / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_present = False
    
    return all_present

def test_code_syntax():
    """Test code syntax"""
    print("\nTesting code syntax...")
    
    try:
        # Test main application file
        src_path = Path(__file__).parent / "src" / "phishguard_windows.py"
        with open(src_path, 'r') as f:
            code = f.read()
        
        # Basic syntax check
        compile(code, str(src_path), 'exec')
        print("✅ Main application syntax OK")
        
        # Test launcher
        launcher_path = Path(__file__).parent / "launcher.py"
        with open(launcher_path, 'r') as f:
            launcher_code = f.read()
        
        compile(launcher_code, str(launcher_path), 'exec')
        print("✅ Launcher syntax OK")
        
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🛡️ PhishGuard Pro Windows App - Test Suite")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_config,
        test_code_syntax,
        test_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Windows app is ready.")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())