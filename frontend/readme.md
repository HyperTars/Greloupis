[![logo](../documents/greloupis-horizontal.png)](https://greloupis-frontend.herokuapp.com/)

# Greloupis - An online video sharing platform

- Tech Stack & Compatibility

    [![npm](https://img.shields.io/badge/npm-6.14.8-blue)](https://blog.npmjs.org/post/626732790304686080/release-6148)
    [![node.js](https://img.shields.io/badge/Node.js-14.15.0-blue)](https://nodejs.org/dist/latest-v14.x/docs/api/)
    [![React](https://img.shields.io/badge/React-17.0.1-blue)](https://reactjs.org/versions)
    [![nginx](https://img.shields.io/badge/Nginx-14.15-blue)](https://www.nginx.com/)
    [![ant design](https://img.shields.io/badge/Ant_Design-4.8.5-blue)](https://ant.design/)
    [![material ui](https://img.shields.io/badge/Material_UI-4.11.0-blue)](https://material-ui.com/)
    [![JW player](https://img.shields.io/badge/React_JW_Player-1.9.1-blue)](https://www.npmjs.com/package/react-jw-player)
    [![aws](https://img.shields.io/badge/AWS_SDK-2.797.0-blue)](https://www.npmjs.com/package/aws-sdk)

- CI / CD

    [![CI/CD](https://github.com/HyperTars/Greloupis/workflows/CI/CD/badge.svg)](https://github.com/HyperTars/Greloupis/actions?query=workflow%3ACI%2FCD)
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
- [Greloupis - An online video sharing platform](#greloupis---an-online-video-sharing-platform)
  - [Table of Content](#table-of-content)
  - [Designs](#designs)
    - [Homepage Design](#homepage-design)
    - [Search Design](#search-design)
    - [Player Design](#player-design)
    - [Dashboard Design](#dashboard-design)
    - [Uploading Design](#uploading-design)
    - [Error Page Design](#error-page-design)
    - [Web Server Design](#web-server-design)
    - [Coding Style](#coding-style)
  - [Setup Guide](#setup-guide)
    - [Environment Requirement](#environment-requirement)
    - [Install Dependencies](#install-dependencies)
    - [Run Test](#run-test)
    - [Run](#run)
    - [Dockerize](#dockerize)
    - [Deploy](#deploy)
  - [Contributors](#contributors)

## Designs
### Login & Register
- Login
![login](../documents/images/login.png)

- Register
![register](../documents/images/register.png)

### Homepage Design
- We list Top 10 Hit Videos in our homepage.
- Private videos are hidden (not listed here).
![home](../documents/images/home.png)

### Search Design
- We support multi attribute search, including
    - User: user name, user email, user state/country/zip, user street address, user phont number, etc.
    - Video: video title, video channel, video tag, video category, video description, etc.
- Private videos & pending videos(videos being transcoded and not ready for streaming) are hidden to all users except the video's author.
![search](../documents/images/search.png)

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
- You can like, dislike, star, and comment on videos.
- Private & pending videos are not allowed to be accessed unless logged in with author's account.
![player](../documents/images/video.png)

### Dashboard Design
- You can manage your user profile
- You can see all videos you uploaded and their status (pending, private, public), and you can manage them (update video information or delete video)
- You can see your playback history with playback date
- You can see all the videos you starred, liked, commented.
- Private users' detail information and their private videos are hidden unless logged in by themselves.

- Self dashboard
![dashboard](../documents/images/dashboard.png)

- Private user profile
![private](../documents/images/private.png)

### Uploading Design
- You can upload your video first, after you successfully uploaded your video, you can edit video information while it is transcoding
- We will generate a thumbnail automatically, but you can upload it by yourself if you like.

- Video upload
![upload](../documents/images/upload.png)

- Video update
![video-update](../documents/images/video-update.png)

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

- **AWS Setup Guide**
    - You should create S3 buckets for storing images and videos, set [URL Endpoints](src/components/Endpoint.js) and add auth keypair to [Environment Variable](../documents/EnvironmentSettings.md)

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
    - Otherwise, you should configure [Endpoints](src/components/Endpoint.js), set it to `HEROKU_ENDPOINT` manually

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
- This section is for you to dockerize manually. Normally, GitHub Action will do the dockerize job once master branch is updated.
- Before dockerize, make sure you've set up [environment variable](../documents/EnvironmentSettings.md)
    - FRONTEND_BUILD
    - FRONTEND_REPO (you can also change it in [makefile](makefile))
- To dockerize backend, run
```bash
make docker_build docker_push
```

### Deploy
- This section is for you to deploy manually. Normally, GitHub Action will do the deploy job once master branch is updated.
- Before deploy, make sure you've set up [environment variable](../documents/EnvironmentSettings.md)
    - FRONTEND_BUILD
    - FRONTEND_REPO (you can also change it in [makefile](makefile))
    - HEROKU_API_KEY
    - HEROKU_APP_FRONTEND
- To deploy to heroku, run
```bash
make heroku
```


## Contributors
  
  GitHub | Name | NetID
  --- | --- | ---
  [HyperTars](https://github.com/HyperTars) | Wenzhou Li | [wl2154](mailto:wl2154@nyu.edu)
  [MikeYan01](https://github.com/MikeYan01) | Linyi Yan | [ly1333](mailto:ly1333@nyu.edu)
