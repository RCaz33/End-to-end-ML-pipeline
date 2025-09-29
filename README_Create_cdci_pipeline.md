# CI/CD Pipeline Setup

1. Create GitHub Workflow
Create `.github/workflows/deploy_heroku.yml`:

```yaml
paths:
    - 'src/models'
```
so it triggers only when new models are set for Baseline/Challenger

2. Add GitHub Secrets
Go to repo Settings → Secrets → Actions:
- `DOCKER_USER`: Your Docker Hub username
- `DOCKER_PASS`: Your Docker Hub password/token
- `HEROKU_API_KEY`: Heroku Dashboard → Account Settings → API Key → Reveal
- `HEROKU_APP_NAME`: The name given to the app to Heroku
- `DOCKER_USER`: DockerHub username @ https://hub.docker.com


3. Trigger
Push to `main` branch → Auto build & deploy