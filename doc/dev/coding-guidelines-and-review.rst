.. vim: set filetype=rst

Coding guidelines and code review checklist
===========================================

This document is for anyone who want to contribute code to the screed
project, and describes our coding standards and code review checklist.

----

Coding standards
----------------

All plain-text files should have line widths of 80 characters or less unless
that is not supported for the particular file format.

Vim user can set the indentation with::

	set expandtab
	set shiftwidth=4
	set softtabstop=4

We are a pure Python project and `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`__ is our
standard. The ```pep8``` and ```autopep8``` Makefile targets are helpful. 

Code  and documentation must have its spelling checked. Vim users can
run::

        :setlocal spell spelllang=en_us

Use `]s` and `[s` to navigate between misspellings and `z=` to suggest a
correctly spelled word. `zg` will add a word as a good word.

GNU `aspell` can also be used to check the spelling in a single file::

        aspell check --mode $filename

Code Review
-----------

Please read `11 Best Practices for Peer Code Review
<http://smartbear.com/SmartBear/media/pdfs/WP-CC-11-Best-Practices-of-Peer-Code-Review.pdf>`__.

See also `Code reviews: the lab meeting for code
<http://fperez.org/py4science/code_reviews.html>`__ and
`the PyCogent coding guidelines
<http://pycogent.org/coding_guidelines.html>`__.

Checklist
---------

Copy and paste the following into a pull request comment when it is
ready for review::
   
   - [ ] Is it mergeable?
   - [ ] `make test` Did it pass the tests?
   - [ ] `make clean diff-cover` If it introduces new functionality, is it tested?
   - [ ] `make format diff_pylint_report doc` Is it well formatted?
   - [ ] Is it documented in the `ChangeLog`?
     http://en.wikipedia.org/wiki/Changelog#Format
   - [ ] Was a spellchecker run on the source code and documentation after
     changes were made?

**Note** that after you submit the comment you can check and uncheck
the individual boxes on the formatted comment; no need to put x or y
in the middle.
