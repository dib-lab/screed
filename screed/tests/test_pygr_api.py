from __future__ import absolute_import, unicode_literals

import pytest
pygr = pytest.importorskip("pygr")

import screed  # nopep8
from screed.DBConstants import fileExtension  # nopep8
from screed.pygr_api import ScreedSequenceDB, ScreedSequenceDB_ByIndex  # nopep8
from pickle import dump, load  # nopep8
from io import StringIO  # nopep8
import os  # nopep8

testfa = os.path.join(os.path.dirname(__file__), 'test.fa')


def setup():
    screed.read_fasta_sequences(testfa)


def teardown():
    os.unlink(testfa + fileExtension)


def test_name_iterator_methods():
    db = ScreedSequenceDB(testfa)

    # test the various iterator methods for equal results from db
    a = sorted([(x, db[x]) for x in db])
    b = sorted([i for i in db.iteritems()])
    c = sorted([(v.name, v) for v in db.itervalues()])

    assert a == b
    assert a == c


def test_index_iterator_methods():
    db = ScreedSequenceDB_ByIndex(testfa)

    # test the various iterator methods for equal results from db
    m = sorted([(x, db[x]) for x in db])
    n = sorted([i for i in db.iteritems()])
    o = sorted([(v.record.id, v) for v in db.itervalues()])

    assert m == n
    assert m == o, (m, o)


def test_name_index_equality():
    db1 = ScreedSequenceDB(testfa)
    db2 = ScreedSequenceDB_ByIndex(testfa)

    # must use something other than the obj itself for comparison...
    v1 = sorted([(v.name, v.seq) for v in db1.itervalues()])
    v2 = sorted([(v.name, v.seq) for v in db2.itervalues()])
    assert v1 == v2, (v1, v2)


def test_seqinfodict_by_name():
    db1 = ScreedSequenceDB(testfa)
    sd = db1.seqInfoDict

    m = sorted([y.id for (x, y) in sd.iteritems()])
    n = sorted([x.id for x in sd.itervalues()])

    assert m == n, (m, n)


def test_seqinfodict_by_index():
    db1 = ScreedSequenceDB_ByIndex(testfa)
    sd = db1.seqInfoDict

    m = sorted([x for (x, y) in sd.iteritems()])
    n = sorted([x for x in sd.iterkeys()])

    assert m == n, (m, n)


def test_pickle_ByName():
    db = ScreedSequenceDB(testfa)
    ofp = StringIO()

    dump(db, ofp)

    ifp = StringIO(ofp.getvalue())
    db2 = load(ifp)
    assert db.filepath == db2.filepath


def test_pickle_ByIndex():
    db = ScreedSequenceDB_ByIndex(testfa)
    ofp = StringIO()

    dump(db, ofp)

    ifp = StringIO(ofp.getvalue())
    db2 = load(ifp)
    assert db.filepath == db2.filepath
