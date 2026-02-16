# make pep8 to check for basic Python code compliance
# make pylint to check Python code for enhanced compliance including naming
#  and documentation
# make coverage-report to check coverage of the python scripts by the tests

PYSOURCES=$(wildcard screed/*.py)
TESTSOURCES=$(wildcard screed/tests/*.py)
SOURCES=$(PYSOURCES)

VERSION=$(shell git describe --tags --dirty | sed s/v//)
all:
	python -m build .

install: FORCE
	pip install -e .

install-dependencies: FORCE
	pip install -e .[all]

develop: FORCE
	pip install -e .

dist: dist/screed-$(VERSION).tar.gz

dist/screed-$(VERSION).tar.gz: $(SOURCES)
	python -m build --sdist .

clean: FORCE
	pip uninstall screed || true
	rm -rf build/
	rm -rf coverage-debug .coverage coverage.xml
	rm -rf doc/_build
	rm -rf .eggs/ *.egg-info/ .cache/ __pycache__/ *.pyc */*.pyc */*/*.pyc

pep8: $(PYSOURCES) $(TESTSOURCES)
	pycodestyle --exclude=_version.py screed/

pylint: FORCE
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		screed || true

doc: FORCE
	cd doc && make html

test: FORCE
	pytest

FORCE:
