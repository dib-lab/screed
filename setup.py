#!/usr/bin/env python
# Copyright (c) 2016, The Regents of the University of California.
from setuptools import setup

setup(name='screed',
#      packages=['screed', 'screed.tests'],
#      package_data={
#          'screed.tests': ['test.*', 'test-whitespace.fa', 'empty.fa']},
      setup_requires=['pytest-runner'],
      tests_require=['pytest >= 3.0', 'pytest-cov'],
      )
