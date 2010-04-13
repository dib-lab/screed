#!/usr/bin/env python

import timeit
import sys

if __name__ == '__main__':
    runStatement = """
for i in xrange(0, 100000):
    entry = db.loadRecordByName(random.choice(keys))
"""

    setupStatement = """
import os, sys
import random
import pgdb
db = pgdb.pgdb()
keys = db.keys()
"""

    t = timeit.Timer(runStatement, setupStatement)

    print "[PGRES RUN]"
    print t.repeat(2, 1)
