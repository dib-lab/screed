import os
import sys


if __name__ == '__main__':
    from setuptools import setup
    setup_params = {
        "setup_requires": ['pytest_runner'],
        "tests_require": ['pytest'],
    }
    setup(**setup_params)

    import pytest
    errno = pytest.main(["-m not known_failing", '-v',
                         os.path.dirname(__file__)])
    sys.exit(errno)
