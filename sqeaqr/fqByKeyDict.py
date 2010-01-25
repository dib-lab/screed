import fqByIntDict
import dbEntries

class sqeaqrDB(fqByIntDict.sqeaqrDB):
    def __getitem__(self, key):
        QUERY = "SELECT INTDEX, NAME, SEQUENCE, ACCURACY FROM %s WHERE NAME = ?" \
                % self._tableName
        retrieved = self.sqdb.execute(QUERY, (key,))
        
        try:
            pairs = zip(self.fields, retrieved.next())
        except StopIteration:
            raise KeyError("Key %s not found" % key)
        return dbEntries._sqeaqr_record(pairs)

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
        QUERY = "SELECT INTDEX, NAME, SEQUENCE, ACCURACY FROM %s WHERE NAME = ?" % \
                self._tableName
        for key in self.keys():
            retrieved = self.sqdb.execute(QUERY, (key,))
            pairs = zip(self.fields, retrieved.next())
            yield dbEntries._sqeaqr_record(pairs)



