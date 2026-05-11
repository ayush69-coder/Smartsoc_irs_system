#!/usr/bin/env python3
"""
Build script for PhishGuard Pro Windows Application

This script creates a standalone Windows executable using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build Windows executable"""
    print("Building Windows executable...")
    
    # Get paths
    script_dir = Path(__file__).parent
    src_dir = script_dir / "src"
    dist_dir = script_dir / "dist"
    
    # Clean previous builds
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create single executable
        "--windowed",  # No console window
        "--name", "PhishGuardPro",
        "--icon", str(script_dir / "assets" / "icon.ico"),  # If icon exists
        "--add-data", f"{script_dir / 'config'};config",  # Include config
        "--distpath", str(dist_dir),
        "--workpath", str(script_dir / "build"),
        "--specpath", str(script_dir),
        str(src_dir / "phishguard_windows.py")
    ]
    
    # Remove icon parameter if icon doesn't exist
    if not (script_dir / "assets" / "icon.ico").exists():
        cmd = [arg for arg in cmd if not arg.endswith("icon.ico")]
        cmd = [arg for arg in cmd if arg != "--icon"]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=script_dir)
    
    if result.returncode == 0:
        print("✅ Build successful!")
        print(f"Executable created in: {dist_dir}")
        return True
    else:
        print("❌ Build failed!")
        return False

def create_installer():
    """Create a simple installer package"""
    print("Creating installer package...")
    
    script_dir = Path(__file__).parent
    dist_dir = script_dir / "dist"
    installer_dir = script_dir / "installer"
    
    # Create installer directory
    installer_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_path = dist_dir / "PhishGuardPro.exe"
    if exe_path.exists():
        shutil.copy2(exe_path, installer_dir / "PhishGuardPro.exe")
    
    # Copy config
    config_src = script_dir / "config"
    config_dst = installer_dir / "config"
    if config_src.exists():
        shutil.copytree(config_src, config_dst, dirs_exist_ok=True)
    
    # Create README
    readme_content = """PhishGuard Pro Windows Application

Installation:
1. Copy all files to a folder on your computer
2. Run PhishGuardPro.exe
3. Make sure the backend server is running on http://localhost:8000

Requirements:
- Windows 10 or later
- Backend server running (see main project documentation)

For support, visit: https://github.com/vishxtr/HACKATHON_REAL2.0
"""
    
    with open(installer_dir / "README.txt", "w") as f:
        f.write(readme_content)
    
    print(f"✅ Installer package created in: {installer_dir}")

def main():
    """Main build function"""
    print("🛡️ PhishGuard Pro Windows Build Script")
    print("=" * 40)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        install_pyinstaller()
    
    # Build executable
    if build_executable():
        create_installer()
        print("\n🎉 Build completed successfully!")
        print("You can find the executable in the 'dist' folder")
        print("and the installer package in the 'installer' folder")
    else:
        print("\n❌ Build failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())