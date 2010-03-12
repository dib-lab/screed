# Copyright (c) 2008-2010, Michigan State University

"""
seqparse contains custom parsers for parsing sequence information into
screed databases. An example 'hava' parser is included
"""

import dbConstants
import os
from __init__ import create_db

# Parser for the fake 'hava' sequence
def read_hava_sequences(filename):
    """
    Function to parse text from the given HAVA file into a screed database
    """
    def havaiter(handle):
        """
        Iterator over a 'hava' sequence file, returning records
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

    fields = ('hava', 'quarzk', 'muchalo', 'fakours', 'selimizicka', 'marshoon')
        
    # Will raise an exception if the file doesn't exist
    theFile = open(filename, "rb")

    # Setup the iterator function
    iterfunc = havaiter(theFile)

    # Create the screed db
    create_db(filename, fields, iterfunc)
    theFile.close()
