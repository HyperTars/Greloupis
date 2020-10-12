LINTER = flake8
SRC_DIR = source
REQ_DIR = requirements

FORCE:

prod:	tests github

run:
	python -m source.app FLASK_APP=app flask run --host=127.0.0.1 --port=8000
	
github:	FORCE
	git pull origin master
	git commit -a
	git push origin master

test:	lint unit
	echo "lint unit tests"

unit:	FORCE
	echo "We have to write some tests!"
	# test

lint:	FORCE
	$(LINTER) $(SRC_DIR)/*.py --exit-zero --ignore=W191,E265,F405

dev_env:	FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt

docs:	#FORCE
	cd $(SRC_DIR); make docs

connect:
	chmod 400 documents/DevOps.pem
	ssh -i "documents/DevOps.pem" ubuntu@ec2-54-205-45-145.compute-1.amazonaws.com

