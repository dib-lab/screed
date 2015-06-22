
# Release v0.9

We are pleased to announce the release of Screed v0.9. Screed is a database
engine capable of storing and retrieving short-read sequence data and is
designed to be fast and adaptable to different sequence file formats.

This version of Screed features Python 3 syntax with compatibility with Python 2. Additional changes have broken backwards compatibility in several small ways in preparation for our 1.0 release and adoption of strict semantic versioning from there on out.

It is also the first release since our move to the University of Davis, California and also under our new name, the Lab for Data Intensive Biology.

Documentation is available at http://screed.readthedocs.org/en/v0.9/

## New items of note:

- Now a primarily Python 3 codebase with Python 2 compatibility. https://github.com/dib-lab/screed/pull/41 @luizirber & @mr-c

- Tests now correctly run using temporary directories and the test data is now shipped allowing the tests to be run after installation. https://github.com/dib-lab/screed/pull/30 @bocajnotnef https://github.com/dib-lab/screed/pull/40 @mr-c
- The private method `screed/screedRecord._screed_record_dict()` has been renamed to `screed.screedRecord.Record()`. This is **not** a backwards compatible change. https://github.com/dib-lab/screed/pull/35 @sguermond
- `screed.open()` now accepts `-` as a synonym for STDIN and is now an (optional) context manager. It no longer defaults to parsing out a separate description from the name. The description field will br removed altogether from the next release. This is **not** a backwards compatible change. https://github.com/dib-lab/screed/pull/36 @anotherthomas  https://github.com/dib-lab/screed/pull/39 https://github.com/dib-lab/screed/pull/41 @luizirber https://github.com/dib-lab/screed/pull/43 @ctb 
- The FASTQ parser was improved and it no longer hangs in the presence of empty lines. https://github.com/dib-lab/screed/pull/38 @proteasome
- Screed records now slice correctly https://github.com/dib-lab/screed/pull/41 @wrightmhw @luizirber 


## Other bugs fixed/issues closed:

- Release notes are now a part of the documentation. https://github.com/dib-lab/screed/pull/33 @bocajnotnef 
- A test was made more robust to prevent hangs. https://github.com/dib-lab/screed/pull/37 @anotherthomas 

## Known Issues

These are all pre-existing

 - Screed does not support gzip file streaming. This is an issue with Python 2.x and will likely *not* be fixed in future releases. This is being tracked in ged-lab/khmer#700
 - Screed is overly tolerant of spaces in fast{a,q} which is against spec. This is being tracked in ged-lab/khmer#108
 
## Contributors

@luizirber @mr-c @bocajnotnef @ctb \*@proteasome \*@anotherthomas \*@sguermond 

\* Indicates new contributors
