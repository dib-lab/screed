import UserDict
import os
import sqlite3
import dbEntries
from sqeaqrExtension import fileExtension

class sqeaqrDB(object, UserDict.DictMixin):
    def __init__(self, filepath):
        self._tableName = 'DICTIONARY_TABLE'
        self._orderBy = ' ORDER BY INTDEX '
        self.fields = dbEntries.FASTQFIELDS

        if not filepath.endswith(fileExtension):
            filepath += fileExtension
            
        create = not os.path.isfile(filepath)
        self.sqdb = sqlite3.connect(filepath)
        if create:
            self._createSqDb()

    def _createSqDb(self):
        """
        Creates a table to use for storing sequences
        """
        self.sqdb.execute('CREATE TABLE %s (INTDEX INTEGER PRIMARY KEY, NAME TEXT, SEQUENCE TEXT, ACCURACY TEXT);' %
                          self._tableName)

    def __getitem__(self, key):
        QUERY = "SELECT INTDEX, NAME, SEQUENCE, ACCURACY FROM %s WHERE NAME = ?" \
                % self._tableName

        retrieved = self.sqdb.execute(QUERY, (key,))

        try:
            pairs = zip(self.fields, retrieved.next())
        except StopIteration:
            raise KeyError("Key %s not found" % key)
        return dbEntries._sqeaqr_record(pairs)

    def __setitem__(self, name, infoBaseObject):
        QUERY = "REPLACE INTO %s (NAME, SEQUENCE, ACCURACY) VALUES (?, ?, ?)" \
                % self._tableName
        self.sqdb.execute(QUERY, (infoBaseObject.name,
                                  infoBaseObject.sequence,
                                  infoBaseObject.accuracy))

    def __len__(self):
        for length, in self.sqdb.execute("SELECT count(1) FROM %s" % self._tableName):
            return length

    def __delitem__(self, key):
        if not key in self.keys():
            raise KeyError("Key %s not found" % key)
        QUERY = "DELETE FROM %s WHERE NAME = ?" % self._tableName
        if self.sqdb.execute(QUERY, (key,)) < 1:
            raise KeyError("Key %s not found" % key)

    def keys(self):
        QUERY = "SELECT NAME FROM %s %s" % (self._tableName, self._orderBy)
        result = []
        for key, in self.sqdb.execute(QUERY):
            result.append(str(key))
        return result

    def itervalues(self):
        QUERY = "SELECT INTDEX, NAME, SEQUENCE, ACCURACY FROM %s WHERE NAME = ?" % \
                self._tableName
        for key in self.keys():
            retrieved = self.sqdb.execute(QUERY, (key,))
            pairs = zip(self.fields, retrieved.next())
            yield dbEntries._sqeaqr_record(pairs)
                
    def iteritems(self):
        for v in self.itervalues():
            yield v.index, v

    def close(self):
        if self.sqdb is not None:
            self.sqdb.commit()
            self.sqdb.close()
            self.sqdb = None
