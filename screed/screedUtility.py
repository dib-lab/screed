# Copyright (c) 2008-2010, Michigan State University

import dbConstants
import os
import sqlite3
import types

def getScreedDB(filepath):
    """
    Opens a screed database ready for querying. filepath is the string
    path to the screed database to open. Returns a 5 tuple containing:
    (database object, _standardStub, _fieldTuple, _qMarks, _queryBy)
    """
    # Ensure the filepath is correctly formatted with the extension to
    # the database filename
    if not filepath.endswith(dbConstants.fileExtension):
        filepath += dbConstants.fileExtension

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

    return (sqdb, _standardStub, _fieldTuple, _qMarks, _queryBy)

def _getQueryBy(sqdb):
    """
    Retrieves the name of the field used for querying by name in the database.
    This is the name of the first field in the administration table
    """
    query = 'SELECT FIELDNAME FROM %s WHERE ID=1' % dbConstants._SCREEDADMIN
    result, = sqdb.execute(query).fetchone()
    return result

def _getFieldTuple(sqdb):
    """
    Creates the ordered tuple of fields from the database
    e.x, returns: (id, name, description)
    """
    query = 'SELECT FIELDNAME FROM %s' % dbConstants._SCREEDADMIN
    result = [dbConstants._PRIMARY_KEY.lower()]
    for fieldName, in sqdb.execute(query):
        result.append(fieldName)

    return tuple(result)

def _retrieveStandardStub(sqdb):
    """
    Retrieves the names of the fields from the admin table and returns an
    sql substring that can be used for querying.
    e.x: table contains:
    FIELDNAME
    'name'
    'description'
    returns: 'name, description'
    """
    query = "SELECT FIELDNAME FROM %s" % dbConstants._SCREEDADMIN
    return "".join(['%s,' % fieldName for fieldName in sqdb.execute(query)])[:-1]

def _toQmarks(sqdb):
    """
    Retrieves the count of items in the admin table and builds the sql question
    marks in the format needed for substitution into an sql query
    e.x: table has 3 elements
    returns: '?, ?, ?'
    """
    query = "SELECT COUNT(1) FROM %s" % dbConstants._SCREEDADMIN
    result, = sqdb.execute(query).fetchone()
    return ("?," * result)[:-1]
