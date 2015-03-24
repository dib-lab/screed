
# Release v0.8

We are pleased to announce the release of Screed v0.8. Screed is a database
engine capable of storing and retrieving short-read sequence data. Screed is
designed to be fast and adaptable to different sequence file formats. This 
release of Screed we consider to be stable and complete.

This version of Screed contains developer documentation for contributing to the
Screed project and a code of conduct for interacting with other contributors
and project maintainers. Documentation is available at
http://screed.readthedocs.org/en/v0.8/ 

## New items of note:

This release successfully installs and passes its unit tests on Ubuntu 14.04 
and the latest release of Mac OS X 10 "Yosemite". It also passes the khmer 
acceptance tests as per the [eelpond testing protocol.]
(https://github.com/ged-lab/literate-resting/blob/master/kp/README.txt)

 - Screed now has automatic compression detection via magic bit sniffing gzip, 
 bzip and zip files(from @mr-c)
 - Screed now supports streaming of uncompressed FASTA and FASTQ files. Bzip2 
 files can also be streamed but not gzip files. ([from @mr-c]
 (https://github.com/ged-lab/screed/pull/11))
 - Screed now has a Changelog, developer documentation and uses the 'quality' 
 attribute over the 'accuracy' attribute in dealing with FASTQ reads. ([from 
 @bocajnotnef] (https://github.com/ged-lab/khmer/issues/625))
 - Versioneer version string generator has been added ([from @bocajnotnef]
 (https://github.com/ged-lab/screed/pull/14))
 - Dooxygen documentation engine has been added ([from @mr-c]
 (https://github.com/ged-lab/screed/pull/13))
 - code of conduct and developer documentation has been added ([from @ctb, 
 @mr-c and @bocajnotnef] (https://github.com/ged-lab/screed/pull/14))
 - detailed Changelog has been added ([from @bocajnotnef]
 (https://github.com/ged-lab/screed/pull/14))

## Notable bugs fixed/issues closed:
 - [A khmer script was not accepting reads on the stdin]
      (https://github.com/ged-lab/khmer/issues/633) by @mr-c
 - [screed returning the wrong version and breaking dev installs]
      (https://github.com/ged-lab/khmer/issues/803) by @mr-c

## Known Issues

These are all pre-existing

 - Screed records cannot be sliced requiring un-Pythonic techniques to achieve 
 the same behavior [Issue #768] (https://github.com/ged-lab/khmer/issues/768) 
 This will be included in the next release.
 - Screed self-tests do not use a temporary directory which causes tests run 
 from package-based installs to fail [Issue #748] 
 (https://github.com/ged-lab/khmer/issues/748) 
 - Screed does not support gzip file streaming. This is an issue with 
 Python 2.x and will likely *not* be fixed in future releases. [Issue #700] 
 (https://github.com/ged-lab/khmer/issues/700)

## Contributors

@ctb @mr-c @bocajnotnef @luizirber @brtaylor92 @grpratt
