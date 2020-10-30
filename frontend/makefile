FRONTEND_REPO = hypertars/greloupis-frontend
TAG = latest

run_react:
	npm start

test:
	npm run test

report:
	npx jest --coverage

docker_build:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker build -f Dockerfile -t $(FRONTEND_BUILD):$(TAG) .
	- docker tag $(FRONTEND_BUILD) $(FRONTEND_REPO)
	- docker push $(FRONTEND_REPO)

docker_run:
	- docker run -p 3000:3000 --rm -it -v /app/node_modules -e CHOKIDAR_USEPOLLING=true $(FRONTEND_BUILD)

docker_hub:
	- docker run -p 3000:3000 --rm -it $(FRONTEND_REPO):$(TAG)
