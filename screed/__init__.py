"""
screed is a database tool useful for retrieving arbitrary kinds of sequence
data through a on-disk database that emulates a read-only Python dictionary.
Functions contained here include:
read_fastq_sequences
read_fasta_sequences
These two functions are useful for taking a FASTQ or FASTA formatted file
and parsing it into a screed database.
Also contained is the core 'screed' dictionary used for opening screed
databases in read-only mode.
"""
import dbConstants
import os
import createdb
import types
import screedUtility
import UserDict
import screedRecord

FASTQFIELDTYPES = ('name', 'sequence','accuracy')
FASTAFIELDTYPES = ('name', 'description', 'sequence')

def read_fastq_sequences(filename):
    """
    Function to parse text from the given FASTQ file into a screed database
    """

    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Delete old screed database if that exists
    if os.path.isfile(filename + dbConstants.fileExtension):
        os.unlink(filename + dbConstants.fileExtension)

    fqCreate = createdb.createdb(filename, FASTQFIELDTYPES)

    while 1:
        data = {}
        firstLine = theFile.readline().strip().split('@')
        if len(firstLine) == 1: # Reached eof
            break
        # Make sure the FASTQ file is being read correctly
        assert firstLine[0] == ''
        name = firstLine[1]
        data['name'] = name
        data['sequence'] = theFile.readline().strip()
        theFile.read(2) # Ignore the '+\n'
        data['accuracy'] = theFile.readline().strip()
        fqCreate.feed(data)

    theFile.close()
    fqCreate.close()

def read_fasta_sequences(filename):
    """
    Function to parse text from the given FASTA file into a screed database
    """
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Delete old screed database if that exists
    if os.path.isfile(filename + dbConstants.fileExtension):
        os.unlink(filename + dbConstants.fileExtension)

    faCreate = createdb.createdb(filename, FASTAFIELDTYPES)

    # Parse text and add to database
    nextChar = theFile.read(1)
    while nextChar != '':
        data = {}
        assert nextChar == '>'
        topLine = theFile.readline().strip().split(' ', 1)

        # Extract the name
        name = topLine[0]
        data['name'] = name

        # Extract the description
        description = ''
        if len(topLine) == 2:
            description = topLine[1]
        data['description'] = description

        # Collect sequence lines into a list
        sequenceList = []
        nextChar = theFile.read(1)
        while nextChar != '' and nextChar != '>':
            sequenceLine = nextChar + theFile.readline().strip()
            sequenceList.append(sequenceLine)
            nextChar = theFile.read(1)
            
        sequence = "".join(sequenceList)
        data['sequence'] = sequence
        faCreate.feed(data)
        
    theFile.close()
    faCreate.close()

class screedDB(object, UserDict.DictMixin):
    """
    Core on-disk dictionary interface for reading screed databases. Accepts a
    path string to a screed database
    """
    def __init__(self, filepath):
        self._db, self._standardStub, self._fieldTuple, self._qMarks, \
                  self._queryBy = screedUtility.getScreedDB(filepath)
        self._cursor = self._db.cursor()

        # Retrieve the length of the database
        query = 'SELECT MAX(%s) FROM %s' % (dbConstants._PRIMARY_KEY,
                                            dbConstants._DICT_TABLE)
        self._len, = self._cursor.execute(query).fetchone()

    def close(self):
        if self._db is not None:
            self._db.commit()
            self._db.close()
            self._db = None

    def __getitem__(self, key):
        """
        Retrieves from database the record with the key 'key'
        """
        key = str(key) # So lazy retrieval objectes are evaluated
        query = 'SELECT %s FROM %s WHERE %s=?' % (self._queryBy,
                                                  dbConstants._DICT_TABLE, self._queryBy)
        res = self._cursor.execute(query, (key,))
        if type(res.fetchone()) == types.NoneType:
            raise KeyError("Key %s not found" % key)
        return screedRecord._buildRecord(self._fieldTuple, self._cursor,
                                         dbConstants._PRIMARY_KEY, key, self._queryBy,
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
        index = int(index) + 1 # Hack to make indexing start at 0
        query = 'SELECT %s FROM %s WHERE %s=?' % (dbConstants._PRIMARY_KEY,
                                                  dbConstants._DICT_TABLE, dbConstants._PRIMARY_KEY)
        res = self._cursor.execute(query, (index,))
        if type(res.fetchone()) == types.NoneType:
            raise KeyError("Index %d not found" % index)
        return screedRecord._buildRecord(self._fieldTuple,self._cursor,
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
        for index in xrange(1, self.__len__()+1):
            yield screedRecord._buildRecord(self._fieldTuple, self._cursor,
                                            dbConstants._PRIMARY_KEY, index,
                                            dbConstants._PRIMARY_KEY,
                                            dbConstants._DICT_TABLE)

    def iterkeys(self):
        """
        Iterator over keys in the database
        """
        query = 'SELECT %s FROM %s' % (self._queryBy, dbConstants._DICT_TABLE)
        for key, in self._cursor.execute(query):
            yield key

    def iteritems(self):
        """
        Iterator returning an (index, record) pair
        """
        for v in self.itervalues():
            yield str(v[dbConstants._PRIMARY_KEY]), v

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
                (self._queryBy, dbConstants._DICT_TABLE, self._queryBy)
        if self._cursor.execute(query, (key,)).fetchone() == None:
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
