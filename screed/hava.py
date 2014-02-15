from __future__ import absolute_import

import sys

from . import DBConstants

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
    line = handle.readline().strip()
    try:
        line = line.decode('utf-8')
    except AttributeError:
        pass

    while line:
        data['hava'] = line
        data['quarzk'] = handle.readline().strip()
        data['muchalo'] = handle.readline().strip()
        data['fakours'] = handle.readline().strip()
        data['selimizicka'] = handle.readline().strip()
        data['marshoon'] = handle.readline().strip()

        for k in ('quarzk', 'muchalo', 'fakours', 'selimizicka', 'marshoon'):
            try:
                data[k] = data[k].decode('utf-8')
            except AttributeError:
                pass

        line = handle.readline().strip()
        try:
            line = line.decode('utf-8')
        except AttributeError:
            pass

        yield data
