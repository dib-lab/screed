import screed
import os

class nostring:
    def __init__(self):
        self.exists = True
    def __str__(self):
        raise AttributeError
    def __repr__(self):
        raise AttributeError

def test_comparisons():
    testfile = os.path.join(os.path.dirname(__file__), 'test.fa')
    screed.read_fasta_sequences(testfile)
    
    db = screed.ScreedDB(testfile)
    ns = nostring()

    for k in db:
        record = db.get(k)
        try:
            res = (record.sequence == ns)
        except TypeError:
            assert True
        except:
            assert False, "should have caught the TypeError"

    for k in db:
        record = db.get(k)
        try:
            res = (record.sequence != ns)
        except TypeError:
            assert True
        except:
            assert False, "should have caught the TypeError"

    for k in db:
        record = db.get(k)
        try:
            res = (record.sequence >= ns)
        except TypeError:
            assert True
        except:
            assert False, "should have caught the TypeError"
