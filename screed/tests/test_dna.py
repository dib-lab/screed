import os
import screed
from screed.DBConstants import fileExtension


class Test_dna(object):

    """Tests the dna module of screed"""
    def test_is_DNA(args):
        valid_DNA_str = "ATCCG"
        invalid_DNA_str = "ATXXG"
        assert screed.dna.is_DNA(valid_DNA_str)
        assert not screed.dna.is_DNA(invalid_DNA_str)

    def test_complement(args):
        dna = "ATCCG"
        comp = "TAGGC"
        assert screed.dna.complement(dna) == comp

    def test_reverse(args):
        dna = "ATCCG"
        reverse = "GCCTA"
        assert screed.dna.reverse(dna) == reverse

    def test_reverse_complement(args):
        dna = "ATCCG"
        reverse_complement = "CGGAT"
        assert screed.dna.reverse_complement(dna) == reverse_complement
