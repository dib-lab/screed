import array
import string

legal_dna = "ACGTN"


def is_DNA(seq):
    """
    Returns 1 if it contains only legal values for a DNA sequence.

    c.f.  http://www.ncbi.nlm.nih.gov/BLAST/fasta.html
    """
    for ch in seq:
        if ch not in legal_dna:
            return 0

    return 1


def reverse_complement(s):
    """
    Build reverse complement of 's'.
    """
    s = s.upper()
    assert is_DNA(s), "Your sequence must be DNA!"

    r = reverse(s)
    rc = complement(r)

    return rc


rc = reverse_complement                 # alias 'rc' to 'reverse_complement'

try:
    __complementTranslation = str.maketrans('ACTG', 'TGAC')
except AttributeError:
    __complementTranslation = string.maketrans('ACTG', 'TGAC')


def complement(s):
    """
    Return complement of 's'.
    """
    c = s.translate(__complementTranslation)
    return c


def reverse(s):
    """
    Return reverse of 's'.
    """
    r = "".join(reversed(s))

    return r
