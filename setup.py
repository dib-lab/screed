#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    print '(WARNING: importing distutils, not setuptools!)'
    from distutils.core import setup

setup(name='screed',
      version='0.7',
      description='A short read database',
      author='Alex Nolley, C. Titus Brown',
      author_email='ctb@msu.edu',
      url='http://github.com/ged-lab/screed/',
      packages=['screed', 'screed.tests'],
      package_data={'screed.tests': ['test.*', 'test-whitespace.fa']},
      license='BSD',
      test_suite = 'nose.collector'
      )
