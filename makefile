LINTER = flake8
BACKEND_DIR = backend
FRONTEND_DIR = frontend
REQ_DIR = requirements
TAG = latest
DOCKER_REPO = hypertars/greloupis

FORCE:

prod:	dev_env tests github

run:
	cd $(BACKEND_DIR); make run

github:	FORCE
	- git commit -a
	- git push origin

tests:	dev_env unit report lint
	echo "unittest and lint check finished"

unit:   FORCE
	cd $(BACKEND_DIR); make unit

lint:	FORCE
	$(LINTER) $(BACKEND_DIR)/. --exit-zero --ignore=E501

dev_env:	FORCE
	cd $(BACKEND_DIR); make dev_env

docs:	#FORCE
	cd $(BACKEND_DIR); make docs

report:
	cd $(BACKEND_DIR); make report

coverage:
	cd $(BACKEND_DIR); make coverage

connect:
	- chmod 400 documents/DevOps.pem
	- ssh -i "documents/DevOps.pem" $(EC2_SERVER)

docker_build:
	docker-compose build

docker_run:
	docker-compose up

docker_status:
	docker-compose ps

docker_push:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker-compose build --pull
	- docker-compose push

docker_build_backend:
	cd $(BACKEND_DIR); make docker_build

docker_run_backend:
	cd $(BACKEND_DIR); make docker_run

docker_build_frontend:
	cd $(FRONTEND_DIR); make docker_build

docker_run_frontend:
	cd $(FRONTEND_DIR); make docker_run

docker_clean:
	- docker stop $(docker ps -aq)
	- docker system prune -a

heroku:
	- docker login --username _ --password=$(HEROKU_API_KEY) registry.heroku.com
	- heroku container:push web --app $(HEROKU_APP_NAME)
	- heroku container:release web --app $(HEROKU_APP_NAME)
