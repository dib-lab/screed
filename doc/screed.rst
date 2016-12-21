===========
User Manual
===========

.. note::

   Some doctests are included in :doc:`example`. The examples in this
   document are meant for human consumption only. They will not work in
   doctests!

screed parses FASTA and FASTQ files, generates databases, and lets you query
these databases. Values such as sequence name, sequence description, sequence
quality, and the sequence itself can be retrieved from these databases.

Installation
============

The following software packages are required to run screed:

* Python 2 (2.7) or Python 3 (3.3 or newer)
* pytest (only required to running tests)

Use pip to download, and install Screed and its dependencies::

    pip install screed

To run the optional tests type::

    python -m screed.tests

Command-line Quick Start
========================

Creating a database
-------------------

.. code::

    $ screed db <fasta/fastq file>

Dumping a database to a file
----------------------------

.. code::

    $ screed dump_fasta <screed database file> <fasta output>
    $ screed dump_fastq <screed database file> <fastq output>

If no output file is provided, sequences are written to the terminal (stdout) by
default.

Python Quick Start
==================

Reading FASTA/FASTQ files
-------------------------

   >>> import screed
   >>> with screed.open(filename) as seqfile:
   >>>     for read in seqfile:
   ...         print(read.name, read.sequence)

Here, :code:`filename` can be a FASTA or FASTQ file, and can be uncompressed,
gzip-compressed, or bzip2-compressed. screed natively supports FASTA and FASTQ
databases creation. If your sequences are in a different format see the
developer documentation on :doc:`dev/parsers`.

Creating a database
-------------------

    >>> import screed
    >>> screed.make_db('screed/tests/test-data/test.fa')

This loads a FASTA file :code:`screed/tests/test-data/test.fa` into a screed database
named :code:`screed/tests/test-data/test.fa_screed`. A couple of things to note:

* The screed database is independent of the text file from which it was derived,
  so moving, renaming or deleting :code:`screed/tests/test-data/test.fa` will not affect
  the newly created database.
* The :code:`make_db` function inferred the file type as FASTA automatically.
  The :code:`read_fasta_sequences()` and :code:`read_fastq_sequences()`
  functions are available if you'd prefer to be explicit.

    >>> screed.read_fasta_sequences('screed/tests/test-data/test.fasta')
    >>> screed.read_fastq_sequences('screed/tests/test-data/test.fastq')

Opening a database
------------------

The class :code:`ScreedDB` is used to read screed databases, regardless of what
file format they were derived from (FASTA/FASTQ/hava/etc.). One reader to rule
them all!

From the Python prompt, import the ScreedDB class and load some databases::

    >>> from screed import ScreedDB
    >>> fadb = ScreedDB('screed/tests/test-data/test.fa')
    >>> fqdb = ScreedDB('screed/tests/test-data/test.fastq')

Notice how you didn't need to write the '_screed' at the end of the file names?
screed automatically adds that to the file name if you didn't.

Database dictionary interface
-----------------------------

Since screed emulates a read-only dictionary interface, any methods that don't
modify a dictionary are supported::

    >>> fadb.keys()
    >>> fqdb.keys()

Each record in the database contains 'fields' such as name and sequence
information. If the database was derived from a FASTQ file, quality and optional
annotation strings are included. Conversely, FASTA-derived databases have a
description field.

To retrieve the names of records in the database::

    >>> names = fadb.keys()

The size of the databases (number of sequence records) is easily found::

    >>> len(fadb)
    22
    >>> len(fqdb)
    125

Retrieving records from a database
----------------------------------

A record is the standard container unit in screed. Each has *fields* that vary
slightly depending on what kind of file the database was derived from. For
instance, a FASTQ-derived screed database has an id, a name, a quality score and
a sequence. A FASTA-derived screed database has an id, name, description and a
sequence.

Retrieving entire records::

    >>> records = [r for r in fadb.itervalues()]

Each record is a dictionary of fields. The names of fields are keys into this
dictionary with the actual information as values. For example::

    >>> record = fadb[fadb.keys()[0]]
    >>> index = record['id']
    >>> name = record['name']
    >>> description = record['description']
    >>> sequence = record['sequence']

What this does is retrieve the first record object in the screed database, then
retrieve the index, name, description and sequence from the record object using
standard dictionary key -> value pairs.

Retrieving partial sequences (slicing)
--------------------------------------

screed supports the concept of retrieving a *slice* or a subset of a sequence
string. The motivation is speed: if you have a database entry with a very long
sequence string but only want a small portion of the string, it is faster to
retrieve only the portion than to retrieve the entire string and then perform
standard Python string slicing.

By default, screed's FASTA database creator sets up the :code:`sequence` column
to support slicing. For example, if you have an entry with name :code:`someSeq`
which has a 10K long sequence, and you want a slice of the sequence spanning
positions 4000 to 4080::

    >>> seq = db['someSeq'].sequence
    >>> slice = seq[4000:4080]

This is much faster than say::

    >>> seq = str(db['someSeq'].sequence)
    >>> slice = seq[4000:4080]

Because deep down, less information is being read off the disk. The :code`str()`
method above causes the entire sequence to be retrieved as a string. Then Python
slicing is done on the string :code:`seq` and the subset stored in
:code:`slice`.

Retrieving records *via* index
------------------------------

Sometimes you don't care what the name of a sequence is; you're only interested
in its position in the database. In these cases, retrieval via index is the
method you'll want to use::

    >>> record = fqdb.loadRecordByIndex(5)

An index is like an offset into the database. The order records were kept in the
FASTA or FASTQ file determines the index in their resulting screed database. The
first record in a sequence file will have an index of 0, the second, an index of
1 and so on.

File Formats As Understood By Screed
====================================

While the screed database remains non-specific to file formats, the included
FASTA and FASTQ parsers expect specific formats. These parsers attempt to handle
the most common attributes of sequence files, though they can not support all
features.

FASTQ
-----

The FASTQ parsing function is :code:`read_fastq_sequences()` and is located in
the screed module.

The first line in a record must begin with '@' and is followed by a record
identifier (a name). An optional annotations string may be included after a
space on the same line.

The second line begins the sequence line(s) which may be line wrapped. screed
defines no limit on the length of sequence lines and no length on how many
sequence lines a record may contain.

After the sequence line(s) comes a '+' character on a new line. Some FASTQ
formats require the first line to be repeated after the '+' character, but since
this adds no new information to the record, :code:`read_fastq_sequences()` will
ignore this if it is included.

The quality line(s) is last. Like the sequence line(s) this may be line wrapped.
:code:`read_fastq_sequences()` will raise an exception if the quality and
sequence strings are of unequal length. screed performs no checking for valid
quality scores.

FASTA
-----

The FASTA parsing function is read_fasta_sequences() and is also located in the
screed module.

The first line in a record must begin with '>' and is followed with the
sequence's name and an optional description. If the description is included, it
is separated from the name with a space. Note that though the FASTA format
doesn't require named records, screed does. Without a unique name, screed can't
look up sequences by name.

The second line begins the line(s) of sequence. Like the FASTQ parser,
:code:`read_fasta_sequences()` allows any number of lines of any length.

FASTA <-> FASTQ Conversion
==========================

As an extra nicety, screed can convert FASTA files to FASTQ and back again.

FASTA to FASTQ
--------------

The function used for this process is called 'ToFastq' and is located
in the screed module. It takes the path to a screed database as the
first argument and a path to the desired FASTQ file as the second
argument. There is also a shell interface if the screed module is in
your PYTHONPATH::

    $ python -m screed dump_fastq <path to fasta db> [ <converted fastq file> ]

The FASTA name attribute is directly dumped from the file. The
sequence attribute is also dumped pretty much directly, but is line
wrapped to 80 characters if it is longer.

Any description line in the FASTA database is stored as a FASTQ annotation
string with no other interpretation done.

Finally, as there is no quality or quality score in a FASTA file, a
default one is generated. The generation of the quality follows the
Sanger FASTQ conventions. The score is 1 (ASCII: '"') meaning a
probability of about 75% that the read is incorrect (1 in 4
chance). This PHRED quality score is calculated from the Sanger
format: Q = -10log(p) where p is the probability of an incorrect
read. Obviously this is a very rough way of providing a quality score
and it is only intended to fill in the requirements of a FASTQ
file. Any application needing a true measurement of the quality
should not rely on this automatic conversion.

FASTQ to FASTA
--------------

The function used for this process is called 'toFasta' and is located
in the screed module. It takes the path to a screed database as the
first argument and a path to the desired FASTA file as the second
argument. Like the ToFastq function before, there is a shell interface
to ToFasta if the screed module is in your PYTHONPATH::

    $ python -m screed dump_fasta <path to fastq db> [ <converted fasta file> ]

As above, the name and sequence attributes are directly dumped from
the FASTQ database to the FASTA file with the sequence line wrapping
to 80 characters.

If it exists, the FASTQ annotation tag is stored as the FASTA description tag.
As there is no equivalent in FASTA, the FASTQ quality score is ignored.
