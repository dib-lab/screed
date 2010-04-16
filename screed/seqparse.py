# Copyright (c) 2008-2010, Michigan State University

"""
seqparse contains custom sequence parsers for extending screed's
functionality to arbitrary sequence formats. An example 'hava'
parser is included for API reference
"""

import DBConstants
import os
from createscreed import create_db
from openscreed import ScreedDB
from fastq import fastq_iter
from fasta import fasta_iter

def read_fastq_sequences(filename):
    """
    Function to parse text from the given FASTQ file into a screed database
    """
    FASTQFIELDTYPES = (('name', DBConstants._INDEXED_TEXT_KEY),
                       ('annotations', DBConstants._STANDARD_TEXT),
                       ('sequence', DBConstants._STANDARD_TEXT),
                       ('accuracy', DBConstants._STANDARD_TEXT))

    # Will raise an exception if the file doesn't exist
    theFile = open(filename, 'rb')

    # Setup the iterator function
    iterfunc = fastq_iter(theFile)

    # Create the screed db
    create_db(filename, FASTQFIELDTYPES, iterfunc)

    theFile.close()

    return ScreedDB(filename)

def read_fasta_sequences(filename):
    """
    Function to parse text from the given FASTA file into a screed database
    """

    FASTAFIELDTYPES = (('name', DBConstants._INDEXED_TEXT_KEY),
                       ('description', DBConstants._STANDARD_TEXT),
                       ('sequence', DBConstants._SLICABLE_TEXT))
    
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Setup the iterator function
    iterfunc = fasta_iter(theFile)

    # Create the screed db
    create_db(filename, FASTAFIELDTYPES, iterfunc)
    
    theFile.close()

    return ScreedDB(filename)

# Parser for the fake 'hava' sequence
def read_hava_sequences(filename):
    """
    Function to parse text from the given HAVA file into a screed database
    """
    def havaiter(handle):
        """
        Iterator over a 'hava' sequence file, returning records. handle
        is a handle to a file opened for reading
        """
        data = {}
        line = handle.readline().strip()
        while line:
            data['hava'] = line
            data['quarzk'] = handle.readline().strip()
            data['muchalo'] = handle.readline().strip()
            data['fakours'] = handle.readline().strip()
            data['selimizicka'] = handle.readline().strip()
            data['marshoon'] = handle.readline().strip()

            line = handle.readline().strip()
            yield data

    fields = (('hava', DBConstants._INDEXED_TEXT_KEY),
              ('quarzk', DBConstants._STANDARD_TEXT),
              ('muchalo', DBConstants._STANDARD_TEXT),
              ('fakours', DBConstants._STANDARD_TEXT),
              ('selimizicka', DBConstants._STANDARD_TEXT),
              ('marshoon', DBConstants._STANDARD_TEXT))
        
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Setup the iterator function
    iterfunc = havaiter(theFile)

    # Create the screed db
    create_db(filename, fields, iterfunc)
    theFile.close()

    return ScreedDB(filename)
