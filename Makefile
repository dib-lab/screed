# make pep8 to check for basic Python code compliance
# make autopep8 to fix most pep8 errors
# make pylint to check Python code for enhanced compliance including naming
#  and documentation
# make coverage-report to check coverage of the python scripts by the tests

PYSOURCES=$(wildcard screed/*.py)
TESTSOURCES=$(wildcard screed/tests/*.py)
SOURCES=$(PYSOURCES) setup.py
DEVPKGS=pep8==1.5.7 diff_cover autopep8 pylint coverage pytest pytest-cov sphinx

VERSION=$(shell git describe --tags --dirty | sed s/v//)
all:
	./setup.py build

install-dependencies:
	pip install --upgrade $(DEVPKGS) || pip2 install --upgrade $(DEVPKGS)
	pip install --upgrade --requirement doc/requirements.txt

install: FORCE
	./setup.py build install

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
	pep8 --exclude=_version.py setup.py screed/

pep8_report.txt: $(PYSOURCES) $(TESTSOURCES)
	pep8 --exclude=_version.py setup.py screed/ > pep8_report.txt || true

diff_pep8_report: pep8_report.txt
	diff-quality --violations=pep8 pep8_report.txt

autopep8: $(PYSOURCES) $(TESTSOURCS)
	autopep8 --recursive --in-place --exclude _version.py --ignore E309 \
		setup.py screed

# A command to automatically run autopep8 on appropriate files
format: autopep8
	# Do nothing

pylint: FORCE
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		setup.py screed || true

pylint_report.txt: ${PYSOURCES} $(TESTSOURCES)
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		setup.py screed > pylint_report.txt || true

diff_pylint_report: pylint_report.txt
	diff-quality --violations=pylint pylint_report.txt

.coverage: $(PYSOURCES) $(TESTSOURCES)
	./setup.py test --addopts="--cov"

coverage.xml: .coverage
	coverage xml --omit 'screed/tests/*'

coverage.html: htmlcov/index.html

htmlcov/index.html: .coverage
	coverage html --omit 'screed/tests/*'
	@echo Test coverage is now in htmlcov/index.html

coverage-report: .coverage
	coverage report --omit 'screed/tests/*'

diff-cover: coverage.xml
	diff-cover coverage.xml

diff-cover.html: coverage.xml
	diff-cover coverage.xml --html-report diff-cover.html

tests.xml: FORCE
	./setup.py test --addopts "--junitxml=$@"

doxygen: doc/doxygen/html/index.html

doc: build/sphinx/html/index.html

convert-release-notes:
		for file in doc/release-notes/*.md; do \
				pandoc --from=markdown --to=rst $${file} > $${file%%.md}.rst; \
				done

build/sphinx/html/index.html: $(SOURCES) $(wildcard doc/*.txt) doc/conf.py all
		./setup.py build_sphinx --fresh-env
		@echo ''
		@echo '--> docs in build/sphinx/html <--'
		@echo ''

doc/doxygen/html/index.html: ${CPPSOURCES} ${PYSOURCES}
	mkdir -p doc/doxygen
	sed "s/\$${VERSION}/`python get_version.py`/" Doxyfile.in > \
		Doxyfile
	doxygen

test: FORCE
	./setup.py develop
	./setup.py test

sloccount.sc: ${PYSOURCES} Makefile
	sloccount --duplicates --wide --details screed setup.py Makefile \
		> sloccount.sc

sloccount: 
	sloccount screed setup.py Makefile

FORCE:
