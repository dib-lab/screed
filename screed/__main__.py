#!/usr/bin/env python

# Copyright (c) 2016, The Regents of the University of California.

from __future__ import absolute_import, print_function

import argparse
import sys

from . import createscreed
from . import dump_fasta
from . import dump_fastq


class ScreedCommands(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="",
            usage='''screed <command> [<args>]

Available:

    db <filename>               Creates a screed database.
    dump_fasta <db> <output>    Convert a screed database to a FASTA file
    dump_fastq <db> <output>    Convert a screed database to a FASTQ file

''')

        commands = {
            'db': createscreed.main,
            'dump_fasta': dump_fasta.main,
            'dump_fastq': dump_fastq.main,
        }

        parser.add_argument('command')
        args = parser.parse_args(sys.argv[1:2])
        if args.command not in commands:
            print('Unrecognized command')
            parser.print_help()
            sys.exit(1)

        cmd = commands[args.command]
        cmd(sys.argv[2:])


def main():
    ScreedCommands()
    return 0

if __name__ == "__main__":
    main()
