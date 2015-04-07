import screed
from screed.DBConstants import fileExtension
import os


class nostring:
    def __init__(self):
        self.exists = True

    def __str__(self):
        raise AttributeError

    def __repr__(self):
        raise AttributeError

    def __cmp__(self):
        raise AttributeError


class test_comparisons():

    def setup(self):
        self._testfile = os.path.join(os.path.dirname(__file__), 'test.fa')
        screed.read_fasta_sequences(self._testfile)

        self._db = screed.ScreedDB(self._testfile)
        self._ns = nostring()

    def test_eq(self):
        for k in self._db:
            record = self._db.get(k)
            try:
                res = (record.sequence == self._ns)
                assert False, "should have thrown a TypeError"
            except TypeError:
                pass

    def test_neq(self):
        for k in self._db:
            record = self._db.get(k)
            try:
                res = (record.sequence != self._ns)
                assert False, "should have thrown a TypeError"
            except TypeError:
                pass

    def test_comp_greateq(self):
        for k in self._db:
            record = self._db.get(k)
            try:
                seq = record.sequence
                res = (seq >= self._ns)
                assert False, "should have thrown a NotImplementedError"
            except NotImplementedError:
                pass

    def test_comp_lesseq(self):
        for k in self._db:
            record = self._db.get(k)
            try:
                res = (record.sequence <= self._ns)
                assert False, "Should hae thrown a NotImplementedError"
            except NotImplementedError:
                pass

    def test_comp_less(self):
        for k in self._db:
            record = self._db.get(k)
            try:
                res = (record.sequence < self._ns)
                assert False, "Should have thrown a NotImplementedError"
            except NotImplementedError:
                pass

    def test_comp_great(self):
        for k in self._db:
            record = self._db.get(k)
            try:
                res = (record.sequence > self._ns)
                assert False, "Should have thrown a NotImplementedError"
            except NotImplementedError:
                pass

    def teardown(self):
        os.unlink(self._testfile + fileExtension)
