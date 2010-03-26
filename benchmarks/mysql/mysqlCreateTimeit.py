#!/usr/bin/env python

import sys
import timeit

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s <filename> <fa/fq>" % sys.argv[0]
        exit(1)

    filename = sys.argv[1]
    fafq = sys.argv[2]

    fqrunStatement = "create.create_db(FASTQFIELDTYPES, iterfunc)\n\
theFile.close()"

    fqsetupStatement = "import os, sys\n\
import create\n\
thisdir = sys.path[0]\n\
libdir = os.path.abspath(os.path.join(thisdir, '..', '..', 'screed'))\n\
sys.path.insert(0, libdir)\n\
from fastq import fqiter\n\
create.droptables()\n\
FASTQFIELDTYPES = ('name', 'annotations', 'sequence', 'accuracy')\n\
theFile = open('%s', 'rb')\n\
iterfunc = fqiter(theFile)" % filename

    farunStatement = "create.create_db(FASTAFIELDTYPES, iterfunc)\n\
theFile.close()"

    fasetupStatement = "import os, sys\n\
import create\n\
thisdir = sys.path[0]\n\
libdir = os.path.abspath(os.path.join(thisdir, '..', '..', 'screed'))\n\
sys.path.insert(0, libdir)\n\
from fasta import faiter\n\
create.droptables()\n\
FASTAFIELDTYPES = ('name', 'description', 'sequence')\n\
theFile = open('%s', 'rb')\n\
iterfunc = faiter(theFile)" % filename

    t = None
    if fafq == 'fasta':
        t = timeit.Timer(farunStatement, fasetupStatement)
    elif fafq == 'fastq':
        t = timeit.Timer(fqrunStatement, fqsetupStatement)
    else:
        raise ValueError("Invalid db type specified: %s" % fafq)

    print "[MYSQL]%s:" % filename
    print t.repeat(2, 1)
