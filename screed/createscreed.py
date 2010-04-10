import dbConstants
import os
import sqlite3

def create_db(filepath, fields, rcrditer):
    """
    Creates a screed database in the given filepath. Fields is a tuple
    specifying the names and relative order of attributes in a
    record. rcrditer is an iterator returning records over a
    sequence dataset. Records yielded are in dictionary form
    """
    if not filepath.endswith(dbConstants.fileExtension):
        filepath += dbConstants.fileExtension

    if os.path.exists(filepath): # Remove existing files
        os.unlink(filepath)

    con = sqlite3.connect(filepath)
    cur = con.cursor()

    # Create the admin table
    cur.execute('CREATE TABLE %s (%s INTEGER PRIMARY KEY, '\
                '%s TEXT, %s TEXT)' % (dbConstants._SCREEDADMIN,
                                       dbConstants._PRIMARY_KEY,
                                       dbConstants._FIELDNAME,
                                       dbConstants._ROLENAME))
    query = 'INSERT INTO %s (%s, %s) VALUES (?, ?)' % \
            (dbConstants._SCREEDADMIN, dbConstants._FIELDNAME,
             dbConstants._ROLENAME)

    # Put the primary key in as an attribute
    cur.execute(query, (dbConstants._PRIMARY_KEY,
                        dbConstants._PRIMARY_KEY_ROLE))
    for attribute, role in fields:
        cur.execute(query, (attribute, role))

    # Setup the dictionary table creation field substring
    fieldsub = ','.join(['%s TEXT' % field for field, role in fields])

    # Create the dictionary table
    cur.execute('CREATE TABLE %s (%s INTEGER PRIMARY KEY, %s)' %
                (dbConstants._DICT_TABLE, dbConstants._PRIMARY_KEY,
                 fieldsub))

    # Attribute to index
    queryby = fields[0][0] # Defaults to the first field
    for fieldname, role in fields:
        if role == dbConstants._INDEXED_TEXT_KEY:
            queryby = fieldname
            break

    # Make the index on the 'queryby' attribute
    cur.execute('CREATE UNIQUE INDEX %sidx ON %s(%s)' %
                (queryby, dbConstants._DICT_TABLE, queryby))

    # Setup the 'qmarks' sqlite substring
    qmarks = ','.join(['?' for i in range(len(fields))])

    # Setup the sql substring for inserting fields into database
    fieldsub = ','.join([fieldname for fieldname, role in fields])

    query = 'INSERT INTO %s (%s) VALUES (%s)' %\
            (dbConstants._DICT_TABLE, fieldsub, qmarks)
    # Pull data from the iterator and store in database
    for record in rcrditer:
        data = tuple([record[fieldname] for fieldname, role in fields])
        cur.execute(query, data)

    con.commit()
    con.close()
