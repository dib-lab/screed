# Copyright (c) 2008, Michigan State University.

"""
seqparse contains custom sequence parsers for extending screed's
functionality to arbitrary sequence formats. An example 'hava'
parser is included for API reference
"""

from __future__ import absolute_import

import os

from .createscreed import create_db
from .openscreed import ScreedDB
from . import openscreed
from . import fastq
from . import fasta
from . import hava

# [AN] these functions look strangely similar


def read_fastq_sequences(filename):
    """
    Function to parse text from the given FASTQ file into a screed database
    """
    # Will raise an exception if the file doesn't exist
    iterfunc = openscreed.Open(filename, parse_description=True)

    # Create the screed db
    create_db(filename, fastq.FieldTypes, iterfunc)

    return ScreedDB(filename)


def read_fasta_sequences(filename):
    """
    Function to parse text from the given FASTA file into a screed database
    """
    # Will raise an exception if the file doesn't exist
    iterfunc = openscreed.Open(filename, parse_description=True)

    # Create the screed db
    create_db(filename, fasta.FieldTypes, iterfunc)

    return ScreedDB(filename)


def read_hava_sequences(filename):
    """
    Function to parse text from the given HAVA file into a screed database
    """
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Setup the iterator function
    iterfunc = hava.hava_iter(theFile)

    # Create the screed db
    create_db(filename, hava.FieldTypes, iterfunc)
    theFile.close()

    return ScreedDB(filename)
