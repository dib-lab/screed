#!/usr/bin/env python
from __future__ import print_function
try:
    from setuptools import setup
except ImportError:
    print('(WARNING: importing distutils, not setuptools!)')
    from distutils.core import setup

import versioneer

setup(version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      name='screed',
      description='A short read database',
      author='Alex Nolley, C. Titus Brown',
      author_email='ctb@msu.edu',
      url='http://github.com/dib-lab/screed/',
      include_package_data=True,
      packages=['screed', 'screed.tests'],
      package_data={
          'screed.tests': ['test.*', 'test-whitespace.fa', 'empty.fa']},
      license='BSD',
      test_suite='nose.collector',
      extras_require={'tests': ['nose >= 1.0']},
      install_requires=['bz2file']
      )
