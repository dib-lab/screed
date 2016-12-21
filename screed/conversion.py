# Copyright (c) 2008-2010, Michigan State University.

from __future__ import absolute_import
from .openscreed import ScreedDB

_MAXLINELEN = 80
_null_quality = '\"'  # ASCII 34, e.g 75% chance of incorrect read


def GetComments(value):
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
        res.append(longString[begin:begin + _MAXLINELEN])
        begin += _MAXLINELEN

    return '\n'.join(res)


def GenerateQuality(value):
    """
    Returns quality from value if it exists. Otherwise, makes
    a null quality. Quality is line wrapped to _MAXLINELEN
    either way
    """
    if 'quality' in value:
        return linewrap(value['quality'])

    return linewrap(_null_quality * len(str(value['sequence'])))


def ToFastq(dbFile, outputFile):
    """
    Opens the screed database file and attempts to dump it
    to a FASTQ-formatted text file
    """
    outFile = open(outputFile, 'wb')
    db = ScreedDB(dbFile)

    for n, value in enumerate(db.itervalues()):
        line = '@%s %s\n%s\n+\n%s\n' % (value['name'],
                                        GetComments(value),
                                        linewrap(str(value['sequence'])),
                                        GenerateQuality(value))
        outFile.write(line.encode('UTF-8'))
    db.close()
    outFile.close()

    return n + 1


def ToFasta(dbFile, outputFile):
    """
    Opens the screed database file and attempts to dump it
    to a FASTA-formatted text file
    """
    outFile = open(outputFile, 'wb')
    db = ScreedDB(dbFile)

    for n, value in enumerate(db.itervalues()):
        line = '>%s %s\n%s\n' % (value['name'], GetComments(value),
                                 linewrap(str(value['sequence'])))
        outFile.write(line.encode('UTF-8'))

    db.close()
    outFile.close()

    return n + 1
