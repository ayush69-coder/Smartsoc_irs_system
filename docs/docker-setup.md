# PhishGuard Pro - Docker Setup

This guide explains how to run PhishGuard Pro using Docker and Docker Compose.

## Prerequisites

- Docker 20.10+ 
- Docker Compose 2.0+
- At least 4GB RAM available
- Ports 3000, 8000, 5432, 6379 available

## Quick Start

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd phishguard-pro
   ```

2. **Start all services:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop all services:**
   ```bash
   docker-compose down
   ```

## Service Details

### Backend Service
- **Container:** `phishguard-backend`
- **Port:** 8000
- **Health Check:** http://localhost:8000/api/health
- **Data Volume:** `./data:/app/data`

### Frontend Service  
- **Container:** `phishguard-frontend`
- **Port:** 3000
- **Health Check:** http://localhost:3000
- **Dependencies:** Backend service

### Redis Service (Optional)
- **Container:** `phishguard-redis`
- **Port:** 6379
- **Purpose:** Caching and session storage

### PostgreSQL Service (Optional)
- **Container:** `phishguard-postgres`
- **Port:** 5432
- **Database:** `phishguard`
- **Credentials:** `phishguard/phishguard_demo_2024`

## Development Mode

For development with hot reloading:

```bash
# Backend only
docker-compose up backend

# Frontend only  
docker-compose up frontend

# All services
docker-compose up
```

## Production Deployment

1. **Build production images:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
   ```

2. **Deploy with production settings:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

## Environment Variables

Create a `.env` file in the project root:

```env
# Backend
PYTHONPATH=/app
ENVIRONMENT=production
JWT_SECRET=your-secret-key
DATABASE_URL=postgresql://phishguard:phishguard_demo_2024@postgres:5432/phishguard

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=production
```

## Data Persistence

- **Backend data:** Stored in `./data` directory (mounted volume)
- **PostgreSQL data:** Stored in Docker volume `postgres_data`
- **Redis data:** Stored in Docker volume `redis_data`

## Monitoring and Logs

```bash
# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Check service status
docker-compose ps

# Check resource usage
docker stats
```

## Troubleshooting

### Common Issues

1. **Port conflicts:**
   ```bash
   # Check what's using the ports
   lsof -i :3000
   lsof -i :8000
   ```

2. **Permission issues:**
   ```bash
   # Fix data directory permissions
   sudo chown -R $USER:$USER ./data
   ```

3. **Container won't start:**
   ```bash
   # Check container logs
   docker-compose logs backend
   docker-compose logs frontend
   ```

4. **Database connection issues:**
   ```bash
   # Restart database service
   docker-compose restart postgres
   ```

### Health Checks

```bash
# Check backend health
curl http://localhost:8000/api/health

# Check frontend health
curl http://localhost:3000

# Check all services
docker-compose ps
```

## Scaling

To scale services:

```bash
# Scale backend to 3 instances
docker-compose up -d --scale backend=3

# Scale frontend to 2 instances
docker-compose up -d --scale frontend=2
```

## Security Considerations

1. **Change default passwords** in production
2. **Use secrets management** for sensitive data
3. **Enable HTTPS** with reverse proxy
4. **Regular security updates** for base images
5. **Network isolation** for production deployment

## Backup and Recovery

```bash
# Backup PostgreSQL data
docker-compose exec postgres pg_dump -U phishguard phishguard > backup.sql

# Restore PostgreSQL data
docker-compose exec -T postgres psql -U phishguard phishguard < backup.sql

# Backup application data
tar -czf data-backup.tar.gz ./data
```

## Performance Tuning

1. **Resource limits** in docker-compose.yml
2. **Database connection pooling**
3. **Redis caching** for frequently accessed data
4. **CDN** for static assets
5. **Load balancing** for multiple instances