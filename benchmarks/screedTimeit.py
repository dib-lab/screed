#!/usr/bin/env python
# Copyright (c) 2016, The Regents of the University of California.

import timeit
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s <filename>" % sys.argv[0]
        exit(1)

    screedFile = sys.argv[1]
    if not os.path.isfile(screedFile):
        print "No such file: %s" % screedFile
        exit(1)

    runStatement = """
for i in xrange(0, 100000):
    entry = str(db[random.choice(keys)].sequence)
"""

    setupStatement = """
import os, sys
import random
thisdir = sys.path[0]
libdir = os.path.abspath(os.path.join(thisdir, '..'))
sys.path.insert(0, libdir)
import screed
db = screed.openscreed.ScreedDB('%s')
keys = db.keys()
""" % screedFile

    t = timeit.Timer(runStatement, setupStatement)

    print "[SCREED RUN]%s:" % screedFile
    print t.repeat(2, 1)
