#!/usr/bin/env python
# Copyright (c) 2016, The Regents of the University of California.

import sys, os
import random

seqLength = 37

class collectionOFiles(object):
    def __init__(self, baseName, divisions, totalSize):
        self.baseName = baseName
        self.divisions = divisions
        self.totalSize = totalSize

        self.fileHandles = {}
        for i in range(0, divisions):
            filename = self.baseName + "_%d" % i
            fh = open(filename, "wb")
            divisor = 2 ** i

            self.fileHandles[filename]= (fh, self.totalSize/divisor, 0)

    def writeRecord(self, name, sequence, quality):
        toRemove = []
        for filename in self.fileHandles:
            file, limit, count = self.fileHandles[filename]
            file.write("%s\n%s\n+\n%s\n" % (name, sequence, quality))
            count += 1
            if count >= limit:
                file.close()
                toRemove.append(filename)
            else:
                self.fileHandles[filename] = (file, limit, count)

        for fh in toRemove:
            self.fileHandles.pop(fh)

    def finished(self):
        return len(self.fileHandles) == 0


def genSeq(length):
    """
    Generates a sequence with length characters
    """
    choices = ['A','T','C','G']
    result = []
    for i in range(0, length):
        result.append(random.choice(choices))
    return "".join(result)

def genAcc(length):
    """
    Generates a quality with length characters
    """
    choices = ['A','1','7','3','.',';','*','<']
    result = []
    for i in range(0, length):
        result.append(random.choice(choices))
    return "".join(result)

def createFastqFiles(filename, size, divisions):
    cof = collectionOFiles(filename, divisions, size)
    counter = 0
    while(not cof.finished()):
        name = "@HWI-EAS_4_PE-F%d" % counter
        sequence = genSeq(seqLength)
        quality = genAcc(seqLength)
        cof.writeRecord(name, sequence, quality)
        counter += 1
    return

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: <filename> <size> <divisions>"
        exit(1)

    filename = sys.argv[1]
    size = int(sys.argv[2])
    divisions = int(sys.argv[3])

    createFastqFiles(filename, size, divisions)
