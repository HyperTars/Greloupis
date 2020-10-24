LINTER = flake8
SRC_DIR = source
REQ_DIR = requirements

FORCE:

prod:	dev_env test github

run:    dev_env
	python3 -m source.app FLASK_APP=app flask run --host=0.0.0.0 --port=5000
	
github:	FORCE
	git pull origin master
	git commit -a
	git push origin master

test:	unit report lint
	echo "unittest and lint check finished"

unit:   FORCE
	coverage run --source=source -m pytest --disable-pytest-warnings
	# python3 -m source.test

lint:	FORCE
	$(LINTER) $(SRC_DIR)/. --exit-zero --ignore=E501,F401,F403,F405,F841

dev_env:	FORCE
	pip3 install -r $(REQ_DIR)/requirements-dev.txt

docs:	#FORCE
	cd $(SRC_DIR); make docs

report:
	coverage report

coveralls:
	coveralls

codecov:
	codecov -t a767bea5-9464-4229-b6f4-e420874311b3

connect:
	chmod 400 documents/DevOps.pem
	ssh -i "documents/DevOps.pem" ubuntu@ec2-54-205-45-145.compute-1.amazonaws.com

