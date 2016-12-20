import os
import sys


if __name__ == '__main__':
    from setuptools import setup
    setup_params = {
        "setup_requires": ['pytest_runner'],
        "tests_require": ['pytest'],
    }
    rootdir = os.path.dirname(os.path.dirname(__file__))
    #  TODO: read opts from pytest.ini
    opts = '-m "not known_failing" -v'
    sys.argv[1:] = ['pytest', '--addopts=' + opts]
    os.chdir(rootdir)
    setup(**setup_params)
    sys.exit()
