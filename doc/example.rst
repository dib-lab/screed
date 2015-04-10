===============
screed examples
===============

.. contents:

Basic Usage
===========

Load screed, index the database, and return a dictionary-like object:

 >>> import screed
 >>> db = screed.read_fasta_sequences('../screed/tests/test.fa')

Get the list of sequence names, sort alphabetically, and look at the
first one:

 >>> names = db.keys()
 >>> names.sort()
 >>> names[0]
 u'ENSMICT00000000730'

Retrieve that record:

 >>> r = db[names[0]]
 >>> print r.keys()
 [u'description', u'id', u'name', u'sequence']

Print out the internal ID number and the name:

 >>> print r.id
 13
 >>> print r.name
 ENSMICT00000000730
