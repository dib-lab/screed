#!/usr/bin/env python
from __future__ import print_function
try:
    from setuptools import setup
except ImportError:
    print('(WARNING: importing distutils, not setuptools!)')
    from distutils.core import setup

import imp
fp, pathname, description = imp.find_module('versioneer')
versioneer = imp.load_module('versioneer', fp, pathname, description)
del imp
versioneer.VCS = 'git'
versioneer.versionfile_source = 'screed/_version.py'
versioneer.versionfile_build = 'screed/_version.py'
versioneer.tag_prefix = 'v'  # i.e. v1.2.0
versioneer.parentdir_prefix = '.'
CMDCLASS = versioneer.get_cmdclass()

setup(name='screed',
      version=versioneer.get_version(),
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
      cmdclass=versioneer.get_cmdclass(),
      install_requires=['bz2file']
      )
