from __future__ import absolute_import, unicode_literals
import screed
from screed.DBConstants import fileExtension
import os
from io import StringIO
from . import screed_tst_utils as utils
import shutil


def test_new_record():
    # test for a bug where the record dict was not reset after each
    # sequence load, leading to all records being identical if you
    # kept a handle on the returned dictionary.

    s = StringIO(">1\nACTG\n>2\nACGG\n")

    records = list(iter(screed.fasta.fasta_iter(s)))
    assert records[0]['name'] == '1'
    assert records[1]['name'] == '2'


class Test_fasta(object):

    def setup(self):
        self._testfa = utils.get_temp_filename('test.fa')
        shutil.copy(utils.get_test_data('test.fa'), self._testfa)

        screed.read_fasta_sequences(self._testfa)
        self.db = screed.ScreedDB(self._testfa)

    def teardown(self):
        os.unlink(self._testfa + fileExtension)

    def test_length(self):
        assert len(self.db) == 22

    def test_keys(self):
        for key in self.db:
            assert key == self.db[key].name

    def test_id_retrieval(self):
        for key in self.db:
            record = self.db[key]
            intRcrd = self.db.loadRecordByIndex(record.id)
            assert record == intRcrd

    def test_length_2(self):
        read = self.db[self.db.keys()[0]]

        assert len(read) == len(read.sequence)

    def test_contains_front(self):
        first = self.db[self.db.keys()[0]]
        assert first.id == 0
        assert first.name == 'ENSMICT00000012722'
        assert first.description == 'cdna:pseudogene scaffold:micMur1:'\
            'scaffold_185008:9:424:1 gene:ENSMICG00000012730'
        assert str(first.sequence).startswith('TGCAGAAAATATCAAGAGTCAGC'
                                              'AGAAAAACTATACAAGGGCTGGT'
                                              'ATTTTGATTATTCT')

    def test_contains_middle(self):
        middle = self.db[self.db.keys()[10]]
        assert middle.id == 10
        assert middle.name == 'ENSMICT00000012078'
        assert middle.description == 'cdna:pseudogene scaffold:micMur1'\
            ':scaffold_180699:3:774:-1 gene:ENSMICG00000012085'
        assert str(middle.sequence).startswith('GCGCACTCCCAGTGGCTACCCA'
                                               'CGGCAGGAGGCGGCGGCAGTGA'
                                               'CTGGGCCGGCGGCCCG')

    def test_contains_end(self):
        end = self.db[self.db.keys()[21]]
        assert end.id == 21
        assert end.name == 'ENSMICT00000003880'
        assert end.description == 'cdna:novel scaffold:micMur1:scaffol'\
            'd_175819:130:631:1 gene:ENSMICG00000003884'
        assert str(end.sequence).startswith('ATGCTGCCTAAGTTTGACCCCAACG'
                                            'CGATCAAAGTCATGTACCTGAGGTG'
                                            'CACGGGTGGC')

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert self.db.get('FOO') is None

        assert 'FOO' not in self.db

    def test_iterv(self):
        entries = []
        for entry in self.db:
            entries.append(self.db[entry])

        ivalues = list(self.db.itervalues())
        assert all(entry in ivalues for entry in entries)

    def test_iteri(self):
        for id, entry in self.db.iteritems():
            assert id == self.db[entry.name].id
            assert entry == self.db[entry.name]


class Test_fasta_whitespace(object):

    def setup(self):
        self._testfa = utils.get_temp_filename('test-whitespace.fa')
        shutil.copy(utils.get_test_data('test-whitespace.fa'), self._testfa)

        screed.read_fasta_sequences(self._testfa)
        self.db = screed.ScreedDB(self._testfa)

    def test_for_omitted_record(self):
        assert 'ENSMICT00000012401' in self.db

    def teardown(self):
        os.unlink(self._testfa + fileExtension)


def test_writer():
    fp = StringIO()
    w = screed.fasta.FASTA_Writer("", fp)

    class FakeRecord(object):
        pass

    read = FakeRecord()
    read.name = 'foo'
    read.description = 'bar'
    read.sequence = 'ATCG'

    w.write(read)

    assert fp.getvalue() == '>foo bar\nATCG\n'


def test_writer_2():
    fp = StringIO()
    w = screed.fasta.FASTA_Writer("", fp)

    class FakeRecord(object):
        pass

    read = FakeRecord()
    read.name = 'foo'
    read.description = 'bar'
    read.sequence = 'ATCG'

    read_iter = [read]

    w.consume(read_iter)

    assert fp.getvalue() == '>foo bar\nATCG\n'


def test_fasta_slicing():
    testfa = utils.get_temp_filename('test.fa')
    shutil.copy(utils.get_test_data('test.fa'), testfa)

    with screed.open(testfa) as sequences:
        record = next(sequences)

    trimmed = record[:10]
    assert trimmed['sequence'] == "TGCAGAAAAT"

    for s in (slice(5, 10), slice(2, 26), slice(5, -1, 2),
              slice(-2, -10, 1), slice(-1, 5, 2), slice(5)):
        trimmed = record[s]

        assert trimmed['name'] == record['name']
        assert trimmed.name == record.name

        assert trimmed['description'] == record['description']
        assert trimmed.description == record.description

        assert trimmed['sequence'] == record['sequence'][s]
        assert trimmed.sequence == record.sequence[s]
