[![logo](../documents/greloupis-horizontal.png)](https://greloupis-frontend.herokuapp.com/)

# Greloupis - An online video sharing platform

- Tech Stack & Compatibility

    [![npm](https://img.shields.io/badge/npm-6.14.8-blue)](https://blog.npmjs.org/post/626732790304686080/release-6148)
    [![node.js](https://img.shields.io/badge/node.js-14.15.0-blue)](https://nodejs.org/dist/latest-v14.x/docs/api/)
    [![nginx](https://img.shields.io/badge/nginx-14.15-blue)](https://www.nginx.com/)

- CI / CD

    [![build](https://travis-ci.com/HyperTars/Online-Video-Platform.svg?token=btA3ungCKHqWzLxCoxT7&branch=master)](https://travis-ci.com/HyperTars/Online-Video-Platform)
    [![docker status](https://img.shields.io/docker/cloud/build/hypertars/greloupis-frontend)](https://hub.docker.com/r/hypertars/greloupis-frontend)
    [![docker image size](https://img.shields.io/docker/image-size/hypertars/greloupis-frontend)](https://hub.docker.com/r/hypertars/greloupis-frontend/tags)
    [![docker build](https://img.shields.io/docker/cloud/automated/hypertars/greloupis-frontend)](https://hub.docker.com/r/hypertars/greloupis-frontend/builds)
    [![Heroku](https://pyheroku-badge.herokuapp.com/?app=greloupis-frontend&style=flat)](https://greloupis-frontend.herokuapp.com/)

<!-- [Video.js](https://img.shields.io/badge/Video.js-7.8.4-blue) -->
<!-- [![tested with jest](https://img.shields.io/badge/tested_with-jest-99424f.svg)](https://github.com/facebook/jest) -->
<!-- [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier) -->

- Websites and Metrics Monitors
    - [Heroku Frontend Site](https://greloupis-frontend.herokuapp.com/)
    - [Heroku Frontend Metrics Monitor](https://metrics.librato.com/s/public/wxet4vyas)
    - [Docker Backend Repo](https://hub.docker.com/r/hypertars/greloupis-frontend/tags)

## Table of Content
- [Features & Designs](#Designs)
  * [Homepage Design](#Homepage-Design)
  * [Search Design](#Search-Design)
  * [Player Design](#Player-Design)
  * [Dashboard Design](#Dashboard-Design)
  * [Uploading Design](#Uploading-Design)
  * [Error Page Design](#Error-Page-Design)
  * [Web Server Design](#Web-Server-Design)
  * [Coding Style](#Coding-Style)
- [Setup Guide](#Setup-Guide)
  * [Environment Requirement](#Environment-Requirement)
  * [Install Dependencies](#Install-Dependencies)
  * [Run Test](#Run-Test)
  * [Run](#Run)
  * [Dockerize](#Dockerize)
  * [Deploy](#Deploy)
- [Contributors](#Contributors)

## Designs
### Homepage Design
- We list Top 10 Hit Videos in our homepage.
- Private videos are hidden (not listed here).

### Search Design
- We support multi attribute search, including
    - User: user name, user email, user state/country/zip, user street address, user phont number, etc.
    - Video: video title, video channel, video tag, video category, video description, etc.
- Private videos & pending videos are hidden (unless logged in with author's account).

### Player Design
- We support multi resolution video playback, you can select quality when you play video, including
    - FHD 1080p
    - HD 720p
    - SD 540p
- We support rewind, full screen, and keyboard control, including
    - ←: back 5 seconds
    - →: forward 5 seconds
    - ↑: volume up
    - ↓: volume down
    - num 0-9: redirect to position in percentage (0%, 10%, 20%, 30%, ... 90%)
- If logged in, we remember your last playback position, you will be redirect to the position the next time you open the video.
- You can like, dislike, start, and comment on videos.
- Private & pending videos are not allowed to access unless logged in with author's account.

### Dashboard Design
- You can manage your user profile
- You can see all videos you uploaded and its status (pending, private, public), and you can manage them
- You can see your playback history with playback date
- You can see all the videos you starred, liked, commented.
- Private users' detail information and their private videos are hidden unless logged in by themselves.

### Uploading Design
- You can upload your video first, after you successfully uploaded your video, you can edit video information while it is transcoding
- We will generate a thumbnail automatically, but you can upload it by yourself if you like.

### Error Page Design
- We design three error pages
    - [403 Forbidden](public/403.html)
    - [404 Not Found](public/404.html)
    - [500 Internal Server Error](public/500.html)
- You can try to access them directly
    - [403 Forbidden](https://greloupis-frontend.herokuapp.com/403)
    - [404 Not Found](https://greloupis-frontend.herokuapp.com/404)
    - [500 Internal Server Error](https://greloupis-frontend.herokuapp.com/500)

### Web Server Design
- We use [nginx](configs/nginx.template) as our frontend webserver. See how it is configured in [Dockerfile](Dockerfile)

### Coding Style
- React: [JSX](https://reactjs.org/docs/introducing-jsx.html)


## Setup Guide

### Environment Requirement
- **Please make sure the following dependencies are installed and configured before running**
    - npm (6.14.8)
    - node.js (14.15.0)
    - Set up [Environment Variable](../documents/env.sh)

### Install Dependencies
- To install dependencies, run
```bash
make dev_env
```

### Run Test
- To run test, run
```bash
make tests
```

### Run
- Before running
    - If you want to run frontend locally, we recommend you run backend locally at the same time
    - Otherwise, you should configure [backend endpoint](src/components/Endpoint.js), set it to `HEROKU_ENDPOINT` manually

- To run frontend only (http://localhost:3000 or http://0.0.0.0:3000)
    - From Docker Hub
        ```bash
        make docker_hub
        ```
    - From local docker build
        ```bash
        make docker_build docker_run
        ```
    - From native npm
        ```bash
        make run_frontend
        ```

### Dockerize
- This section is for you to dockerize manually. Normally, Travis-CI will do the dockerize job once master branch is updated.
- Before dockerize, make sure you've set up [environment variable](../documents/env.sh)
    - FRONTEND_BUILD
    - FRONTEND_REPO (you can also change it in [makefile](makefile))
- To dockerize backend, run
```bash
make docker_build docker_push
```

### Deploy
- This section is for you to deploy manually. Normally, Travis-CI will do the deploy job once master branch is updated.
- Before deploy, make sure you've set up [environment variable](../documents/env.sh)
    - FRONTEND_BUILD
    - FRONTEND_REPO (you can also change it in [makefile](makefile))
    - HEROKU_API_KEY
    - HEROKU_APP_NAME
- To deploy to heroku, run
```bash
make heroku
```


## Contributors
  
  GitHub | Name | NetID
  --- | --- | ---
  [HyperTars](https://github.com/HyperTars) | Wenzhou Li | [wl2154](mailto:wl2154@nyu.edu)
  [MikeYan01](https://github.com/MikeYan01) | Linyi Yan | [ly1333](mailto:ly1333@nyu.edu)
  [FatBin](https://github.com/FatBin) | Xuanbin Luo | [xl2806](mailto:xl2806@nyu.edu)
