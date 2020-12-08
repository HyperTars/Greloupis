# Greloupis - Environment Variables

# Running Configuration: dev | test | prod
# Frontend: src/Endpoint.js
# Backend: settings.py
# Docker: docker-compose.yml, frontend/makefile, backend/makefile
export PROFILE="dev"

# Coverage Service
export COVERALLS_REPO_TOKEN=<coveralls repo token>
export CODECOV_TOKEN=<codecov token>

# Docker
export DOCKER_USER=<docker user>
export DOCKER_EMAIL=<docker email>
export DOCKER_PASS=<docker password or auth key>
export FRONTEND_BUILD="greloupis-frontend"
export BACKEND_BUILD="greloupis-backend"

# Heroku
export HEROKU_API_KEY=<heroku api key>
export HEROKU_EMAIL=<heroku email>
export HEROKU_APP_BACKEND="greloupis-backend"
export HEROKU_APP_FRONTEND="greloupis-frontend"

# AWS - S3 Video Bucket
export ACCESS_KEY_ID1=<aws s3 video bucket access key>
export SECRET_KEY1=<aws s3 video bucket secret key>

# AWS - S3 Image Bucket
export ACCESS_KEY_ID2=<aws s3 image bucket access key>
export SECRET_KEY2=<aws s3 image bucket secret key>
export AWS_THUMBNAIL_FOLDER=<aws s3 thumbnail folder>

# AWS - Cloud Front
export AWS_CLOUD_FRONT=<aws cloud front address>

# AWS - Backend Post Key (after transcoding finished, post {AWS_AUTH_KEY=$AWS_AUTH_KEY, video_id=$video_id} to /video/aws)
# Backend: configs/config_base.py, routes/route_video.py
export AWS_AUTH_KEY=<self defined aws-backend communication auth key>

# MongoDB
export MONGO_DEV=<MongoDB develop collection URI>
export MONGO_TEST=<MongoDB test collection URI>
export MONGO_PROD=<MongoDB production collection URI>