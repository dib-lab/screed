from screedExtension import fileExtension
import UserDict
import os
import sqlite3

# [AN] switch to cursor?
# [AN] remove decision about using querying by name or id

_SCREEDADMIN = 'SCREEDADMIN'
_DICT_TABLE = 'DICTIONARY_TABLE'
_PRIMARY_KEY = 'ID'

class _screed_record(UserDict.DictMixin):
    """
    Simple dict-like record interface with bag behavior.
    """
    def __init__(self, *args, **kwargs):
        self.d = dict(*args, **kwargs)
        
    def __getitem__(self, name):
        return self.d[name]

    def __setitem__(self, name, value):
        self.d[name] = value
    
    def __getattr__(self, name):
        try:
            return self.d[name]
        except KeyError:
            raise AttributeError, name

    def keys(self):
        return self.d.keys()

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

    sqdb = None
    if not os.path.isfile(filepath): # Db file doesn't exist, should I create?
        if fields == None: # Need to create, but don't have fields!
            raise ValueError("Fields not specified and database doesn't exist")
        sqdb = _createSqDb(filepath, fields)
    else:
        sqdb = sqlite3.connect(filepath)

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
    query = 'SELECT FIELDNAME FROM %s' % _SCREEDADMIN
    result, = sqdb.execute(query).next()
    return result.lower()

def _getFieldTuple(sqdb):
    """
    Creates the ordered tuple of fields from the database
    e.x, returns: (id, name, description)
    """
    query = 'SELECT * FROM %s' % _SCREEDADMIN
    result = [_PRIMARY_KEY.lower()]
    for fieldName, fieldType, in sqdb.execute(query):
        result.append(str(fieldName.lower()))

    return tuple(result)

def _createSqDb(filepath, fields):
    """
    Creates the screed database. This consists of a small 'SCREEDADMIN' table which
    holds accounting information such as name and number of fields and a
    'DICTIONARY_TABLE' which holds the actual information to be handled for the user
    """
    sqdb = sqlite3.connect(filepath)

    # Create the admin table
    sqdb.execute('CREATE TABLE %s (FIELDNAME TEXT, FIELDTYPE TEXT)' %
                      _SCREEDADMIN)
    
    query = 'INSERT INTO %s (FIELDNAME, FIELDTYPE) VALUES (?, ?)' % \
            _SCREEDADMIN

    for fieldName, fieldType in fields:
        sqdb.execute(query, (fieldName.upper(), fieldType.upper()))

    # Create the dictionary table
    sqdb.execute('CREATE TABLE %s (%s INTEGER PRIMARY KEY, %s)' %
                      (_DICT_TABLE, _PRIMARY_KEY, toCreateStub(fields)))
    return sqdb

def _retrieveStandardStub(sqdb):
    """
    Retrieves the names of the fields from the admin table and returns a sql sub-
    string that can be used for querying.
    e.x: table contains:
    FIELDNAME      FIELDTYPE
    'NAME'         TEXT
    'DESCRIPTION'  TEXT
    returns: 'NAME, DESCRIPTION'
    """
    sqlList = []
    query = "SELECT * FROM %s" % _SCREEDADMIN
    for fieldName, fieldType in sqdb.execute(query):
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

def _retrieve(sqdb, getQuery):
    retrieved = sqdb.execute(getQuery)

def toCreateStub(fieldTuple):
    """
    Parses the ordered name, value pairs in fieldTuple into a create stub
    ready to be inserted into the command to create the sql table.
    e.x: given input (('name', 'text'), ('description', 'text'))
    returns: 'NAME TEXT, DESCRIPTION TEXT'
    """
    sqlList = []
    for fieldName, fieldType in fieldTuple:
        sqlList.append('%s %s' % (fieldName.upper(), fieldType.upper()))
        sqlList.append(', ')
    sqlList.pop()
    return "".join(sqlList)
