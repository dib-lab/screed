# Copyright (c) 2016, The Regents of the University of California.

from __future__ import absolute_import
from functools import total_ordering
import types
from . import DBConstants
import gzip
import bz2
from io import BytesIO

try:
    from collections.abc import MutableMapping
except ImportError:
    import UserDict
    MutableMapping = UserDict.DictMixin


class Record(MutableMapping):
    """
    Simple dict-like record interface with bag behavior.
    """

    def __init__(self, name=None, sequence=None, **kwargs):
        d = dict()
        if name is not None:
            d['name'] = name
        if sequence is not None:
            d['sequence'] = sequence

        d.update(kwargs)

        if 'quality' in d and d['quality'] is None:
            del d['quality']
        self.d = d

    def __setitem__(self, name, value):
        self.d[name] = value

    def __getattr__(self, name):
        try:
            return self.d[name]
        except KeyError:
            raise AttributeError(name)

    def __len__(self):
        return len(self.sequence)

    def keys(self):
        return self.d.keys()

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            trimmed = dict(self.d)
            trimmed['sequence'] = trimmed['sequence'][idx]
            if 'quality' in trimmed:
                trimmed['quality'] = trimmed['quality'][idx]
            return Record(**trimmed)
        return self.d[idx]

    def __delitem__(self, key):
        del self.d[key]

    def __iter__(self):
        return iter(self.d)

    def __repr__(self):
        return repr(self.d)


@total_ordering
class _screed_attr(object):

    """
    Sliceable database object that supports lazy retrieval
    """

    def __init__(self, dbObj, attrName, rowName, queryBy):
        """
        Initializes database object with specific record retrieval
        information
        dbOjb = database handle
        attrName = name of attr in db
        rowName = index/name of row
        queryBy = by name or index
        """
        self._dbObj = dbObj
        self._attrName = attrName
        self._rowName = rowName
        self._queryBy = queryBy

    def __getitem__(self, sliceObj):
        """
        Slicing interface. Returns the slice range given.
        *.start + 1 to be compatible with sqlite's 1 not 0 scheme
        """
        if not isinstance(sliceObj, slice):
            raise TypeError('__getitem__ argument must be of slice type')
        if not sliceObj.start <= sliceObj.stop:  # String reverse in future?
            raise ValueError('start must be less than stop in slice object')
        length = sliceObj.stop - sliceObj.start

        query = 'SELECT substr(%s, %d, %d) FROM %s WHERE %s = ?' \
                % (self._attrName, sliceObj.start + 1, length,
                   DBConstants._DICT_TABLE,
                   self._queryBy)
        cur = self._dbObj.cursor()
        result = cur.execute(query, (str(self._rowName),))
        try:
            subStr, = result.fetchone()
        except TypeError:
            raise KeyError("Key %s not found" % self._rowName)
        return str(subStr)

    def __len__(self):
        """
        Returns the length of the string
        """
        return len(self.__str__())

    def __repr__(self):
        """
        Prints out the name of the class and the name of the sliceable attr
        """
        return "<%s '%s'>" % (self.__class__.__name__, self._attrName)

    def __eq__(self, given):
        """
        Compares attribute to given object in string form
        """
        if isinstance(given, bytes):
            return given == self.__str__()
        else:
            return str(given) == self.__str__()

    def __lt__(self, given):
        if isinstance(given, bytes):
            return self.__str__() < given
        else:
            return self.__str__() < str(given)

    def __str__(self):
        """
        Returns the full attribute as a string
        """
        query = 'SELECT %s FROM %s WHERE %s = ?' \
                % (self._attrName, DBConstants._DICT_TABLE, self._queryBy)
        cur = self._dbObj.cursor()
        result = cur.execute(query, (str(self._rowName),))
        try:
            record, = result.fetchone()
        except TypeError:
            raise KeyError("Key %s not found" % self._rowName)
        return str(record)


def _buildRecord(fieldTuple, dbObj, rowName, queryBy):
    """
    Constructs a dict-like object with record attribute names as keys and
    _screed_attr objects as values
    """

    # Separate the lazy and full retrieval objects
    kvResult = []
    fullRetrievals = []
    for fieldname, role in fieldTuple:
        if role == DBConstants._SLICEABLE_TEXT:
            kvResult.append((fieldname, _screed_attr(dbObj,
                                                     fieldname,
                                                     rowName,
                                                     queryBy)))
        else:
            fullRetrievals.append(fieldname)

    # Retrieve the full text fields from the db
    subs = ','.join(fullRetrievals)
    query = 'SELECT %s FROM %s WHERE %s=?' % \
            (subs, DBConstants._DICT_TABLE, queryBy)
    cur = dbObj.cursor()
    res = cur.execute(query, (rowName,))

    # Add the full text fields to the result tuple list
    data = tuple([str(r) for r in res.fetchone()])
    kvResult.extend(zip(fullRetrievals, data))

    # Hack to make indexing start at 0
    hackedResult = []
    for key, value in kvResult:
        if key == DBConstants._PRIMARY_KEY:
            hackedResult.append((key, int(value) - 1))
        else:
            hackedResult.append((key, value))

    return Record(**dict(hackedResult))


def write_fastx(record, fileobj):
    """Write sequence record to 'fileobj' in FASTA/FASTQ format."""
    isbytesio = isinstance(fileobj, BytesIO)
    iswb = hasattr(fileobj, 'mode') and fileobj.mode == 'wb'
    outputvalid = isbytesio or iswb
    if not outputvalid:
        message = ('cannot call "write_fastx" on object, must be of a file '
                   'handle with mode "wb" or an instance of "BytesIO"')
        raise AttributeError(message)

    defline = record.name
    if hasattr(record, 'description'):
        defline += ' ' + record.description

    if hasattr(record, 'quality'):
        recstr = '@{defline}\n{sequence}\n+\n{quality}\n'.format(
            defline=defline,
            sequence=record.sequence,
            quality=record.quality)
    else:
        recstr = '>{defline}\n{sequence}\n'.format(
            defline=defline,
            sequence=record.sequence)

    fileobj.write(recstr.encode('utf-8'))


def write_fastx_pair(read1, read2, fileobj):
    """Write a pair of sequence records to 'fileobj' in FASTA/FASTQ format."""
    if hasattr(read1, 'quality'):
        assert hasattr(read2, 'quality')
    write_record(read1, fileobj)
    write_record(read2, fileobj)
