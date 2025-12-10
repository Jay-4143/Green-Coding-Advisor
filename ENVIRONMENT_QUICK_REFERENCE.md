# Environment Configuration Quick Reference

## Backend Setup

### 1. Create `.env` file
```bash
cd backend
cp env.example .env
```

### 2. Required Variables (Minimum)
```env
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=green_coding
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ENVIRONMENT=production
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
```

### 3. Validate Configuration
```bash
python validate_env.py
```

## Frontend Setup

### 1. Create `.env` file
```bash
cd frontend
# Create .env file manually
```

### 2. Required Variable
```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

### 3. Build
```bash
npm run build
```

## Generate Secret Key

```bash
# Using OpenSSL
openssl rand -hex 32

# Using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

## Common Commands

### Validate Backend Config
```bash
cd backend
python validate_env.py
```

### Check Environment Variables
```bash
# Backend
cd backend
cat .env

# Frontend
cd frontend
cat .env
```

## Production Checklist

- [ ] MongoDB Atlas connection string configured
- [ ] Strong SECRET_KEY generated (32+ characters)
- [ ] ENVIRONMENT=production
- [ ] DEBUG=False
- [ ] ALLOWED_ORIGINS set to production domain(s)
- [ ] Frontend VITE_API_BASE_URL points to production API
- [ ] Validation script passes: `python validate_env.py`
- [ ] `.env` files are in `.gitignore`
- [ ] Secrets are stored securely (not in code)

## Documentation

- **Backend**: See [backend/PRODUCTION_ENV_SETUP.md](backend/PRODUCTION_ENV_SETUP.md)
- **Frontend**: See [frontend/ENV_SETUP.md](frontend/ENV_SETUP.md)

