#!/usr/bin/env python

# Copyright (c) 2008-2010, Michigan State University

from __init__ import screedDB
import sys, os

_MAXSEQLINELEN = 80

def toFastq(dbFile, outputFile):
    outFile = open(outputFile, 'wb')
    db = screedDB(dbFile)

    for value in db.itervalues():
        outFile.write('@%s\n%s\n+\n%s\n' % (value['name'], value['sequence'],
                                            value['accuracy']))
    
    db.close()
    outFile.close()
    return


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s <dbfilename> <outputfilename>" % sys.argv[0]
        exit(1)

    dbFile = sys.argv[1]
    outputFile = sys.argv[2]

    if not os.path.isfile(dbFile):
        print "No such file: %s" % dbFile
        exit(1)
    if os.path.isfile(outputFile):
        os.unlink(outputFile)
    
    toFastq(dbFile, outputFile)
