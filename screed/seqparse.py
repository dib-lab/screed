# Copyright (c) 2008-2010, Michigan State University

"""
seqparse contains definitions of parsers that are used to
extract sequence information from files. These parsers
feed the data to their respective dict writers which
create the databases
"""

import dbConstants
import os
import createdb

FASTQFIELDTYPES = ('name', 'sequence','accuracy')
FASTAFIELDTYPES = ('name', 'description', 'sequence')

def read_fastq_sequences(filename):
    """
    Function to parse text from the given FASTQ file into a screed database
    """

    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Delete old screed database if that exists
    if os.path.isfile(filename + dbConstants.fileExtension):
        os.unlink(filename + dbConstants.fileExtension)

    fqCreate = createdb.createdb(filename, FASTQFIELDTYPES)

    while 1:
        data = {}
        firstLine = theFile.readline().strip().split('@')
        if len(firstLine) == 1: # Reached eof
            break
        # Make sure the FASTQ file is being read correctly
        assert firstLine[0] == ''
        name = firstLine[1]
        data['name'] = name
        data['sequence'] = theFile.readline().strip()
        theFile.read(2) # Ignore the '+\n'
        data['accuracy'] = theFile.readline().strip()
        fqCreate.feed(data)

    theFile.close()
    fqCreate.close()

def read_fasta_sequences(filename):
    """
    Function to parse text from the given FASTA file into a screed database
    """
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Delete old screed database if that exists
    if os.path.isfile(filename + dbConstants.fileExtension):
        os.unlink(filename + dbConstants.fileExtension)

    faCreate = createdb.createdb(filename, FASTAFIELDTYPES)

    # Parse text and add to database
    nextChar = theFile.read(1)
    while nextChar != '':
        data = {}
        assert nextChar == '>'
        topLine = theFile.readline().strip().split(' ', 1)

        # Extract the name
        name = topLine[0]
        data['name'] = name

        # Extract the description
        description = ''
        if len(topLine) == 2:
            description = topLine[1]
        data['description'] = description

        # Collect sequence lines into a list
        sequenceList = []
        nextChar = theFile.read(1)
        while nextChar != '' and nextChar != '>':
            sequenceLine = nextChar + theFile.readline().strip()
            sequenceList.append(sequenceLine)
            nextChar = theFile.read(1)
            
        sequence = "".join(sequenceList)
        data['sequence'] = sequence
        faCreate.feed(data)
        
    theFile.close()
    faCreate.close()

# Parser for the fake 'hava' sequence
def read_hava_sequences(filename):
    """
    Function to parse text from the given HAVA file into a screed database
    """
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    fields = ('hava', 'quarzk', 'muchalo', 'fakours', 'selimizicka', 'marshoon')
    haCreate = createdb.createdb(filename, fields)

    # Parse text and add to database
    nextChar = theFile.read(1)
    while nextChar != '':
        data = {}
        data['hava'] = nextChar + theFile.readline().strip()
        data['quarzk'] = theFile.readline().strip()
        data['muchalo'] = theFile.readline().strip()
        data['fakours'] = theFile.readline().strip()
        data['selimizicka'] = theFile.readline().strip()
        data['marshoon'] = theFile.readline().strip()

        haCreate.feed(data)
        nextChar = theFile.read(1)

    theFile.close()
    haCreate.close()
