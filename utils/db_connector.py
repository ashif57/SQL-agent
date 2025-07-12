import psycopg2
import pandas as pd

def get_connection(host, port, dbname, user, password):
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

def run_query(sql, host, port, dbname, user, password):
    conn = get_connection(host, port, dbname, user, password)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df
