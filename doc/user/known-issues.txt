.. vim: set filetype=rst

============
Known Issues
============

This document details the known issues in the current release of screed. All
issues for screed are tracked at https://github.com/ged-lab/khmer/labels/screed

List of known issues
====================

Screed does not support gzip file streaming. This is an issue
with Python 2.x and will likely *not* be fixed in future
releases. https://github.com/ged-lab/khmer/issues/700

Screed is overly tolerant of spaces in fast{q,a} which is against
spec. https://github.com/ged-lab/khmer/issues/108

Screed records cannot be sliced requiring un-Pythonic techniques
to achieve the same behavior This will be included in a future
release. https://github.com/ged-lab/khmer/issues/768

Screed self-tests do not use a temporary directory which causes tests run
from package-based installs to fail https://github.com/ged-lab/khmer/issues/748

