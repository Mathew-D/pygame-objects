#Made by: Mathew Dusome
#Added the DB options
#To use:
#  connection = create_connection('database_name.db')
#  create_table(connection,"test",["first TEXT", "last TEXT"]) 
#  insert_db(connection,"lesson",["firstname","lastname","age"],["zzz","xxx",211])
#  result=select_db(connection,"test").fetchall()
#  result = select_db(connection,"lesson",["first='bob'","lastname='ian'"]).fetchall()
#  update_db(connection,"test",["first='joe'"],"id=4")
#  update_db(connection,"test",["first='joe'","last='dusome'"],"id=4")
#  delete_db(db_connection, "test", ["name", "year"], ["value of name", "value of year"])
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

