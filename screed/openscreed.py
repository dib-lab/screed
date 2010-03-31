import dbConstants
import os
import types
import UserDict
import screedRecord
import dbConstants
import os
import types
import sqlite3

class screedDB(object, UserDict.DictMixin):
    """
    Core on-disk dictionary interface for reading screed databases. Accepts a
    path string to a screed database
    """
    def __init__(self, filepath):
        if not filepath.endswith(dbConstants.fileExtension):
            filepath += dbConstants.fileExtension
            
        self._db = sqlite3.connect(filepath)
        cursor = self._db.cursor()

        # Make sure the database is a prepared screed database
        query = "SELECT name FROM sqlite_master WHERE type='table'"\
                "ORDER BY name"
        res = cursor.execute(query)
        try:
            dictionary_table, = res.fetchone()
            admin_table, = res.fetchone()

            if dictionary_table != dbConstants._DICT_TABLE:
                raise TypeError
            if admin_table != dbConstants._SCREEDADMIN:
                raise TypeError

        except TypeError:
            self._db.close()
            raise TypeError("Database %s is not a proper screed database"
                            % filepath)
        
        nothing = res.fetchone()
        if type(nothing) != types.NoneType:
            self._db.close()
            raise TypeError("Database %s has too many tables." % filename)
        
        # Store the fields of the admin table in a tuple
        query = "SELECT %s, %s FROM %s ORDER BY %s" % \
                (dbConstants._ADM_PRIMARY_KEY,
                 dbConstants._FIELDNAME,
                 dbConstants._SCREEDADMIN,
                 dbConstants._ADM_PRIMARY_KEY)
        res = cursor.execute(query)
        self._fieldTuple = tuple([field for idx, field in res])

        # [AN] change when concept of 'roles' introduced
        # Select the first field as the queryby key
        self._queryBy = self._fieldTuple[1]

        # Retrieve the length of the database
        query = 'SELECT MAX(%s) FROM %s' % (dbConstants._PRIMARY_KEY,
                                            dbConstants._DICT_TABLE)
        self._len, = cursor.execute(query).fetchone()

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
        key = str(key) # So lazy retrieval objectes are evaluated
        query = 'SELECT %s FROM %s WHERE %s=?' % (self._queryBy,
                                                  dbConstants._DICT_TABLE,
                                                  self._queryBy)
        res = cursor.execute(query, (key,))
        if type(res.fetchone()) == types.NoneType:
            raise KeyError("Key %s not found" % key)
        return screedRecord._buildRecord(self._fieldTuple, cursor,
                                         dbConstants._PRIMARY_KEY, key,
                                         self._queryBy,
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
        cursor = self._db.cursor()
        index = int(index) + 1 # Hack to make indexing start at 0
        query = 'SELECT %s FROM %s WHERE %s=?' % (dbConstants._PRIMARY_KEY,
                                                  dbConstants._DICT_TABLE,
                                                  dbConstants._PRIMARY_KEY)
        res = cursor.execute(query, (index,))
        if type(res.fetchone()) == types.NoneType:
            raise KeyError("Index %d not found" % index)
        return screedRecord._buildRecord(self._fieldTuple, cursor,
                                         dbConstants._PRIMARY_KEY, index,
                                         dbConstants._PRIMARY_KEY,
                                         dbConstants._DICT_TABLE)
    
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

    def itervalues(self):
        """
        Iterator over records in the database
        """
        cursor = self._db.cursor()
        for index in xrange(1, self.__len__()+1):
            yield screedRecord._buildRecord(self._fieldTuple, cursor,
                                            dbConstants._PRIMARY_KEY, index,
                                            dbConstants._PRIMARY_KEY,
                                            dbConstants._DICT_TABLE)

    def iterkeys(self):
        """
        Iterator over keys in the database
        """
        cursor = self._db.cursor()
        query = 'SELECT %s FROM %s' % (self._queryBy, dbConstants._DICT_TABLE)
        for key, in cursor.execute(query):
            yield key

    def iteritems(self):
        """
        Iterator returning a (index, record) pairs
        """
        for v in self.itervalues():
            yield str(v[dbConstants._PRIMARY_KEY]), v

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
                (self._queryBy, dbConstants._DICT_TABLE, self._queryBy)
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
