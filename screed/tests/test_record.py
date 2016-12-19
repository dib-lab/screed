from __future__ import absolute_import, unicode_literals, print_function
from screed import Record
import pytest


@pytest.mark.xfail(raises=TypeError)
def test_create_noname():
    r = Record(sequence='ATGGAC')


@pytest.mark.xfail(raises=TypeError)
def test_create_noseq():
    r = Record(name='somename')


# copied over from khmer tests/test_read_parsers.py
def test_read_type_basic():
    # Constructing without mandatory arguments should raise an exception
    with pytest.raises(TypeError):
        Record()

    name = "895:1:1:1246:14654 1:N:0:NNNNN"
    sequence = "ACGT"
    r = Record(name, sequence)

    assert r.name == name
    assert r.sequence == sequence
    assert not hasattr(r, 'quality'), x
    assert not hasattr(r, 'annotations'), x
