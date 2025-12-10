# Green Coding Advisor - Deployment Guide

Complete guide for deploying the Green Coding Advisor to production.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [MongoDB Atlas Setup](#mongodb-atlas-setup)
3. [Environment Configuration](#environment-configuration)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Platform Deployment](#cloud-platform-deployment)
6. [SSL and Domain Setup](#ssl-and-domain-setup)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

## Pre-Deployment Checklist

- [ ] MongoDB Atlas cluster created and configured
- [ ] Environment variables set in production
- [ ] Strong secret keys generated
- [ ] Domain name registered
- [ ] SSL certificate obtained
- [ ] CI/CD pipeline configured
- [ ] Monitoring set up
- [ ] Backup strategy defined
- [ ] Security audit completed

## MongoDB Atlas Setup

### 1. Create Cluster

1. Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster (M0 free tier is fine for testing)
3. Choose your preferred region

### 2. Configure Network Access

1. Go to **Network Access**
2. Add your server IP address (or `0.0.0.0/0` for development)
3. For production, use specific IPs only

### 3. Create Database User

1. Go to **Database Access**
2. Create a new user with read/write permissions
3. Save the username and password securely

### 4. Get Connection String

1. Go to **Clusters** → **Connect**
2. Choose **Connect your application**
3. Copy the connection string
4. Replace `<password>` with your database user password

## Environment Configuration

### Backend Environment Variables

Create `backend/.env`:

```env
# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=green_coding_prod

# JWT
SECRET_KEY=<generate-strong-secret-32-chars-minimum>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=production
DEBUG=False

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email (optional)
MAIL_USERNAME=noreply@yourdomain.com
MAIL_PASSWORD=app-password
MAIL_FROM=noreply@yourdomain.com

# Monitoring (optional)
SENTRY_DSN=https://xxx@sentry.io/xxx
```

### Frontend Environment Variables

Create `frontend/.env.production`:

```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

### Validate Configuration

```bash
cd backend
python validate_env.py
```

## Docker Deployment

### Build Images

```bash
# Backend
docker build -t green-coding-backend ./backend

# Frontend
docker build -t green-coding-frontend ./frontend \
  --build-arg VITE_API_BASE_URL=https://api.yourdomain.com
```

### Run with Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    image: green-coding-backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=${MONGODB_URI}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    restart: unless-stopped

  frontend:
    image: green-coding-frontend
    ports:
      - "80:80"
    restart: unless-stopped
```

Run:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Cloud Platform Deployment

### AWS (EC2)

1. **Launch EC2 Instance:**
   - Choose Ubuntu 22.04 LTS
   - Configure security groups (ports 80, 443, 8000)
   - Create key pair

2. **SSH into Instance:**
   ```bash
   ssh -i key.pem ubuntu@your-ec2-ip
   ```

3. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   ```

4. **Deploy:**
   ```bash
   git clone https://github.com/yourusername/green-coding-advisor.git
   cd green-coding-advisor
   # Set environment variables
   docker-compose -f docker-compose.prod.yml up -d
   ```

5. **Set Up Nginx Reverse Proxy:**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:80;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Heroku

1. **Install Heroku CLI**

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create Apps:**
   ```bash
   heroku create green-coding-backend
   heroku create green-coding-frontend
   ```

4. **Set Environment Variables:**
   ```bash
   heroku config:set MONGODB_URI=... -a green-coding-backend
   heroku config:set SECRET_KEY=... -a green-coding-backend
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

### Railway

1. **Connect Repository:**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub repository

2. **Configure Services:**
   - Add backend service (Python)
   - Add frontend service (Node.js)

3. **Set Environment Variables:**
   - Add all required variables in Railway dashboard

4. **Deploy:**
   - Railway automatically deploys on push

### Render

1. **Create Services:**
   - Backend: Web Service (Python)
   - Frontend: Static Site

2. **Configure:**
   - Set build commands
   - Set start commands
   - Add environment variables

3. **Deploy:**
   - Connect GitHub repository
   - Auto-deploy on push

## SSL and Domain Setup

### Using Let's Encrypt (Certbot)

1. **Install Certbot:**
   ```bash
   sudo apt-get update
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. **Obtain Certificate:**
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. **Auto-Renewal:**
   ```bash
   sudo certbot renew --dry-run
   ```

### Using Cloudflare

1. **Add Domain to Cloudflare:**
   - Add your domain
   - Update nameservers

2. **Enable SSL:**
   - Go to SSL/TLS settings
   - Set to "Full" or "Full (strict)"

3. **Configure DNS:**
   - Add A record pointing to your server IP
   - Add CNAME for www subdomain

### Nginx Configuration with SSL

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring and Maintenance

### Health Checks

Monitor the health endpoint:
```bash
curl https://api.yourdomain.com/health
```

### Logs

**Docker:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**System:**
```bash
journalctl -u your-service -f
```

### Backups

**MongoDB Atlas:**
- Automatic backups enabled by default
- Configure backup schedule in Atlas dashboard

**Manual Backup:**
```bash
mongodump --uri="mongodb+srv://..." --out=backup/
```

### Updates

1. **Pull Latest Code:**
   ```bash
   git pull origin main
   ```

2. **Rebuild Images:**
   ```bash
   docker-compose build
   ```

3. **Restart Services:**
   ```bash
   docker-compose up -d
   ```

4. **Run Migrations:**
   ```bash
   # If needed
   python backend/migrate.py
   ```

## Troubleshooting

### Backend Won't Start

1. Check environment variables
2. Verify MongoDB connection
3. Check logs: `docker-compose logs backend`
4. Validate config: `python validate_env.py`

### Frontend Build Fails

1. Check Node.js version (18+)
2. Clear cache: `rm -rf node_modules .vite`
3. Reinstall: `npm ci`
4. Check environment variables

### Database Connection Issues

1. Verify MongoDB URI
2. Check network access in Atlas
3. Verify credentials
4. Test connection: `mongosh "your-connection-string"`

### SSL Certificate Issues

1. Verify domain ownership
2. Check DNS records
3. Ensure ports 80/443 are open
4. Review Certbot logs: `sudo certbot certificates`

### Performance Issues

1. Check MongoDB indexes
2. Monitor database queries
3. Review application logs
4. Scale resources if needed

## Security Checklist

- [ ] Strong secret keys (32+ characters)
- [ ] HTTPS enabled
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] Security headers set
- [ ] Database access restricted
- [ ] Regular security updates
- [ ] Monitoring and alerting
- [ ] Backup strategy in place

## Support

For deployment issues:
- Check [TROUBLESHOOTING.md](backend/TROUBLESHOOTING.md)
- Review application logs
- Contact support@example.com

---

**Happy Deploying! 🚀**

