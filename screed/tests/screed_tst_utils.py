#
# This file is part of screed, http://github.com/dib-lab/screed/, and is
# Copyright (C) Michigan State University, 2009-2015. It is licensed under
# the three-clause BSD license; see doc/LICENSE.txt.
# Contact: khmer-project@idyll.org
#
# This file has been modified from the khmer project at
# https://github.com/dib-lab/khmer/blob/a8356b7abbebf8540c7656378b1459442b781f87/tests/khmer_tst_utils.py
#

import tempfile
import os
import shutil
from pkg_resources import Requirement, resource_filename, ResolutionError
from io import StringIO
import sys
import traceback


def get_test_data(filename):
    filepath = None
    try:
        filepath = resource_filename(
            Requirement.parse("screed"), "screed/tests/" + filename)
    except ResolutionError:
        pass
    if not filepath or not os.path.isfile(filepath):
        filepath = os.path.join(os.path.dirname(__file__), 'test-data',
                                filename)
    return filepath

cleanup_list = []


def get_temp_filename(filename, tempdir=None):
    if tempdir is None:
        tempdir = tempfile.mkdtemp(prefix='screedtest_')
        cleanup_list.append(tempdir)

    return os.path.join(tempdir, filename)


def cleanup():
    global cleanup_list

    for path in cleanup_list:
        shutil.rmtree(path, ignore_errors=True)
    cleanup_list = []
