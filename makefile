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
	pip3 install -r $(REQ_DIR)/requirements-dev.txt

docs:	#FORCE
	cd $(BACKEND_DIR); make docs

report:
	cd $(BACKEND_DIR); make report

coverage:
	- cd $(BACKEND_DIR); coveralls
	- cd $(BACKEND_DIR); codecov -t $(CODECOV_TOKEN)

connect:
	- chmod 400 documents/DevOps.pem
	- ssh -i "documents/DevOps.pem" $(EC2_SERVER)

docker:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker build -f Dockerfile -t $(DOCKER_BUILD):$(TAG) .
	- docker tag $(DOCKER_BUILD) $(DOCKER_REPO)
	- docker push $(DOCKER_REPO)

docker_run:
	- docker run -p 5000:5000 --rm -it $(DOCKER_REPO):$(TAG)

docker_test:
	- docker stop $(docker ps -aq)
	- docker run -p 5000:5000 $(DOCKER_BUILD)

heroku:
	- docker login --username _ --password=$(HEROKU_API_KEY) registry.heroku.com
	- heroku container:push web --app $(HEROKU_APP_NAME)
	- heroku container:release web --app $(HEROKU_APP_NAME)