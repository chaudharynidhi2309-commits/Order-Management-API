

import os
from psycopg2 import pool
from dotenv import load_dotenv
from flask import jsonify

# Load database credentials from .env
load_dotenv()

# Read config from environment variables
config = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Database parameters
db_params = {
    "database": config['database'],
    "user": config['user'],
    "password": config['password'],
    "host": config['host'],
    "port": config['port']
}

# Helper function to close connection and cursor
def close_conn(conn, cur):
    if cur: 
        cur.close()
    if conn: 
        cpool.putconn(conn)

# Helper function for error messages
def error_message(error, msg):
    return {
        "status": "error",
        "message": msg,
        "error_details": error
    }

# Initialize Connection Pool
cpool = pool.SimpleConnectionPool(minconn=1, maxconn=100, **db_params)
if not cpool:
    raise ConnectionError("Connection pool could not be established.")

print("✅ Connection pool created successfully!")

# EXACTLY AS YOUR SIR WANTS - INSERT/UPDATE/DELETE
def db_crud_query(insert_query):
    conn, cur = None, None
    try:
        conn = cpool.getconn()
        cur = conn.cursor()
        cur.execute(insert_query)
        conn.commit()
    except Exception as e:
        error = str(e)
        msg = 'Server Issue please contact Administration'
        error_res = error_message(error, msg)
        print("error_res", error_res)
        return jsonify(error_res), 400
    finally:
        close_conn(conn, cur)

# EXACTLY AS YOUR SIR WANTS - SELECT
def execute_featch_query(featch_query):
    conn, cur = None, None
    try:
        conn = cpool.getconn()
        cur = conn.cursor()
        cur.execute(featch_query)
        data = cur.fetchall()
        return data
    except Exception as e:
        error = str(e)
        msg = 'Server Issue please contact Administration'
        error_res = error_message(error, msg)
        print("error_res", error_res)
        return jsonify(error_res), 400
    finally:
        close_conn(conn, cur)