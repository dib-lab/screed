# Release 1.0

We are pleased to announce the release of screed 1.0. Screed is a
biological sequence parsing and storage/retrieval library for DNA and
protein sequences. It's designed to be lightweight and easy to use
from Python.

<!-- Summary here -->

Documentation is available at http://screed.readthedocs.org/en/v1.0

## New items of note:

- Features
  * #53 Replace \*_Writer with write_fastx @standage
  * #55 Shell command for screed functions and simplified API for DB creation @luizirber
- Build
  * #49 Codecov, pep8 checks, Python 3.5, PR checklist updates
  * #50 Use pytest as test runner
  * #52 Reduce build matrix
  * #58 Make sure docs are tested in CI build @standage
  * #59 Simpler changelog format @standage
- Fixes
  * #47 Fix RC problems for Python 2.7 @ctb
  * #48 Fix operator comparison
  * #51 Fix imports on screed.fadbm
  * #54 Update tests & constrain behavior in various ways
  * #56 Allow sqlite3 import to fail @ctb
  * #57 Code cleanup @standage
  * #61 Fix test execution when calling as a module @luizirber
  * #62 Cleanup user docs @standage
  * #63 Add missing import for make_db @luizirber
  * #64 Revert Record changes that break with khmer 2.0 @ctb
  * #65 Simplify use of 'open' internally @ctb




## Known Issues

These are all pre-existing

 - Screed does not support gzip file streaming. This is an issue with Python 2.x and will likely *not* be fixed in future releases. This is being tracked in dib-lab/khmer#700
 
 - Screed is overly tolerant of spaces in fast{a,q} which is against spec. This is being tracked in dib-lab/khmer#108
 
## Contributors

@luizirber \*@betatim \*@standage @mr-c @bocajnotnef @ctb

\* Indicates new contributors
