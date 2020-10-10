LINTER = flake8
SRC_DIR = source
REQ_DIR = requirements

FORCE:

prod:	tests github

run:
	python -m source.app FLASK_APP=app flask run --host=127.0.0.1 --port=8000
	
github:	FORCE
	git add .
	git pull origin master
	git commit -a
	git push origin master

tests:	lint unit #test
	echo "lint unit tests"

unit:	FORCE
	echo "We have to write some tests!"
	# test

lint:	FORCE
	$(LINTER) $(SRC_DIR)/*.py --exit-zero --ignore=W191,E265

test:	FORCE
	python $(SRC_DIR)/test.py

dev_env:	FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt

docs:	#FORCE
	cd $(SRC_DIR); make docs
