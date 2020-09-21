# CiliCili Player
Proposal of A DevOps Project

## Overview

[...]

## Assumptions

- We assume that all videos we collect from the Internet are legal and valid
- We assume that some users will actively contribute their experiences and reviews to the system after they watch a video
- We assume that users will not arbitrarily give their ratings and reviews to a video

## Architecture Design

[...]

## Technology Stack

### Front-end

We will use `React.js`, which is a component-based JavaScript library for building user interfaces. See [React.js](https://reactjs.org/) for more details.

### Back-end

We will use `Flask-Rest X`, which is an extension for Python Flask framework that adds support for quickly building REST APIs. See [Flask-Rest X](https://flask-restx.readthedocs.io/en/latest/) for more details.

### Testing

For unit test, we will use:
- `unittest`, to test Python code
- `Jest`, to test React code

We will also use linters listed below to enforce code styling:
- `flake8` for Python
- `eslint` for React

### CI/CD

We will use `Travis CI`, which provides convenient continuous integration & deployment services.

### Deploy and Monitor

We will use `Docker` to set up container for our application for cloud deployment and monitoring in the futurue.

## External API integrations and Data Sources

[...]

## Deliverables

[...]

## Implementation Plan

- Phase 1, due Sept 22
  - [x] Form a group of 3 (Exceptions can be made if you’d like to form a group of 4 or smaller)
  - [x] Set up a Slack channel for communications within your team
  - [x] Set up a GitHub repository for your project
  - [ ] Set up a Kanban board for managing workflow within your team using GitHub “Projects” feature
  - [ ] Formulate your project proposal

- Phase 2, due Sept 29
  - [ ] Setup a Flask-RESTX API server
  - [ ] Aim to have, but not limited to, 8 post and get endpoints

- Phase 3, due Oct 6
  - [ ] Create a Makefile to run tests locally, as well as push code into production

- Phase 4, due Oct 20
  - [ ] Keep developing the application
  - [ ] Write tests when writing the code. Tests include unit test and code styling check

- Phase 5, due Nov 3
  - [ ] Set up a CI/CD pipeline using Travis CI. Use it to push your code to PythonAnywhere

- Phase 6, due Nov 17
  - [ ] Create a Docker container for your application. Deploy it to a cloud service. Create monitoring

- Phase 7, due Dec 8
  - [ ] Final project hand in and presentations.