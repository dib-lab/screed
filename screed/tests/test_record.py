from __future__ import absolute_import, unicode_literals, print_function
from screed import Record
import pytest


def test_create_quality_none():
    r = Record(name='foo', sequence='ATGACG', quality=None)
    assert not hasattr(r, 'quality')


def test_len():
    r = Record(name='foo', sequence='ATGACG')
    assert len(r) == 6


# copied over from khmer tests/test_read_parsers.py
def test_read_type_basic():
    name = "895:1:1:1246:14654 1:N:0:NNNNN"
    sequence = "ACGT"
    r = Record(name, sequence)

    assert r.name == name
    assert r.sequence == sequence
    assert not hasattr(r, 'quality'), x
    assert not hasattr(r, 'annotations'), x


# copied over from khmer tests/test_read_parsers.py
def test_read_type_attributes():
    r = Record(sequence='ACGT', quality='good', name='1234', annotations='ann')
    assert r.sequence == 'ACGT'
    assert r.quality == 'good'
    assert r.name == '1234'
    assert r.annotations == 'ann'
