#!/bin/bash

echo "================================================"
echo "  PhishGuard Pro - Quick Start for Mac/Linux"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo
    echo "Please install Python from: https://python.org"
    echo "Or use your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo
    exit 1
fi

echo "Python found! Starting PhishGuard Pro..."
echo

# Run the quick start script
python3 QUICK_START.py