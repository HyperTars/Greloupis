docker login --username $DOCKER_USER --password $DOCKER_PASS
if [ "$TRAVIS_BRANCH" = "master" ]; then
TAG="latest"
else
TAG="$TRAVIS_BRANCH"
fi
docker build -f dockerfile -t $DOCKER_BUILD:$TAG .
docker tag $DOCKER_BUILD $DOCKER_REPO
docker push $DOCKER_REPO
