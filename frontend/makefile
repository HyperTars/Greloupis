FRONTEND_REPO = hypertars/greloupis-frontend
TAG ?= latest

dev_env_frontend:
	npm install

run_frontend:
	npm start

tests:	test report

test: 
	npm run test

report:
	npx jest --coverage

docker_build:
	- docker build --build-arg ACCESS_KEY_ID1=$(ACCESS_KEY_ID1) --build-arg ACCESS_KEY_ID2=$(ACCESS_KEY_ID2) --build-arg SECRET_KEY1=$(SECRET_KEY1) --build-arg SECRET_KEY2=$(SECRET_KEY2) -f Dockerfile -t $(FRONTEND_BUILD):$(TAG) .

docker_push:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker tag $(FRONTEND_BUILD) $(FRONTEND_REPO)
	- docker push $(FRONTEND_REPO)

docker_run:	docker_run_nginx

docker_run_nginx:
	- docker run -p 3000:3000 --env PORT=3000 --rm -it -v /app/node_modules -e CHOKIDAR_USEPOLLING=true $(FRONTEND_BUILD)

docker_hub:
	- docker run -p 3000:3000 --env PORT=3000 --rm -it $(FRONTEND_REPO):$(TAG)

heroku:
	- docker login --username _ --password=$(HEROKU_API_KEY) registry.heroku.com
	- heroku container:push web --arg ACCESS_KEY_ID1=$(ACCESS_KEY_ID1),ACCESS_KEY_ID2=$(ACCESS_KEY_ID2),SECRET_KEY1=$(SECRET_KEY1),SECRET_KEY2=$(SECRET_KEY2) --app $(FRONTEND_BUILD)
	- heroku container:release web --app $(HEROKU_APP_FRONTEND)
