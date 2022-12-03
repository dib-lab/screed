# make pep8 to check for basic Python code compliance
# make pylint to check Python code for enhanced compliance including naming
#  and documentation
# make coverage-report to check coverage of the python scripts by the tests

PYSOURCES=$(wildcard screed/*.py)
TESTSOURCES=$(wildcard screed/tests/*.py)
SOURCES=$(PYSOURCES) setup.py

VERSION=$(shell git describe --tags --dirty | sed s/v//)
all:
	./setup.py build

install: FORCE
	./setup.py build install

install-dependencies: FORCE
	pip install -e .[all]

develop: FORCE
	./setup.py develop

dist: dist/screed-$(VERSION).tar.gz

dist/screed-$(VERSION).tar.gz: $(SOURCES)
	./setup.py sdist

clean: FORCE
	./setup.py clean --all || true
	rm -rf build/
	rm -rf coverage-debug .coverage coverage.xml
	rm -rf doc/_build
	rm -rf .eggs/ *.egg-info/ .cache/ __pycache__/ *.pyc */*.pyc */*/*.pyc

pep8: $(PYSOURCES) $(TESTSOURCES)
	pycodestyle --exclude=_version.py setup.py screed/

pylint: FORCE
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		setup.py screed || true

doc: FORCE
	cd doc && make html

test: FORCE
	pytest

FORCE:
