# Copyright (c) 2008-2010, Michigan State University

import types
import screedUtility
import UserDict
import screedRecord

class screedDB(object, UserDict.DictMixin):
    """
    Class that supports lookups by id or name into an on-disk dictionary
    implemented in sqlite
    """
    def __init__(self, filepath, fields=None):
        self._db, self._standardStub, self._fieldTuple, self._qMarks, \
                  self._table, self._queryBy, self._primaryKey = \
                  screedUtility.getScreedDB(filepath, fields)
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
                                                  self._table, self._queryBy)
        try:
            res = self._cursor.execute(query, (key,))
        except:
            raise TypeError("query: %s, key: %s" % (type(query), type(key)))
        if type(res.fetchone()) == types.NoneType:
            raise KeyError("Key %s not found" % key)
        return screedRecord._buildRecord(self._fieldTuple, self._cursor,
                                         self._primaryKey, key, self._queryBy,
                                         self._table)

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
        query = 'SELECT %s FROM %s WHERE %s=?' % (self._primaryKey,
                                                  self._table, self._primaryKey)
        res = self._cursor.execute(query, (index,))
        if type(res.fetchone()) == types.NoneType:
            raise KeyError("Index %d not found" % index)
        return screedRecord._buildRecord(self._fieldTuple,self._cursor,
                                         self._primaryKey, index, self._primaryKey,
                                         self._table)
    
    def __setitem__(self, name, dataTuple):
        """
        Assigns data into the dictionary from the ordered dataTuple into the record
        slot with key 'name'.
        e.x: name = 'some read name',
        dataTuple = ('some read name', 'a description of some read name', 'ATCG')
        """
        assert type(dataTuple) == types.TupleType
        QUERY = "REPLACE INTO %s (%s) VALUES (%s)" % \
                (self._table, self._standardStub, self._qMarks)
        self._cursor.execute(QUERY, dataTuple)

    def __len__(self):
        res, = self._cursor.execute('SELECT MAX(%s) FROM %s' % (self._primaryKey,
                                                                self._table)).next()
        return res

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        for index in xrange(1, self.__len__()+1):
            yield screedRecord._buildRecord(self._fieldTuple, self._cursor,
                                            self._primaryKey, index, self._primaryKey,
                                            self._table)

    def iterkeys(self):
        query = 'SELECT %s FROM %s' % (self._queryBy, self._table)
        for key, in self._cursor.execute(query):
            yield key

    def iteritems(self):
        for v in self.itervalues():
            yield str(v[self._primaryKey.lower()]), v

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
                (self._queryBy, self._table, self._queryBy)
        try:
            self._cursor.execute(query, (key,)).next()
        except StopIteration:
            return False
        return True

    # Here follow the methods that are not implemented

    def clear(self):
        raise AttributeError

    def update(self, something):
        raise AttributeError

    def setdefault(self, something):
        raise AttributeError

    def pop(self):
        raise AttributeError

    def popitem(self):
        raise AttributeError
