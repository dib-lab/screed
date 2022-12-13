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

#. Create and activate an empty Python environment::

        mamba create -n screed-rc -y python=3.10 pip make setuptools_scm
        conda activate screed-rc
        python -m pip install -U pip
        python -m pip install -U virtualenv wheel tox-setuptools-version build

#. Start with a clean checkout::

        cd $(mktemp -d)
        git clone git@github.com:dib-lab/screed.git
        cd screed

#. Set the new version number and release candidate::

        new_version=1.1.0
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
        python -c 'import screed; print(screed.__version__)' # double-check version number


        # Test via pip
        cd ../../testenv2
        source bin/activate
        pip install -e \
                git+https://github.com/dib-lab/screed.git@v${new_version}-${rc}#egg=screed
        cd src/screed
        make dist
        make install
        pip install pytest
        pytest screed 
        python -c 'import screed; print(screed.__version__)' # double-check version number
        cp dist/screed-1.1rc1.tar.gz ../../../testenv3 

        # test if the dist made in testenv2 is complete enough to build another
        # functional dist

        cd ../../../testenv3
        source bin/activate
        pip install pytest
        pip install screed*tar.gz
        python -c 'import screed; print(screed.__version__)'
        tar xzf screed*tar.gz
        cd screed*
        make dist
        make test

#. Do any final testing (acceptance tests, etc.) A good test is to install
   the new version of screed and then run the sourmash tests.

How to make a final release
===========================

When you have a thoroughly tested release candidate, cut a release like so:

#. Delete the release candidate tag and push the tag updates to GitHub::

       cd ../../screed
       git tag -d v${new_version}-${rc}
       git push --delete origin v${new_version}${rc}

#. Create the final tag and publish the new release on PyPI (requires an
   authorized account) ::

       git tag v${new_version}
       git push --tags origin
       make dist
       twine upload dist/screed-${new_version}.tar.gz

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

#. Send email including the release notes to khmer@lists.idyll.org and
   khmer-announce@lists.idyll.org

Notes on this document
======================
This is the procedure for cutting a new release of screed. It has been adapted
from the release documentation for the khmer project, found at
http://khmer.readthedocs.org/en/v1.1/release.html.

