import os
import mysql.connector

def get_db_config():
    return {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "user": os.getenv("MYSQL_USER", "testuser"),
        "password": os.getenv("MYSQL_PASSWORD", "testpass"),
        "database": os.getenv("MYSQL_DATABASE", "testdb")
    }

def get_db_connection():
    config = get_db_config()
    return mysql.connector.connect(**config)