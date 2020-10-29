DOCFILES = $(shell ls *.py | sed 's/.py/.html/')

run:
	python3 app.py FLASK_APP=app flask run --host=0.0.0.0 --port=5000

unit:
	coverage run --source ./ -m py.test --disable-pytest-warnings

report:
	coverage report

docs: $(DOCFILES)

%.html: %.py
	pydoc3 -w ./$<
	git add $@