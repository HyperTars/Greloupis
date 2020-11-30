[![logo](../documents/greloupis-horizontal.png)](https://greloupis-frontend.herokuapp.com/)

# Greloupis Backend

- Tech Stack & Compatibility

    [![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://www.python.org/downloads/release/python-385/)
    [![Flask](https://img.shields.io/badge/Flask-1.1.2-blue)](https://pypi.org/project/Flask/)
    [![Flask-RestX](https://img.shields.io/badge/Flask_RestX-0.2.0-blue)](https://flask-restx.readthedocs.io/en/latest/)
    [![Flask-MongoEngine](https://img.shields.io/badge/Flask_MongoEngine-0.9.5-blue)](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/)
    [![Flask-CORS](https://img.shields.io/badge/Flask_CORS-3.0.9-blue)](https://flask-cors.readthedocs.io/en/latest/)
    [![Flask-JWT](https://img.shields.io/badge/Flask_JWT_Extended-3.24.1-blue)](https://flask-jwt-extended.readthedocs.io/en/stable/)
    [![MongoDB](https://img.shields.io/badge/MongoDB-4.4-blue)](https://docs.mongodb.com/manual/release-notes/4.4/)
    [![uWSGI](https://img.shields.io/badge/uWSGI-2.0.19-blue)](https://uwsgi-docs.readthedocs.io/en/latest/)
    [![Flake8](https://img.shields.io/badge/Flake8-3.8.4-blue)](https://flake8.pycqa.org/en/latest/)
    [![PyTest](https://img.shields.io/badge/PyTest-6.1.1-blue)](https://docs.pytest.org/en/stable/announce/release-6.1.1.html)
    [![Coverage](https://img.shields.io/badge/Coverage-5.3-blue)](https://coverage.readthedocs.io/en/coverage-5.3/)
    [![CodeCov](https://img.shields.io/badge/CodeCov-2.1.10-blue)](https://pypi.org/project/codecov/2.1.10/)
    [![PyYAML](https://img.shields.io/badge/PyYAML-5.3.1-blue)](https://pypi.org/project/PyYAML/)
    [![DNSPython](https://img.shields.io/badge/DNS_Python-2.0.0-blue)](https://www.dnspython.org/)

- CI / CD

    <!--[![build](https://travis-ci.com/HyperTars/Online-Video-Platform.svg?token=btA3ungCKHqWzLxCoxT7&branch=master)](https://travis-ci.com/HyperTars/Online-Video-Platform)-->
    [![CI/CD](https://github.com/HyperTars/Online-Video-Platform/workflows/CI/CD/badge.svg)](https://github.com/HyperTars/Online-Video-Platform/actions?query=workflow%3ACI%2FCD)
    [![CodeCov Status](https://codecov.io/gh/HyperTars/Online-Video-Platform/branch/master/graph/badge.svg?token=8K7ODQK5BV)](https://codecov.io/gh/HyperTars/Online-Video-Platform)
    [![Coveralls Status](https://coveralls.io/repos/github/HyperTars/Online-Video-Platform/badge.svg?t=dyCGTT)](https://coveralls.io/github/HyperTars/Online-Video-Platform)
    [![docker status](https://img.shields.io/docker/cloud/build/hypertars/greloupis-backend)](https://hub.docker.com/r/hypertars/greloupis-backend)
    [![docker image size](https://img.shields.io/docker/image-size/hypertars/greloupis-backend)](https://hub.docker.com/r/hypertars/greloupis-backend/tags)
    [![docker build](https://img.shields.io/docker/cloud/automated/hypertars/greloupis-backend)](https://hub.docker.com/r/hypertars/greloupis-backend/builds)
    [![Heroku](https://pyheroku-badge.herokuapp.com/?app=greloupis-backend&style=flat)](https://greloupis-backend.herokuapp.com/)

- Websites and Metrics Monitors
    - [Heroku Backend Site](https://greloupis-backend.herokuapp.com/)
    - [Heroku Backend Metrics Monitor](https://metrics.librato.com/s/public/reo8fj68x)
    - [Docker Backend Repo](https://hub.docker.com/r/hypertars/greloupis-backend/tags)

## Table of Content
- [Setup Guide](#Setup-Guide)
  * [Environment Requirement & Configs](#Environment-Requirement-And-Configs)
  * [Install Dependencies](#Install-Dependencies)
  * [Run Test](#Run-Test)
  * [Run](#Run)
  * [Dockerize](#Dockerize)
  * [Deploy](#Deploy)
- [Features & Designs](#Designs)
  * [Models Design](#Models-Design)
  * [Database Design](#Database-Design)
  * [APIs Design](#APIs-Design)
  * [Components Design](#Components-Design)
  * [Web Server Design](#Web-Server-Design)
  * [Coding Style](#Coding-Style)
- [Tests](#Tests)
- [Contributors](#Contributors)

## Setup Guide

### Environment Requirement And Configs
- **Please make sure the following dependencies are installed and configured before running**
    - Python 3.7 / 3.8 **(3.6 or below and 3.9 are not supported)**
    - Set up [Environment Variable](../documents/env.sh)

- Configurations
    - If you run locally, makefile will set the PROFILE as dev, you can change it in [makefile](makefile)
    - You should configure variables like **MongoDB endpoint**, **AWS endpoint**, loggings, and other settings in [BaseConfig](configs/config_base.py), [DevConfig](configs/config_dev.py), [TestConfig](configs/config_test.py), [ProdConfig](configs/config_prod.py)
        - Note that [TestConfig](configs/config_test.py) is only used for `make tests` and Continuous Integration Test. You'd better create a independent MongoDB Table for it. For developemt use, we recommend you configure [DevConfig](configs/config_dev.py)
        - See how it is related to environment variables [Settings](settings.py)
    - Other settings like [Logging Settings](configs/logging.yml) and [uWSGI Settings](configs/uwsgi.ini)(for docker use)

### Install Dependencies
- To install dependencies, run
```bash
make dev_env_backend
```

### Run Test
- To run test, run
```bash
make tests
```

### Run
- To run backend (SwaggerUI: http://localhost:5000 or http://0.0.0.0:5000)
    - From Docker Hub 
        ```bash
        make docker_hub (including build and run)
        ```
    - From local docker build
        ```bash
        make docker_build docker_run
        ```
    - From uWSGI (use uWSGI to replace flask WSGI)
        ```bash
        make run_wsgi
        ```
    - From native python flask
        ```bash
        make run_python
        ```

### Dockerize
- This section is for you to dockerize manually. Normally, GitHub Action will do the dockerize job once master branch is updated.
- Before dockerize, make sure you've set up [environment variable](../documents/env.sh)
    - PROFILE (you can also change it in [makefile](makefile))
    - BACKEND_BUILD
    - BACKEND_REPO (you can also change it in [makefile](makefile))
- To dockerize backend, run
```bash
make docker_build docker_push
```

### Deploy
- This section is for you to deploy manually. Normally, GitHub Action will do the deploy job once master branch is updated.
- Before deploy, make sure you've set up [environment variable](../documents/env.sh)
    - PROFILE (you can also change it in [makefile](makefile))
    - BACKEND_BUILD
    - BACKEND_REPO (you can also change it in [makefile](makefile))
    - HEROKU_API_KEY
    - HEROKU_APP_NAME
- To deploy to heroku, run
```bash
make heroku
```


## Designs
### Models Design (Entity)
- See full [Models Design](../documents/Models.md)

### Database Design
- See full [Database Design](../documents/Database.md)

### APIs Design
- See full [APIs Design](../documents/APIs.md)
- Or you can access our [backend Swagger UI website](https://greloupis-backend.herokuapp.com/)
    - If you run backend locally and access http://localhost:5000, you will see the same page

### Components Design
1. Processing Queue: Each uploaded video will be pushed to a processing queue to be de-queued later for encoding, thumbnail generation, and storage.
2. Encoder: To encode each uploaded video into multiple formats.
3. Thumbnails generator: To generate a few thumbnails for each video.
4. Video and Thumbnail storage: To store video and thumbnail files in some distributed file storage.
5. User Database: To store user’s information, e.g., name, email, address, etc.
6. Video metadata storage: A metadata database to store all the information about videos like title, file path in the system, uploading user, total views, likes, dislikes, etc. It will also be used to store all the video comments.

- Background Design

    ![BackgroundDesign](../documents/BackgroundDesign.png)

### Web Server Design
- We use [uWSGI](configs/uwsgi.ini) as our frontend webserver. See how it is configured in [Dockerfile](Dockerfile)

### Coding Style
- Python: [PEP8](https://www.python.org/dev/peps/pep-0008/)

## Tests
- See full [Test Cases](../documents/Test.md)
- Coverage
  - [CodeCov](https://codecov.io/gh/HyperTars/Online-Video-Platform)

## Contributors
  
  GitHub | Name | NetID
  --- | --- | ---
  [HyperTars](https://github.com/HyperTars) | Wenzhou Li | [wl2154](mailto:wl2154@nyu.edu)
  [MikeYan01](https://github.com/MikeYan01) | Linyi Yan | [ly1333](mailto:ly1333@nyu.edu)
  [FatBin](https://github.com/FatBin) | Xuanbin Luo | [xl2806](mailto:xl2806@nyu.edu)
