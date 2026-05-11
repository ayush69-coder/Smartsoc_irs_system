#!/usr/bin/env python3
"""
PhishGuard Pro - Setup Test Script

This script tests if PhishGuard Pro is properly set up and ready to run.
Run: python TEST_SETUP.py
"""

import os
import sys
import subprocess
import requests
import time
from pathlib import Path

def print_banner():
    """Print test banner"""
    print("=" * 50)
    print("🧪 PhishGuard Pro - Setup Test")
    print("=" * 50)
    print()

def test_python_deps():
    """Test Python dependencies"""
    print("🐍 Testing Python dependencies...")
    
    required_modules = [
        'fastapi', 'uvicorn', 'pydantic', 'requests', 
        'numpy', 'scikit-learn', 'networkx'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing modules: {', '.join(missing)}")
        print("   Run: pip install -r backend/requirements.txt")
        return False
    
    print("✅ All Python dependencies found")
    return True

def test_node_deps():
    """Test Node.js dependencies"""
    print("\n📦 Testing Node.js dependencies...")
    
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("  ✅ npm available")
        
        # Check if node_modules exists
        if Path("frontend/node_modules").exists():
            print("  ✅ Frontend dependencies installed")
            return True
        else:
            print("  ⚠️  Frontend dependencies not installed")
            print("     Run: cd frontend && npm install")
            return False
    except:
        print("  ⚠️  Node.js not available")
        print("     Install from: https://nodejs.org")
        return False

def test_demo_data():
    """Test demo data"""
    print("\n📊 Testing demo data...")
    
    demo_file = Path("data/demo_campaigns.json")
    if demo_file.exists():
        print("  ✅ Demo data exists")
        return True
    else:
        print("  ⚠️  Demo data missing")
        print("     Run: python data/generate_demo.py")
        return False

def test_backend_startup():
    """Test backend startup"""
    print("\n🚀 Testing backend startup...")
    
    try:
        # Start backend in background
        process = subprocess.Popen(
            [sys.executable, "backend/main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for startup
        time.sleep(5)
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:8000/api/health", timeout=5)
            if response.status_code == 200:
                print("  ✅ Backend started successfully")
                process.terminate()
                return True
            else:
                print(f"  ❌ Backend health check failed: {response.status_code}")
                process.terminate()
                return False
        except requests.exceptions.RequestException:
            print("  ❌ Backend not responding")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"  ❌ Backend startup failed: {e}")
        return False

def test_windows_app():
    """Test Windows app"""
    print("\n🖥️  Testing Windows app...")
    
    try:
        # Test import
        sys.path.insert(0, str(Path("windows_app/src")))
        import phishguard_windows
        print("  ✅ Windows app imports working")
        return True
    except Exception as e:
        print(f"  ❌ Windows app import failed: {e}")
        return False

def show_results(results):
    """Show test results"""
    print("\n" + "=" * 50)
    print("📊 Test Results")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! PhishGuard Pro is ready to run.")
        print("\n🚀 To start:")
        print("   python QUICK_START.py")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        print("\n🔧 To fix issues:")
        print("   python INSTALL.py")

def main():
    """Main test function"""
    print_banner()
    
    results = {
        "Python Dependencies": test_python_deps(),
        "Node.js Dependencies": test_node_deps(),
        "Demo Data": test_demo_data(),
        "Backend Startup": test_backend_startup(),
        "Windows App": test_windows_app()
    }
    
    show_results(results)
    
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main())