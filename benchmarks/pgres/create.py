import os
import psycopg2
import pdbConstants

def create_db(fields, rcrditer):
    """
    Populates the pgres database with records from the record iter
    """
    
    conn = psycopg2.connect('dbname=%s user=%s' % (pdbConstants._DBNAME,
                                                   pdbConstants._USER))
    cur = conn.cursor()

    # Create the admin table
    cur.execute('CREATE TABLE %s (ID serial PRIMARY KEY, '\
               'FIELDNAME TEXT)' % pdbConstants._SCREEDADMIN)

    for attribute in fields:
        cur.execute("INSERT INTO %s (FIELDNAME) VALUES ('%s')" % \
            (pdbConstants._SCREEDADMIN, attribute))

    # Setup the dictionary table creation field substring
    createsub = ','.join(['%s TEXT' % field for field in fields])

    # Create the dictionary table
    cur.execute('CREATE TABLE %s (%s serial PRIMARY KEY, %s)' %
                (pdbConstants._DICT_TABLE, pdbConstants._PRIMARY_KEY,
                 createsub))

    # Attribute to index
    queryby = fields[0]

    # Make the index on the 'queryby' attribute
    cur.execute('CREATE UNIQUE INDEX %sidx ON %s(%s)' %
                (queryby, pdbConstants._DICT_TABLE, queryby))

    # Setup the 'perc' pgres substring
    perc = ', '.join(['%s' for i in range(len(fields))])

    # Setup the sql substring for inserting data into db
    fieldsub = ','.join(fields)

    # Pull data from rcrditer and store in database
    for record in rcrditer:
        data = tuple([record[key] for key in fields])
        cur.execute('INSERT INTO %s (%s) VALUES (%s)' %\
                    (pdbConstants._DICT_TABLE, fieldsub, perc),
                    data)

    conn.commit()
    cur.close()
    conn.close()

def droptables():
    """
    Drops tables in db 
    """
    conn = psycopg2.connect('dbname=%s user=%s' % (pdbConstants._DBNAME,
                                                   pdbConstants._USER))
    cur = conn.cursor()

    try:
        cur.execute('DROP TABLE %s;' % pdbConstants._DICT_TABLE)
    except:
        pass
    try:
        cur.execute('DROP TABLE %s;' % pdbConstants._SCREEDADMIN)
    except:
        pass

    conn.commit()
    cur.close()
    conn.close()
