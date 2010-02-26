import UserDict
import types

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

class _screed_attr(object):
    """
    Sliceable database object that supports lazy retrieval
    """
    def __init__(self, dbObj, primaryKey, attrName, rowName, queryBy, tableName):
        """
        dbOjb = database handle
        primaryKey = integer incrementer on table
        attrName = name of attr as in db (CAPS)
        rowName = index/name of row
        queryBy = by name or index
        tableName = name of table to query on
        """
        self._dbObj = dbObj
        self._primaryKey = primaryKey
        self._attrName = attrName
        self._rowName = rowName
        self._queryBy = queryBy
        self._tableName = tableName

    def __getitem__(self, sliceObj):
        """
        Only supports slicing right now. Returns the slice range given. *.start + 1 to
        be compatible with sqlite's 1 not 0 scheme
        """
        assert type(sliceObj) == types.SliceType
        assert sliceObj.start <= sliceObj.stop # Support string reverse in future maybe
        length = sliceObj.stop - sliceObj.start
        
        query = 'SELECT substr(%s, %d, %d) FROM %s WHERE %s = ?' \
                % (self._attrName, sliceObj.start+1, length, self._tableName, self._queryBy)
        result = self._dbObj.execute(query, (str(self._rowName),))
        try:
            subStr, = result.fetchone()
        except TypeError:
            raise KeyError("Key %s not found" % self._rowName)
        if self._attrName == self._primaryKey:
            return int(subStr) - 1 # Hack to make indexing start at 0
        else:
            return str(subStr)

    def __len__(self):
        return len(self.__repr__())

    def __repr__(self):
        """
        Returns the full attribute
        """
        query = 'SELECT %s FROM %s WHERE %s = ?' \
                % (self._attrName, self._tableName, self._queryBy)
        result = self._dbObj.execute(query, (str(self._rowName),))
        try:
            record, = result.fetchone()
        except TypeError:
            raise KeyError("Key %s not found" % self._rowName)
        if self._attrName == self._primaryKey:
            return str(int(record) -1) # Hack to make indexing start at 0
        else:
            return str(record)

    def __int__(self):
        assert self._attrName == self._primaryKey
        return int(self.__repr__())

    def __eq__(self, given):
        if type(given) == types.StringType:
            return given == self.__repr__()

        try:
            if self._attrName == self._primaryKey:
                return int(given) == self.__int__()
            else:
                return str(given) == self.__repr__()
        except AttributeError:
            raise TypeError("Cannot compare to given type: %s" % type(given))

    def __lt__(self, given):
        if type(given) == types.StringType:
            return self.__repr__() < given

        try:
            if self._attrName == self._primaryKey:
                return self.__int__() < int(given)
            else:
                return self.__repr__() < str(given)
        except AttributeError:
            raise TypeError("Cannot compare to given type: %s" % type(given))

    def __le__(self, given):
        if type(given) == types.StringType:
            return self.__repr__() <= given

        try:
            if self._attrName == self._primaryKey:
                return self.__int__() <= int(given)
            else:
                return self.__repr__() <= str(given)
        except AttributeError:
            raise TypeError("Cannot compare to given type: %s" % type(given))

    def __ne__(self, given):
        if type(given) == types.StringType:
            return self.__repr__() != given

        try:
            if self._attrName == self._primaryKey:
                return self.__int__() != int(given)
            else:
                return self.__repr__() != str(given)
        except AttributError:
            raise TypeError("Cannot compare to given type: %s" % type(given))

    def __gt__(self, given):
        if type(given) == types.StringType:
            return self.__repr__() > given

        try:
            if self._attrName == self._primaryKey:
                return self.__int__() > int(given)
            else:
                return self.__repr__() > str(given)
        except AttributeError:
            raise TypeError("Cannot compare to given type: %s" % type(given))

    def __ge__(self, given):
        if type(given) == types.StringType:
            return self.__repr__() >= given

        try:
            if self._attrName == self._primaryKey:
                return self.__int__() >= int(given)
            else:
                return self.__repr__() >= str(given)
        except AttributeError:
            raise TypeError("Cannot compare to given type: %s" % type(given))

    def __str__(self):
        return self.__repr__()

def _buildRecord(fieldNames, dbObj, primaryKey, rowName, queryBy, tableName):
    """
    Constructs a dict-like object with record attribute names as keys and _screed_attr
    objects as values
    """
    accumulator = []
    for name in fieldNames:
        attrObj = _screed_attr(dbObj, primaryKey, name.upper(), rowName, queryBy, tableName)
        accumulator.append((name, attrObj))
    return _screed_record_dict(accumulator)

def _unicode2Str(arg1, arg2):
    """
    Converts arguments to standard string types and returns a tuple. This function
    is meant to be used in conjunction with map()'ping the results of a database
    query with the names of fields to get rid of the ugly u' in front
    """
    if type(arg2) == types.UnicodeType:
        return (arg1, str(arg2))

    return (arg1, arg2)
