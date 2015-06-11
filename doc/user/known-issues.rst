.. vim: set filetype=rst

============
Known Issues
============

This document details the known issues in the current release of screed. All
issues for screed are tracked at https://github.com/dib-lab/khmer/labels/screed

List of known issues
====================

Screed does not support gzip file streaming. This is an issue
with Python 2.x and will likely *not* be fixed in future
releases. https://github.com/dib-lab/khmer/issues/700

Screed is overly tolerant of spaces in fast{q,a} which is against
spec. https://github.com/dib-lab/khmer/issues/108
