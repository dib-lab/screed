import UserDict
import os
import sqlite3
import dbEntries

class sqeaqrDB(object, UserDict.DictMixin):
    def __init__(self, filepath):
        self._tableName = 'DICTIONARY_TABLE'
        self._orderBy = ' ORDER BY ROWID '
            
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

    def __getitem__(self, index):
        QUERY = "SELECT INTDEX, NAME, SEQUENCE, ACCURACY FROM %s WHERE INTDEX = ?" \
                % self._tableName
        for index, name, sequence, accuracy in self.sqdb.execute(QUERY, (index,)):
            return dbEntries.fastqEntry(index, name, sequence, accuracy)
        raise KeyError("Key %s not found" % index)

    def __setitem__(self, name, infoBaseObject):
        QUERY = "REPLACE INTO %s (NAME, SEQUENCE, ACCURACY) VALUES (?, ?, ?)" \
                % self._tableName
        self.sqdb.execute(QUERY, (infoBaseObject.name,
                                  infoBaseObject.sequence,
                                  infoBaseObject.accuracy))

    def __len__(self):
        for length, in self.sqdb.execute("SELECT count(1) FROM %s" % self._tableName):
            return length

    def __delitem__(self, index):
        if not index in self.keys():
            raise KeyError("Key %s not found" % index)
        QUERY = "DELETE FROM %s WHERE INTDEX = ?" % self._tableName
        if self.sqdb.execute(QUERY, (index,)) < 1:
            raise KeyError("Key %s not found" % index)

    def keys(self):
        QUERY = "SELECT INTDEX FROM %s %s" % (self._tableName, self._orderBy)
        result = []
        for key, in self.sqdb.execute(QUERYp):
            result.append(key)
        return result

    def itervalues(self):
        QUERY = "SELECT NAME, SEQUENCE, ACCURACY FROM %s WHERE INTDEX = ?" % \
                self._tableName
        for index in self.keys():
            for name, sequence, accuracy in self.sqdb.execute(QUERY, (index,)):
                yield (dbEntries.fastqEntry(index, name, sequence, accuracy))
                
    def iteritems(self):
        for v in self.itervalues():
            yield v.index, v

    def close(self):
        if self.sqdb is not None:
            self.sqdb.commit()
            self.sqdb.close()
            self.sqdb = None
