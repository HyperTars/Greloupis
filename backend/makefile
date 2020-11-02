LINTER = flake8
TAG = latest
BACKEND_REPO = hypertars/greloupis-backend

dev_env_backend:
	pip3 install -r requirements.txt
	
run_backend:	run_wsgi
	# python3 app.py FLASK_APP=app flask run --host=0.0.0.0 --port=5000

run_wsgi:
	uwsgi --http localhost:5000 --wsgi-file  wsgi.py --callable app
	
tests:	unit report lint
	echo "unittest and lint check finished"

unit:
	coverage run --source ./ -m py.test --disable-pytest-warnings

report:
	coverage report

coverage:
	- coveralls
	- codecov -t $(CODECOV_TOKEN)

lint:
	$(LINTER) --exit-zero ./

document:
	pydoc -w ./
	mv *.html docs

docker_build:
	- docker build -f Dockerfile -t $(BACKEND_BUILD):$(TAG) .

docker_run:
	- docker run -p 5000:5000 --env PORT=5000 $(BACKEND_BUILD)

docker_push:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker tag $(BACKEND_BUILD) $(BACKEND_REPO)
	- docker push $(BACKEND_REPO)

docker_hub:
	- docker run -p 5000:5000 --env PORT=5000 --rm -it $(BACKEND_REPO):$(TAG)

heroku:
	- docker login --username _ --password=$(HEROKU_API_KEY) registry.heroku.com
	- heroku container:push web --app $(BACKEND_BUILD)
	- heroku container:release web --app $(BACKEND_BUILD)