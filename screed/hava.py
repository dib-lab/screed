# Copyright (c) 2016, The Regents of the University of California.

from __future__ import absolute_import
from . import DBConstants
from .utils import to_str

FieldTypes = (('hava', DBConstants._INDEXED_TEXT_KEY),
              ('quarzk', DBConstants._STANDARD_TEXT),
              ('muchalo', DBConstants._STANDARD_TEXT),
              ('fakours', DBConstants._STANDARD_TEXT),
              ('selimizicka', DBConstants._STANDARD_TEXT),
              ('marshoon', DBConstants._STANDARD_TEXT))


def hava_iter(handle):
    """
    Iterator over a 'hava' sequence file, returning records. handle
    is a handle to a file opened for reading
    """
    data = {}
    line = to_str(handle.readline().strip())
    while line:
        data['hava'] = line
        data['quarzk'] = to_str(handle.readline().strip())
        data['muchalo'] = to_str(handle.readline().strip())
        data['fakours'] = to_str(handle.readline().strip())
        data['selimizicka'] = to_str(handle.readline().strip())
        data['marshoon'] = to_str(handle.readline().strip())

        line = to_str(handle.readline().strip())
        yield data
