#!/usr/bin/env python

# Copyright (c) 2008-2010, Michigan State University

from __init__ import toFastq
import sys, os

## _MAXSEQLINELEN = 80
## null_char = '\"' # ASCII 34, e.g 75% chance of incorrect read

## def getComments(value):
##     """
##     Returns description or annotations from dictionary object
##     """
##     if 'description' in value:
##         return value['description']
##     elif 'annotations' in value:
##         return value['annotations']
##     else:
##         return ''

## def linewrap(longString):
##     """
##     Given a long string of characters, inserts newline characters
##     every _MAXSEQLINELEN characters
##     """
##     res = []
##     begin = 0
##     while begin < len(longString):
##         res.append(longString[begin:begin+_MAXSEQLINELEN])
##         begin += _MAXSEQLINELEN

##     return '\n'.join(res)

## def generateAccuracy(value):
##     """
##     Returns accuracy from value if it exists. Otherwise, makes
##     an accuracy. Accuracy is line wrapped to _MAXSEQLINELEN
##     either way
##     """
##     if 'accuracy' in value:
##         return linewrap(value['accuracy'])

##     return linewrap(null_char * len(value['sequence']))

## def toFastq(dbFile, outputFile):
##     outFile = open(outputFile, 'wb')
##     db = screedDB(dbFile)

##     for value in db.itervalues():
##         outFile.write('@%s %s\n%s\n+\n%s\n' % (value['name'],
##                                                getComments(value),
##                                                linewrap(value['sequence']),
##                                                generateAccuracy(value)))
    
##     db.close()
##     outFile.close()
##     return


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
