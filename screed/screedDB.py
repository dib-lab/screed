# Copyright (c) 2008-2010, Michigan State University

import types
import screedUtility
import dbConstants
import UserDict
import screedRecord

class screedDB(object, UserDict.DictMixin):
    """
    Core of screed. Accepts a path string to the screed database file and
    an optional fields tuple which specifes the names and order of attributes
    per record
    """
    def __init__(self, filepath, fields=None):
        self._db, self._standardStub, self._fieldTuple, self._qMarks, \
                  self._queryBy = screedUtility.getScreedDB(filepath, fields)
        self._cursor = self._db.cursor()

    def close(self):
        if self._db is not None:
            self._db.commit()
            self._db.close()
            self._db = None

    def __getitem__(self, key):
        """
        Retrieves from database the record with the key 'key'
        """
        key = str(key) # So lazy retrieval objectes are evaluated
        query = 'SELECT %s FROM %s WHERE %s=?' % (self._queryBy,
                                                  dbConstants._DICT_TABLE, self._queryBy)
        res = self._cursor.execute(query, (key,))
        if type(res.fetchone()) == types.NoneType:
            raise KeyError("Key %s not found" % key)
        return screedRecord._buildRecord(self._fieldTuple, self._cursor,
                                         dbConstants._PRIMARY_KEY, key, self._queryBy,
                                         dbConstants._DICT_TABLE)

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
        index = int(index) + 1 # Hack to make indexing start at 0
        query = 'SELECT %s FROM %s WHERE %s=?' % (dbConstants._PRIMARY_KEY,
                                                  dbConstants._DICT_TABLE, dbConstants._PRIMARY_KEY)
        res = self._cursor.execute(query, (index,))
        if type(res.fetchone()) == types.NoneType:
            raise KeyError("Index %d not found" % index)
        return screedRecord._buildRecord(self._fieldTuple,self._cursor,
                                         dbConstants._PRIMARY_KEY, index,
                                         dbConstants._PRIMARY_KEY,
                                         dbConstants._DICT_TABLE)
    
    def __len__(self):
        """
        Returns the number of records in the database
        """
        query = 'SELECT MAX(%s) FROM %s' % (dbConstants._PRIMARY_KEY,
                                            dbConstants._DICT_TABLE)
        res, = self._cursor.execute(query).fetchone()
        return res

    def keys(self):
        """
        Returns a list of keys in the database
        """
        return list(self.iterkeys())

    def itervalues(self):
        """
        Iterator over records in the database
        """
        for index in xrange(1, self.__len__()+1):
            yield screedRecord._buildRecord(self._fieldTuple, self._cursor,
                                            dbConstants._PRIMARY_KEY, index,
                                            dbConstants._PRIMARY_KEY,
                                            dbConstants._DICT_TABLE)

    def iterkeys(self):
        """
        Iterator over keys in the database
        """
        query = 'SELECT %s FROM %s' % (self._queryBy, dbConstants._DICT_TABLE)
        for key, in self._cursor.execute(query):
            yield key

    def iteritems(self):
        """
        Iterator returning an (index, record) pair
        """
        for v in self.itervalues():
            yield str(v[dbConstants._PRIMARY_KEY.lower()]), v

    def has_key(self, key):
        """
        Returns true if given key exists in database, false otherwise
        """
        return self.__contains__(key)

    def copy(self):
        """
        Returns shallow copy of itself
        """
        return self

    def __contains__(self, key):
        """
        Returns true if given key exists in database, false otherwise
        """
        query = 'SELECT %s FROM %s WHERE %s = ?' % \
                (self._queryBy, dbConstants._DICT_TABLE, self._queryBy)
        if self._cursor.execute(query, (key,)).fetchone() == None:
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
