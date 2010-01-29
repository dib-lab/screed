# This file contains the classes of entries that will go in each database

import UserDict

# [AN] compress to one tuple/type of db
FASTQFIELDS = ('id', 'name', 'sequence', 'accuracy')
FASTQFIELDTYPES = (('name', 'text'), ('sequence', 'text'), ('accuracy', 'text'))
FASTAFIELDS = ('id', 'name', 'description', 'sequence')
FASTAFIELDTYPES = (('name', 'text'), ('description', 'text'), ('sequence', 'text'))
