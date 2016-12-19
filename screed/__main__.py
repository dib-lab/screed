#!/usr/bin/env python

# Copyright (C) 2016, The Regents of the University of California.

from __future__ import absolute_import, print_function

import argparse
import sys

from . import fqdbm
from . import fadbm
from . import createscreed
from . import dump_to_fasta
from . import dump_to_fastq


class ScreedCommands(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="",
            usage='''screed <command> [<args>]

Commands can be:

    db <filename> "Creates a screed database."
''')

        commands = {
            'db': createscreed.main,
            'dump_to_fasta': dump_to_fasta.main,
            'dump_to_fastq': dump_to_fastq.main,
        }

        parser.add_argument('command')
        args = parser.parse_args(sys.argv[1:2])
        if args.command not in commands:
            print('Unrecognized command')
            parser.print_help()
            sys.exit(1)

        cmd = commands[args.command]
        print('# executing: %s' % args.command, file=sys.stderr)
        cmd(sys.argv[2:])


def main():
    ScreedCommands()
    return 0

if __name__ == "__main__":
    main()
