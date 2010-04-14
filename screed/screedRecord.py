import UserDict
import types
import dbConstants

class _screed_record_dict(UserDict.DictMixin):
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

# [AN] why is tableName needed?
class _screed_attr(object):
    """
    Sliceable database object that supports lazy retrieval
    """
    def __init__(self, dbObj, attrName, rowName, queryBy,
                 tableName):
        """
        Initializes database object with specific record retrieval
        information
        dbOjb = database handle
        attrName = name of attr in db
        rowName = index/name of row
        queryBy = by name or index
        tableName = name of table to query on
        """
        self._dbObj = dbObj
        self._attrName = attrName
        self._rowName = rowName
        self._queryBy = queryBy
        self._tableName = tableName

    def __getitem__(self, sliceObj):
        """
        Slicing interface. Returns the slice range given.
        *.start + 1 to be compatible with sqlite's 1 not 0 scheme
        """
        if type(sliceObj) != types.SliceType:
            raise TypeError('__getitem__ argument must be of slice type')
        if not sliceObj.start <= sliceObj.stop: # String reverse in future?
            raise ValueError('start must be less than stop in slice object')
        length = sliceObj.stop - sliceObj.start
        
        query = 'SELECT substr(%s, %d, %d) FROM %s WHERE %s = ?' \
                % (self._attrName, sliceObj.start+1, length, self._tableName,
                   self._queryBy)
        cur = self._dbObj.cursor()
        result = cur.execute(query, (str(self._rowName),))
        try:
            subStr, = result.fetchone()
        except TypeError:
            raise KeyError("Key %s not found" % self._rowName)
        return str(subStr)

    def __len__(self):
        """
        Returns the length of the string
        """
        return len(self.__repr__())

    def __repr__(self):
        """
        Alias for __str__
        """
        return self.__str__()

    def __cmp__(self, given):
        """
        Handles comparisons other than == and !=
        """
        ownString = __str__()
        if isinstance(given, _screed_attr):
            given = str(given)
        elif not isinstance(given, str):
            raise TypeError("Cannot compare to given type: %s" % type(given))

        if ownString < given:
            return -1
        elif ownString > given:
            return 1
        else:
            return 0

    def __eq__(self, given):
        """
        Compares attribute to given object in string form
        """
        if type(given) == types.StringType:
            return given == self.__str__()

        try:
            return str(given) == self.__str__()
        except AttributeError:
            raise TypeError("Cannot compare to given type: %s" % type(given))

    def __ne__(self, given):
        """
        Compares attribute to given object in string form
        """
        if type(given) == types.StringType:
            return self.__repr__() != given

        try:
            return self.__repr__() != str(given)
        except AttributError:
            raise TypeError("Cannot compare to given type: %s" % type(given))

    def __str__(self):
        """
        Returns the full attribute as a string
        """
        query = 'SELECT %s FROM %s WHERE %s = ?' \
                % (self._attrName, self._tableName, self._queryBy)
        cur = self._dbObj.cursor()
        result = cur.execute(query, (str(self._rowName),))
        try:
            record, = result.fetchone()
        except TypeError:
            raise KeyError("Key %s not found" % self._rowName)
        return str(record)

def _buildRecord(fieldTuple, dbObj, rowName, queryBy, tableName):
    """
    Constructs a dict-like object with record attribute names as keys and
    _screed_attr objects as values
    """

    # Separate the lazy and full retrieval objects
    kvResult = []
    fullRetrievals = []
    for fieldname, role in fieldTuple:
        if role == dbConstants._SLICABLE_TEXT:
            kvResult.append((fieldname, _screed_attr(dbObj,
                                                    fieldname, rowName,
                                                    queryBy, tableName)))
        else:
            fullRetrievals.append(fieldname)

    # Retrieve the full text fields from the db
    subs = ','.join(fullRetrievals)
    query = 'SELECT %s FROM %s WHERE %s=?' % \
            (subs, tableName, queryBy)
    cur = dbObj.cursor()
    res = cur.execute(query, (rowName,))

    # Add the full text fields to the result tuple list
    kvResult.extend(zip(fullRetrievals, res.fetchone()))

    # Hack to make indexing start at 0
    hackedResult = []
    for key, value in kvResult:
        if key == dbConstants._PRIMARY_KEY:
            hackedResult.append((key, value-1))
        else:
            hackedResult.append((key, value))

    return _screed_record_dict(hackedResult)
