import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER", "testuser"),
        password=os.getenv("MYSQL_PASSWORD", "testpass"),
        database=os.getenv("MYSQL_DATABASE", "testdb")
    )