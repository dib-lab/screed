import screed
import os
from dbConstants import fileExtension

def test_nodb():
    """
    Tests if screed throws an appropriate exception if it is
    asked to open a non-screed database
    """
    try:
        db = screed.screedDB('foo')
        assert 1 == 0 # Previous line should throw an error
    except TypeError:
        pass
