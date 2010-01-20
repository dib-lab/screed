import UserDict
import os
import sqlite3
import dbEntries
from sqeaqrExtension import fileExtension

# [AN] consolidate fadbm/fqdbm dict classes into two, by int or by key?
# based on the list of entries which could the the table fields as well

class sqeaqrDB(object, UserDict.DictMixin):
    def __init__(self, filepath):
        self._tableName = 'DICTIONARY_TABLE'
        self._orderBy = ' ORDER BY INTDEX '
        self.fields = dbEntries.FASTAFIELDS

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
        self.sqdb.execute('CREATE TABLE %s (INTDEX INTEGER PRIMARY KEY, NAME TEXT, DESCRIPTION TEXT, SEQUENCE TEXT);' %
                          self._tableName)

    def __getitem__(self, key):
        QUERY = "SELECT INTDEX, NAME, DESCRIPTION, SEQUENCE FROM %s WHERE NAME = ?" \
                % self._tableName
        retrieved = self.sqdb.execute(QUERY, (key,))
        
        try:
            pairs = zip(self.fields, retrieved.next())
        except StopIteration:
            raise KeyError("Key %s not found" % key)
        return dbEntries._sqeaqr_record(pairs)

    def __setitem__(self, name, fieldDict):
        QUERY = "REPLACE INTO %s (NAME, DESCRIPTION, SEQUENCE) VALUES (?, ?, ?)" \
                % self._tableName
        self.sqdb.execute(QUERY, (fieldDict['name'],
                                  fieldDict['description'],
                                  fieldDict['sequence']))

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
            result.append(key)
        return result

    def itervalues(self):
        QUERY = "SELECT INTDEX, NAME, DESCRIPTION, SEQUENCE FROM %s WHERE NAME = ?" % \
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
