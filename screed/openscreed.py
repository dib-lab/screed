# Copyright (c) 2008, Michigan State University.
"""Reader and writer for screed."""

from __future__ import absolute_import

import os
import io
import sys
import gzip
import bz2file
try:
    from collections.abc import MutableMapping
except ImportError:
    import UserDict
    MutableMapping = UserDict.DictMixin

try:
    import sqlite3
except ImportError:
    pass

from . import DBConstants
from . import screedRecord
from .fastq import fastq_iter
from .fasta import fasta_iter
from .utils import to_str


def _normalize_filename(filename):
    """Map '-' to '/dev/stdin' to handle the usual shortcut."""
    if filename == '-':
        filename = '/dev/stdin'
    return filename


class Open(object):
    def __init__(self, filename, *args, **kwargs):
        self.sequencefile = None
        self.iter_fn = self.open_reader(filename, *args, **kwargs)
        if self.iter_fn:
            self.__name__ = self.iter_fn.__name__

    def open_reader(self, filename, *args, **kwargs):
        """
        Make a best-effort guess as to how to parse the given sequence file.

        Handles '-' as shortcut for stdin.
        Deals with .gz, FASTA, and FASTQ records.
        """
        magic_dict = {
            b"\x1f\x8b\x08": "gz",
            b"\x42\x5a\x68": "bz2",
            # "\x50\x4b\x03\x04": "zip"
        }  # Inspired by http://stackoverflow.com/a/13044946/1585509
        filename = _normalize_filename(filename)
        bufferedfile = io.open(file=filename, mode='rb', buffering=8192)
        num_bytes_to_peek = max(len(x) for x in magic_dict)
        file_start = bufferedfile.peek(num_bytes_to_peek)
        compression = None
        for magic, ftype in magic_dict.items():
            if file_start.startswith(magic):
                compression = ftype
                break
        if compression is 'bz2':
            sequencefile = bz2file.BZ2File(filename=bufferedfile)
            peek = sequencefile.peek(1)
        elif compression is 'gz':
            if not bufferedfile.seekable():
                bufferedfile.close()
                raise ValueError("gziped data not streamable, pipe through zcat \
                                first")
            peek = gzip.GzipFile(filename=filename).read(1)
            sequencefile = gzip.GzipFile(filename=filename)
        else:
            peek = bufferedfile.peek(1)
            sequencefile = bufferedfile

        iter_fn = None
        try:
            first_char = peek[0]
        except IndexError as err:
            return []  # empty file

        try:
            first_char = chr(first_char)
        except TypeError:
            pass

        if first_char == '>':
            iter_fn = fasta_iter
        elif first_char == '@':
            iter_fn = fastq_iter

        if iter_fn is None:
            raise ValueError("unknown file format for '%s'" % filename)

        self.sequencefile = sequencefile
        return iter_fn(sequencefile, *args, **kwargs)

    def __enter__(self):
        return self.iter_fn

    def __exit__(self, *exc_info):
        self.close()

    def __iter__(self):
        if self.iter_fn:
            return self.iter_fn
        return iter(())

    def close(self):
        if self.sequencefile is not None:
            self.sequencefile.close()


class ScreedDB(MutableMapping):

    """
    Core on-disk dictionary interface for reading screed databases. Accepts a
    path string to a screed database
    """

    def __init__(self, filepath):
        try:
            sqlite3
        except NameError:
            raise Exception("error: sqlite3 is needed for this " +
                            "functionality, but is not installed.")

        self._filepath = filepath
        self._db = None
        if not self._filepath.endswith(DBConstants.fileExtension):
            self._filepath += DBConstants.fileExtension

        if not os.path.exists(self._filepath):
            raise ValueError('No such file: %s' % self._filepath)

        self._db = sqlite3.connect(self._filepath)
        cursor = self._db.cursor()

        # Make sure the database is a prepared screed database
        query = "SELECT name FROM sqlite_master WHERE type='table' "\
                "ORDER BY name"
        res = cursor.execute(query)
        try:
            dictionary_table, = res.fetchone()
            admin_table, = res.fetchone()

            if dictionary_table != DBConstants._DICT_TABLE:
                raise TypeError
            if admin_table != DBConstants._SCREEDADMIN:
                raise TypeError

        except TypeError:
            self._db.close()
            raise TypeError("Database %s is not a proper screed database"
                            % self._filepath)

        nothing = res.fetchone()
        if nothing is not None:
            self._db.close()
            raise TypeError("Database %s has too many tables." % filename)

        # Store the fields of the admin table in a tuple
        query = "SELECT %s, %s FROM %s" % \
            (DBConstants._FIELDNAME,
             DBConstants._ROLENAME,
             DBConstants._SCREEDADMIN)
        res = cursor.execute(query)
        self.fields = tuple([(str(field), role) for field, role in res])

        # Indexed text column for querying, search fields to find
        self._queryBy = self.fields[1][0]
        for fieldname, role in self.fields:
            if role == DBConstants._INDEXED_TEXT_KEY:
                self._queryBy = fieldname

        # Sqlite PRAGMA settings for speed
        cursor.execute("PRAGMA cache_size=2000")

        # Retrieve the length of the database
        query = 'SELECT MAX(%s) FROM %s' % (DBConstants._PRIMARY_KEY,
                                            DBConstants._DICT_TABLE)
        self._len, = cursor.execute(query).fetchone()

    def __del__(self):
        """
        Alias for close()
        """
        self.close()

    def close(self):
        """
        Closes the sqlite database handle
        """
        if self._db is not None:
            self._db.close()
            self._db = None

    def __getitem__(self, key):
        """
        Retrieves from database the record with the key 'key'
        """
        cursor = self._db.cursor()
        key = str(key)  # So lazy retrieval objectes are evaluated
        query = 'SELECT %s FROM %s WHERE %s=?' % (self._queryBy,
                                                  DBConstants._DICT_TABLE,
                                                  self._queryBy)
        res = cursor.execute(query, (key,))
        if res.fetchone() is None:
            raise KeyError("Key %s not found" % key)
        return screedRecord._buildRecord(self.fields, self._db,
                                         key,
                                         self._queryBy)

    def values(self):
        """
        Retrieves all records from the database and returns them as a list
        """
        return list(self.itervalues())

    def items(self):
        """
        Retrieves all records from the database and returns them as a list of
        (key, record) tuple pairs
        """
        return list(self.iteritems())

    def loadRecordByIndex(self, index):
        """
        Retrieves record from database at the given index
        """
        cursor = self._db.cursor()
        index = int(index) + 1  # Hack to make indexing start at 0
        query = 'SELECT %s FROM %s WHERE %s=?' % (DBConstants._PRIMARY_KEY,
                                                  DBConstants._DICT_TABLE,
                                                  DBConstants._PRIMARY_KEY)
        res = cursor.execute(query, (index,))
        if res.fetchone() is None:
            raise KeyError("Index %d not found" % index)
        return screedRecord._buildRecord(self.fields, self._db,
                                         index,
                                         DBConstants._PRIMARY_KEY)

    def __len__(self):
        """
        Returns the number of records in the database
        """
        return self._len

    def keys(self):
        """
        Returns a list of keys in the database
        """
        return list(self.iterkeys())

    def __repr__(self):
        """
        Returns a string with some general information about the database
        """
        return "<%s, '%s'>" % (self.__class__.__name__,
                               self._filepath)

    def itervalues(self):
        """
        Iterator over records in the database
        """
        for index in range(1, self.__len__() + 1):
            yield screedRecord._buildRecord(self.fields, self._db,
                                            index,
                                            DBConstants._PRIMARY_KEY)

    def iterkeys(self):
        """
        Iterator over keys in the database
        """
        cursor = self._db.cursor()
        query = 'SELECT %s FROM %s ORDER BY id' % (
            self._queryBy, DBConstants._DICT_TABLE)
        for key, in cursor.execute(query):
            yield key

    def __iter__(self):
        return self.iterkeys()

    def iteritems(self):
        """
        Iterator returning a (index, record) pairs
        """
        for v in self.itervalues():
            yield v[DBConstants._PRIMARY_KEY], v

    def has_key(self, key):
        """
        Returns true if given key exists in database, false otherwise
        """
        return key in self

    def copy(self):
        """
        Returns shallow copy
        """
        return self

    def __contains__(self, key):
        """
        Returns true if given key exists in database, false otherwise
        """
        cursor = self._db.cursor()
        query = 'SELECT %s FROM %s WHERE %s = ?' % \
                (self._queryBy, DBConstants._DICT_TABLE, self._queryBy)
        if cursor.execute(query, (key,)).fetchone() is None:
            return False
        return True

    # Here follow the methods that are not implemented

    def __setitem__(self, something):
        """
        Not implemented (Read-only database)
        """
        raise NotImplementedError

    def __delitem__(self, something):
        """
        Not implemented (Read-only database)
        """
        raise NotImplementedError

    def clear(self):
        """
        Not implemented (Read-only database)
        """
        raise NotImplementedError

    def update(self, something):
        """
        Not implemented (Read-only database)
        """
        raise NotImplementedError

    def setdefault(self, something):
        """
        Not implemented (Read-only database)
        """
        raise NotImplementedError

    def pop(self):
        """
        Not implemented (Read-only database)
        """
        raise NotImplementedError

    def popitem(self):
        """
        Not implemented (Read-only database)
        """
        raise NotImplementedError
