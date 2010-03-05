# Copyright (c) 2008-2010, Michigan State University

from screedExtension import fileExtension
import os
import sqlite3
import types

_SCREEDADMIN = 'SCREEDADMIN'
_DICT_TABLE = 'DICTIONARY_TABLE'
_PRIMARY_KEY = 'ID'

def getScreedDB(filepath, fields=None):
    """
    Opens and prepares a screedDB. The order of arguments is:
    filepath: the string path to the screed database to open
    fields: either None if the the database has already been created or
        a tuple of 2-tuples specifying the names and types of fields
        to be used in the creation of the sql database. The first element
        in fields will be the 'key' or 'name' used to query the database
        later
    Returns a 7 tuple containing:
    (database object, _standardStub, _fieldTuple, _qMarks, _DICT_TABLE,
    _queryBy, _PRIMARY_KEY)
    """
    # Ensure the filepath is correctly formatted with the extension to
    # the database filename
    if not filepath.endswith(fileExtension):
        filepath += fileExtension

    if type(fields) != types.NoneType:
        assert type(fields[0]) == types.StringType

    sqdb = None
    _queryBy = None
    if not os.path.isfile(filepath): # Db file doesn't exist, should I create?
        if fields == None: # Need to create, but don't have fields!
            raise ValueError("Fields not specified and database doesn't exist")
        sqdb, _queryBy = _createSqDb(filepath, fields)
    else:
        sqdb = sqlite3.connect(filepath)
        _queryBy = _getQueryBy(sqdb)

    # Create the standard sql query stub
    _standardStub = _retrieveStandardStub(sqdb)

    # Get the name/key used for querying the database
    _queryBy = _getQueryBy(sqdb)

    # Create the ordered tuple of fields
    _fieldTuple = _getFieldTuple(sqdb)

    # Create the string of question marks
    _qMarks = _toQmarks(sqdb)

    return (sqdb, _standardStub, _fieldTuple, _qMarks, _DICT_TABLE,
            _queryBy, _PRIMARY_KEY)

def _getQueryBy(sqdb):
    """
    Retrieves the name of the field used for querying by name in the database.
    This is the name of the first field in the administration table
    """
    query = 'SELECT FIELDNAME FROM %s WHERE ID=1' % _SCREEDADMIN
    result, = sqdb.execute(query).next()
    return result.lower()

def _getFieldTuple(sqdb):
    """
    Creates the ordered tuple of fields from the database
    e.x, returns: (id, name, description)
    """
    query = 'SELECT FIELDNAME FROM %s' % _SCREEDADMIN
    result = [_PRIMARY_KEY.lower()]
    for fieldName, in sqdb.execute(query):
        result.append(str(fieldName.lower()))

    return tuple(result)

def _createSqDb(filepath, fields):
    """
    Creates the screed database. This consists of a small 'SCREEDADMIN' table which
    holds accounting information such as name and number of fields and a
    'DICTIONARY_TABLE' which holds the actual information to be handled for the user
    """
    sqdb = sqlite3.connect(filepath)

    c = sqdb.cursor()

    # Create the admin table
    c.execute('CREATE TABLE %s (ID INTEGER PRIMARY KEY, FIELDNAME TEXT)' %
                      _SCREEDADMIN)

    query = 'INSERT INTO %s (FIELDNAME) VALUES (?)' % \
            _SCREEDADMIN

    for fieldName in fields:
        c.execute(query, (fieldName.upper(),))

    _queryBy = _getQueryBy(c)

    # Create the dictionary table
    c.execute('CREATE TABLE %s (%s INTEGER PRIMARY KEY, %s)' %
                      (_DICT_TABLE, _PRIMARY_KEY, toCreateStub(fields)))
    # Create the dictionary index
    c.execute('CREATE UNIQUE INDEX %sidx ON %s(%s)' % (_queryBy, _DICT_TABLE, _queryBy))
    return sqdb, _queryBy

def _retrieveStandardStub(sqdb):
    """
    Retrieves the names of the fields from the admin table and returns a sql sub-
    string that can be used for querying.
    e.x: table contains:
    FIELDNAME
    'NAME'
    'DESCRIPTION'
    returns: 'NAME, DESCRIPTION'
    """
    sqlList = []
    query = "SELECT FIELDNAME FROM %s" % _SCREEDADMIN
    for fieldName, in sqdb.execute(query):
        sqlList.append('%s' % fieldName)
        sqlList.append(', ')
    sqlList.pop()
    return str("".join(sqlList))

def _toQmarks(sqdb):
    """
    Retrieves the count of items in the admin table and builds the sql question
    marks in the format needed for substitution into an sql query
    e.x: table has 3 elements
    returns: '?, ?, ?'
    """
    sqlList = []
    query = "SELECT COUNT(1) FROM %s" % _SCREEDADMIN
    result, = sqdb.execute(query).next()
    for i in xrange(0, result):
        sqlList.append("?")
        sqlList.append(", ")
    sqlList.pop()
    return "".join(sqlList)

def toCreateStub(fieldTuple):
    """
    Parses the ordered names of attributes in fieldTuple into a create stub
    ready to be inserted into the command to create the sql table.
    e.x: given input: ('name', 'description')
    returns: 'NAME TEXT, DESCRIPTION TEXT'
    """
    sqlList = []
    for fieldName in fieldTuple:
        sqlList.append('%s TEXT' % fieldName.upper())
        sqlList.append(', ')
    sqlList.pop()
    return "".join(sqlList)
