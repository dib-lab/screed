"""
seqparse contains definitions of parsers that are used to
extract sequence information from files. These parsers
feed the data to their respective dict writers which
create the databases
"""
import screedDB
import dbEntries
import os
import screedExtension

class DbException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def read_fastq_sequences(filename):
    """
    Function to parse text from the given FASTQ file into a screed database
    """

    try:
        theFile = open(filename, "rb")
    except IOError, e: 
        raise DbException(str(e))

    # Delete old screed database if that exists
    if os.path.isfile(filename + screedExtension.fileExtension):
        os.unlink(filename + screedExtension.fileExtension)

    fqDb = screedDB.screedDB(filename, fields=dbEntries.FASTQFIELDTYPES)

    while 1:
        # [AN] does this have to be empty? could make set here instead of in db
        data = [] # Emtpy id entry 
        firstLine = theFile.readline().strip().split('@')
        if len(firstLine) == 1: # Reached eof
            break
        # Make sure the FASTQ file is being read correctly
        assert firstLine[0] == ''
        name = firstLine[1]
        data.append(name) # The name
        data.append(theFile.readline().strip()) # The sequence
        theFile.read(2) # Ignore the '+\n'
        data.append(theFile.readline().strip()) # The accuracy
        fqDb[name] = tuple(data)

    theFile.close()
    fqDb.close()

def read_fasta_sequences(filename):
    """
    Function to parse text from the given FASTA file into a screed database
    """
    try:
        theFile = open(filename, "rb")
    except IOError, e:
        raise DbException(str(e))

    # Delete old screed database if that exists
    if os.path.isfile(filename + screedExtension.fileExtension):
        os.unlink(filename + screedExtension.fileExtension)

    faDb = screedDB.screedDB(filename, fields=dbEntries.FASTAFIELDTYPES)

    # Parse text and add to database
    nextChar = theFile.read(1)
    while nextChar != '':
        data = [] # Empty id entry
        assert nextChar == '>'
        topLine = theFile.readline().strip().split(' ', 1)

        # Extract the name
        name = topLine[0]
        data.append(name) # The name

        # Extract the description
        description = ''
        if len(topLine) == 2:
            description = topLine[1]
        data.append(description) # The description

        # Collect sequence lines into a list
        sequenceList = []
        nextChar = theFile.read(1)
        while nextChar != '' and nextChar != '>':
            sequenceLine = nextChar + theFile.readline().strip()
            sequenceList.append(sequenceLine)
            nextChar = theFile.read(1)
            
        sequence = "".join(sequenceList)
        data.append(sequence) # The sequence
        faDb[name] = tuple(data)
        
    theFile.close()
    faDb.close()

# # Parser for the fake 'hava' sequence
## def read_hava_sequences(filename, multiplier=2):
##     """
##     Function to parse text from the given HAVA file into a screed database
##     """
##     try:
##         theFile = open(filename, "rb")
##     except IOError, e:
##         raise dbw.DbException(str(e))

##     attributes = ("hava", "quarzk", "muchalo", "fakours", "selimizicka", "marshoon")
##     db = openDBW(attributes, filename, multiplier)

##     if db.is_open() == False:
##         raise dbw.DbException("ERROR: DATABASE FILES ARE NOT OPEN")

##     # Parse text and add to database
##     nextChar = theFile.read(1)
##     while nextChar != '':
##         hava = nextChar + theFile.readline().strip()
##         quarzk = theFile.readline().strip()
##         muchalo = theFile.readline().strip()
##         fakours = theFile.readline().strip()
##         selimizicka = theFile.readline().strip()
##         marshoon = theFile.readline().strip()

##         recordString, attributeLengths = combineRecord((hava, quarzk, muchalo,
##                                                         fakours, selimizicka,
##                                                         marshoon))
##         db.writeRecord(recordString, attributeLengths)
##         nextChar = theFile.read(1)

##     theFile.close()
##     db.close()
