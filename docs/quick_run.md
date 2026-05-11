# Quick Run Guide for Judges

## Prerequisites
- Docker & Docker Compose installed
- 4GB RAM available
- Ports 3000 and 8000 available

## 6-Step Quick Start

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd phishguard-pro
```

### 2. Start Demo Environment
```bash
./bin/present.sh
```

### 3. Open Dashboard
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### 4. Load Browser Extension
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension/dist` folder
5. Pin the extension to toolbar

### 5. Test the Demo
1. Visit suspicious URLs like `bit.ly/suspicious`
2. Check the Live Feed for simulated events
3. Explore the Domain Graph visualization
4. Try policy management features

### 6. Stop Demo
```bash
docker-compose down
```

## Expected URLs & Ports
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## Troubleshooting

### Backend won't start
```bash
docker-compose logs backend
```

### Frontend won't load
```bash
docker-compose logs frontend
```

### Extension not working
- Ensure demo mode is enabled in extension popup
- Check browser console for errors
- Verify backend is running on port 8000

### Port conflicts
```bash
# Check what's using the ports
lsof -i :3000
lsof -i :8000

# Kill processes if needed
kill -9 <PID>
```

## Demo Features to Show
1. **Overview Dashboard** - KPIs and recent alerts
2. **Live Feed** - Real-time event monitoring
3. **Domain Graph** - Threat visualization
4. **Browser Extension** - Real-time protection
5. **Policy Management** - Custom rules
6. **Analyst Tools** - Investigation features

## Time Required
- **Setup**: 2-3 minutes
- **Demo**: 5-7 minutes
- **Cleanup**: 30 seconds