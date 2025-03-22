import psycopg2
import sqlite3
import mysql.connector
from django.conf import settings

def get_db_connection(db_name):
    """
    Establish connection to the specified database.
    """
    if db_name == "postgres":
        return psycopg2.connect(
            user=settings.POSTGRES_USER ,     
            host=settings.POSTGRES_HOST  ,     
            database= settings.POSTGRES_DB,  
            password=settings.POSTGRES_PASSWORD   
        )
    elif db_name == "sqlite":
        return sqlite3.connect(settings.SQLITE_DB)
    
    elif db_name == "mysql":
        return mysql.connector.connect(
            database=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
        )
    else:
        raise ValueError("Invalid database selection")
