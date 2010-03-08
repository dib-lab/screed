# Copyright (c) 2008-2010, Michigan State University

"""
seqparse contains definitions of parsers that are used to
extract sequence information from files. These parsers
feed the data to their respective dict writers which
create the databases
"""
#import screedDB
import os
import createdb

FASTQFIELDTYPES = ('name', 'sequence','accuracy')
FASTAFIELDTYPES = ('name', 'description', 'sequence')
fileExtension = '_screed'

def read_fastq_sequences(filename):
    """
    Function to parse text from the given FASTQ file into a screed database
    """

    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Delete old screed database if that exists
    if os.path.isfile(filename + fileExtension):
        os.unlink(filename + fileExtension)

 #   fqDb = screedDB.screedDB(filename, fields=FASTQFIELDTYPES)
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
#        data.append(name) # The name
        data['sequence'] = theFile.readline().strip()
#        data.append(theFile.readline().strip()) # The sequence
        theFile.read(2) # Ignore the '+\n'
#        data.append(theFile.readline().strip()) # The accuracy
        data['accuracy'] = theFile.readline().strip()
        fqCreate.feed(data)
#        fqDb[name] = tuple(data)

    theFile.close()
    fqCreate.close()
#    fqDb.close()

def read_fasta_sequences(filename):
    """
    Function to parse text from the given FASTA file into a screed database
    """
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Delete old screed database if that exists
    if os.path.isfile(filename + fileExtension):
        os.unlink(filename + fileExtension)

    faCreate = createdb.createdb(filename, FASTAFIELDTYPES)

#    faDb = screedDB.screedDB(filename, fields=FASTAFIELDTYPES)

    # Parse text and add to database
    nextChar = theFile.read(1)
    while nextChar != '':
        data = {}
#        data = [] # Empty id entry
        assert nextChar == '>'
        topLine = theFile.readline().strip().split(' ', 1)

        # Extract the name
        name = topLine[0]
        data['name'] = name
#        data.append(name) # The name

        # Extract the description
        description = ''
        if len(topLine) == 2:
            description = topLine[1]
        data['description'] = description
#        data.append(description) # The description

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
#        data.append(sequence) # The sequence
#        faDb[name] = tuple(data)
        
    theFile.close()
    faCreate.close()
#    faDb.close()

# Parser for the fake 'hava' sequence
def read_hava_sequences(filename):
    """
    Function to parse text from the given HAVA file into a screed database
    """
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    fields = ('hava', 'quarzk', 'muchalo', 'fakours', 'selimizicka', 'marshoon')
    haCreate = createdb.createdb(filename, fields)
#    db = screedDB.screedDB(filename, fields)

    # Parse text and add to database
    nextChar = theFile.read(1)
    while nextChar != '':
        data = {}
##         hava = nextChar + theFile.readline().strip()
##         quarzk = theFile.readline().strip()
##         muchalo = theFile.readline().strip()
##         fakours = theFile.readline().strip()
##         selimizicka = theFile.readline().strip()
##         marshoon = theFile.readline().strip()
        data['hava'] = nextChar + theFile.readline().strip()
        data['quarzk'] = theFile.readline().strip()
        data['muchalo'] = theFile.readline().strip()
        data['fakours'] = theFile.readline().strip()
        data['selimizicka'] = theFile.readline().strip()
        data['marshoon'] = theFile.readline().strip()

        haCreate.feed(data)
#        db[hava] = (hava, quarzk, muchalo, fakours, selimizicka, marshoon)
        nextChar = theFile.read(1)

    theFile.close()
    haCreate.close()
#    db.close()
