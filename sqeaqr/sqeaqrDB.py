import types
import sqeaqrUtility
import UserDict

class sqeaqrDB(object, UserDict.DictMixin):
    """
    Class that supports lookups by id or name into an on-disk dictionary
    implemented in sqlite
    """
    def __init__(self, filepath, queryBy=None, fields=None):
        self._db, self._standardStub, self._fieldTuple, self._qMarks, \
                  self._queryBy, self._table, self._primaryKey = \
                  sqeaqrUtility.getSqeaqrDB(filepath, queryBy, fields)

    def close(self):
        if self._db is not None:
            self._db.commit()
            self._db.close()
            self._db = None

    def __getitem__(self, key):
        query = "SELECT ID, %s FROM %s WHERE %s = ?" \
                % (self._standardStub, self._table, self._queryBy)
        retrieved = self._db.execute(query, (key,))

        try:
            pairs = zip(self._fieldTuple, retrieved.next())
        except StopIteration:
            raise KeyError("Key %s not found" % key)
        return sqeaqrUtility._sqeaqr_record(pairs)

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
