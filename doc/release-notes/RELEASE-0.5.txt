============
Release v0.5
============

We are proud to announce the release of screed v0.5. screed is a database engine
capable of storing and retriving short-read sequence data. screed is designed
to be fast and adaptable to different sequence file formats. This marks the
first release of screed which we consider stable and complete.

Features:
 - Read sequence data from FASTA/FASTQ files into screed databases
 - Save screed databases back to FASTA/FASTQ files
 - Lookup sequence data by index (offset) or name
 - Native support for sequence substring slicing
 - Convert between FASTA <-> FASTQ file formats

screed is written entirely in Python and uses the Sqlite database for backend
storage. screed can be downloaded from the public git repository:
http://github.com/acr/screed.git

screed is licensed under the BSD license which can be viewed in the
doc/LICENSE.txt file.
