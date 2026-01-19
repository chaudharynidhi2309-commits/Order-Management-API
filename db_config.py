import os
from psycopg2 import pool
from dotenv import load_dotenv

# Load database credentials from .env
load_dotenv()

try:
    # Initialize Connection Pool
    db_pool = pool.SimpleConnectionPool(
        1, 10, # Min 1 connection, Max 10 connections
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    if db_pool:
        print("✅ Connection pool created successfully!")

except Exception as e:
    print(f"❌ Error: Could not connect to database. {e}")

# Helper function to get a connection from the pool
def get_db_connection():
    return db_pool.getconn()

# Helper function to put the connection back in the pool
def release_db_connection(conn):
    db_pool.putconn(conn)