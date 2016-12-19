import sys

if __name__ == '__main__':
    import pytest
    errno = pytest.main(['-m', '"not known_failing"', '-v'])
    #errno = pytest.main()
    print('DEBUG', file=sys.stderr)
    sys.exit(errno)
