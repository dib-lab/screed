import screed
from dbConstants import fileExtension
import os

class Test_fastq(object):
    def setup(self):
        self._testfq = os.path.join(os.path.dirname(__file__), 'test.fastq')
        screed.read_fastq_sequences(self._testfq)
        self.db = screed.screedDB(self._testfq)

    def teardown(self):
        os.unlink(self._testfq + fileExtension)

    def test_length(self):
        assert len(self.db) == 125

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
        assert first.name == 'HWI-EAS_4_PE-FC20GCB:2:1:492:573/2'
        assert first.sequence == 'ACAGCAAAATTGTGATTGAGGATGAAGAACTGCTGT'
        assert first.accuracy == 'AA7AAA3+AAAAAA.AAA.;7;AA;;;;*;<1;<<<'

    def test_contains_middle(self):
        middle = self.db[self.db.keys()[62]]
        assert middle.id == 62
        assert middle.name == 'HWI-EAS_4_PE-FC20GCB:2:1:245:483/2'
        assert middle.sequence == 'TGTCGAGCAAAGCAAAACAGGCGTAAAAATTGCCAT'
        assert middle.accuracy == 'AAAAAAAAAAAAAAAAAAAAA>AAAAAAAA?9>6><'

    def test_contains_end(self):
        end = self.db[self.db.keys()[124]]
        assert end.id == 124
        assert end.name == 'HWI-EAS_4_PE-FC20GCB:2:1:350:588/2'
        assert end.sequence == 'GGTACAAAATAGATGCTGGACTCTCCGAATCCTATA'
        assert end.accuracy == ';?5AAAAAAAAAA?A??;?AA;AAA>AAAA?4?844'

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
