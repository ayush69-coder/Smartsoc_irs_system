#!/usr/bin/env python3
"""
Test runner for PhishGuard Pro backend
"""
import subprocess
import sys
import os

def run_tests():
    """Run all backend tests"""
    print("🧪 Running PhishGuard Pro Backend Tests")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run pytest with coverage
    cmd = [
        "python3", "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ pytest not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-cov"])
        return run_tests()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)