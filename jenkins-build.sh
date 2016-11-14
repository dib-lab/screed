#!/bin/bash

if type python2> /dev/null 2>&1
then
    PYTHON_EXECUTABLE=$(which python2)
else
    PYTHON_EXECUTABLE=$(which python)
fi
virtualenv -p ${PYTHON_EXECUTABLE} .env

. .env/bin/activate
make install-dependencies > install_dependencies.out
make develop
make coverage.xml
make tests.xml
if type doxygen >/dev/null 2>&1
then
        make doxygen 2>&1 > doxygen.out
fi
make pylint_report.txt
make pep8_report.txt
if type sloccount >/dev/null 2>&1
then
        make sloccount.sc
fi

