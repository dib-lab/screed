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

def _unicode2Str(arg1, arg2):
    """
    Converts arguments to standard string types and returns a tuple. This function
    is meant to be used in conjunction with map()'ping the results of a database
    query with the names of fields to get rid of the ugly u' in front
    """
    if type(arg2) == types.UnicodeType:
        return (arg1, str(arg2))

    return (arg1, arg2)
