# Copyright (c) 2008-2010, Michigan State University

import types
import screedUtility
import UserDict

# [AN] remove decision about using querying by name or id
# [AN] inconsistant naming scheme: allowing user to specify field names
# but needing certain names here

class _screed_record_iter(object):
    """
    Iterator over screed database, returning records
    """
    def __init__(self, db):
        self.db = db
        self.i = 1
        self.n = len(db)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i > self.n:
            raise StopIteration

        record = self.db.loadRecordByIndex(self.i)
        self.i += 1
        return record

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
        Calls loadRecordByName to retrieve the record with the given name
        """
        return self.loadRecordByName(key)

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
        index += 1 # Hack to make indexing start at 0
        assert index >= 1 # sqlite starts numbering at 1
        query = 'SELECT * FROM %s WHERE %s = ?' \
                % (self._table, self._primaryKey)
        result = self._cursor.execute(query, (index,))
        try:
            pairs = map(screedUtility.toStrings, self._fieldTuple, result.next())
        except StopIteration:
            raise KeyError("Index %s not found" % index)
        result = screedUtility._screed_record(pairs)
        result[self._primaryKey.lower()] -= 1 # Hack to make indexing start at 0
        return result

    def loadRecordByName(self, name):
        """
        Retrieves from database the record with the name 'name'
        """
        query = "SELECT %s, %s FROM %s WHERE %s = ?" \
                 % (self._primaryKey, self._standardStub, self._table, self._queryBy)
        retrieved = self._cursor.execute(query, (name,))
        try:
            pairs = map(screedUtility.toStrings, self._fieldTuple, retrieved.next())
        except StopIteration:
            raise KeyError("Key %s not found" % name)
        result = screedUtility._screed_record(pairs)
        result[self._primaryKey.lower()] -= 1 # Hack to make indexing start at 0
        return result
    
    def __setitem__(self, name, dataTuple):
        """
        Assigns data into the dictionary from the ordered dataTuple into the record
        slot with key 'name'.
        e.x: name = 'some read name',
        dataTuple = ('some read name', 'a description of some read name', 'ATCG')
        """
        # [AN] make a test for the existence of the name before inserting new data
        assert type(dataTuple) == types.TupleType
        QUERY = "REPLACE INTO %s (%s) VALUES (%s)" % \
                (self._table, self._standardStub, self._qMarks)
        self._cursor.execute(QUERY, dataTuple)

    def __len__(self):
        res, = self._cursor.execute('SELECT MAX(%s) FROM %s' % (self._primaryKey,
                                                                self._table)).next()
        return res

    def keys(self):
        query = 'SELECT %s FROM %s' % (self._queryBy, self._table)
        result = []
        for key, in self._cursor.execute(query):
            result.append(key)
        return result

    def itervalues(self):
        query = 'SELECT %s, %s FROM %s WHERE %s = ?' % \
                (self._primaryKey, self._standardStub, self._table, self._queryBy)
        for key in self.keys():
            retrieved = self._cursor.execute(query, (key,))
            pairs = map(screedUtility.toStrings, self._fieldTuple, retrieved.next())
            result = screedUtility._screed_record(pairs)
            result[self._primaryKey.lower()] -= 1 # Hack to make indexing start at 0
            yield result

    def iterkeys(self):
        for k in self.keys():
            yield k

    def getSliceById(self, index, field, begin, length):
        """
        Returns a slice of a sequence indexed by index
        """
        assert field in self._fieldTuple
        index += 1 # Hack to make indexing start at 0
        begin += 1 # Sqlite begins at 1, not 0
        assert index >= 1 and begin >= 1

        query = 'SELECT substr(%s, %d, %d) FROM %s WHERE %s = ?' \
                % (field, begin, length, self._table, self._primaryKey)
        result = self._cursor.execute(query, (index,))
        stringSlice, = result.fetchone()
        if not stringSlice:
            raise KeyError("Index %s not found" % index)
        return str(stringSlice)
        
    def getSliceByName(self, name, field, begin, length):
        """
        Returns a slice of a sequence indexed by name
        """
        assert field in self._fieldTuple
        begin += 1 # Sqlite begins at 1, not 0

        query = 'SELECT substr(%s, %d, %d) FROM %s WHERE %s = ?' \
                % (field, begin, length, self._table, self._queryBy)
        result = self._cursor.execute(query, (name,))
        stringSlice, = result.fetchone()
        if not stringSlice:
            raise KeyError("Key %s not found" % name)
        return str(stringSlice)

    def iteritems(self):
        for v in self.itervalues():
            yield v[self._primaryKey.lower()], v

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
