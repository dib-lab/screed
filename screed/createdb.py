import os
import sqlite3
import dbConstants

class createdb(object):
    """
    Class used for creating screed databases. Records are passed to the object
    via the feed method. When finished, the object must be closed
    """
    def __init__(self, filepath, attributes):
        """
        Opens a new screed database at the given filepath. Attributes is a tuple
        containing the names and order of atrributes per record
        """
        if not filepath.endswith(dbConstants.fileExtension):
            filepath += dbConstants.fileExtension

        if os.path.exists(filepath): # Remove existing files
            os.unlink(filepath)

        self._attributes = attributes
        self._con = sqlite3.connect(filepath)
        self._c = self._con.cursor()
        self._queryby = self._attributes[0] # Key is first attribute
        self._makeadmintable()
        self._makedicttable()
        self._open = True

    def _tocreatestub(self):
        """
        Parses self._attributes into an SQL stub to be inserted into statements
        """
        sqlList = []
        for attribute in self._attributes:
            sqlList.append('%s TEXT' % attribute)
            sqlList.append(', ')
        sqlList.pop()
        return "".join(sqlList)

    def _makedicttable(self):
        """
        Method to setup the dictionary table for storing records
        """
        # Make the table
        self._c.execute('CREATE TABLE %s (%s INTEGER PRIMARY KEY, %s)' %
                        (dbConstants._DICT_TABLE, dbConstants._PRIMARY_KEY,
                         self._tocreatestub()))
        # Make the index
        self._c.execute('CREATE UNIQUE INDEX %sidx ON %s(%s)' %
                        (self._queryby, dbConstants._DICT_TABLE,
                         self._queryby))

    def _makeadmintable(self):
        """
        Method to setup the admin table containing attribute information
        """
        self._c.execute('CREATE TABLE %s (ID INTEGER PRIMARY KEY, '\
                        'FIELDNAME TEXT)' % dbConstants._SCREEDADMIN)

        query = 'INSERT INTO %s (FIELDNAME) VALUES (?)' % \
                dbConstants._SCREEDADMIN
        for attribute in self._attributes:
            self._c.execute(query, (attribute,))

    def feed(self, dictobj):
        """
        Method for storing records. dictobj is a dictionary object with
        name->value pairs of record attributes
        """
        qmarks = ('?, ' * len(self._attributes))[:-2]
        attributes = (''.join(['%s, ' % attr for attr in self._attributes]))[:-2]
        sub = tuple([dictobj[key] for key in self._attributes])
        query = 'INSERT INTO %s (%s) VALUES (%s)' %\
                (dbConstants._DICT_TABLE, attributes, qmarks)
        self._c.execute(query, sub)

    def close(self):
        """
        Closes the object and the sqlite database handle
        """
        if self._open:
            self._con.commit()
            self._con.close()
            self._open = False
