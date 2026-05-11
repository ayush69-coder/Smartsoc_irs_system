#!/usr/bin/env python3
"""
PhishGuard Pro - Quick Start Script

This script makes it super easy to get PhishGuard Pro running on any laptop.
Just run: python QUICK_START.py

Author: PhishGuard Pro Team
"""

import os
import sys
import subprocess
import platform
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("🛡️  PhishGuard Pro - Quick Start")
    print("=" * 60)
    print("Making phishing detection simple and accessible!")
    print()

def check_python():
    """Check Python version"""
    print("🐍 Checking Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Please install Python from https://python.org")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install Python packages
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
        print("✅ Python dependencies installed")
        
        # Install Node.js dependencies if available
        if shutil.which("npm"):
            try:
                subprocess.run(["npm", "install"], cwd="frontend", check=True)
                print("✅ Frontend dependencies installed")
            except subprocess.CalledProcessError:
                print("⚠️  Frontend dependencies installation failed - continuing anyway")
        else:
            print("⚠️  Node.js not found - frontend features will be limited")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_demo_data():
    """Create demo data if missing"""
    print("\n📊 Setting up demo data...")
    
    demo_file = Path("data/demo_campaigns.json")
    if not demo_file.exists():
        print("Creating demo data...")
        # Run the demo data generator
        try:
            subprocess.run([sys.executable, "data/generate_demo.py"], check=True)
            print("✅ Demo data created")
        except:
            print("⚠️  Demo data creation failed - using fallback")
    else:
        print("✅ Demo data already exists")

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting backend server...")
    
    try:
        # Start backend in background
        backend_process = subprocess.Popen(
            [sys.executable, "backend/main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get("http://localhost:8000/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server started successfully")
                return backend_process
        except:
            pass
        
        print("⚠️  Backend may still be starting...")
        return backend_process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend (if Node.js available)"""
    print("\n🌐 Starting frontend...")
    
    if not shutil.which("npm"):
        print("⚠️  Node.js not available - skipping frontend")
        return None
    
    # Check if node_modules exists, install if not
    if not Path("frontend/node_modules").exists():
        print("Installing frontend dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd="frontend", check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("⚠️  Frontend dependencies installation failed - skipping frontend")
            return None
    
    try:
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd="frontend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ Frontend started")
        return frontend_process
    except Exception as e:
        print(f"⚠️  Frontend failed to start: {e}")
        return None

def open_browser():
    """Open browser to the application"""
    print("\n🌐 Opening application in browser...")
    
    try:
        webbrowser.open("http://localhost:3000")  # Frontend
        time.sleep(1)
        webbrowser.open("http://localhost:8000/docs")  # API docs
        print("✅ Browser opened")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")

def show_instructions():
    """Show usage instructions"""
    print("\n" + "=" * 60)
    print("🎉 PhishGuard Pro is now running!")
    print("=" * 60)
    print()
    print("📍 Access Points:")
    print("   • Frontend: http://localhost:3000")
    print("   • API Docs: http://localhost:8000/docs")
    print("   • API Health: http://localhost:8000/api/health")
    print()
    print("🖥️  Windows Desktop App:")
    print("   • Run: python windows_app/launcher.py")
    print("   • Or: double-click windows_app/run_phishguard.bat")
    print()
    print("🛑 To stop the servers:")
    print("   • Press Ctrl+C in this terminal")
    print("   • Or close this window")
    print()
    print("📚 For more info, see README.md")
    print("=" * 60)

def main():
    """Main quick start function"""
    print_banner()
    
    # Check Python
    if not check_python():
        input("Press Enter to exit...")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        input("Press Enter to exit...")
        return 1
    
    # Create demo data
    create_demo_data()
    
    # Start services
    backend_process = start_backend()
    frontend_process = start_frontend()
    
    # Open browser
    open_browser()
    
    # Show instructions
    show_instructions()
    
    try:
        # Keep running until user stops
        print("\n🔄 Services running... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping services...")
        
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("👋 Thanks for using PhishGuard Pro!")
    
    return 0

if __name__ == "__main__":
    # Add shutil import
    import shutil
    sys.exit(main())