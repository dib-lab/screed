#!/usr/bin/env python
# Copyright (c) 2016, The Regents of the University of California.
from __future__ import print_function
try:
    from setuptools import setup
except ImportError:
    print('(WARNING: importing distutils, not setuptools!)')
    from distutils.core import setup

setup(name='screed',
      description='A short read database',
      author='Alex Nolley, C. Titus Brown',
      author_email='ctbrown@ucdavis.edu',
      url='http://github.com/dib-lab/screed/',
      zip_safe=False,
      include_package_data=True,
      packages=['screed', 'screed.tests'],
      package_data={
          'screed.tests': ['test.*', 'test-whitespace.fa', 'empty.fa']},
      license='BSD',
      setup_requires=['pytest-runner', 'setuptools_scm'],
      use_scm_version={ 'write_to': 'screed/version.py' },
      tests_require=['pytest >= 3.0', 'pytest-cov'],
      install_requires=['bz2file'],
      entry_points={'console_scripts': [
          'screed = screed.__main__:main'
          ]
      })
