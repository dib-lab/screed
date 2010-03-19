# Copyright (c) 2008-2010, Michigan State University

"""
screed is a database tool useful for retrieving arbitrary kinds of sequence
data through a on-disk database that emulates a read-only Python dictionary.
Functions contained here include:
read_fastq_sequences
read_fasta_sequences
create_db

read_*_sequences are useful for extracting record data from a FASTA or
FASTQ file
create_db is used by the above two to format the records into a screed
database

Classes contained here:
screedDB

screedDB is the core dictionary class used for opening prepared screed
databases. This is only for reading pre-created databases since screedDB
supports no dictionary altering methods.
"""
from openscreed import screedDB
from conversion import toFastq
from conversion import toFasta
from createscreed import create_db
from seqparse import read_fastq_sequences
from seqparse import read_fasta_sequences

__version__ = '0.5'
