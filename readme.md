# DevOps-Project
- Integration

    [![build](https://travis-ci.com/HyperTars/Online-Video-Platform.svg?token=btA3ungCKHqWzLxCoxT7&branch=master)](https://travis-ci.com/HyperTars/Online-Video-Platform)
    [![CodeCov Status](https://codecov.io/gh/HyperTars/Online-Video-Platform/branch/master/graph/badge.svg?token=8K7ODQK5BV)](https://codecov.io/gh/HyperTars/Online-Video-Platform/tree/master/source)
    [![Coverall Status](https://coveralls.io/repos/github/HyperTars/Online-Video-Platform/badge.svg?t=dyCGTT)](https://coveralls.io/github/HyperTars/Online-Video-Platform)

- Delivery (Frontend)

    [![docker status](https://img.shields.io/docker/cloud/build/hypertars/greloupis-frontend)](https://hub.docker.com/r/hypertars/greloupis-frontend)
    [![docker image size](https://img.shields.io/docker/image-size/hypertars/greloupis-frontend)](https://hub.docker.com/r/hypertars/greloupis-frontend/tags)
    [![docker build](https://img.shields.io/docker/cloud/automated/hypertars/greloupis-frontend)](https://hub.docker.com/r/hypertars/online-video-platform/greloupis-frontends)
    [![Heroku](https://pyheroku-badge.herokuapp.com/?app=greloupis-frontend&style=flat)](http://greloupis-frontend.herokuapp.com/)

- Delivery (Backend)

    [![docker status](https://img.shields.io/docker/cloud/build/hypertars/greloupis-backend)](https://hub.docker.com/r/hypertars/greloupis-backend)
    [![docker image size](https://img.shields.io/docker/image-size/hypertars/greloupis-backend)](https://hub.docker.com/r/hypertars/greloupis-backend/tags)
    [![docker build](https://img.shields.io/docker/cloud/automated/hypertars/greloupis-backend)](https://hub.docker.com/r/hypertars/greloupis-backend/builds)
    [![Heroku](https://pyheroku-badge.herokuapp.com/?app=greloupis-backend&style=flat)](http://greloupis-backend.herokuapp.com/)

- Environment Compatibility

    [![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://www.python.org/downloads/release/python-385/)
    [![npm](https://img.shields.io/badge/npm-6.14.8-blue)](https://blog.npmjs.org/post/626732790304686080/release-6148)
    [![node.js](https://img.shields.io/badge/node.js-14.15.0-blue)](https://nodejs.org/dist/latest-v14.x/docs/api/)
    [![Flask](https://img.shields.io/badge/Flask-1.1.2-blue)](https://pypi.org/project/Flask/)
    [![React](https://img.shields.io/badge/React-17.0.0-blue)](https://reactjs.org/versions)
    [![MongoDB](https://img.shields.io/badge/MongoDB-4.4-blue)](https://docs.mongodb.com/manual/release-notes/4.4/)
    [![uWSGI](https://img.shields.io/badge/uWSGI-2.0.19-blue)](https://uwsgi-docs.readthedocs.io/en/latest/)

<!-- [Video.js](https://img.shields.io/badge/Video.js-7.8.4-blue) -->
<!-- [![tested with jest](https://img.shields.io/badge/tested_with-jest-99424f.svg)](https://github.com/facebook/jest) -->
<!-- [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier) -->
<!-- [![stars](https://img.shields.io/github/stars/HyperTars/Online-Video-Platform.svg?style=plasticr)](https://github.com/HyperTars/Online-Video-Platform/stargazers) -->
<!-- [![commit activity](https://img.shields.io/github/commit-activity/y/HyperTars/Online-Video-Platform.svg?style=plasticr)](https://github.com/HyperTars/Online-Video-Platform/commits/master) -->
<!-- [![last commit](https://img.shields.io/github/last-commit/HyperTars/Online-Video-Platform.svg?style=plasticr)](https://github.com/HyperTars/Online-Video-Platform/commits/master) -->


### Project Proposal
- [Proposal](documents/Proposal.md)
  
### Setup Guide

#### Environment Requirement
- Python 3.7 / 3.8 **(3.6 or below and 3.9 are not supported)**
- npm (6.14.8)
- node.js (14.15.0)

#### Install dependencies
- To install dependencies, run
```bash
make dev_env
```

#### Run test
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
- To run both frontend(http://localhost:3000) and backend (http://localhost:5000)
    - Start (build from docker-compose.yml)
        ```bash
        make docker_build
        ```
    - Run
        ```bash
        make docker_run
        ```

- To run backend only (http://localhost:5000 or http://0.0.0.0:5000)
    - From Docker Hub 
        ```bash
        make docker_run_backend (including build and run)
        ```
    - From local docker build
        ```bash
        make docker_build_backend
        ```
    - From uWSGI (use uWSGI to replace flask WSGI)
        ```bash
        make run_backend
        ```
    - From native python flask
        ```bash
        python3 backend/app.py FLASK_APP=app flask run --host=0.0.0.0 --port=5000
        ```

- To run frontend only (http://localhost:3000 or http://0.0.0.0:3000)
    - From Docker Hub
        ```bash
        make docker_run_frontend
        ```
    - From local docker build
        ```bash
        make docker_build_frontend
        ```
    - From native npm
        ```bash
        make run_frontend
        ```

### Designs
#### Coding Style
- Python: [PEP8](https://www.python.org/dev/peps/pep-0008/)
- React: [ES6](http://es6-features.org/)

#### Models Design (Entity)
- See full [Models Design](documents/Models.md)

#### Database Design
- See full [Database Design](documents/Database.md)

#### APIs Design
- See full [APIs Design](documents/APIs.md)

#### Components Design
1. Processing Queue: Each uploaded video will be pushed to a processing queue to be de-queued later for encoding, thumbnail generation, and storage.
2. Encoder: To encode each uploaded video into multiple formats.
3. Thumbnails generator: To generate a few thumbnails for each video.
4. Video and Thumbnail storage: To store video and thumbnail files in some distributed file storage.
5. User Database: To store user’s information, e.g., name, email, address, etc.
6. Video metadata storage: A metadata database to store all the information about videos like title, file path in the system, uploading user, total views, likes, dislikes, etc. It will also be used to store all the video comments.

- Architecture Design
    
    ![Architecture Design Diagram](documents/ArchitectureDesign_resize.png)
    
- Background Design

    ![BackgroundDesign](documents/BackgroundDesign.png)

### Tests
- See full [Test Cases](documents/Test.md)
- Coverage
  - [CodeCov](https://codecov.io/gh/HyperTars/Online-Video-Platform)
  - [Coveralls](https://coveralls.io/github/HyperTars/Online-Video-Platform)

### CI / CD 
- We use `Travis-CI`, `Docker` and `Heroku` to do CI/CD works
  - Our [Travis Conf](.travis.yml) and [Travis-CI Page](https://travis-ci.com/github/HyperTars/Online-Video-Platform)
  - Our [Docker Conf](docker-compose.yml) and [Docker Frontend](https://hub.docker.com/r/hypertars/greloupis-frontend/tags) | [Docker Backend](https://hub.docker.com/r/hypertars/greloupis-backend/tags)
  - Our [Heroku Frontend](http://greloupis-frontend.herokuapp.com/) and [Heroku Backend](http://greloupis-backend.herokuapp.com/)


### Contributors
  
  GitHub | Name | NetID
  --- | --- | ---
  [HyperTars](https://github.com/HyperTars) | Wenzhou Li | [wl2154](mailto:wl2154@nyu.edu)
  [MikeYan01](https://github.com/MikeYan01) | Linyi Yan | [ly1333](mailto:ly1333@nyu.edu)
  [FatBin](https://github.com/FatBin) | Xuanbin Luo | [xl2806](mailto:xl2806@nyu.edu)