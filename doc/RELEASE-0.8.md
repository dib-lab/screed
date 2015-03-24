
# Release v0.8


We are pleased to announce the release of Screed v0.8. Screed is a database
engine capable of storing and retrieving short-read sequence data. Screed is
designed to be fast and adaptable to different sequence file formats. This 
release of Screed we consider to be stable and complete.

This version of Screed contains developer documentation for contributing to the
Screed project and a code of conduct for interacting with other contributors
and project maintainers. 

## Features and Major Changes:
 - bz2 compressed file streaming
 - 'accuracy' attribute has been changed to 'quality'
 - versioneer version string generator has been added
 - dooxygen documentation engine has been added
 - code of conduct and developer documentation has been added
 - detailed changelog has been added

## Closed Issues:
    * [Screed gzip/bz2 file sniffing]
      (https://github.com/ged-lab/khmer/issues/432)
    * [change accuracy to quality, add a changelog, general code cleanup]
      (https://github.com/ged-lab/khmer/issues/625)
    * [normalize-by-median not accepting reads on stdin]
      (https://github.com/ged-lab/khmer/issues/633)
    * [screed returning the wrong version and breaking dev installs]
      (https://github.com/ged-lab/khmer/issues/803)
    * [make len(read) == len(read.sequence)]
      (https://github.com/ged-lab/khmer/issues/705)
    * [removed extraneous doc/scheme.txt]
      (https://github.com/ged-lab/khmer/issues/800)

## Known Issues

    * Screed records cannot be sliced. [Issue #768 (khmer repo)]
    (https://github.com/ged-lab/khmer/issues/768) This will be included in the
    next release.
    * Screed self-tests do not use a temporary directory [Issue #748 (khmer
    repo)] (https://github.com/ged-lab/khmer/issues/748) This is an issue if
    the tests directory is read-only. 
    * Screed does not support gzip file streaming. This is an issue with
    python 2.x and will likely not be fixed in future releases.

## Contributors

@ctb @mr-c @bocajnotnef @luizirber @brtaylor92 @grpratt
