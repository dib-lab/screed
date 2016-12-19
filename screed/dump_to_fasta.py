#!/usr/bin/env python

# Copyright (C) 2008-2010, Michigan State University
# Copyright (C) 2016, The Regents of the University of California.

from __future__ import print_function
from screed import ToFasta
import argparse
import sys
import os


# Shell interface to the ToFasta screed conversion function
def main(args):
    parser = argparse.ArgumentParser(
        description="Convert a screed database to a FASTA file")
    parser.add_argument('dbfile')
    parser.add_argument('outputfile')
    args = parser.parse_args(args)

    if not os.path.isfile(args.dbfile):
        print("No such file: %s" % args.dbfile)
        exit(1)
    if os.path.isfile(args.outputfile):
        os.unlink(args.outputfile)

    ToFasta(args.dbfile, args.outputfile)


if __name__ == '__main__':
    main(sys.argv[1])
