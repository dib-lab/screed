# Copyright (c) 2016, The Regents of the University of California.

from __future__ import absolute_import
from . import DBConstants
from .screedRecord import Record
from .utils import to_str

FieldTypes = (('name', DBConstants._INDEXED_TEXT_KEY),
              ('annotations', DBConstants._STANDARD_TEXT),
              ('sequence', DBConstants._STANDARD_TEXT),
              ('quality', DBConstants._STANDARD_TEXT))


def fastq_iter(handle, line=None, parse_description=False):
    """
    Iterator over the given FASTQ file handle returning records. handle
    is a handle to a file opened for reading
    """
    if line is None:
        line = handle.readline()
    line = to_str(line.strip())
    while line:
        data = {}

        if line and not line.startswith('@'):
            raise IOError("Bad FASTQ format: no '@' at beginning of line")

        # Try to grab the name and (optional) annotations
        if parse_description:
            try:
                data['name'], data['annotations'] = line[1:].split(' ', 1)
            except ValueError:  # No optional annotations
                data['name'] = line[1:]
                data['annotations'] = ''
                pass
        else:
            data['name'] = line[1:]
            data['annotations'] = ''

        # Extract the sequence lines
        sequence = []
        line = to_str(handle.readline().strip())
        while line and not line.startswith('+') and not line.startswith('#'):
            sequence.append(line)
            line = to_str(handle.readline().strip())

        data['sequence'] = ''.join(sequence)

        # Extract the quality lines
        quality = []
        line = to_str(handle.readline().strip())
        seqlen = len(data['sequence'])
        aclen = 0
        while not line == '' and aclen < seqlen:
            quality.append(line)
            aclen += len(line)
            line = to_str(handle.readline().strip())

        data['quality'] = ''.join(quality)
        if len(data['sequence']) != len(data['quality']):
            raise IOError('sequence and quality strings must be '
                          'of equal length')

        yield Record(**data)
