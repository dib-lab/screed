#!/usr/bin/env python
# Copyright (c) 2016, The Regents of the University of California.

import sys, os
import random

seqLength = (8000, 12000)

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

    def writeRecord(self, name, description, sequence):
        toRemove = []
        for filename in self.fileHandles:
            file, limit, count = self.fileHandles[filename]
            file.write("%s %s\n%s\n" % (name, description, sequence))
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

def genSeq(min, max):
    """
    Generates a sequence with min <= length <= max
    """
    choices = ['A','T','C','G']
    result = []
    length = random.randrange(min, max)
    for i in range(0, length):
        result.append(random.choice(choices))
        if i % 80 == 0:
            result.append('\n')
    return "".join(result)

def createFastaFiles(filename, size, divisions):
    cof = collectionOFiles(filename, divisions, size)
    counter = 0
    description="cdna:Genscan chromosome:PPYG2:6_qbl_hap2_random:95622:98297:1"
    while(not cof.finished()):
        name = ">GENSCAN00%d" % counter
        sequence = genSeq(seqLength[0], seqLength[1])
        cof.writeRecord(name, description, sequence)
        counter += 1
    return

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: <filename> <size> <divisions>"
        exit(1)

    filename = sys.argv[1]
    size = int(sys.argv[2])
    divisions = int(sys.argv[3])

    createFastaFiles(filename, size, divisions)
