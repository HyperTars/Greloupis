run_react:
	npm start

test:
	npm run test

report:
	npx jest --coverage

docker_build:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker build -f Dockerfile -t frontend:dev .
#	- docker tag $frontend $(DOCKER_REPO)
#	- docker push $(DOCKER_REPO)

docker_run:
	- docker stop $(docker ps -aq)
	- docker run -p 3000:3000 --rm -it -v /app/node_modules -e CHOKIDAR_USEPOLLING=true frontend:dev
