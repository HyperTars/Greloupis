LINTER = flake8
BACKEND_DIR = backend
REQ_DIR = requirements
TAG = latest
DOCKER_REPO = hypertars/online-video-platform

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

docker:
	cd $(BACKEND_DIR); make docker

docker_run:
	cd $(BACKEND_DIR); make docker_run

docker_test:
	cd $(BACKEND_DIR); make docker_test

docker_clean:
	- docker stop $(docker ps -aq)
	- docker system prune -a

heroku:
	- docker login --username _ --password=$(HEROKU_API_KEY) registry.heroku.com
	- heroku container:push web --app $(HEROKU_APP_NAME)
	- heroku container:release web --app $(HEROKU_APP_NAME)
