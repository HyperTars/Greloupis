FRONTEND_REPO = hypertars/greloupis-frontend
TAG = latest

dev_env_frontend:
	npm install
	npm run build

run_frontend:
	npm start

tests:
	npm run test

report:
	npx jest --coverage

docker_build:
	- docker build -f Dockerfile -t $(FRONTEND_BUILD):$(TAG) .

docker_push:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker tag $(FRONTEND_BUILD) $(FRONTEND_REPO)
	- docker push $(FRONTEND_REPO)

docker_run:	docker_run_nginx

docker_run_nginx:
	- docker run -p 80:3000 --env PORT=3000 --rm -it -v /app/node_modules -e CHOKIDAR_USEPOLLING=true $(FRONTEND_BUILD)

docker_hub:
	- docker run -p 80:80 --rm -it $(FRONTEND_REPO):$(TAG)

heroku:
	- docker login --username _ --password=$(HEROKU_API_KEY) registry.heroku.com
	- heroku container:push web --app greloupis-frontend
	- heroku container:release web --app greloupis-frontend