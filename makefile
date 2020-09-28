LINTER = flake8
SRC_DIR = source
REQ_DIR = requirements

FORCE:

prod:	tests github

github:	FORCE
	echo "Makefile update git"
	- git commit -a
	- git push origin master

tests:	lint unit

unit:	FORCE
	echo "We have to write some tests!"

lint:	FORCE
	$(LINTER) $(SRC_DIR)/*.py

dev_env:	FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt