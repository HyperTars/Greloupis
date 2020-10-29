LINTER = flake8
SRC_DIR = source
REQ_DIR = requirements
TAG = latest
DOCKER_REPO = hypertars/online-video-platform

FORCE:

prod:	dev_env tests github

run:    dev_env
	python3 -m source.app FLASK_APP=app flask run --host=0.0.0.0 --port=5000
	
github:	FORCE
	- git add .
	- git commit -a
	- git push origin

tests:	unit report lint
	echo "unittest and lint check finished"

unit:   FORCE
	coverage run --source=source -m pytest --disable-pytest-warnings

lint:	FORCE
	$(LINTER) $(SRC_DIR)/. --exit-zero --ignore=E501

dev_env:	FORCE
	pip3 install -r $(REQ_DIR)/requirements-dev.txt

docs:	#FORCE
	cd $(SRC_DIR); make docs

report:
	coverage report

coverage:
	- coveralls
	- codecov -t $(CODECOV_TOKEN)

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

heroku:
	- docker login --username _ --password=$(HEROKU_API_KEY) registry.heroku.com
	- heroku container:push web --app $(HEROKU_APP_NAME)
	- heroku container:release web --app $(HEROKU_APP_NAME)
