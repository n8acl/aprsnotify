
def insert_sql(conn,sql,values_list):
    # Executes SQL for inserts - Doesn't return anything

    with conn.connect() as connection:
        connection.execute(sql,values_list)
        connection.commit()
        connection.close()


def exec_sql(conn,sql):
    # Executes SQL for Updates, inserts and deletes - Doesn't return anything

    with conn.connect() as connection:
        connection.execute(sql)
        connection.commit()
        connection.close()

def select_sql(conn, sql):
    # Executes SQL for Selects - Returns a "value"

    with conn.connect() as connection:
        result = connection.execute(sql).fetchall()
    return result

def exec_proc(conn,proc,values):
    # Executes SQL Stored Procedures - Doesn't return anything

    connection = conn.raw_connection()

    try:
        cursor = connection.cursor()
        cursor.callproc(proc, values)
        cursor.close()
        connection.commit()
    finally:
        connection.close()