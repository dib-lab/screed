import screed
import os
from screed.DBConstants import fileExtension


def test_no_sqlite_openscreed():
    import screed.openscreed

    saveme = screed.openscreed.sqlite3
    del screed.openscreed.sqlite3

    try:
        try:
            screed.openscreed.ScreedDB('xxx')
        except Exception as e:
            assert 'sqlite3 is needed' in str(e)
    finally:
        screed.openscreed.sqlite3 = saveme


def test_no_sqlite_createscreed():
    import screed.createscreed

    saveme = screed.createscreed.sqlite3
    del screed.createscreed.sqlite3

    try:
        try:
            screed.createscreed.create_db(None, None, None)
        except Exception as e:
            assert 'sqlite3 is needed' in str(e)
    finally:
        screed.createscreed.sqlite3 = saveme


def test_nodb():
    """
    Tests if screed throws an appropriate exception if it is
    asked to open a non-existant screed database
    """
    try:
        db = screed.ScreedDB('foo')
        assert 1 == 0  # Previous line should throw an error
    except ValueError:
        pass


def test_wrongdb():
    """
    Tests if screed throws an appropriate exception if it is
    asked to open a file that isn't a screed database
    """
    try:
        blah = 'blah_screed'
        blah_file = open(blah, 'wb')
        blah_file.close()

        db = screed.ScreedDB(blah)
        os.unlink(blah)
        assert 1 == 0
    except TypeError:
        os.unlink(blah)
        pass
