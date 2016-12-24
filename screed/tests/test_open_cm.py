# Copyright (c) 2008-2015, Michigan State University
"""
Test the use of `screed.open` as a ContextManager.
"""

from . import screed_tst_utils as utils
import screed
import screed.openscreed


def test_empty_open():
    filename = utils.get_test_data('empty.fa')
    with screed.open(filename) as f:
        assert len(list(f)) == 0


def test_simple_open():
    filename = utils.get_test_data('test.fa')

    n = -1
    with screed.open(filename, parse_description=True) as f:
        for n, record in enumerate(f):
            assert record.name == 'ENSMICT00000012722'
            break

        assert n == 0, n


def test_simple_close():
    filename = utils.get_test_data('test.fa')

    n = -1
    f = screed.open(filename, parse_description=True)
    for n, record in enumerate(f):
        assert record.name == 'ENSMICT00000012722'
        break

    assert n == 0, n
    f.close()


def test_simple_open_fq():
    filename = utils.get_test_data('test.fastq')

    n = -1
    with screed.open(filename) as f:
        for n, record in enumerate(f):
            assert record.name == 'HWI-EAS_4_PE-FC20GCB:2:1:492:573/2'
            break

        assert n == 0


def test_gz_open():
    filename1 = utils.get_test_data('test.fa')
    filename2 = utils.get_test_data('test.fa.gz')
    with screed.open(filename1) as f1, screed.open(filename2) as f2:
        for n, (r1, r2) in enumerate(zip(f1, f2)):
            assert r1.name == r2.name

        assert n > 0


def test_bz2_open():
    filename1 = utils.get_test_data('test.fa')
    filename2 = utils.get_test_data('test.fa.bz2')
    with screed.open(filename1) as f1, screed.open(filename2) as f2:
        for n, (r1, r2) in enumerate(zip(f1, f2)):
            assert r1.name == r2.name

        assert n > 0


def test_gz_open_fastq():
    filename1 = utils.get_test_data('test.fastq')
    filename2 = utils.get_test_data('test.fastq.gz')
    with screed.open(filename1) as f1, screed.open(filename2) as f2:
        for n, (r1, r2) in enumerate(zip(f1, f2)):
            assert r1.name == r2.name

        assert n > 0


def test_unknown_fileformat():
    try:
        with screed.open(__file__):
            pass
    except ValueError as err:
        assert "unknown file format" in str(err)
