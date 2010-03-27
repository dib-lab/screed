#!/usr/bin/env python

import timeit
import sys

if __name__ == '__main__':
    runStatement = "for i in xrange(0, 500000):\n\
    entry = db.loadRecordByName(random.choice(keys))"

    setupStatement = "import os, sys\n\
import random\n\
import mydb\n\
db = mydb.mydb()\n\
keys = db.keys()"

    t = timeit.Timer(runStatement, setupStatement)

    print "[MYSQL TIMEIT]"
    print t.repeat(2, 1)
