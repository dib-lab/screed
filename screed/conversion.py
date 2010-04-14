# Copyright (c) 2008-2010, Michigan State University

from openscreed import screedDB

_MAXLINELEN = 80
_null_accuracy = '\"' # ASCII 34, e.g 75% chance of incorrect read

def getComments(value):
    """
    Returns description or annotations attributes from given
    dictionary object
    """
    if 'description' in value:
        return value['description']
    elif 'annotations' in value:
        return value['annotations']
    else:
        return ''

def linewrap(longString):
    """
    Given a long string of characters, inserts newline characters
    every _MAXLINELEN characters
    """
    res = []
    begin = 0
    while begin < len(longString):
        res.append(longString[begin:begin+_MAXLINELEN])
        begin += _MAXLINELEN

    return '\n'.join(res)

def generateAccuracy(value):
    """
    Returns accuracy from value if it exists. Otherwise, makes
    a null accuracy. Accuracy is line wrapped to _MAXLINELEN
    either way
    """
    if 'accuracy' in value:
        return linewrap(value['accuracy'])

    return linewrap(_null_accuracy * len(str(value['sequence'])))

def toFastq(dbFile, outputFile):
    """
    Opens the screed database file and attempts to dump it
    to a FASTQ-formatted text file
    """
    outFile = open(outputFile, 'wb')
    db = screedDB(dbFile)

    for value in db.itervalues():
        outFile.write('@%s %s\n%s\n+\n%s\n' % (value['name'],
                                               getComments(value),
                                               linewrap(str(value['sequence'])),
                                               generateAccuracy(value)))
    db.close()
    outFile.close()

def toFasta(dbFile, outputFile):
    """
    Opens the screed database file and attempts to dump it
    to a FASTA-formatted text file
    """
    outFile = open(outputFile, 'wb')
    db = screedDB(dbFile)

    for value in db.itervalues():
        outFile.write('>%s %s\n%s\n' % (value['name'], getComments(value),
                                        linewrap(str(value['sequence']))))
    
    db.close()
    outFile.close()
