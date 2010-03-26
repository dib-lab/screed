import os
import MySQLdb
import mdbConstants

def create_db(fields, rcrditer):
    """
    Populates the mysql database with records from the record iter
    """
    conn = MySQLdb.connect(db=mdbConstants._DBNAME, user=mdbConstants._USER)

    cur = conn.cursor()

    # Create the admin table
    cur.execute('CREATE TABLE %s (ID int NOT NULL auto_increment, '\
               'FIELDNAME TEXT, PRIMARY KEY(ID))' % mdbConstants._SCREEDADMIN)

    for attribute in fields:
        cur.execute("INSERT INTO %s (FIELDNAME) VALUES ('%s')" % \
            (mdbConstants._SCREEDADMIN, attribute))

    # Setup the dictionary table creation field substring
    otherFields = fields[1:]
    createsub = ['%s TEXT' % field for field in otherFields]
    createsub.insert(0, '%s VARCHAR(100)' % fields[0])
    createsub = ','.join(createsub)

    # Create the dictionary table
    cur.execute('CREATE TABLE %s (%s int NOT NULL auto_increment, %s, PRIMARY KEY(%s))' %
                (mdbConstants._DICT_TABLE, mdbConstants._PRIMARY_KEY,
                 createsub,
                 mdbConstants._PRIMARY_KEY))

    # Attribute to index
    queryby = fields[0]

    # Make the index on the 'queryby' attribute
    cur.execute('CREATE UNIQUE INDEX %sidx ON %s(%s)' %
                (queryby, mdbConstants._DICT_TABLE, queryby))

    # Setup the 'perc' pgres substring
    perc = ', '.join(['%s' for i in range(len(fields))])

    # Setup the sql substring for inserting data into db
    fieldsub = ','.join(fields)

    # Pull data from rcrditer and store in database
    for record in rcrditer:
        data = tuple([record[key] for key in fields])
        cur.execute('INSERT INTO %s (%s) VALUES (%s)' %\
                    (mdbConstants._DICT_TABLE, fieldsub, perc),
                    data)

    conn.commit()
    cur.close()
    conn.close()

def droptables():
    """
    Drops tables in db 
    """
    conn = MySQLdb.connect(db=mdbConstants._DBNAME, user=mdbConstants._USER)

    cur = conn.cursor()

    try:
        cur.execute('DROP TABLE %s;' % mdbConstants._DICT_TABLE)
    except:
        pass
    try:
        cur.execute('DROP TABLE %s;' % mdbConstants._SCREEDADMIN)
    except:
        pass

    conn.commit()
    cur.close()
    conn.close()
