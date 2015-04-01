import screed
import os
import ipdb

class nostring:
    def __init__(self):
        self.exists = True
    def __str__(self):
        raise Exception
    def __repr__(self):
        raise Exception

def test_eq():
    testfile = os.path.join(os.path.dirname(__file__), 'test.fa')
    ns = nostring()

    for r in screed.open(testfile):
        r.sequence.__eq__(ns)
        # # # # # # # # ipdb.set_trace()

