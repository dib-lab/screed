#!/usr/bin/env python

import sys
import timeit

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s <filename> <fa/fq>" % sys.argv[0]
        exit(1)

    filename = sys.argv[1]
    fafq = sys.argv[2]

    fqrunStatement = """
createscreed.create_db(filename, FASTQFIELDTYPES, iterfunc)
theFile.close()
"""

    fqsetupStatement = """
import os, sys
thisdir = sys.path[0]
libdir = os.path.abspath(os.path.join(thisdir, '..', 'screed'))
sys.path.insert(0, libdir)
import createscreed
from fastq import fqiter
FASTQFIELDTYPES = ('name', 'annotations', 'sequence', 'accuracy')
filename = '%s'
theFile = open(filename, 'rb')
iterfunc = fqiter(theFile)
""" % filename

    farunStatement = """
createscreed.create_db(filename, FASTAFIELDTYPES, iterfunc)
theFile.close()
"""

    fasetupStatement = """
import os, sys
thisdir = sys.path[0]
libdir = os.path.abspath(os.path.join(thisdir, '..', 'screed'))
sys.path.insert(0, libdir)
import createscreed
from fasta import faiter
FASTAFIELDTYPES = ('name', 'description', 'sequence')
filename = '%s'
theFile = open(filename, 'rb')
iterfunc = faiter(theFile)
""" % filename

    t = None
    if fafq == 'fasta':
        t = timeit.Timer(farunStatement, fasetupStatement)
    elif fafq == 'fastq':
        t = timeit.Timer(fqrunStatement, fqsetupStatement)
    else:
        raise ValueError("Invalid db type specified: %s" % fafq)

    print "[SCREED CREATE]%s:" % filename
    print t.repeat(2, 1)
