# Copyright (c) 2008, Michigan State University.

"""
screed is a database tool useful for retrieving arbitrary kinds of sequence
data through a on-disk database that emulates a read-only Python dictionary.

For opening a screed database, the 'ScreedDB' class is used. This class
accepts a string file path to a pre-created screed database. Read-only
dictionary methods are implemented here.

For creating a screed database, the 'create_db' function is used. This
function accepts an iterator as an argument which will yield records
from its respective sequence file. create_db will sequentially pull
records from the iterator, writing them to disk in a screed database
until the iterator is done.

Automatic ways for parsing FASTA and FASTQ files are accessed through
the read_fast*_sequences functions. These parse the given sequence
file into a screed database.

Conversion between sequence file types is provided in the ToFastq and
ToFasta functions
"""

from __future__ import absolute_import

from screed.openscreed import ScreedDB
from screed.openscreed import Open as open
from screed.conversion import ToFastq
from screed.conversion import ToFasta
from screed.createscreed import create_db, make_db
from screed.seqparse import read_fastq_sequences
from screed.seqparse import read_fasta_sequences
from screed.dna import rc
from screed.screedRecord import Record

from screed._version import get_versions
__version__ = get_versions()['version']
del get_versions

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
