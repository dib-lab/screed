#!/usr/bin/env python

# Copyright (C) 2008-2010, 2014-2015 Michigan State University
# Copyright (C) 2016, The Regents of the University of California.

from __future__ import absolute_import

import argparse
import sys
from screed import read_fastq_sequences
from screed import DBConstants


def main(args):
    # Make sure the user entered the command line arguments correctly
    parser = argparse.ArgumentParser(
        description="A shell interface to the screed FQDBM database "
                    "writing function")
    parser.add_argument('filename')
    args = parser.parse_args(args)

    read_fastq_sequences(args.filename)

    print("Database saved in {}{}".format(args.filename, DBConstants.fileExtension))
    exit(0)


if __name__ == "__main__":
	main(sys.argv[1:])
