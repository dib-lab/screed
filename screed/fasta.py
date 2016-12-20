# Copyright (c) 2016, The Regents of the University of California.

from __future__ import absolute_import
from . import DBConstants
from .screedRecord import Record
from .utils import to_str

FieldTypes = (('name', DBConstants._INDEXED_TEXT_KEY),
              ('description', DBConstants._STANDARD_TEXT),
              ('sequence', DBConstants._SLICEABLE_TEXT))


def fasta_iter(handle, parse_description=False, line=None):
    """
    Iterator over the given FASTA file handle, returning records. handle
    is a handle to a file opened for reading
    """
    if line is None:
        line = handle.readline()

    while line:
        data = {}

        line = to_str(line.strip())
        if not line.startswith('>'):
            raise IOError("Bad FASTA format: no '>' at beginning of line")

        if parse_description:  # Try to grab the name and optional description
            try:
                data['name'], data['description'] = line[1:].split(' ', 1)
            except ValueError:  # No optional description
                data['name'] = line[1:]
                data['description'] = ''
        else:
            data['name'] = line[1:]
            data['description'] = ''

        data['name'] = data['name'].strip()
        data['description'] = data['description'].strip()

        # Collect sequence lines into a list
        sequenceList = []
        line = to_str(handle.readline())
        while line and not line.startswith('>'):
            sequenceList.append(line.strip())
            line = to_str(handle.readline())

        data['sequence'] = ''.join(sequenceList)
        yield Record(**data)
