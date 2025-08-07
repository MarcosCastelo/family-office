# Docker Setup for Family Office

This document describes how to set up and deploy the Family Office application using Docker.

## Prerequisites

- Docker
- Docker Compose
- Make (optional, for using Makefile commands)

## Quick Start

### Local Development

1. **Build and start all services:**
   ```bash
   make build
   make up
   ```

2. **Access the application:**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - Database: localhost:5432

3. **Run database migrations:**
   ```bash
   make migrate
   ```

### Manual Commands

If you prefer not to use Make:

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Services

### Backend (Flask)
- **Port:** 8000
- **Health Check:** http://localhost:8000/health
- **Database:** PostgreSQL
- **Framework:** Flask with Poetry

### Frontend (React)
- **Port:** 3000
- **Framework:** React + TypeScript + Vite
- **Server:** Nginx

### Database (PostgreSQL)
- **Port:** 5432
- **Database:** family_office
- **User:** postgres
- **Password:** password

## Railway Deployment

### Backend Deployment

1. **Connect your repository to Railway**
2. **Set environment variables:**
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `SECRET_KEY`: Your secret key
   - `JWT_SECRET_KEY`: Your JWT secret
   - `FLASK_ENV`: production

3. **Deploy:**
   Railway will automatically detect the Dockerfile and deploy your application.

### Frontend Deployment

1. **Create a new service in Railway**
2. **Set the source directory to `frontend/`**
3. **Set environment variables:**
   - `NODE_ENV`: production

## Environment Variables

### Backend (.env)
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://postgres:password@db:5432/family_office
GEMINI_API_KEY=your-gemini-api-key
```

### Production (Railway)
```env
FLASK_ENV=production
DATABASE_URL=your-production-database-url
SECRET_KEY=your-production-secret
JWT_SECRET_KEY=your-production-jwt-secret
GEMINI_API_KEY=your-gemini-api-key
```

## Useful Commands

```bash
# View all available commands
make help

# View logs for specific service
make logs-backend
make logs-frontend
make logs-db

# Restart specific service
make restart-backend
make restart-frontend

# Access container shell
make shell
make db-shell

# Run tests
make test

# Clean up everything
make clean
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Check what's using the port
   lsof -i :8000
   lsof -i :3000
   lsof -i :5432
   ```

2. **Database connection issues:**
   ```bash
   # Check database logs
   make logs-db
   
   # Access database shell
   make db-shell
   ```

3. **Build failures:**
   ```bash
   # Clean and rebuild
   make clean
   make build
   ```

### Health Checks

- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000/health

## Production Considerations

1. **Security:**
   - Use strong, unique secrets
   - Enable HTTPS
   - Set up proper CORS policies

2. **Performance:**
   - Configure proper worker processes
   - Set up caching
   - Monitor resource usage

3. **Monitoring:**
   - Set up logging
   - Configure health checks
   - Monitor database performance

## File Structure

```
.
├── Dockerfile                 # Backend Docker configuration
├── docker-compose.yml         # Local development setup
├── railway.toml              # Railway deployment config
├── .dockerignore             # Files to exclude from Docker build
├── Makefile                  # Development commands
├── frontend/
│   ├── Dockerfile            # Frontend Docker configuration
│   ├── nginx.conf            # Nginx configuration
│   └── .dockerignore         # Frontend-specific exclusions
└── app/
    └── routes/
        └── health.py         # Health check endpoint
``` 