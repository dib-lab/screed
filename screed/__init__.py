"""
screed is a database tool useful for retrieving arbitrary kinds of sequence
data through a on-disk database that emulates a read-only Python dictionary.
Functions contained here include:
read_fastq_sequences
read_fasta_sequences
These two functions are useful for taking a FASTQ or FASTA formatted file
and parsing it into a screed database.
Classes contained here include:
screedDB
createdb
screedDB is the core dictionary class used for opening prepared screed
databases. This is only for reading pre-created databases since screedDB
supports no dictionary altering methods.
createdb is the class used to create screed databases. A file path is
passed in the constructor and then sequence records are sequentially
given to the createdb object
"""
import dbConstants
import os
import types
import screedUtility
import UserDict
import screedRecord
import sqlite3

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

    fqCreate = createdb(filename, FASTQFIELDTYPES)

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

    faCreate = createdb(filename, FASTAFIELDTYPES)

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

class createdb(object):
    """
    Class used for creating screed databases. Records are passed to the object
    via the feed method. When finished, the object must be closed
    """
    def __init__(self, filepath, attributes):
        """
        Opens a new screed database at the given filepath. Attributes is a tuple
        containing the names and order of atrributes per record
        """
        if not filepath.endswith(dbConstants.fileExtension):
            filepath += dbConstants.fileExtension

        if os.path.exists(filepath): # Remove existing files
            os.unlink(filepath)

        self._attributes = attributes
        self._con = sqlite3.connect(filepath)
        self._c = self._con.cursor()
        self._queryby = self._attributes[0] # Key is first attribute
        self._makeadmintable()
        self._makedicttable()
        self._open = True

    def _tocreatestub(self):
        """
        Parses self._attributes into an SQL stub to be inserted into statements
        """
        sqlList = []
        for attribute in self._attributes:
            sqlList.append('%s TEXT' % attribute)
            sqlList.append(', ')
        sqlList.pop()
        return "".join(sqlList)

    def _makedicttable(self):
        """
        Method to setup the dictionary table for storing records
        """
        # Make the table
        self._c.execute('CREATE TABLE %s (%s INTEGER PRIMARY KEY, %s)' %
                        (dbConstants._DICT_TABLE, dbConstants._PRIMARY_KEY,
                         self._tocreatestub()))
        # Make the index
        self._c.execute('CREATE UNIQUE INDEX %sidx ON %s(%s)' %
                        (self._queryby, dbConstants._DICT_TABLE,
                         self._queryby))

    def _makeadmintable(self):
        """
        Method to setup the admin table containing attribute information
        """
        self._c.execute('CREATE TABLE %s (ID INTEGER PRIMARY KEY, '\
                        'FIELDNAME TEXT)' % dbConstants._SCREEDADMIN)

        query = 'INSERT INTO %s (FIELDNAME) VALUES (?)' % \
                dbConstants._SCREEDADMIN
        for attribute in self._attributes:
            self._c.execute(query, (attribute,))

    def feed(self, dictobj):
        """
        Method for storing records. dictobj is a dictionary object with
        name->value pairs of record attributes
        """
        qmarks = ('?, ' * len(self._attributes))[:-2]
        attributes = (''.join(['%s, ' % attr for attr in self._attributes]))[:-2]
        sub = tuple([dictobj[key] for key in self._attributes])
        query = 'INSERT INTO %s (%s) VALUES (%s)' %\
                (dbConstants._DICT_TABLE, attributes, qmarks)
        self._c.execute(query, sub)

    def close(self):
        """
        Closes the object and the sqlite database handle
        """
        if self._open:
            self._con.commit()
            self._con.close()
            self._open = False
