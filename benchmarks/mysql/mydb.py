import mdbConstants
import MySQLdb
import UserDict
import types

class _mdb_record_dict(UserDict.DictMixin):
    """
    Simple dict-like record interface with bag behavior.
    """
    def __init__(self, *args, **kwargs):
        self.d = dict(*args, **kwargs)
        
    def __getitem__(self, name):
        return self.d[name]

    def __setitem__(self, name, value):
        self.d[name] = value
    
    def __getattr__(self, name):
        try:
            return self.d[name]
        except KeyError:
            raise AttributeError, name

    def keys(self):
        return self.d.keys()

class mydb(object):
    def __init__(self):
        self._conn = MySQLdb.connect(db=mdbConstants._DBNAME, user=mdbConstants._USER)
                                       
        cur = self._conn.cursor()
        cur.execute('SELECT id, fieldname FROM %s' % mdbConstants._SCREEDADMIN)
        self._adm = dict(cur.fetchall())
        keys = self._adm.keys()
        keys.sort()

        self._fields = self._adm.values()
        self._fields.insert(0, mdbConstants._PRIMARY_KEY.lower())
        self._fieldStr = ",".join(self._fields)

        self._queryBy = self._adm[keys[0]]

    def close(self):
        """
        Closes the database handles
        """
        self._conn.close()

    def loadRecordByIndex(self, idx):
        """
        Loads a record from the database by index
        """
    
    def loadRecordByName(self, key):
        """
        As above, by name
        """
        cursor = self._conn.cursor()
        query = "SELECT %s FROM %s WHERE %s='%s'" % (self._queryBy,
                                                     mdbConstants._DICT_TABLE,
                                                     self._queryBy,
                                                     key)
        cursor.execute(query)
        if type(cursor.fetchone()) == types.NoneType:
            raise KeyError("Key %s not found" % key)

        query = "SELECT %s FROM %s WHERE %s='%s'" % (self._fieldStr,
                                                     mdbConstants._DICT_TABLE,
                                                     self._queryBy,
                                                     key)
        cursor.execute(query)
        return _mdb_record_dict(zip(self._fields, cursor.fetchone()))

    def keys(self):
        """
        Returns a list of keys in database
        """
        cursor = self._conn.cursor()
        query = "SELECT %s FROM %s" % (self._queryBy,
                                       mdbConstants._DICT_TABLE)
        cursor.execute(query)
        return [elem for elem, in cursor]
