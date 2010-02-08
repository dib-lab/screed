#!/usr/bin/env python

# Copyright (c) 2008-2010, Michigan State University

import screedDB
import sys, os

_MAXSEQLINELEN = 80

class _seq_iter(object):
    """
    Yields string of characters of _MAXSEQLINELEN characters in length
    from a given input string
    """
    def __init__(self, sequence):
        self.seq = sequence
        self.len = len(sequence)
        self.begin = 0
        self.end = 0
        self.step = _MAXSEQLINELEN

    def __iter__(self):
        return self

    def next(self):
        if self.begin == self.len:
            raise StopIteration

        self.end += self.step
        if self.end > self.len:
            self.end = self.len

        res = self.seq[self.begin:self.end]
        self.begin = self.end
        return res

def toFasta(dbFile, outputFile):
    outFile = open(outputFile, 'wb')
    db = screedDB.screedDB(dbFile)

    for value in db.itervalues():
        outFile.write('>%s %s\n' % (value['name'], value['description']))
        # Write the sequence as multiple if longer than self.step
        seq = _seq_iter(value['sequence'])
        for line in seq:
            outFile.write('%s\n' % line)
    
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
    
    toFasta(dbFile, outputFile)
