from __future__ import absolute_import, unicode_literals
import screed
from screed.DBConstants import fileExtension
from screed.screedRecord import write_fastx
import os
from io import StringIO
from io import BytesIO
from . import screed_tst_utils as utils
import shutil
import pytest


class FakeRecord(object):
    """Empty extensible object"""
    pass


def test_new_record():
    # test for a bug where the record dict was not reset after each
    # sequence load, leading to all records being identical if you
    # kept a handle on the returned dictionary.

    s = StringIO("@1\nACTG\n+\nAAAA\n@2\nACGG\n+\nAAAA\n")

    records = list(iter(screed.fastq.fastq_iter(s)))
    assert records[0]['name'] == '1'
    assert records[1]['name'] == '2'


def test_parse_description_true():
    # test for a bug where the record dict was not reset after each
    # sequence load, leading to all records being identical if you
    # kept a handle on the returned dictionary.

    s = StringIO("@1 FOO\nACTG\n+\nAAAA\n@2\nACGG\n+\nAAAA\n")

    records = list(iter(screed.fastq.fastq_iter(s, parse_description=True)))
    assert records[0]['name'] == '1'
    assert records[1]['name'] == '2'


def test_parse_description_false():
    # test for a bug where the record dict was not reset after each
    # sequence load, leading to all records being identical if you
    # kept a handle on the returned dictionary.

    s = StringIO("@1 FOO\nACTG\n+\nAAAA\n@2\nACGG\n+\nAAAA\n")

    records = list(iter(screed.fastq.fastq_iter(s, parse_description=False)))
    assert records[0]['name'] == '1 FOO'
    assert records[1]['name'] == '2'

    # also is default behavior
    s = StringIO("@1 FOO\nACTG\n+\nAAAA\n@2\nACGG\n+\nAAAA\n")

    records = list(iter(screed.fastq.fastq_iter(s)))
    assert records[0]['name'] == '1 FOO'
    assert records[1]['name'] == '2'


class Test_fastq(object):

    def setup(self):
        self._testfq = utils.get_temp_filename('test.fastq')
        shutil.copy(utils.get_test_data('test.fastq'), self._testfq)

        screed.read_fastq_sequences(self._testfq)
        self.db = screed.ScreedDB(self._testfq)

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
        assert first.quality == 'AA7AAA3+AAAAAA.AAA.;7;AA;;;;*;<1;<<<'

    def test_contains_middle(self):
        middle = self.db[self.db.keys()[62]]
        assert middle.id == 62
        assert middle.name == 'HWI-EAS_4_PE-FC20GCB:2:1:245:483/2'
        assert middle.sequence == 'TGTCGAGCAAAGCAAAACAGGCGTAAAAATTGCCAT'
        assert middle.quality == 'AAAAAAAAAAAAAAAAAAAAA>AAAAAAAA?9>6><'

    def test_contains_end(self):
        end = self.db[self.db.keys()[124]]
        assert end.id == 124
        assert end.name == 'HWI-EAS_4_PE-FC20GCB:2:1:350:588/2'
        assert end.sequence == 'GGTACAAAATAGATGCTGGACTCTCCGAATCCTATA'
        assert end.quality == ';?5AAAAAAAAAA?A??;?AA;AAA>AAAA?4?844'

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


def test_output_sans_desc():
    read = FakeRecord()
    read.name = 'foo'
    read.sequence = 'ATCG'
    read.quality = '####'

    fileobj = BytesIO()
    write_fastx(read, fileobj)
    assert fileobj.getvalue().decode('utf-8') == '@foo\nATCG\n+\n####\n'


def test_output_with_desc():
    read = FakeRecord()
    read.name = 'foo'
    read.description = 'bar'
    read.sequence = 'ATCG'
    read.quality = '####'

    fileobj = BytesIO()
    write_fastx(read, fileobj)
    assert fileobj.getvalue().decode('utf-8') == '@foo bar\nATCG\n+\n####\n'


def test_output_two_reads():
    fileobj = BytesIO()
    for i in range(2):
        read = FakeRecord()
        read.name = 'seq{}'.format(i)
        read.sequence = 'GATTACA' * (i + 1)
        read.quality = '#######' * (i + 1)
        write_fastx(read, fileobj)
    testoutput = ('@seq0\nGATTACA\n+\n#######\n'
                  '@seq1\nGATTACAGATTACA\n+\n##############\n')
    assert fileobj.getvalue().decode('utf-8') == testoutput


def test_output_bad_mode():
    read = FakeRecord()
    read.name = 'foo'
    read.description = 'bar'
    read.sequence = 'ATCG'
    read.quality = '####'

    fileobj = StringIO()
    with pytest.raises(AttributeError) as ae:
        write_fastx(read, fileobj)
    assert 'cannot call "write_fastx" on object' in str(ae)


def test_fastq_slicing():
    testfq = utils.get_temp_filename('test.fastq')
    shutil.copy(utils.get_test_data('test.fastq'), testfq)

    with screed.open(testfq) as sequences:
        record = next(sequences)

    trimmed = record[:10]
    assert trimmed['sequence'] == "ACAGCAAAAT"
    assert trimmed['quality'] == "AA7AAA3+AA"

    for s in (slice(5, 10), slice(2, 26), slice(5, -1, 2),
              slice(-2, -10, 1), slice(-1, 5, 2), slice(5)):
        trimmed = record[s]

        assert trimmed['name'] == record['name']
        assert trimmed.name == record.name

        assert trimmed['sequence'] == record['sequence'][s]
        assert trimmed.sequence == record.sequence[s]

        assert trimmed['quality'] == record['quality'][s]
        assert trimmed.quality == record.quality[s]
