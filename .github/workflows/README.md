# GitHub Actions CI/CD Workflows

This directory contains GitHub Actions workflows for automated testing, code quality checks, and deployment.

## Workflows

### 1. CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**Jobs:**
- **Backend Tests**: Runs pytest with MongoDB test database
- **Backend Linting**: Runs pylint and radon for code quality
- **Frontend Tests**: Runs Vitest unit tests
- **Frontend Build**: Verifies production build succeeds
- **Frontend E2E**: Runs Playwright end-to-end tests
- **Docker Build**: Builds and validates Docker images
- **All Checks Summary**: Aggregates results from all jobs

**Status Badge:**
```markdown
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI%20Pipeline/badge.svg)
```

### 2. Deploy (`deploy.yml`)

**Triggers:**
- Push to `main` branch (staging)
- Tags starting with `v*` (production)
- Manual workflow dispatch

**Environments:**
- **Staging**: Automatic on push to `main`
- **Production**: On version tags or manual trigger

**Required Secrets:**
- `PROD_MONGODB_URI`: Production MongoDB connection string
- `PROD_MONGODB_DB`: Production database name
- `PROD_SECRET_KEY`: Production JWT secret key
- `PROD_ALLOWED_ORIGINS`: Production CORS origins
- `PROD_API_URL`: Production API URL for frontend build
- `STAGING_API_URL`: Staging API URL for frontend build

### 3. Code Quality (`code-quality.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests
- Weekly schedule (Mondays at 9 AM UTC)

**Checks:**
- **Backend**: pylint, radon (complexity), bandit (security), safety (vulnerabilities)
- **Frontend**: ESLint (if configured), TypeScript type checking, outdated dependencies

### 4. Dependabot Auto-merge (`dependabot.yml`)

Automatically merges Dependabot PRs after CI passes.

## Setup Instructions

### 1. Configure GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions, and add:

**Required for Production Deployment:**
```
PROD_MONGODB_URI
PROD_MONGODB_DB
PROD_SECRET_KEY
PROD_ALLOWED_ORIGINS
PROD_API_URL
STAGING_API_URL
```

**Optional:**
```
SENTRY_DSN
ELECTRICITY_MAPS_API_KEY
```

### 2. Configure Environments

Go to Settings → Environments and create:
- **staging**: For staging deployments
- **production**: For production deployments (add protection rules)

### 3. Enable Dependabot

Dependabot is configured via `.github/dependabot.yml`. It will:
- Check for updates weekly
- Create PRs automatically
- Auto-merge after CI passes (if enabled)

### 4. Test the Workflows

1. **Test CI Pipeline:**
   ```bash
   git checkout -b test-ci
   git commit --allow-empty -m "test: trigger CI"
   git push origin test-ci
   ```

2. **Test Deployment:**
   - Create a tag: `git tag v1.0.0`
   - Push tag: `git push origin v1.0.0`
   - Or use manual workflow dispatch in GitHub UI

## Workflow Status

View workflow runs at:
`https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

## Troubleshooting

### Backend Tests Failing

- Check MongoDB service is running in CI
- Verify test database name matches `MONGODB_DB` env var
- Check test environment variables are set correctly

### Frontend E2E Tests Failing

- Ensure backend server starts before E2E tests
- Check `VITE_API_BASE_URL` is set correctly
- Verify Playwright browsers are installed

### Docker Build Failing

- Check Dockerfile syntax
- Verify all dependencies are in requirements.txt/package.json
- Check for missing build context files

### Deployment Failing

- Verify all required secrets are set
- Check environment protection rules
- Validate production environment configuration

## Customization

### Adding New Jobs

1. Add job to `ci.yml`:
```yaml
new-job:
  name: New Job
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    # ... your steps
```

2. Add to `all-checks` job dependencies:
```yaml
needs: [backend-tests, ..., new-job]
```

### Changing Schedules

Edit the `schedule` section in workflow files:
```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
```

### Adding Deployment Targets

Edit `deploy.yml` to add new deployment steps:
```yaml
- name: Deploy to AWS
  run: |
    aws ecs update-service ...
```

## Best Practices

1. **Never commit secrets** - Use GitHub Secrets
2. **Use environment protection** - Require approvals for production
3. **Test locally first** - Run tests before pushing
4. **Monitor workflows** - Set up notifications for failures
5. **Keep workflows updated** - Update action versions regularly

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Docker Buildx](https://docs.docker.com/buildx/)
- [Playwright CI](https://playwright.dev/docs/ci)

