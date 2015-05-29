from __future__ import absolute_import
import os
import screed
from screed.DBConstants import fileExtension
from . import screed_tst_utils as utils
import shutil


class Test_dict_methods(object):

    """
    Make sure that screed returns sensible results for standard dictionary
    queries.
    """

    def setup(self):
        self._testfa = utils.get_temp_filename('test.fa')
        shutil.copy(utils.get_test_data('test.fa'), self._testfa)

        screed.read_fasta_sequences(self._testfa)
        self.db = screed.ScreedDB(self._testfa)

    def teardown(self):
        os.unlink(self._testfa + fileExtension)

    def test_iter_stuff(self):
        db = self.db
        keys = db.keys()
        ikeys = list(db.iterkeys())
        assert all(key in ikeys for key in keys)

        values = db.values()
        ivalues = list(db.itervalues())
        assert all(value in ivalues for value in values)

        items = db.items()
        iitems = list(db.iteritems())
        assert all(item in iitems for item in items)

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert db.get('FOO') is None

        assert 'FOO' not in self.db

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert 'FOO' not in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except NotImplementedError:
            pass

        try:
            db.update({})
            assert 0
        except NotImplementedError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except NotImplementedError:
            pass

        try:
            db.pop()
            assert 0
        except NotImplementedError:
            pass

        try:
            db.popitem()
            assert 0
        except NotImplementedError:
            pass
