# Release 1.0

We are pleased to announce the release of screed 1.0. Screed is a
biological sequence parsing and storage/retrieval library for DNA and
protein sequences. It's designed to be lightweight and easy to use
from Python.

This version is the first with API compatibility guarantees,
following the [semantic versioning guidelines][0].
Most changes are internal or API clarifications,
but there is a new shell command for screed functions and an unified function
for writing FAST{A,Q} records.

Documentation is available at http://screed.readthedocs.org/en/v1.0

## New items of note:

- New shell commands for common screed operations:
  - `db` for database creation (`python -m screed db <filename>`)
  - dumping FAST{A,Q} records from a db
  (`python -m screed dump_fasta <db> <output>`
  and `python -m screed dump_fastq <db> <output>`). #55 @luizirber
- Remove `\*_Writer` classes and unify record writing in the `write_fastx`
  function. #53 @standage
- We now use pytest as a test runner,
  codecov for code coverage,
  and a simplified changelog format. #50 #49 #59 @luizirber @standage

## Other bugs fixed/issues closed:

- Fix reverse complement problems for Python 2.7. #47 @ctb
- Fix operator comparison. #48 @luizirber
- Update tests & constrain behavior for screed Records. #54 @ctb
- Allow sqlite3 import to fail. #56 @ctb
- Cleanup user docs and code. #62 #57 @standage
- Simplify use of 'open' internally. #65 @ctb

## Known Issues

These are all pre-existing

 - Screed does not support gzip file streaming. This is an issue with Python 2.x and will likely *not* be fixed in future releases. This is being tracked in dib-lab/khmer#700

 - Screed is overly tolerant of spaces in fast{a,q} which is against spec. This is being tracked in dib-lab/khmer#108

## Contributors

@luizirber \*@betatim \*@standage @ctb

\* Indicates new contributors

[0]: http://semver.org/
