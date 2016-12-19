import os
import sys

if __name__ == '__main__':
    import pytest
    errno = pytest.main(["-m not known_failing", '-v',
                         os.path.dirname(__file__)])
    sys.exit(errno)
