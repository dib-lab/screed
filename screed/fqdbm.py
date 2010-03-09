#!/usr/bin/env python

# Copyright (c) 2008-2010, Michigan State University

import sys
import __init__
import dbConstants

# A python implementation of the FASTQ database writer
if __name__ == "__main__":
    # Make sure the user entered the command line arguments correctly
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: USAGE IS: %s <dbfilename>\n" % sys.argv[0]);
        exit(1)

    filename = sys.argv[1]
    __init__.read_fastq_sequences(filename)

    print "Database saved in %s_%s" % (sys.argv[1], dbConstants.fileExtension)
