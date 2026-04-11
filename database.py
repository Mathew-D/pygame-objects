#Made by: Mathew Dusome
#SQLite database helper functions
#
#IMPORT:
#    import objects.database as db
#
#FUNCTION PARAMETERS:
#
#create_connection(db_file)
#    db_file --> Path to database file (e.g., 'database.db')
#    Returns: Connection object or None
#
#create_table(conn, table, columns)
#    conn    --> Database connection object
#    table   --> Name of table to create
#    columns --> List of column definitions (e.g., ["first TEXT", "last TEXT", "age INTEGER"])
#
#insert_db(conn, table, columns, data)
#    conn    --> Database connection object
#    table   --> Table name to insert into
#    columns --> List of column names (e.g., ["first", "last", "age"])
#    data    --> List of values to insert (e.g., ["John", "Doe", 30])
#
#select_db(conn, table, columns_and_data=None)
#    conn              --> Database connection object
#    table             --> Table name to select from
#    columns_and_data  --> Optional list of conditions (e.g., ["first='John'", "age=30"])
#    Returns: Query results (call .fetchall() to get list)
#
#update_db(conn, table, columns_and_data, where_to_update)
#    conn              --> Database connection object
#    table             --> Table name to update
#    columns_and_data  --> List of updates (e.g., ["first='Jonathan'", "age=31"])
#    where_to_update   --> Condition for which rows to update (e.g., "id=1")
#
#delete_db(conn, table, columns, values)
#    conn    --> Database connection object
#    table   --> Table name to delete from
#    columns --> List of column names to match (e.g., ["first", "age"])
#    values  --> List of values to match (e.g., ["John", 30])
#
#EXAMPLE: Complete workflow
#1. Create connection
#  connection = db.create_connection('database.db')
#
#2. Create table
#  db.create_table(connection, "users", ["first TEXT", "last TEXT", "age INTEGER"])
#
#3. Insert data
#  db.insert_db(connection, "users", ["first", "last", "age"], ["John", "Doe", 30])
#  db.insert_db(connection, "users", ["first", "last", "age"], ["Jane", "Smith", 25])
#
#4. Select all records
#  results = db.select_db(connection, "users").fetchall()
#
#5. Select with conditions
#  results = db.select_db(connection, "users", ["first='John'", "age=30"]).fetchall()
#
#6. Update records
#  db.update_db(connection, "users", ["first='Jonathan'", "age=31"], "id=1")
#
#7. Delete records
#  db.delete_db(connection, "users", ["first", "age"], ["John", 30])
import sqlite3 
def create_connection(db_file):
    #create a database connection to the SQLite database
    #return: Connection object or None
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def create_table(conn,table, columns):
    col = ",".join(columns)
    sql = f'''CREATE TABLE IF NOT EXISTS {table}( id INTEGER PRIMARY KEY, {col});'''
    conn.execute(sql)

def insert_db(conn,table, columns,data):
    sql=f'''INSERT INTO {table} {tuple(columns)} VALUES {tuple(data)};'''
    conn.execute(sql)
    conn.commit()

def select_db(conn,table,columns_and_data=None):
    if not columns_and_data==None:
        col = " AND ".join(columns_and_data)
        sql=f'''SELECT * FROM {table} WHERE {col}'''
        return conn.execute(sql)
    else:
        sql =f"SELECT * from {table}"
        return conn.execute(sql)

def update_db(conn,table,columns_and_data,where_to_update):
    col = ",".join(columns_and_data)
    sql = f"UPDATE {table} set {col} where {where_to_update}"
    conn.execute(sql)
    conn.commit()  

def delete_db(conn, table, columns: list, values: list):
    if len(columns) != len(values):
        raise ValueError("Length of columns and values must match.")
    # Build WHERE clause with placeholders
    where_clause = " AND ".join([f"{col} = ?" for col in columns])
    # Final SQL statement
    sql = f'DELETE FROM {table} WHERE {where_clause}'
    # Execute with the values list
    conn.execute(sql, values)
    conn.commit()

