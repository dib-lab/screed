#!/usr/bin/env python

import sys
import seqparse
import screedExtension

# A python implementation of the FASTA database writer
if __name__ == "__main__":
    # Make sure the user entered the command line arguments correctly
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: USAGE IS: %s <dbfilename>\n" % sys.argv[0])
        exit(1)

    filename = sys.argv[1]
    seqparse.read_fasta_sequences(filename)
    
    print "Database saved in %s_%s" % (sys.argv[1], screedExtension.fileExtension)

