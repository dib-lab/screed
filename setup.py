#!/usr/bin/env python
# Copyright (c) 2016, The Regents of the University of California.
from __future__ import print_function
try:
    from setuptools import setup
except ImportError:
    print('(WARNING: importing distutils, not setuptools!)')
    from distutils.core import setup

test_deps = ['pytest >= 3.0', 'pytest-cov', 'pycodestyle']
setup_deps = ['pytest-runner', 'setuptools_scm']
install_deps = ['bz2file']
extras = { 'test': test_deps,
           'all': test_deps + install_deps + setup_deps
         }

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
      setup_requires=setup_deps,
      use_scm_version={'write_to': 'screed/version.py'},
      tests_require=test_deps,
      install_requires=install_deps,
      extras_require=extras,
      entry_points={'console_scripts': [
          'screed = screed.__main__:main'
          ]
      })
