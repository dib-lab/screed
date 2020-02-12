#!/usr/bin/env python
# Copyright (c) 2016, The Regents of the University of California.
from __future__ import print_function
try:
    from setuptools import setup
except ImportError:
    print('(WARNING: importing distutils, not setuptools!)')
    from distutils.core import setup

import versioneer

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='screed',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Luiz Irber, Peter Cock, Michael R. Crusoe, Jacob Fenton, '
             'Thomas Fenzl, Sarah Guermond, Tim Head, Mark Mandel, '
             'Kevin D. Murray, Alexander Nolley, Camille Scott, '
             'Daniel Standage, Benjamin R. Taylor, Michael Wright, en zyme, '
             'C. Titus Brown',
      author_email='ctbrown@ucdavis.edu',
      url='http://github.com/dib-lab/screed/',
      zip_safe=False,
      include_package_data=True,
      packages=['screed', 'screed.tests'],
      package_data={
          'screed.tests': ['test.*', 'test-whitespace.fa', 'empty.fa']},
      license='BSD',
      setup_requires=['pytest-runner'],
      tests_require=['pytest >= 3.0', 'pytest-cov'],
      install_requires=['bz2file'],
      entry_points={'console_scripts': [
          'screed = screed.__main__:main'
          ]
      })
