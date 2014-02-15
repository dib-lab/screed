from __future__ import absolute_import

import sys
from . import DBConstants
from .screedRecord import _screed_record_dict

FieldTypes = (('name', DBConstants._INDEXED_TEXT_KEY),
              ('annotations', DBConstants._STANDARD_TEXT),
              ('sequence', DBConstants._STANDARD_TEXT),
              ('accuracy', DBConstants._STANDARD_TEXT))

def fastq_iter(handle, line=None, parse_description=True):
    """
    Iterator over the given FASTQ file handle returning records. handle
    is a handle to a file opened for reading
    """
    if line is None:
        line = handle.readline()
    line = line.strip()
    try:
        line = line.decode('utf-8')
    except AttributeError:
        pass

    while line:
        data = _screed_record_dict()

        if not line.startswith('@'):
            raise IOError("Bad FASTQ format: no '@' at beginning of line")

        # Try to grab the name and (optional) annotations
        if parse_description:
            try:
                data['name'], data['annotations'] = line[1:].split(' ',1)
            except ValueError: # No optional annotations
                data['name'] = line[1:]
                data['annotations'] = ''
                pass
        else:
            data['name'] = line[1:]
            data['annotations'] = ''

        # Extract the sequence lines
        sequence = []
        line = handle.readline().strip()
        try:
            line = line.decode('utf-8')
        except AttributeError:
            pass

        while not line.startswith('+') and not line.startswith('#'):
            sequence.append(line)
            line = handle.readline().strip()
            try:
                line = line.decode('utf-8')
            except AttributeError:
                pass

        data['sequence'] = ''.join(sequence)

        # Extract the accuracy lines
        accuracy = []
        line = handle.readline().strip()
        try:
            line = line.decode('utf-8')
        except AttributeError:
            pass

        seqlen = len(data['sequence'])
        aclen = 0
        while not line == '' and aclen < seqlen:
            accuracy.append(line)
            aclen += len(line)
            line = handle.readline().strip()
            try:
                line = line.decode('utf-8')
            except AttributeError:
                pass

        data['accuracy'] = ''.join(accuracy)
        if len(data['sequence']) != len(data['accuracy']):
            raise IOError('sequence and accuracy strings must be '\
                          'of equal length')

        yield data
