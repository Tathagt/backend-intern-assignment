# Backend Deployment Guide

## Deploy to Railway

### Using Railway CLI

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login:
```bash
railway login
```

3. Initialize project:
```bash
railway init
```

4. Add MongoDB:
```bash
railway add mongodb
```

5. Deploy:
```bash
railway up
```

### Using Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `Tathagt/backend-intern-assignment`
5. Add MongoDB service
6. Set environment variables
7. Deploy

## Deploy to Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - Name: `org-management-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add MongoDB (use MongoDB Atlas)
6. Set environment variables
7. Create Web Service

## Deploy to Heroku

1. Install Heroku CLI
2. Login:
```bash
heroku login
```

3. Create app:
```bash
heroku create org-management-api
```

4. Add MongoDB:
```bash
heroku addons:create mongolab
```

5. Deploy:
```bash
git push heroku main
```

## Deploy with Docker

### Build and Run Locally

```bash
docker-compose up -d
```

### Deploy to Docker Hub

```bash
docker build -t yourusername/org-management-api .
docker push yourusername/org-management-api
```

### Deploy to AWS ECS/Fargate

1. Push image to ECR
2. Create ECS cluster
3. Define task definition
4. Create service
5. Configure load balancer

## Environment Variables

Required environment variables:

```env
MONGODB_URL=mongodb://your-mongodb-url
DATABASE_NAME=master_db
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## MongoDB Setup

### Option 1: MongoDB Atlas (Recommended)

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Create database user
4. Whitelist IP addresses (0.0.0.0/0 for development)
5. Get connection string
6. Update MONGODB_URL in environment variables

### Option 2: Self-hosted MongoDB

```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

## Health Check Endpoint

```
GET /
```

Returns:
```json
{
  "message": "Organization Management Service API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

## API Documentation

Once deployed, access interactive API docs at:
- Swagger UI: `https://your-domain.com/docs`
- ReDoc: `https://your-domain.com/redoc`

## Security Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Use HTTPS in production
- [ ] Restrict MongoDB access (IP whitelist)
- [ ] Enable CORS only for trusted domains
- [ ] Set up rate limiting
- [ ] Enable logging and monitoring
- [ ] Regular security updates
- [ ] Backup database regularly

## Monitoring

### Recommended Tools

- **Logging**: Papertrail, Loggly
- **Monitoring**: New Relic, Datadog
- **Error Tracking**: Sentry
- **Uptime**: UptimeRobot, Pingdom

### Health Checks

Set up health check endpoints:
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

## Scaling

### Horizontal Scaling

1. Deploy multiple instances behind load balancer
2. Use MongoDB replica set
3. Implement Redis for session management

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Optimize database queries
3. Add database indexes

## Backup Strategy

1. **Automated Backups**: Enable MongoDB Atlas automated backups
2. **Manual Backups**: 
```bash
mongodump --uri="mongodb://your-connection-string"
```
3. **Backup Schedule**: Daily at 2 AM UTC
4. **Retention**: Keep 30 days of backups

## Rollback Plan

1. Keep previous deployment version
2. Use blue-green deployment
3. Database migrations should be reversible
4. Test rollback procedure regularly