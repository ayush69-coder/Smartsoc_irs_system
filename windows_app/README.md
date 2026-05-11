# PhishGuard Pro - Windows Desktop Application

A standalone Windows desktop application for the PhishGuard Pro phishing detection and response platform.

## Features

- 🔍 **URL Analysis**: Analyze URLs for phishing threats in real-time
- 📊 **Live Feed**: Monitor live phishing events and threats
- ⚙️ **Settings**: Configure API endpoints and backend settings
- 📝 **Logging**: Built-in application logging and monitoring
- 🎨 **Modern UI**: Clean, intuitive desktop interface

## Requirements

- Windows 10 or later
- Python 3.8 or later (if running from source)
- PhishGuard Pro backend server running on `http://localhost:8000`

## Quick Start

### Option 1: Run from Source (Recommended for Development)

1. **Install Python Dependencies**:
   ```bash
   pip install requests
   ```

2. **Start the Backend Server**:
   ```bash
   # In the main project directory
   python scripts/setup_and_verify.py
   # Or start manually:
   cd backend
   python main.py
   ```

3. **Run the Windows App**:
   ```bash
   # Double-click run_phishguard.bat
   # Or run from command line:
   python launcher.py
   ```

### Option 2: Build Executable (For Distribution)

1. **Install Build Tools**:
   ```bash
   pip install pyinstaller
   ```

2. **Build the Executable**:
   ```bash
   python build_windows.py
   ```

3. **Run the Executable**:
   - Find `PhishGuardPro.exe` in the `dist` folder
   - Double-click to run

## Usage

### URL Analysis
1. Go to the "URL Analysis" tab
2. Enter a URL in the input field
3. Click "Analyze URL"
4. View the phishing score and detailed analysis

### Live Feed Monitoring
1. Go to the "Live Feed" tab
2. Click "Refresh" to load recent events
3. Enable "Auto-refresh" for continuous monitoring
4. Use the filter to search for specific events

### Settings
1. Go to the "Settings" tab
2. Configure the backend API URL if needed
3. Start/stop the backend server
4. View application logs

## Configuration

The application can be configured by editing `config/app_config.json`:

```json
{
  "api": {
    "base_url": "http://localhost:8000",
    "timeout": 30
  },
  "ui": {
    "window_width": 1200,
    "window_height": 800
  }
}
```

## Troubleshooting

### Backend Not Running
- Make sure the PhishGuard Pro backend is running on `http://localhost:8000`
- Check the "Settings" tab for backend status
- Use the "Start Backend" button if available

### Connection Errors
- Verify the API URL in settings
- Check firewall settings
- Ensure the backend server is accessible

### Missing Dependencies
- Run `pip install requests` to install required packages
- Make sure Python 3.8+ is installed

## Development

### Project Structure
```
windows_app/
├── src/
│   └── phishguard_windows.py    # Main application
├── config/
│   └── app_config.json          # Configuration
├── assets/                      # Icons and resources
├── dist/                        # Built executables
├── installer/                   # Installer package
├── launcher.py                  # Application launcher
├── build_windows.py             # Build script
├── run_phishguard.bat           # Windows batch launcher
├── run_phishguard.ps1           # PowerShell launcher
└── README.md                    # This file
```

### Building from Source
1. Install PyInstaller: `pip install pyinstaller`
2. Run build script: `python build_windows.py`
3. Find executable in `dist/` folder

## Support

For issues and support:
- GitHub Repository: https://github.com/vishxtr/HACKATHON_REAL2.0
- Check the main project documentation
- Review application logs in the Settings tab

## License

© 2024 PhishGuard Pro. All rights reserved.

---

**Note**: This Windows application is a client for the PhishGuard Pro platform. Make sure the backend server is running before using the application.