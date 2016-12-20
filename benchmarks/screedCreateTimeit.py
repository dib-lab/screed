#!/usr/bin/env python
# Copyright (c) 2016, The Regents of the University of California.

import sys
import timeit

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s <filename> <fa/fq>" % sys.argv[0]
        exit(1)

    filename = sys.argv[1]
    fafq = sys.argv[2]

    fqrunStatement = """
createscreed.create_db(filename, fastq.FieldTypes, iterfunc)
theFile.close()
"""

    fqsetupStatement = """
import os, sys
thisdir = sys.path[0]
libdir = os.path.abspath(os.path.join(thisdir, '..', 'screed'))
sys.path.insert(0, libdir)
import createscreed
import fastq
FASTQFIELDTYPES = ('name', 'annotations', 'sequence', 'quality')
filename = '%s'
theFile = open(filename, 'rb')
iterfunc = fastq.fastq_iter(theFile)
""" % filename

    farunStatement = """
createscreed.create_db(filename, fasta.FieldTypes, iterfunc)
theFile.close()
"""

    fasetupStatement = """
import os, sys
thisdir = sys.path[0]
libdir = os.path.abspath(os.path.join(thisdir, '..', 'screed'))
sys.path.insert(0, libdir)
import createscreed
import fasta
FASTAFIELDTYPES = ('name', 'description', 'sequence')
filename = '%s'
theFile = open(filename, 'rb')
iterfunc = fasta.fasta_iter(theFile)
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
