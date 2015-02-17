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
create.create_db(FASTQFIELDTYPES, iterfunc)
theFile.close()
"""

    fqsetupStatement = """
import os, sys
import create
thisdir = sys.path[0]
libdir = os.path.abspath(os.path.join(thisdir, '..', '..', 'screed'))
sys.path.insert(0, libdir)
from fastq import fqiter
create.droptables()
FASTQFIELDTYPES = ('name', 'annotations', 'sequence', 'quality')
theFile = open('%s', 'rb')
iterfunc = fqiter(theFile)
""" % filename

    farunStatement = """
create.create_db(FASTAFIELDTYPES, iterfunc)
theFile.close()
"""

    fasetupStatement = """
import os, sys
import create
thisdir = sys.path[0]
libdir = os.path.abspath(os.path.join(thisdir, '..', '..', 'screed'))
sys.path.insert(0, libdir)
from fasta import faiter
create.droptables()
FASTAFIELDTYPES = ('name', 'description', 'sequence')
theFile = open('%s', 'rb')
iterfunc = faiter(theFile)
""" % filename

    t = None
    if fafq == 'fasta':
        t = timeit.Timer(farunStatement, fasetupStatement)
    elif fafq == 'fastq':
        t = timeit.Timer(fqrunStatement, fqsetupStatement)
    else:
        raise ValueError("Invalid db type specified: %s" % fafq)

    print "[PGRES CREATE]%s:" % filename
    print t.repeat(2, 1)
