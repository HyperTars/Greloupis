LINTER = flake8
SRC_DIR = source
REQ_DIR = requirements

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
	$(LINTER) $(SRC_DIR)/. --exit-zero --ignore=E501,F401,F403,F405,F841

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
	- ssh -i "documents/DevOps.pem" ubuntu@ec2-54-205-45-145.compute-1.amazonaws.com

docker:
	- docker build -f Dockerfile -t online-video-platform:latest .
	- docker tag online-video-platform hypertars/online-video-platform
	- docker push hypertars/online-video-platform

dockerrun:
	- docker run -p 5000:5000 --rm -it hypertars/online-video-platform:latest
