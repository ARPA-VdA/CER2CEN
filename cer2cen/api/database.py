def get_primary(connection, table):
    """
    Retrieves the name of the primary key column for a given table in the database.

    This function executes a SQL query to determine the primary key of the specified table. 
    The primary key is crucial for performing operations like identifying unique records or 
    querying new records based on the last migrated primary key.

    Parameters
    ----------
    connection : MySQLConnection
        The database connection object used to execute the query.
    table : str
        The name of the table for which the primary key is being retrieved.

    Returns
    -------
    str
        The name of the primary key column for the given table.
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'")

    row= cursor.fetchone()
    cursor.close()

    return row["Column_name"]

def get_new(connection, table, lastid):
    """
    Retrieves new records from the table where the primary key is greater than the last migrated ID.

    This function is designed to fetch records that are newly added or updated after the last 
    migration checkpoint, identified by the last primary key value (`lastid`). The records 
    are fetched in ascending order of the primary key to ensure a sequential data migration.

    Parameters
    ----------
    connection : MySQLConnection
        The database connection object used to execute the query.
    table : str
        The name of the table from which new records are being fetched.
    lastid : int
        The last migrated primary key value. Records with a primary key greater than this value
        will be considered as new.

    Returns
    -------
    list of dict
        A list of dictionaries where each dictionary represents a row in the table. Each key-value 
        pair in the dictionary corresponds to a column name and its associated value.
    """
    pk = get_primary(connection, table)

    cursor = connection.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM {table} WHERE {pk} > {lastid} ORDER BY {pk} ASC")
    
    row = cursor.fetchall()

    cursor.close()

    return row

def get_post_string(row):
    """
    Prints the key-value pairs of a row dictionary and then prints the entire row.

    This function is mainly for debugging or logging purposes. It loops through each key-value
    pair in the provided dictionary (representing a table row) and prints them, followed by
    printing the entire row.

    Parameters
    ----------
    row : dict
        A dictionary representing a single row from the table, where keys are column names
        and values are the corresponding values for that row.

    Returns
    -------
    None
    """
    for k, v in row.items():
        print(k, v)
    print(row)