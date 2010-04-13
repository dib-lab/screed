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
import mydb
db = mydb.mydb()
keys = db.keys()
"""

    t = timeit.Timer(runStatement, setupStatement)

    print "[MYSQL TIMEIT]"
    print t.repeat(2, 1)
