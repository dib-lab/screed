.. vim: set filetype=rst

=====================
Release Documentation
=====================


Introduction
============

This is the release documentation for releasing a new version of screed. This
document is meant for screed release managers. Michael R. Crusoe and C. Titus
Brown have released screed in the past. Jake Fenton is the first to release
screed using this checklist.

Getting Started
===============

#. Start with a clean checkout::

        cd $(mktemp -d)
        git clone git@github.com:dib-lab/screed.git
        cd screed

#. Review the git logs since the previous release and make sure that
   ChangeLog reflects the major changes::

        git log --minimal --patch \
                `git describe --tags --always --abbrev=0`..HEAD

#. Review the issue list for any existing bugs that won't be fixed in the
   release and ensure they're documented in ``doc/known-issues.txt``

#. Set the new version number and release candidate::

        new_version=1.0.5
        rc=rc1

   Tag the release candidate with the new version prefixed by the letter 'v'::

        git tag v${new_version}-${rc}
        git push --tags git@github.com:dib-lab/screed.git

#. Test the release candidate::

        cd ..
        virtualenv testenv1
        virtualenv testenv2
        virtualenv testenv3
        virtualenv testenv4

        # first we test the tag
        cd testenv1
        source bin/activate
        git clone --depth 1 --branch v${new_version}-${rc} \
                https://github.com/dib-lab/screed.git
        cd screed
        make install-dependencies
        make install
        make test
        python -c 'import screed; print screed.__version__' # double-check version number

        # Test via pip
        cd ../../testenv2
        source bin/activate
        pip install -e \
                git+https://github.com/dib-lab/screed.git@v${new_version}-${rc}#egg=screed
        cd src/screed
        make dist
        make install
        nosetests screed --attr '!known_failing'
        python -c 'import screed; print screed.__version__'
        cp dist/screed*tar.gz ../../../testenv3

        # test if the dist made in testenv2 is complete enough to build another
        # functional dist

        cd ../../../testenv3
        source bin/activate
        pip install nose
        pip install screed*tar.gz
        nosetests screed --attr '!known_failing'
        python -c 'import screed; print screed.__version__'
        tar xzf screed*tar.gz
        cd screed*
        make dist
        make test

#. Publish the new release on the testing PyPI server. You will need to
   change your PyPI credentials as documented here:
   https://wiki.python.org/moin/TestPyPI. You may need to re-register::

        python setup.py register --repository test

   Now, upload the new release::

        python setup.py sdist upload -r test

   Test the PyPI release in a new virtualenv::

        cd ../../testenv4
        source bin/activate
        pip install -U setuptools
        pip install nose
        pip install -i https://testpypi.python.org/pypi --pre --no-clean screed
        nosetests screed --attr '!known_failing'
        python -c 'import screed; print screed.__version__'
        cd build/screed
        ./setup.py nosetests --attr '!known_failing'

#. Do any final testing (acceptance tests, etc.) Note that the acceptance tests
   for screed are to run the khmer automated tests with the new version of
   screed installed and then to run the khmer acceptance tests.

#. Make sure any release notes are merged into doc/release-notes/. Release
   notes should be written in the `.md` format to satisfy the requirements for
   GitHub release notes. The `convert-release-notes` make target can be used to 
   generate `.rst` files from the `.md` notes.


How to make a final release
===========================

When you have a thoroughly tested release candidate, cut a release like so:

#. Create the final tag and publish the new release on PyPI (requires an
   authorized account) ::

       cd ../../../screed
       git tag v${new_version}
       python setup.py register sdist upload

#. Delete the release candidate tag and push the tag updates to GitHub::

       git tag -d v${new_version}-${rc}
       git push git@github.com:dib-lab/screed.git
       git push --tags git@github.com:dib-lab/screed.git

#. Add the release on GitHub, using the tag you just pushed. Name it "Version
   X.Y.Z" and copy/paste in the release notes.

#. Update the Read the Docs to point to the new version. Visit
   https://readthedocs.org/builds/screed/ and ‘Build Version: master’ to pick up
   the new tag. Once that build has finished check the “Activate” box next to
   the new version at https://readthedocs.org/dashboard/screed/versions/ under
   “Choose Active Versions”. Finally change the default version at
   https://readthedocs.org/dashboard/screed/advanced/ to the new version.

#. Delete any RC tags created:: 
   
       git tag -d ${new_version}-${rc}
       git push origin :refs/tags/${new_version}-${rc}

#. Tweet about the new release

Notes on this document
======================
This is the procedure for cutting a new release of screed. It has been adapted
from the release documentation for the khmer project, found at
http://khmer.readthedocs.org/en/v1.1/release.html.
