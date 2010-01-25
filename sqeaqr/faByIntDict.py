import fqByIntDict
import dbEntries

class sqeaqrDB(fqByIntDict.sqeaqrDB):
    def __init__(self, filepath):
        fqByIntDict.sqeaqrDB.__init__(self, filepath)
        self.fields = dbEntries.FASTAFIELDS

    def _createSqDb(self):
        """
        Creates a table to use for storing sequences
        """
        self.sqdb.execute('CREATE TABLE %s (INTDEX INTEGER PRIMARY KEY, NAME TEXT, DESCRIPTION TEXT, SEQUENCE TEXT);' %
                          self._tableName)

    def __getitem__(self, index):
        QUERY = "SELECT INTDEX, NAME, DESCRIPTION, SEQUENCE FROM %s WHERE INTDEX = ?" \
                % self._tableName
        retrieved = self.sqdb.execute(QUERY, (index,))
        
        try:
            pairs = zip(self.fields, retrieved.next())
        except StopIteration:
            raise KeyError("Key %s not found" % index)
        return dbEntries._sqeaqr_record(pairs)

    def __setitem__(self, name, fieldDict):
        QUERY = "REPLACE INTO %s (NAME, DESCRIPTION, SEQUENCE) VALUES (?, ?, ?)" \
                % self._tableName
        self.sqdb.execute(QUERY, (fieldDict['name'],
                                  fieldDict['description'],
                                  fieldDict['sequence']))
    def itervalues(self):
        QUERY = "SELECT INTDEX, NAME, DESCRIPTION, SEQUENCE FROM %s WHERE INTDEX = ?" % \
                self._tableName
        for index in self.keys():
            retrieved = self.sqdb.execute(QUERY, (index,))
            pairs = zip(self.fields, retrieved.next())
            yield dbEntries._sqeaqr_record(pairs)
