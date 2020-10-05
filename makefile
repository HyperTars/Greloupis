LINTER = flake8
SRC_DIR = source
REQ_DIR = requirements

FORCE:

prod:	tests github

github:	FORCE
	git add .
	- git commit -a
	- git push origin master

tests:	lint unit
	echo "lint unit tests"

unit:	FORCE
	echo "We have to write some tests!"
	# flake8 here

lint:	FORCE
	$(LINTER) . --exit-zero --ignore=W191,E265
	#$(LINTER) $(SRC_DIR)/*.py --exit-zero --ignore=W191,E265, E117, E265, E231, E309, E251

dev_env:	FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt
