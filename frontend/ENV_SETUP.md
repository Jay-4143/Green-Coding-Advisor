# Frontend Environment Configuration

This guide explains how to configure environment variables for the Green Coding Advisor frontend.

## Quick Start

1. **Create `.env` file in the `frontend` directory:**
   ```bash
   cd frontend
   touch .env
   ```

2. **Add your configuration:**
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

3. **Restart the development server**

## Environment Variables

### VITE_API_BASE_URL (REQUIRED)

The base URL for the backend API.

**Development:**
```env
VITE_API_BASE_URL=http://localhost:8000
```

**Production:**
```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

**Note:** In Vite, environment variables must be prefixed with `VITE_` to be exposed to the client-side code.

## Usage in Code

Environment variables are accessed via `import.meta.env`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
```

## Build-Time Configuration

Environment variables are embedded at **build time**, not runtime. This means:

1. Set environment variables before running `npm run build`
2. Different builds require different `.env` files or build commands
3. For production, use `.env.production` or set variables in your CI/CD pipeline

## Production Build

### Option 1: Using .env.production

Create `frontend/.env.production`:
```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

Build:
```bash
npm run build
```

### Option 2: Using Environment Variables

```bash
VITE_API_BASE_URL=https://api.yourdomain.com npm run build
```

### Option 3: Using CI/CD Variables

Set `VITE_API_BASE_URL` in your CI/CD platform (GitHub Actions, GitLab CI, etc.) and it will be available during build.

## Docker Deployment

When using Docker, pass environment variables:

```dockerfile
ENV VITE_API_BASE_URL=https://api.yourdomain.com
```

Or use build args:
```dockerfile
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
```

Build:
```bash
docker build --build-arg VITE_API_BASE_URL=https://api.yourdomain.com .
```

## Security Notes

⚠️ **Important:** All `VITE_` prefixed variables are exposed to the client-side code. 

- ✅ Safe to expose: API URLs, feature flags, public configuration
- ❌ Never expose: API keys, secrets, private tokens

For sensitive data, always use the backend API as a proxy.

## Troubleshooting

### "API_BASE_URL is undefined"

- Ensure variable is prefixed with `VITE_`
- Restart the development server after changing `.env`
- Check that `.env` file is in the `frontend` directory

### CORS Errors

- Verify `VITE_API_BASE_URL` matches your backend CORS configuration
- Check that backend `ALLOWED_ORIGINS` includes your frontend URL

### Build Issues

- Clear build cache: `rm -rf node_modules/.vite`
- Ensure environment variables are set before build
- Check build logs for variable substitution

## Example Configurations

### Development
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Staging
```env
VITE_API_BASE_URL=https://api-staging.yourdomain.com
```

### Production
```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

## Next Steps

After configuring:

1. ✅ Test API connection in development
2. ✅ Verify CORS configuration matches
3. ✅ Build and test production build locally
4. ✅ Deploy with correct environment variables

