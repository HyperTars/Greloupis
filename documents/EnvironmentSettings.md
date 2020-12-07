# Greloupis - Environment Settings

- We have lots of environment variables used in our project, which you should set before running.
- You can set by using [Environment Variable Checklist](../environ.sh)

## Table of Content
- [Greloupis - Envoronment Settings](#Greloupis---Environment-Settings)
  - [Table of Content](#table-of-content)
  - [Essential Dependencies](#Essential-Dependencies)
  - [Local Running Environment Variables](#CI--CD-Workflow-Environment-Variables)
  - [CI/CD Workflow Environment Vairables](#GitHub-Action-Secrets-(CI))

## Essential Dependencies
- Frontend: npm 14.15.0
- Backend: python 3.7 | python 3.8

- Docker-compose & docker.sh (run both frontend and backend in one terminal with one command)
  - AWS_AUTH_KEY
  - ACCESS_KEY_ID1
  - ACCESS_KEY_ID2
  - SECRET_KEY1
  - SECRET_KEY2

## Local Running Environment Variables
### Frontend Environment Variables
- React
  - ACCESS_KEY_ID1
  - ACCESS_KEY_ID2
  - SECRET_KEY1
  - SECRET_KEY2
  - PROFILE
  - [Backend and S3 Endpoints](../frontend/src/components/Endpoint.js)

- Dockerfile
  - ACCESS_KEY_ID1
  - ACCESS_KEY_ID2
  - SECRET_KEY1
  - SECRET_KEY2

- Makefile: You can run and test frontend separately.
  - ACCESS_KEY_ID1
  - ACCESS_KEY_ID2
  - SECRET_KEY1
  - SECRET_KEY2
  - FRONTEND_BUILD
  - FRONTEND_REPO
  - TAG
  - HEROKU_APP_FRONTEND

### Backend Environment Variables

- Python Flask
  - AWS_AUTH_KEY
  - PROFILE
  - [MongoDB Endpoint](../backend/configs/config_dev.py)
  - [AWS CloudFront & S3 Endpoints](../backend/configs/config_base.py)

- Makefile: You can run and test backend separately.
  - CODECOV_TOKEN
  - DOCKER_USER
  - DOCKER_PASS
  - BACKEND_BUILD
  - BACKEND_REPO
  - TAG
  - HEROKU_APP_BACKEND

## CI / CD Workflow Environment Variables

### GitHub Action Secrets (CI)
[GitHub Action Settings](../.github/workflows/cicd.yml)

#### Coverage Service
- COVERALLS_REPO_TOKEN
- CODECOV_TOKEN
#### Docker
- DOCKER_USER
- DOCKER_EMAIL
- DOCKER_PASS
#### Test And Build
- AWS_AUTH_KEY
- ACCESS_KEY_ID1
- ACCESS_KEY_ID2
- SECRET_KEY1
- SECRET_KEY2
#### Deploy
- HEROKU_EMAIL
- HEROKU_API_KEY

### Heroku
#### Heroku Frontend App
- ACCESS_KEY_ID1
- ACCESS_KEY_ID2
- SECRET_KEY1
- SECRET_KEY2

#### Heroku Backend App
- AWS_AUTH_KEY