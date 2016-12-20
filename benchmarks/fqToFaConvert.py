#!/usr/bin/env python
# Copyright (c) 2016, The Regents of the University of California.
import sys
import os

class fastaModel(object):
    """
    Contains methods for writing data to a file in the fasta format
    """
    def __init__(self, fileHandle):
        self.fileHandle = fileHandle
        self.currSeq = ""

    def writeName(self, name):
        """
        Writes the given name to the fileHandle in the fasta format
        """
        self.fileHandle.write(">%s " % name.strip())

    def writeDescription(self, description):
        """
        Writes the given description and the stored sequence to the file
        """
        self.fileHandle.write("%s\n%s\n" % (description.strip(), self.currSeq))

    def writeSequence(self, sequence):
        """
        Stores the given sequence until a call to writeDescription is made
        so that the description and sequence will be stored in the correct
        fasta order
        """
        self.currSeq = sequence.strip()

def convertFastqToFasta(inputFilename, outputFilename):
    """
    Converts the given fastq file (inputFilename) to an equilivalent fasta file
    (outputFilename). The fastq's quality information is converted to a fasta's
    'description' field. Sequence and name fields are left alone
    """

    inputFile = open(inputFilename, "rb")
    outputFile = open(outputFilename, "wb")

    model = fastaModel(outputFile)

    for line in inputFile:
        if line.startswith("@"): # Line is a name
            model.writeName(line[1:])
        elif line.startswith('+'): # Next line is the quality
            quality = inputFile.next()
            model.writeDescription(quality)
        else: # Line is the sequence
            model.writeSequence(line)

    outputFile.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: <input filename> <output filename>"
        exit(1)

    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]

    if not os.path.isfile(inputFilename):
        print "Error: %s doesn't exist" % inputFilename
        exit(2)

    convertFastqToFasta(inputFilename, outputFilename)
