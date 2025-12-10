# CI/CD Pipeline Setup Guide

This guide explains how to set up and use the GitHub Actions CI/CD pipeline for the Green Coding Advisor project.

## Overview

The CI/CD pipeline includes:
- ✅ Automated testing (backend unit/integration, frontend unit/E2E)
- ✅ Code quality checks (linting, security scanning)
- ✅ Docker image building
- ✅ Automated deployment (staging & production)
- ✅ Dependabot integration for dependency updates

## Quick Start

### 1. Push to GitHub

The workflows will automatically run on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Version tags (for production deployment)

### 2. Configure Secrets

Go to your repository → **Settings** → **Secrets and variables** → **Actions**

Add the following secrets for production deployment:

```
PROD_MONGODB_URI=mongodb+srv://...
PROD_MONGODB_DB=green_coding_prod
PROD_SECRET_KEY=<generate-strong-secret>
PROD_ALLOWED_ORIGINS=https://yourdomain.com
PROD_API_URL=https://api.yourdomain.com
STAGING_API_URL=https://staging-api.yourdomain.com
```

### 3. Set Up Environments

Go to **Settings** → **Environments** and create:

- **staging**: For staging deployments
- **production**: For production deployments (add protection rules)

## Workflows

### CI Pipeline (`ci.yml`)

Runs on every push and PR. Includes:

1. **Backend Tests**
   - Unit and integration tests with MongoDB
   - Environment validation

2. **Backend Linting**
   - Pylint code quality checks
   - Radon complexity analysis

3. **Frontend Tests**
   - Vitest unit tests
   - Test coverage reporting

4. **Frontend Build**
   - Production build verification
   - Build artifact upload

5. **Frontend E2E**
   - Playwright end-to-end tests
   - Requires backend server running

6. **Docker Build**
   - Backend and frontend image builds
   - Build cache optimization

### Deploy (`deploy.yml`)

**Staging Deployment:**
- Triggers: Push to `main` branch
- Builds and pushes Docker images
- Tags: `main`, `staging-<sha>`, `latest`

**Production Deployment:**
- Triggers: Version tags (`v*`) or manual dispatch
- Validates production environment
- Builds and pushes Docker images
- Tags: Semantic version tags (`v1.0.0`, `v1.0`, `v1`, `latest`)

### Code Quality (`code-quality.yml`)

Runs weekly and on PRs. Includes:

- **Backend**: pylint, radon, bandit (security), safety (vulnerabilities)
- **Frontend**: ESLint, TypeScript checks, dependency updates

### Dependabot (`dependabot.yml`)

Automatically:
- Checks for dependency updates weekly
- Creates PRs for updates
- Auto-merges after CI passes (optional)

## Testing Locally

Before pushing, test workflows locally:

### Backend Tests
```bash
cd backend
python -m pip install -r requirements.txt
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm ci
npm test
npm run test:e2e
```

### Docker Builds
```bash
# Backend
docker build -t backend-test ./backend

# Frontend
docker build -t frontend-test ./frontend
```

## Deployment Process

### Staging Deployment

1. **Automatic**: Push to `main` branch
   ```bash
   git checkout main
   git push origin main
   ```

2. **Monitor**: Check Actions tab for deployment status

### Production Deployment

**Option 1: Version Tag**
```bash
git tag v1.0.0
git push origin v1.0.0
```

**Option 2: Manual Dispatch**
1. Go to **Actions** → **Deploy** → **Run workflow**
2. Select `production` environment
3. Click **Run workflow**

## Monitoring

### View Workflow Runs

Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

### Status Badges

Add to your README:

```markdown
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI%20Pipeline/badge.svg)
![Deploy](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Deploy/badge.svg)
```

### Notifications

Configure notifications in GitHub:
- **Settings** → **Notifications** → **Actions**

## Troubleshooting

### Backend Tests Failing

**Issue**: MongoDB connection errors
- **Solution**: Check MongoDB service is running in CI
- Verify `MONGODB_URI` environment variable

**Issue**: Import errors
- **Solution**: Ensure all dependencies in `requirements.txt`
- Check Python version matches (`3.11`)

### Frontend E2E Tests Failing

**Issue**: Backend not starting
- **Solution**: Check backend logs in CI output
- Verify MongoDB is accessible
- Increase wait time if needed

**Issue**: Timeout errors
- **Solution**: Increase timeout in Playwright config
- Check network connectivity

### Docker Build Failing

**Issue**: Build context errors
- **Solution**: Verify Dockerfile paths are correct
- Check all required files are in context

**Issue**: Dependency installation fails
- **Solution**: Check `requirements.txt`/`package.json` syntax
- Verify all dependencies are available

### Deployment Failing

**Issue**: Missing secrets
- **Solution**: Add all required secrets in repository settings
- Verify secret names match workflow file

**Issue**: Environment protection
- **Solution**: Approve deployment in Environments tab
- Check protection rules

## Customization

### Adding New Tests

1. Add test file to `backend/tests/` or `frontend/src/components/__tests__/`
2. Tests will run automatically in CI

### Adding New Jobs

Edit `.github/workflows/ci.yml`:

```yaml
new-job:
  name: New Job
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    # ... your steps
```

### Changing Schedules

Edit `schedule` in workflow files:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
```

## Best Practices

1. **Test Locally First**: Run tests before pushing
2. **Small PRs**: Keep changes focused and testable
3. **Monitor Workflows**: Set up notifications for failures
4. **Review Dependabot PRs**: Don't auto-merge critical updates
5. **Use Environments**: Protect production with approval rules
6. **Version Tags**: Use semantic versioning (`v1.0.0`)

## Security

- ✅ Never commit secrets to repository
- ✅ Use GitHub Secrets for sensitive data
- ✅ Enable branch protection rules
- ✅ Require reviews for production deployments
- ✅ Regularly update dependencies
- ✅ Monitor security alerts

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)
- [Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)

## Support

For issues or questions:
- Check workflow logs in Actions tab
- Review [TROUBLESHOOTING.md](backend/TROUBLESHOOTING.md)
- Check [CI/CD README](.github/workflows/README.md)

