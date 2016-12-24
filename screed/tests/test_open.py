# Copyright (c) 2008-2015, Michigan State University
"""
Test `screed.open`.
"""

from __future__ import absolute_import

import os.path
import sys
import subprocess

from . import screed_tst_utils as utils
import screed
import screed.openscreed


def test_empty_open():
    filename = utils.get_test_data('empty.fa')
    assert len(list(screed.open(filename))) == 0


def test_open_maps_dash():
    """Test mapping of '-'."""
    #  pylint: disable=protected-access
    filename = '-'
    mapped = screed.openscreed._normalize_filename(filename)

    assert '/dev/stdin' == mapped


def test_open_stdin():
    """Test feeding data through stdin.

    Uses a subprocess with the data file directlyused as stdin."""
    filename1 = utils.get_test_data('test.fa')
    command = ["python", "-c", "from __future__ import print_function;"
               "import screed; print(list(screed.open('-')))"]
    with open(filename1, 'rb') as data_file:
        output = subprocess.Popen(command,
                                  stdin=data_file, universal_newlines=True,
                                  stdout=subprocess.PIPE).communicate()[0]
        assert "'name': 'ENSMICT00000012722'" \
            or "'name': u'ENSMICT00000012722'" in output, output


def test_simple_open():
    filename = utils.get_test_data('test.fa')

    n = -1
    for n, record in enumerate(screed.open(filename, parse_description=True)):
        assert record.name == 'ENSMICT00000012722'
        break
    assert n == 0, n


def test_simple_open_fq():
    filename = utils.get_test_data('test.fastq')

    n = -1
    for n, record in enumerate(screed.open(filename)):
        assert record.name == 'HWI-EAS_4_PE-FC20GCB:2:1:492:573/2'
        break
    assert n == 0


def test_gz_open():
    filename1 = utils.get_test_data('test.fa')
    filename2 = utils.get_test_data('test.fa.gz')
    for n, (r1, r2) in enumerate(zip(screed.open(filename1),
                                     screed.open(filename2))):
        assert r1.name == r2.name

    assert n > 0


def test_bz2_open():
    filename1 = utils.get_test_data('test.fa')
    filename2 = utils.get_test_data('test.fa.bz2')
    for n, (r1, r2) in enumerate(zip(screed.open(filename1),
                                     screed.open(filename2))):
        assert r1.name == r2.name

    assert n > 0


def test_gz_open_fastq():
    filename1 = utils.get_test_data('test.fastq')
    filename2 = utils.get_test_data('test.fastq.gz')
    for n, (r1, r2) in enumerate(zip(screed.open(filename1),
                                     screed.open(filename2))):
        assert r1.name == r2.name

    assert n > 0


def test_unknown_fileformat():

    try:
        screed.open(__file__)
    except ValueError as err:
        assert "unknown file format" in str(err)
