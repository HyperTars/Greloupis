LINTER = flake8
TAG = latest
BACKEND_REPO = hypertars/greloupis-backend
DOCFILES = $(shell ls *.py | sed 's/.py/.html/')

dev_env_backend:
	pip3 install -r requirements.txt
	
run_backend:
	python3 app.py FLASK_APP=app flask run --host=0.0.0.0 --port=5000

wsgi_run:
	gunicorn --bind 0.0.0.0:5000 wsgi:app

tests:	dev_env_backend unit report lint
	echo "unittest and lint check finished"

unit:
	coverage run --source ./ -m py.test --disable-pytest-warnings

report:
	coverage report

coverage:
	- coveralls
	- codecov -t $(CODECOV_TOKEN)

lint:
	$(LINTER) . --exit-zero  --ignore=E501

docs: $(DOCFILES)

docker_build:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker build -f Dockerfile -t $(BACKEND_BUILD):$(TAG) .
	- docker tag $(BACKEND_BUILD) $(BACKEND_REPO)
	- docker push $(BACKEND_REPO)

docker_run:
	- docker run -p 5000:5000 $(BACKEND_BUILD)

docker_hub:
	- docker run -p 5000:5000 --rm -it $(BACKEND_REPO):$(TAG)

%.html: %.py
	pydoc3 -w ./$<
	git add $@
