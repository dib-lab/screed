import test_fasta
import test_fastq
import tempfile
import os
import sys
import io
import threading
import subprocess
import screed
from nose.plugins.attrib import attr
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

    # make a fifo to simulate streaming
    os.mkfifo(fifo)

    exception = []
    # FIFOs MUST BE OPENED FOR READING BEFORE THEY ARE WRITTEN TO
    # If this isn't done, they will BLOCK and things will hang.
    # rvalues will hold the return from the threaded function
    thread = threading.Thread(target=streamer_reader, args=[fifo, exception])
    thread.start()

    ifile = io.open(ifilename, 'rb')
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
    streamer(os.path.join(os.path.dirname(__file__), 'test.fa'))


def test_stream_fq():
    streamer(os.path.join(os.path.dirname(__file__), 'test.fastq'))


@attr('known_failing')
def test_stream_fa_gz():
    streamer(os.path.join(os.path.dirname(__file__), 'test.fa.gz'))


def test_stream_gz_fail():
    try:
        streamer(os.path.join(os.path.dirname(__file__), 'test.fastq.gz'))
        assert 0, "This should not work yet"
    except ValueError as err:
        print str(err)


@attr('known_failing')
def test_stream_fq_gz():
    streamer(os.path.join(os.path.dirname(__file__), 'test.fastq.gz'))


def test_stream_fa_bz2():
    streamer(os.path.join(os.path.dirname(__file__), 'test.fa.bz2'))


def test_stream_fq_bz2():
    streamer(os.path.join(os.path.dirname(__file__), 'test.fastq.bz2'))
