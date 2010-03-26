#!/usr/bin/env python

import timeit
import sys

if __name__ == '__main__':
    runStatement = "for i in xrange(0, 500000):\n\
    entry = db.loadRecordByName(random.choice(keys))"

    setupStatement = "import os, sys\n\
import random\n\
import pgdb\n\
db = pgdb.pgdb()\n\
keys = db.keys()"

    t = timeit.Timer(runStatement, setupStatement)

    print t.repeat(2, 1)
