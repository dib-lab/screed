# This file contains the classes of entries that will go in each database

import UserDict

FASTQFIELDS = ['index', 'name', 'sequence', 'accuracy']

class _sqeaqr_record(UserDict.DictMixin):
    """
    Simple dict-like record interface with bag behavior.
    """
    def __init__(self, *args, **kwargs):
        self.d = dict(*args, **kwargs)
        
    def __getitem__(self, name):
        return self.d[name]
    
    def __getattr__(self, name):
        try:
            return self.d[name]
        except KeyError:
            raise AttributeError, name

    def keys(self):
        return self.d.keys()


class fastqEntry(object):
    """ Holds entry data for entries in a fastq-derived database """
    def __init__(self, index=0, name='', sequence='', accuracy=''):
        self.index = index
        self.name = str(name)
        self.sequence = str(sequence)
        self.accuracy = str(accuracy)
