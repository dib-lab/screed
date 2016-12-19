# Release 1.0

We are pleased to announce the release of Screed v0.9. Screed is a database
engine capable of storing and retrieving short-read sequence data and is
designed to be fast and adaptable to different sequence file formats.

We are pleased to announce the release of screed 1.0. Screed is a
biological sequence parsing and storage/retrieval library for DNA and
protein sequences. It's designed to be lightweight and easy to use
from Python.

Documentation is available at http://screed.readthedocs.org/en/v1.0

## New items of note:

## Known Issues

These are all pre-existing

 - Screed does not support gzip file streaming. This is an issue with Python 2.x and will likely *not* be fixed in future releases. This is being tracked in ged-lab/khmer#700
 
 - Screed is overly tolerant of spaces in fast{a,q} which is against spec. This is being tracked in ged-lab/khmer#108
 
## Contributors

@luizirber @mr-c @bocajnotnef @ctb \*@proteasome \*@anotherthomas \*@sguermond 
(UPDATE ME FOR RELEASE)

\* Indicates new contributors
