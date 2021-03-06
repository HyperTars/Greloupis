[![logo](documents/greloupis-horizontal.png)](https://greloupis-frontend.herokuapp.com/)

# Greloupis - An online video sharing platform

- Main Tech Stack & Compatibility

    [![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://www.python.org/downloads/release/python-385/)
    [![npm](https://img.shields.io/badge/npm-6.14.8-blue)](https://blog.npmjs.org/post/626732790304686080/release-6148)
    [![node.js](https://img.shields.io/badge/node.js-14.15.0-blue)](https://nodejs.org/dist/latest-v14.x/docs/api/)
    [![Flask](https://img.shields.io/badge/Flask-1.1.2-blue)](https://pypi.org/project/Flask/)
    [![React](https://img.shields.io/badge/React-17.0.1-blue)](https://reactjs.org/versions)
    [![MongoDB](https://img.shields.io/badge/MongoDB-4.4-blue)](https://docs.mongodb.com/manual/release-notes/4.4/)

- Continuous Integration

    [![CI/CD](https://github.com/HyperTars/Greloupis/workflows/CI/CD/badge.svg)](https://github.com/HyperTars/Greloupis/actions?query=workflow%3ACI%2FCD)
    [![CodeCov Status](https://codecov.io/gh/HyperTars/Greloupis/branch/master/graph/badge.svg?token=8K7ODQK5BV)](https://codecov.io/gh/HyperTars/Greloupis)
    [![Coverage Status](https://coveralls.io/repos/github/HyperTars/Greloupis/badge.svg?branch=master)](https://coveralls.io/github/HyperTars/Greloupis?branch=master)
    
- Continuous Delivery & Deploy (Frontend)

    [![docker status](https://img.shields.io/docker/cloud/build/hypertars/greloupis-frontend)](https://hub.docker.com/r/hypertars/greloupis-frontend)
    [![docker image size](https://img.shields.io/docker/image-size/hypertars/greloupis-frontend)](https://hub.docker.com/r/hypertars/greloupis-frontend/tags)
    [![docker build](https://img.shields.io/docker/cloud/automated/hypertars/greloupis-frontend)](https://hub.docker.com/r/hypertars/greloupis-frontend/builds)
    [![Heroku](https://pyheroku-badge.herokuapp.com/?app=greloupis-frontend&style=flat)](https://greloupis-frontend.herokuapp.com/)

- Continuous Delivery & Deploy (Backend)

    [![docker status](https://img.shields.io/docker/cloud/build/hypertars/greloupis-backend)](https://hub.docker.com/r/hypertars/greloupis-backend)
    [![docker image size](https://img.shields.io/docker/image-size/hypertars/greloupis-backend)](https://hub.docker.com/r/hypertars/greloupis-backend/tags)
    [![docker build](https://img.shields.io/docker/cloud/automated/hypertars/greloupis-backend)](https://hub.docker.com/r/hypertars/greloupis-backend/builds)
    [![Heroku](https://pyheroku-badge.herokuapp.com/?app=greloupis-backend&style=flat)](https://greloupis-backend.herokuapp.com/)

- Git Statistics

    [![size](https://img.shields.io/github/languages/code-size/hypertars/greloupis?style=plasticr)](https://github.com/HyperTars/Greloupis)
    [![commit activity](https://img.shields.io/github/commit-activity/y/hypertars/greloupis?style=plasticr)](https://github.com/HyperTars/Greloupis/commits/master)
    [![last commit](https://img.shields.io/github/last-commit/HyperTars/Greloupis.svg?style=plasticr)](https://github.com/HyperTars/Greloupis/commits/master)
    

- Websites and Metrics Monitors
    - Our [Heroku Frontend Site](https://greloupis-frontend.herokuapp.com/) | [Heroku Backend Site](https://greloupis-backend.herokuapp.com/)
    - Our [Heroku Frontend Metrics Monitor](https://metrics.librato.com/s/public/wxet4vyas) | [Heroku Backend Metrics Monitor](https://metrics.librato.com/s/public/reo8fj68x)

## Table of Content
- [Greloupis - An online video sharing platform](#greloupis---an-online-video-sharing-platform)
  - [Table of Content](#table-of-content)
  - [Documents](#documents)
    - [Project Proposal](#project-proposal)
    - [Frontend Details](#frontend-details)
    - [Backend Details](#backend-details)
    - [Transcoder Details](#transcoder-details)
    - [CI / CD Workflow](#ci--cd-workflow)
    - [Environment Settings](#environment-settings)
  - [Setup Guide](#setup-guide)
      - [Environment Requirement](#environment-requirement)
      - [Install Dependencies](#install-dependencies)
      - [Run Test](#run-test)
      - [Make Prod](#make-prod)
      - [Run](#run)
  - [Designs](#designs)
    - [APIs](#apis)
    - [Architecture](#architecture)
  - [CI / CD](#ci--cd)
  - [Contributors](#contributors)

## Documents
### [Project Proposal](documents/Proposal.md)
### [Frontend Details](frontend/readme.md)
### [Backend Details](backend/readme.md)
### [Transcoder Details](transcoder/readme.md)
### [CI / CD Workflow](documents/cicd.md)
### [Environment Settings](documents/EnvironmentSettings.md)

## Setup Guide

#### Environment Requirement
- Python 3.7 / 3.8 **(3.6 or below and 3.9 are not supported)**
- npm (6.14.8)
- node.js (14.15.0)
- [Environment Variables](documents/EnvironmentSettings.md)
- Make sure MongoDB & AWS Endpoints are all set, see more details in [Backend Setup Guide](backend/readme.md#Environment-Requirement-And-Configs)
- Avatar and Thumbnail images requires you to configure AWS S3 Service, see more details in [Frontend Setup Guide](frontend/readme.md#Environment-Requirement)
- Video upload and streaming requires you to configure AWS Transcoding Service, see more details in [Transcoder Setup Guide](transcoder/readme.md)

#### Install Dependencies
- To install dependencies, run
```bash
make dev_env
```

#### Run Test
- To run test, run
```bash
make tests
```

#### Make Prod
- To make prod, run
```bash
make prod
```

#### Run
- To run both frontend(http://localhost:3000) and backend (http://localhost:5000) locally
    - Start (build from [docker-compose.yml](docker-compose.yml))
        ```bash
        make docker_build
        ```
    - Run
        ```bash
        make docker_run
        ```
- Or you can access our [website deployed on Heroku](https://greloupis-frontend.herokuapp.com/)
- To test our project, you can try to register or log in with existed user for testing
    - For existed users, you can [search their username](https://greloupis-frontend.herokuapp.com/search?keyword=)
    - User accounts for testing
        - Username: hypertars, Password: hypertars
        - Username: milvus, Password: milvus
        - Username: eclipse, Password: eclipse

## Designs

### APIs
- See full [APIs Design](documents/APIs.md)
- Or you can access our [backend Swagger UI website](https://greloupis-backend.herokuapp.com/)

### Architecture
    
![Architecture Design Diagram](documents/images/GreloupisArchitecture-2.svg)

### [Frontend](frontend/readme.md)

### [Backend](backend/readme.md)

### [Transcoder](transcoder/readme.md)

## CI / CD
- We use `GitHub Action`, `Docker` and `Heroku` to do CI/CD works
  - Full [Test Cases](documents/Test.md)
  - Coverage (test results) [CodeCov](https://codecov.io/gh/HyperTars/Greloupis) | [Coverall](https://coveralls.io/github/HyperTars/Greloupis)
  - [GitHub Action Conf](.github/workflows/cicd.yml) | [Github Action Status](https://github.com/HyperTars/Greloupis/actions?query=workflow%3ACI%2FCD)
  - [Docker Conf](docker-compose.yml) | [Docker Frontend Repo](https://hub.docker.com/r/hypertars/greloupis-frontend/tags) | [Docker Backend Repo](https://hub.docker.com/r/hypertars/greloupis-backend/tags)
  - [Heroku Frontend](https://greloupis-frontend.herokuapp.com/) | [Heroku Backend](https://greloupis-backend.herokuapp.com/)
  - [Heroku Frontend Metrics Monitor](https://metrics.librato.com/s/public/wxet4vyas) | [Heroku Backend Metrics Monitor](https://metrics.librato.com/s/public/reo8fj68x)
- See more details about our [CI / CD Workflow](documents/cicd.md)

## Contributors
  
  GitHub | Name | NetID
  --- | --- | ---
  [HyperTars](https://github.com/HyperTars) | Wenzhou Li | [wl2154](mailto:wl2154@nyu.edu)
  [MikeYan01](https://github.com/MikeYan01) | Linyi Yan | [ly1333](mailto:ly1333@nyu.edu)
  [FatBin](https://github.com/FatBin) | Xuanbin Luo | [xl2806](mailto:xl2806@nyu.edu)
