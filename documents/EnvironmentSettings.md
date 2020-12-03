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

## Local Running Environment Variables
### Frontend Environment Variables

#### React

#### Dockerfile

#### Makefile
- You can run and test frontend only.

### Backend Environment Variables

#### Python Flask

#### Dockerfile

#### Makefile
- You can run and test backend only.

### Docker-Compose Environment Variables
- With docker-compose, you can run both frontend and backend in one terminal with one command.

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
#### Heroku Frontend
- ACCESS_KEY_ID1
- ACCESS_KEY_ID2
- SECRET_KEY1
- SECRET_KEY2

#### Heroku Backend
- AWS_AUTH_KEY