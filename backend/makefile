LINTER = flake8
TAG = latest
DOCKER_REPO = hypertars/online-video-platform
DOCFILES = $(shell ls *.py | sed 's/.py/.html/')

dev_env:
	pip3 install -r requirements.txt
	
run:
	python3 app.py FLASK_APP=app flask run --host=0.0.0.0 --port=5000

wsgi_run:
	gunicorn --bind 0.0.0.0:5000 wsgi:app

unit:
	coverage run --source ./ -m py.test --disable-pytest-warnings

report:
	coverage report

coverage:
	- coveralls
	- codecov -t $(CODECOV_TOKEN)

docs: $(DOCFILES)

docker_build:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker build -f Dockerfile -t $(DOCKER_BUILD):$(TAG) .
	- docker tag $(DOCKER_BUILD) $(DOCKER_REPO)
	- docker push $(DOCKER_REPO)

docker_run:
	- docker stop $(docker ps -aq)
	- docker run -p 5000:5000 $(DOCKER_BUILD)

docker_hub:
	- docker run -p 5000:5000 --rm -it $(DOCKER_REPO):$(TAG)

%.html: %.py
	pydoc3 -w ./$<
	git add $@
