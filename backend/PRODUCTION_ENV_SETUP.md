# Production Environment Configuration Guide

This guide explains how to set up environment variables for production deployment of the Green Coding Advisor.

## Quick Start

1. **Copy the example file:**
   ```bash
   cd backend
   cp env.example .env
   ```

2. **Edit `.env` with your production values**

3. **Validate your configuration:**
   ```bash
   python validate_env.py
   ```

## Required Environment Variables

### MongoDB Configuration (REQUIRED)

```env
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGODB_DB=green_coding
```

**How to get MongoDB Atlas connection string:**
1. Log in to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Go to your cluster → "Connect"
3. Choose "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your database user password
6. Replace `<dbname>` if needed (or add it to the connection string)

### JWT Configuration (REQUIRED)

```env
SECRET_KEY=your-super-secret-key-change-in-production-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Generate a secure secret key:**
```bash
# Using OpenSSL
openssl rand -hex 32

# Using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Environment Settings (REQUIRED)

```env
ENVIRONMENT=production
DEBUG=False
```

**Important:** Always set `DEBUG=False` in production for security.

### CORS Configuration (REQUIRED)

```env
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Important:** 
- Remove `localhost` URLs in production
- Use HTTPS URLs only
- Separate multiple origins with commas

## Optional Environment Variables

### Email Configuration

Required for email verification and password reset features:

```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_TLS=True
MAIL_SSL=False
```

**Gmail Setup:**
1. Enable 2-factor authentication
2. Generate an "App Password" in your Google Account settings
3. Use the app password as `MAIL_PASSWORD`

### Redis Configuration

For caching and background task processing:

```env
REDIS_URL=redis://:password@host:port
```

**Redis Cloud Setup:**
1. Sign up at [Redis Cloud](https://redis.com/try-free/)
2. Create a database
3. Copy the connection URL

### Monitoring (Sentry)

For error tracking and monitoring:

```env
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

**Sentry Setup:**
1. Sign up at [Sentry.io](https://sentry.io)
2. Create a new project
3. Copy the DSN

### Carbon Tracking API

For real-time carbon intensity data:

```env
ELECTRICITY_MAPS_API_KEY=your-electricity-maps-api-key
CODECARBON_REGION=usa
CODECARBON_OFFLINE=True
```

**Electricity Maps Setup:**
1. Sign up at [Electricity Maps](https://www.electricitymaps.com/)
2. Get your API key from the dashboard

## Security Best Practices

### 1. Never Commit `.env` Files

Ensure `.env` is in `.gitignore`:
```gitignore
.env
.env.local
.env.*.local
```

### 2. Use Strong Secrets

- **SECRET_KEY**: Minimum 32 characters, use cryptographically secure random generation
- **Database passwords**: Use strong, unique passwords
- **API keys**: Store securely, rotate regularly

### 3. Environment-Specific Files

- **Development**: `.env` (local development)
- **Staging**: `.env.staging` (if using staging environment)
- **Production**: Use environment variables or secrets management service

### 4. Secrets Management Services

For production, consider using:
- **AWS Secrets Manager**
- **Azure Key Vault**
- **HashiCorp Vault**
- **Docker Secrets**
- **Kubernetes Secrets**

## Validation

Run the validation script before deploying:

```bash
python validate_env.py
```

This will check:
- ✅ Required variables are set
- ✅ Production values are not using defaults
- ✅ Secret keys meet minimum length requirements
- ✅ CORS origins don't include localhost in production
- ✅ Debug mode is disabled in production

## Docker Deployment

When using Docker, pass environment variables:

```bash
docker run -e MONGODB_URI="..." -e SECRET_KEY="..." ...
```

Or use a `.env` file with `docker-compose`:
```yaml
services:
  backend:
    env_file:
      - .env
```

## Cloud Platform Setup

### AWS (EC2/Elastic Beanstalk)

1. Use **AWS Systems Manager Parameter Store** or **Secrets Manager**
2. Set environment variables in Elastic Beanstalk console
3. Or use `.ebextensions` configuration files

### Heroku

```bash
heroku config:set MONGODB_URI="..."
heroku config:set SECRET_KEY="..."
```

### Railway/Render/Fly.io

Set environment variables in the platform dashboard or CLI.

## Troubleshooting

### "MONGODB_URI must be set" Error

- Ensure `.env` file exists in the `backend` directory
- Check that `MONGODB_URI` is set (not empty)
- Verify the connection string format

### "SECRET_KEY must be changed" Error

- Generate a new secret key (see above)
- Update `.env` file
- Restart the application

### CORS Errors in Production

- Verify `ALLOWED_ORIGINS` includes your frontend domain
- Ensure URLs use HTTPS (not HTTP)
- Check that there are no trailing slashes

### Connection Issues

- Verify MongoDB Atlas network access allows your server IP
- Check firewall rules
- Ensure credentials are correct

## Example Production `.env`

```env
# MongoDB
MONGODB_URI=mongodb+srv://prod_user:SecurePassword123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=green_coding_prod

# JWT
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=production
DEBUG=False

# CORS
ALLOWED_ORIGINS=https://green-coding-advisor.com,https://www.green-coding-advisor.com

# Email
MAIL_USERNAME=noreply@green-coding-advisor.com
MAIL_PASSWORD=app_password_here
MAIL_FROM=noreply@green-coding-advisor.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

# Redis
REDIS_URL=redis://:password@redis-host:6379/0

# Monitoring
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
```

## Next Steps

After configuring environment variables:

1. ✅ Run `python validate_env.py` to verify configuration
2. ✅ Test locally with production-like settings
3. ✅ Deploy to staging environment first
4. ✅ Monitor logs for any configuration issues
5. ✅ Set up monitoring and alerting

## Support

For issues or questions:
- Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Review application logs
- Validate configuration with `validate_env.py`

