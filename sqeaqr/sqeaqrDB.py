import types
import sqeaqrUtility
import UserDict

# [AN] remove decision about using querying by name or id
# [AN] inconsistant naming scheme: allowing user to specify field names
# but needing certain names here

class _sqeaqr_record_iter(object):
    """
    Iterator over sqeaqr database, returning records
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

class sqeaqrDB(object, UserDict.DictMixin):
    """
    Class that supports lookups by id or name into an on-disk dictionary
    implemented in sqlite
    """
    def __init__(self, filepath, fields=None):
        self._db, self._standardStub, self._fieldTuple, self._qMarks, \
                  self._table, self._queryBy, self._primaryKey = \
                  sqeaqrUtility.getSqeaqrDB(filepath, fields)

    def close(self):
        if self._db is not None:
            self._db.commit()
            self._db.close()
            self._db = None

    def __getitem__(self, key):
        """
        Calls loadRecordByName to retrieve the record with the given name
        """
        return loadRecordByName(key)

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

    def __getitem__(self, key):
        query = "SELECT %s, %s FROM %s WHERE %s = ?" \
                % (self._primaryKey, self._standardStub, self._table, self._queryBy)
        retrieved = self._db.execute(query, (key,))

        try:
            pairs = zip(self._fieldTuple, retrieved.next())
        except StopIteration:
            raise KeyError("Key %s not found" % key)
        return sqeaqrUtility._sqeaqr_record(pairs)

    def loadRecordByIndex(self, index):
        """
        Retrieves record from database at the given index
        """
        assert index > 0 # sqlite starts numbering at 1
        query = 'SELECT * FROM %s WHERE %s = ?' \
                % (self._table, self._primaryKey)
        result = self._db.execute(query, (index,))
        try:
            pairs = zip(self._fieldTuple, result.next())
        except StopIteration:
            raise KeyError("Index %s not found" % index)
        return sqeaqrUtility._sqeaqr_record(pairs)

    def loadRecordByName(self, name):
        """
        Retrieves from database the record with the name 'name'
        """
        query = 'SELECT * FROM %s WHERE %s = ?' \
                % (self._table, self._queryBy)
        result = self._db.execute(query, name)
        try:
            pairs = zip(self._fieldTuple, retrieved.next())
        except StopIteration:
            raise KeyError("Key %s not found" % name)
        return sqeaqrUtility._sqeaqr_record(pairs)

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
        self._db.execute(QUERY, dataTuple)

    def __len__(self):
        res, = self._db.execute('SELECT COUNT(1) FROM %s' % self._table).next()
        return res

    def __delitem__(self):
        raise NotImplementedError('sqeaqr doesn\'t do this')

    def keys(self):
        query = 'SELECT %s FROM %s' % (self._queryBy, self._table)
        result = []
        for key, in self._db.execute(query):
            result.append(key)
        return result

    def itervalues(self):
        query = 'SELECT %s, %s FROM %s WHERE %s = ?' % \
                (self._primaryKey, self._standardStub, self._table, self._queryBy)
        for key in self.keys():
            retrieved = self._db.execute(query, (key,))
            pairs = zip(self._fieldTuple, retrieved.next())
            yield sqeaqrUtility._sqeaqr_record(pairs)

    def iteritems(self):
        for v in self.itervalues():
            yield v[self._primaryKey.lower()], v


    def __contains__(self, key):
        """
        Returns true if given key exists in database, false otherwise
        """
        query = 'SELECT %s FROM %s WHERE %s = ?' % \
                (self._queryBy, self._table, self._queryBy)
        try:
            self._db.execute(query, (key,)).next()
        except StopIteration:
            return False
        return True
        
        
