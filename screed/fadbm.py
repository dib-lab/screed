#!/usr/bin/env python

# Copyright (C) 2008-2010, 2014-2015 Michigan State University
# Copyright (C) 2016, The Regents of the University of California.

from __future__ import absolute_import

import sys
from screed import read_fasta_sequences
from screed import DBConstants

# A shell interface to the screed FADBM database writing function
if __name__ == "__main__":
    # Make sure the user entered the command line arguments correctly
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: USAGE IS: %s <dbfilename>\n" % sys.argv[0])
        exit(1)

    filename = sys.argv[1]
    read_fasta_sequences(filename)

    print("Database saved in %s%s" % (sys.argv[1], DBConstants.fileExtension))
    exit(0)
