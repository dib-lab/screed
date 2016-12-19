#!/usr/bin/env python

# Copyright (C) 2016, The Regents of the University of California.

from __future__ import absolute_import

import argparse
import sys

from . import fqdbm
from . import fadbm
from . import createscreed


class ScreedCommands(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="",
            usage='''screed <command> [<args>]

Commands can be:

    createdb <filename> "Creates a screed database."
    fadbm <filename>    "Creates a screed FADBM database."
    fqdbm <filename>    "Creates a screed FQDBM database."
''')

        commands = {
            'fadbm': fadbm.main,
            'fqdbm': fqdbm.main,
            'createdb': createscreed.main,
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
