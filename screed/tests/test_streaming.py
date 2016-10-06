# Copyright (c) 2008-2015, Michigan State University

from __future__ import print_function
from __future__ import absolute_import

import tempfile
import os
import sys
import io
import threading
import subprocess

import pytest

import screed
from . import screed_tst_utils as utils
from . import test_fasta
from . import test_fastq
from screed.DBConstants import fileExtension


def streamer_reader(ifilename, exception):
    try:
        for read in screed.open(ifilename):
            pass
    except Exception as e:
        exception.append(e)


def streamer(ifilename):

    # Get temp filenames, etc.
    in_dir = tempfile.mkdtemp(prefix="screedtest_")
    fifo = os.path.join(in_dir, 'fifo')
    ifile = io.open(ifilename, 'rb')

    # make a fifo to simulate streaming
    os.mkfifo(fifo)

    exception = []
    # FIFOs MUST BE OPENED FOR READING BEFORE THEY ARE WRITTEN TO
    # If this isn't done, they will BLOCK and things will hang.
    # rvalues will hold the return from the threaded function
    thread = threading.Thread(target=streamer_reader, args=[fifo, exception])
    thread.start()

    fifofile = io.open(fifo, 'wb')
    # read binary to handle compressed files
    chunk = ifile.read(8192)
    while len(chunk) > 0:
        fifofile.write(chunk)
        chunk = ifile.read(8192)

    fifofile.close()

    thread.join()

    if len(exception) > 0:
        raise exception[0]


def test_stream_fa():
    streamer(utils.get_test_data('test.fa'))


def test_stream_fq():
    streamer(utils.get_test_data('test.fastq'))


@pytest.mark.known_failing
def test_stream_fa_gz():
    streamer(utils.get_test_data('test.fa.gz'))


def test_stream_gz_fail():
    try:
        streamer(utils.get_test_data('test.fastq.gz'))
        assert 0, "This should not work yet"
    except ValueError as err:
        print(str(err))


@pytest.mark.known_failing
def test_stream_fq_gz():
    streamer(utils.get_test_data('test.fastq.gz'))


def test_stream_fa_bz2():
    streamer(utils.get_test_data('test.fa.bz2'))


def test_stream_fq_bz2():
    streamer(utils.get_test_data('test.fastq.bz2'))
