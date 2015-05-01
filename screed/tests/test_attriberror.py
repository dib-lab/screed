import screed
from screed.DBConstants import fileExtension
import os
import screed_tst_utils as utils
import shutil


class nostring:
    def __init__(self):
        self.exists = True

    def __str__(self):
        return ""

    def __repr__(self):
        return ""


class test_comparisons():

    def setup(self):
        self._testfile = utils.get_temp_filename('test.fa')
        shutil.copy(utils.get_test_data('test.fa'), self._testfile)
        screed.read_fasta_sequences(self._testfile)

        self._db = screed.ScreedDB(self._testfile)
        self._ns = nostring()

    def test_eq(self):
        for k in self._db:
            record = self._db.get(k)
            res = (record.sequence == self._ns)
            assert res == False, res

    def test_neq(self):
        for k in self._db:
            record = self._db.get(k)
            res = (record.sequence <> self._ns)
            assert res == True, res

    def test_comp_greateq(self):
        for k in self._db:
            record = self._db.get(k)
            res = (record.sequence >= self._ns)
            assert res == True, res

    def test_comp_lesseq(self):
        for k in self._db:
            record = self._db.get(k)
            res = (record.sequence <= self._ns)
            assert res == False, res

    def test_comp_less(self):
        for k in self._db:
            record = self._db.get(k)
            res = (record.sequence < self._ns)
            assert res == False, res

    def test_comp_great(self):
        for k in self._db:
            record = self._db.get(k)
            res = (record.sequence > self._ns)
            assert res == True, res

    def test_le__(self):
        for k in self._db:
            record = self._db.get(k)
            res = record.sequence.__le__(self._ns)
            assert res == NotImplemented, res

    def test_ge__(self):
        for k in self._db:
            record = self._db.get(k)
            res = record.sequence.__ge__(self._ns)
            assert res == NotImplemented, res

    def test_lt__(self):
        for k in self._db:
            record = self._db.get(k)
            res = record.sequence.__lt__(self._ns)
            assert res == NotImplemented, res

    def test_gt__(self):
        for k in self._db:
            record = self._db.get(k)
            res = record.sequence.__gt__(self._ns)
            assert res == NotImplemented, res

    def teardown(self):
        os.unlink(self._testfile + fileExtension)
