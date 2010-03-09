# Copyright (c) 2008-2010, Michigan State University

"""
seqparse contains custom parsers for parsing sequence information into
screed databases. An example 'hava' parser is included
"""

import dbConstants
import os
from __init__ import createdb
#import createdb

# Parser for the fake 'hava' sequence
def read_hava_sequences(filename):
    """
    Function to parse text from the given HAVA file into a screed database
    """
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    fields = ('hava', 'quarzk', 'muchalo', 'fakours', 'selimizicka', 'marshoon')
    haCreate = createdb(filename, fields)

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
