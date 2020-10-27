# DevOps-Project
[![build](https://travis-ci.com/HyperTars/Online-Video-Platform.svg?token=btA3ungCKHqWzLxCoxT7&branch=master)](https://travis-ci.com/HyperTars/Online-Video-Platform)
[![CodeCov Status](https://codecov.io/gh/HyperTars/Online-Video-Platform/branch/master/graph/badge.svg?token=8K7ODQK5BV)](https://codecov.io/gh/HyperTars/Online-Video-Platform/tree/master/source)
[![Coverall Status](https://coveralls.io/repos/github/HyperTars/Online-Video-Platform/badge.svg?t=dyCGTT)](https://coveralls.io/github/HyperTars/Online-Video-Platform)

<!-- [![stars](https://img.shields.io/github/stars/HyperTars/Online-Video-Platform.svg?style=plasticr)](https://github.com/HyperTars/Online-Video-Platform/stargazers) -->
<!-- [![commit activity](https://img.shields.io/github/commit-activity/y/HyperTars/Online-Video-Platform.svg?style=plasticr)](https://github.com/HyperTars/Online-Video-Platform/commits/master) -->
<!-- [![last commit](https://img.shields.io/github/last-commit/HyperTars/Online-Video-Platform.svg?style=plasticr)](https://github.com/HyperTars/Online-Video-Platform/commits/master) -->

[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://www.python.org/downloads/release/python-385/)
[![npm](https://img.shields.io/badge/npm-6.14.8-blue)](https://blog.npmjs.org/post/626732790304686080/release-6148)
[![node.js](https://img.shields.io/badge/node.js-14.15.0-blue)](https://nodejs.org/dist/latest-v14.x/docs/api/)
[![Flask](https://img.shields.io/badge/Flask-1.1.2-blue)](https://pypi.org/project/Flask/)
[![React](https://img.shields.io/badge/React-17.0.0-blue)](https://reactjs.org/versions)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4-blue)](https://docs.mongodb.com/manual/release-notes/4.4/)
<!-- [Video.js](https://img.shields.io/badge/Video.js-7.8.4-blue) -->


### Project Proposal
- [Proposal](documents/Proposal.md)
  
### Guide

#### Requirement
- Currently we only support `Python 3.7 / 3.8` (3.6 or below and 3.9 is not supported)
- npm

#### Install dependencies
- To install dependencies, run
```bash
make dev_env
```

#### Run test
- To run test, run
```bash
make test
```

#### Start server
- To start server, run
```bash
make run
# OR
python -m source.app FLASK_APP=app flask run --host=127.0.0.1 --port=8000
```

- You should be able to visit http://localhost:5000/ now and see a list of swagger APIs.

    ![API_Preview](documents/API_Swagger.png)


### Designs
#### Coding Style: Naming Convention
- See full [Naming Convention](documents/NamingConventions.md)

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
- Connect to AWS EC2 server:
    ```bash
    make connect
    ```

### CI / CD (TBD)
- We use `Travis` to do CI/CD works
- See our [travis conf](.travis.yml)
- Docker page: [docker page](https://hub.docker.com/r/hypertars/online-video-platform)
- We will deploy our project to our website: www.hypertars.me (under construction)


### Contributors
  
  GitHub | Name | NetID
  --- | --- | ---
  [HyperTars](https://github.com/HyperTars) | Wenzhou Li | [wl2154](mailto:wl2154@nyu.edu)
  [MikeYan01](https://github.com/MikeYan01) | Linyi Yan | [ly1333](mailto:ly1333@nyu.edu)
  [FatBin](https://github.com/FatBin) | Xuanbin Luo | [xl2806](mailto:xl2806@nyu.edu)
