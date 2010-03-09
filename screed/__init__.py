"""
screed is a database tool useful for retrieving arbitrary kinds of sequence
data through a on-disk database that emulates a read-only Python dictionary.
Functions contained here include:
read_fastq_sequences
read_fasta_sequences
These two functions are useful for taking a FASTQ or FASTA formatted file
and parsing it into a screed database
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
