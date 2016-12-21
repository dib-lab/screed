Writing Custom Sequence Parsers
===============================

screed is built to be adaptable to new kinds of file sequence formats.
Included with screed are parsers for handling FASTA and FASTQ sequence
file types, though if you need screed to work with a new format, all
you need to do is write a new parser.

Field Roles
-----------

Each field in a screed database is assigned a role. These roles
describe what kind of information is stored in their field. Right now
there are only 4 different roles in a screed database: the text role,
the sliceable role, the indexed key role and the primary key role. All
roles are defined in the file: screed/DBConstants.py

The text role (DBConstants._STANDARD_TEXT) is the role most fields in
a database will have. This role tells screed that the associated field
is storing standard textual data. Nothing special.

The sliceable role (DBConstants._SLICEABLE_TEXT) is a role that can be
assigned to long sequence fields. screed's default FASTA parser
defines the 'sequence' field with the sliceable role. When screed
retrieves a field that has the sliceable role, it builds a special
data structure that supports slicing into the text.

The indexed key role (DBConstants._INDEXED_TEXT_KEY) is associated
with exactly one of the fields in a screed database. In screed's FASTA
and FASTQ parsers, this role is fulfilled by the 'name' field. This
field is required because it is the field screed tells sqlite to index
when creating the database and it is the field used for name look-ups
when querying a screed database.

The primary key role (DBConstants._PRIMARY_KEY_ROLE) is a role
automatically associated with the 'id' field in each database. This
field is always created with each screed database and always holds
this role. You as a user of screed won't need to worry about this one.

General Parsing Function Format
-------------------------------

create_db is the function central to the creation of screed
databases. This function accepts a file path, a tuple of field names
and roles, and an iterator function. The file path describes where the
screed database should go, the tuple contains the names of fields and
their associated roles and the iterator function yields records in a
dictionary format.

This sub-section describes general steps for preparing and using
screed with a custom sequence parser. Though they don't have to be,
future sequence parsers should be located in the seqparse.py file for
convenience.  These steps will be described in the context of working
from the Python shell.

First import the create_db function::

    >>> from screed import create_db

The create_db class handles the formatting of screed databases and
provides a simple interface for storing sequence data.

Next the database fields and roles must be specified. The fields tell
screed the names and order of the data fields inside each record. For instance,
lets say our new sequence has types 'name', 'bar', and 'baz', all text. The
tuple will be::

    >>> fields = (('name', DBConstants._INDEXED_TEXT_KEY),
                  ('bar', DBConstants._STANDARD_TEXT),
                  ('baz', DBConstants._STANDARD_TEXT))

Notice how 'name' is given the indexed key role and bar and baz are
given text roles? If, for instance, you know 'baz' fields can be very long
and you want to be able to retrieve slices of them, you could specify
fields as::

    >>> fields = (('name', DBConstants._INDEXED_TEXT_KEY),
                  ('bar', DBConstants._STANDARD_TEXT),
                  ('baz', DBConstants._SLICEABLE_TEXT))

All screed databases come with an 'id' field, which is a sequential
numbering order starting at 0 for the first record, 1 for the second, and
so on. The names and number of the other fields are arbitrary with one
restriction: one and only one of the fields must fulfill the indexed key role.

Next, you need to setup an iterator function that will return records in
a dictionary format. Have a look at the 'fastq_iter', 'fasta_iter', or
'hava_iter' functions in the screed/fastq.py, screed/fasta.py, and
screed/hava.py files, respectively for examples on how to write one of these.
If you don't know what an iterator function is, the documentation on the
Python website gives a good description:
http://docs.python.org/library/stdtypes.html#iterator-types.

Once the iterator function is written, it needs to be instantiated. In the
context of the built-in parsing functions, this means opening a file and
passing the file handle to the iterator function::

    >>> seqfile = open('path_to_seq_file', 'rb')
    >>> iter_instance = myiter(seqfile)

Assuming that your iterator function is called 'myiter', this sets up an
instance of it ready to use with create_db.

Now the screed database is created with one command::

    >>> create_db('path_to_screed_db', fields, iter_instance)

If you want the screed database saved at 'path_to_screed_db'. If instead you
want the screed database created in the same directory and with a
similar file name as the sequence file, its OK to do this::

    >>> create_db('path_to_seq_file', fields, iter_instance)

create_db will just append '_screed' to the end of the file name and make
a screed database at that file path so the original file won't be
overwritten.

When you're done the sequence file should be closed::

    >>> seqfile.close()

Using the Built-in Sequence Iterator Functions
----------------------------------------------

This section shows how to use the 'fastq_iter' and 'fasta_iter' functions
for returning records from a sequence file.

These functions both take a file handle as the only argument and then return
a dictionary for each record in the file containing names of fields and
associated data. These functions are primarily used in conjunction with
the db_create() function, but they can be useful by themselves.

First, import the necessary module and open a text file containing sequences.
For this example, the 'fastq_iter' function will be used::

    >>> import screed.fastq
    >>> seqfile = open('path_to_seqfile', 'rb')

Now, the 'fastq_iter' can be instantiated and iterated over::

    >>> fq_instance = screed.fastq(seqfile)
    >>> for record in fq_instance:
    ...     print record.name

That will print the name of every sequence in the file. If instead you want
to accumulate the sequences::

    >>> sequences = []
    >>> for record in fq_instance:
    ...     sequences.append(record.sequence)

These iterators are the core of screed's sequence modularity. If there is
a new sequence format you want screed to work with, all it needs is its
own iterator.

Error checking in parsing methods
---------------------------------

The existing FASTA/FASTQ parsing functions contain some error
checking, such as making sure the file can be opened and checking
correct data is being read. Though screed doesn't enforce this, it is
strongly recommended to include error checking code in your parser. To
remain non-specific to one file sequence type or another, the
underlying screed library can't contain error checking code of this
kind. If errors are not detected by the parsing function, they will be
silently included into the database being built and could cause
problems much later when trying to read from the database.
