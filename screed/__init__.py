# Copyright (c) 2008-2010, Michigan State University

"""
screed is a database tool useful for retrieving arbitrary kinds of sequence
data through a on-disk database that emulates a read-only Python dictionary.
Functions contained here include:
read_fastq_sequences
read_fasta_sequences
create_db

read_*_sequences are useful for extracting record data from a FASTA or
FASTQ file
create_db is used by the above two to format the records into a screed
database

Classes contained here:
screedDB

screedDB is the core dictionary class used for opening prepared screed
databases. This is only for reading pre-created databases since screedDB
supports no dictionary altering methods.
"""
import dbConstants
import os
import types
import screedUtility
import UserDict
import screedRecord
import sqlite3

__version__ = '0.5'


def read_fastq_sequences(filename):
    """
    Function to parse text from the given FASTQ file into a screed database
    """
    def fqiter(handle):
        """
        Iterator over the given FASTQ file handle returning records. handle
        is a handle to a file opened for reading
        """
        data = {}
        line = handle.readline().strip()
        while line:
            if not line.startswith('@'):
                raise IOError("Bad FASTQ format: no '@' at beginning of line")

            # Try to grab the name and (optional) annotations
            try:
                data['name'], data['annotation'] = line[1:].split(' ',1)
            except ValueError: # No optional annotations
                data['name'] = line[1:]
                data['annotations'] = ''
                pass

            # Extract the sequence lines
            sequence = []
            line = handle.readline().strip()
            while not line.startswith('+'):
                sequence.append(line)
                line = handle.readline()

            data['sequence'] = ''.join(sequence)

            # Extract the accuracy lines
            accuracy = []
            line = handle.readline().strip()
            while not line.startswith('@') and not line == '':
                accuracy.append(line)
                line = handle.readline().strip()

            data['accuracy'] = ''.join(accuracy)
            if len(data['sequence']) != len(data['accuracy']):
                raise IOError('sequence and accuracy strings must be of equal length')

            yield data

    FASTQFIELDTYPES = ('name', 'annotations', 'sequence', 'accuracy')

    # Will raise an exception if the file doesn't exist
    theFile = open(filename, 'rb')

    # Setup the iterator function
    iterfunc = fqiter(theFile)

    # Create the screed db
    create_db(filename, FASTQFIELDTYPES, iterfunc)

    theFile.close()

def read_fasta_sequences(filename):
    """
    Function to parse text from the given FASTA file into a screed database
    """

    def faiter(handle):
        """
        Iterator over the given FASTA file handle, returning records. handle
        is a handle to a file opened for reading
        """
        data = {}
        line = handle.readline().strip()
        while line != '':
            if not line.startswith('>'):
                raise IOError("Bad FASTA format: no '>' at beginning of line")

            # Try to grab the name and optional description
            try:
                data['name'], data['description'] = line[1:].split(' ', 1)
            except ValueError: # No optional description
                data['name'] = line
                data['description'] = ''
                pass

            # Collect sequence lines into a list
            sequenceList = []
            line = handle.readline().strip()
            while line != '' and not line.startswith('>'):
                sequenceList.append(line)
                line = handle.readline().strip()

            data['sequence'] = ''.join(sequenceList)
            yield data
                
    
    FASTAFIELDTYPES = ('name', 'description', 'sequence')
    
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Setup the iterator function
    iterfunc = faiter(theFile)

    # Create the screed db
    create_db(filename, FASTAFIELDTYPES, iterfunc)
    
    theFile.close()

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

def create_db(filepath, fields, rcrditer):
    """
    Creates a screed database in the given filepath. Fields is a tuple
    specifying the names and relative order of attributes in a
    record. rcrditer is an iterator returning records over a
    sequence dataset. Records yielded are in dictionary form
    """
    if not filepath.endswith(dbConstants.fileExtension):
        filepath += dbConstants.fileExtension

    if os.path.exists(filepath): # Remove existing files
        os.unlink(filepath)

    con = sqlite3.connect(filepath)
    cur = con.cursor()

    # Create the admin table
    cur.execute('CREATE TABLE %s (ID INTEGER PRIMARY KEY, '\
                'FIELDNAME TEXT)' % dbConstants._SCREEDADMIN)
    query = 'INSERT INTO %s (FIELDNAME) VALUES (?)' % \
            dbConstants._SCREEDADMIN
    for attribute in fields:
        cur.execute(query, (attribute,))

    # Setup the dictionary table creation field substring
    fieldsub = ''.join(['%s TEXT,' % field for field in fields])[:-1]

    # Create the dictionary table
    cur.execute('CREATE TABLE %s (%s INTEGER PRIMARY KEY, %s)' %
                (dbConstants._DICT_TABLE, dbConstants._PRIMARY_KEY,
                 fieldsub))

    # Attribute to index
    queryby = fields[0]

    # Make the index on the 'queryby' attribute
    cur.execute('CREATE UNIQUE INDEX %sidx ON %s(%s)' %
                (queryby, dbConstants._DICT_TABLE, queryby))

    # Setup the 'qmarks' sqlite substring
    qmarks = ('?,' * len(fields))[:-1]

    # Setup the sql substring for inserting fields into database
    fieldsub = ''.join(['%s,' % field for field in fields])[:-1]

    query = 'INSERT INTO %s (%s) VALUES (%s)' %\
            (dbConstants._DICT_TABLE, fieldsub, qmarks)
    # Pull data from the iterator and store in database
    for record in rcrditer:
        data = tuple([record[key] for key in fields])
        cur.execute(query, data)

    con.commit()
    con.close()
