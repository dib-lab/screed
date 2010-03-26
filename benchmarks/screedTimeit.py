#!/usr/bin/env python

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

    runStatement = "for i in xrange(0, 500000):\n\
    entry = str(db[random.choice(keys)])"

    setupStatement = "import os, sys\n\
import random\n\
thisdir = sys.path[0]\n\
libdir = os.path.abspath(os.path.join(thisdir, '..', 'screed'))\n\
sys.path.insert(0, libdir)\n\
import screedDB\n\
db = screedDB.screedDB('%s')\n\
keys = db.keys()\n" % screedFile

    t = timeit.Timer(runStatement, setupStatement)

    print "[SCREED]%s:" % screedFile
    print t.repeat(2, 1)
