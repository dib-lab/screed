import os
import types
import UserDict
import sqlite3
import gzip
import bz2file
import zipfile
import io
import sys

import DBConstants
import screedRecord
from fastq import fastq_iter, FASTQ_Writer
from fasta import fasta_iter, FASTA_Writer


def get_writer_class(read_iter):
    if read_iter.__name__ == 'fasta_iter':
        return FASTA_Writer
    elif read_iter.__name__ == 'fastq_iter':
        return FASTQ_Writer


def open_writer(inp_filename, outp_filename):
    read_iter = open_reader(inp_filename)
    klass = get_writer_class(read_iter)
    return klass(outp_filename)


def open_reader(filename, *args, **kwargs):
    """
    Make a best-effort guess as to how to open/parse the given sequence file.

    Deals with .gz, FASTA, and FASTQ records.
    """
    magic_dict = {
        "\x1f\x8b\x08": "gz",
        "\x42\x5a\x68": "bz2",
        "\x50\x4b\x03\x04": "zip"
    }  # Inspired by http://stackoverflow.com/a/13044946/1585509
    bufferedfile = io.open(file=filename, mode='rb')
    file_start = bufferedfile.peek(max(len(x) for x in magic_dict))
    compression = None
    for magic, ftype in magic_dict.items():
        if file_start.startswith(magic):
            compression = ftype
            break
    if sys.version_info[1] >= 7:
        sequencefile = {
            'gz': lambda: io.BufferedReader(gzip.GzipFile(
                fileobj=bufferedfile)),
            'bz2': lambda: io.BufferedReader(bz2file.BZ2File(
                filename=bufferedfile)),
            'zip': lambda: io.BufferedReader(zipfile.ZipFile(
                file=bufferedfile)),
            None: lambda: bufferedfile}[compression]()
        peek = sequencefile.peek(1)
    else:
        sequencefile = {
            'gz': lambda: gzip.GzipFile(fileobj=bufferedfile),
            'bz2': lambda: io.BufferedReader(bz2file.BZ2File(
                filename=bufferedfile)),
            'zip': lambda: io.BufferedReader(zipfile.ZipFile(
                file=bufferedfile)),
            None: lambda: bufferedfile}[compression]()
        peek = sequencefile.read(1)
        sequencefile.seek(0)

    iter_fn = None
    if peek:
        if peek[0] == '>':
            iter_fn = fasta_iter
        elif peek[0] == '@':
            iter_fn = fastq_iter

    if iter_fn is None:
        raise Exception("unknown file format for '%s'" % filename)

    return iter_fn(sequencefile, *args, **kwargs)

_open = open
open = open_reader


class ScreedDB(object, UserDict.DictMixin):

    """
    Core on-disk dictionary interface for reading screed databases. Accepts a
    path string to a screed database
    """

    def __init__(self, filepath):
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
        if type(nothing) != types.NoneType:
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
        if type(res.fetchone()) == types.NoneType:
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
        if type(res.fetchone()) == types.NoneType:
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
        for index in xrange(1, self.__len__() + 1):
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
        if cursor.execute(query, (key,)).fetchone() == None:
            return False
        return True

    # Here follow the methods that are not implemented

    def __setitem__(self, something):
        """
        Not implemented (Read-only database)
        """
        raise AttributeError

    def clear(self):
        """
        Not implemented (Read-only database)
        """
        raise AttributeError

    def update(self, something):
        """
        Not implemented (Read-only database)
        """
        raise AttributeError

    def setdefault(self, something):
        """
        Not implemented (Read-only database)
        """
        raise AttributeError

    def pop(self):
        """
        Not implemented (Read-only database)
        """
        raise AttributeError

    def popitem(self):
        """
        Not implemented (Read-only database)
        """
        raise AttributeError
