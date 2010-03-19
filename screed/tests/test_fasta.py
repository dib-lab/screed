import screed
from dbConstants import fileExtension
import os

class Test_fasta(object):
    def setup(self):
        self._testfa = os.path.join(os.path.dirname(__file__), 'test.fa')
        screed.read_fasta_sequences(self._testfa)
        self.db = screed.screedDB(self._testfa)

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

    def test_contains_front(self):
        first = self.db[self.db.keys()[0]]
        assert first.id == 0
        assert first.name == 'ENSMICT00000012722'
        assert first.description == 'cdna:pseudogene scaffold:micMur1:'\
               'scaffold_185008:9:424:1 gene:ENSMICG00000012730'
        assert str(first.sequence).startswith('TGCAGAAAATATCAAGAGTCAGC'\
                                              'AGAAAAACTATACAAGGGCTGGT'\
                                              'ATTTTGATTATTCT')

    def test_contains_middle(self):
        middle = self.db[self.db.keys()[10]]
        assert middle.id == 10
        assert middle.name == 'ENSMICT00000012078'
        assert middle.description == 'cdna:pseudogene scaffold:micMur1'\
               ':scaffold_180699:3:774:-1 gene:ENSMICG00000012085'
        assert str(middle.sequence).startswith('GCGCACTCCCAGTGGCTACCCA'\
                                               'CGGCAGGAGGCGGCGGCAGTGA'\
                                               'CTGGGCCGGCGGCCCG')

    def test_contains_end(self):
        end = self.db[self.db.keys()[21]]
        assert end.id == 21
        assert end.name == 'ENSMICT00000003880'
        assert end.description == 'cdna:novel scaffold:micMur1:scaffol'\
               'd_175819:130:631:1 gene:ENSMICG00000003884'
        assert str(end.sequence).startswith('ATGCTGCCTAAGTTTGACCCCAACG'\
                                            'CGATCAAAGTCATGTACCTGAGGTG'\
                                            'CACGGGTGGC')

    def test_contains(self):
        for k in self.db:
            assert self.db.has_key(k)

        assert self.db.get('FOO') == None

        assert not 'FOO' in self.db

    def test_iterv(self):
        entries = []
        for entry in self.db:
            entries.append(self.db[entry])

        ivalues = list(self.db.itervalues())
        assert sorted(entries) == sorted(ivalues)

    def test_iteri(self):
        for id, entry in self.db.iteritems():
            assert id == self.db[entry.name].id
            assert entry == self.db[entry.name]
