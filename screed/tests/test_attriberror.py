import screed
import os

class nostring:
    def __init__(self):
        self.exists = True
    def __str__(self):
        raise AttributeError
    def __repr__(self):
        raise AttributeError

def test_eq():
    testfile = os.path.join(os.path.dirname(__file__), 'test.fa')
    ns = nostring()

    for r in screed.open(testfile):
        r.sequence == ns

