#!/usr/bin/env python

import sys
import timeit

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s <filename> <fa/fq>" % sys.argv[0]
        exit(1)

    filename = sys.argv[1]
    fafq = sys.argv[2]

    fqrunStatement = "createscreed.create_db(filename, FASTQFIELDTYPES, iterfunc)\n\
theFile.close()"

    fqsetupStatement = "import os, sys\n\
thisdir = sys.path[0]\n\
libdir = os.path.abspath(os.path.join(thisdir, '..', 'screed'))\n\
sys.path.insert(0, libdir)\n\
import createscreed\n\
from fastq import fqiter\n\
FASTQFIELDTYPES = ('name', 'annotations', 'sequence', 'accuracy')\n\
filename = '%s'\n\
theFile = open(filename, 'rb')\n\
iterfunc = fqiter(theFile)" % filename

    farunStatement = "createscreed.create_db(filename, FASTAFIELDTYPES, iterfunc)\n\
theFile.close()"

    fasetupStatement = "import os, sys\n\
thisdir = sys.path[0]\n\
libdir = os.path.abspath(os.path.join(thisdir, '..', 'screed'))\n\
sys.path.insert(0, libdir)\n\
import createscreed\n\
from fasta import faiter\n\
FASTAFIELDTYPES = ('name', 'description', 'sequence')\n\
filename = '%s'\n\
theFile = open(filename, 'rb')\n\
iterfunc = faiter(theFile)" % filename

    t = None
    if fafq == 'fasta':
        t = timeit.Timer(farunStatement, fasetupStatement)
    elif fafq == 'fastq':
        t = timeit.Timer(fqrunStatement, fqsetupStatement)
    else:
        raise ValueError("Invalid db type specified: %s" % fafq)

    print "[SCREED CREATE]%s:" % filename
    print t.repeat(2, 1)
