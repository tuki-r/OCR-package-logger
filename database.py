import os

def get_connection():
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        # Production - postegreSQL on Railway
        import psycopg2
        conn = psycopg2.connect(database_url)

    else:
        # Local development - SQL Server
        import pyodbc
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=ImageOCRApp;'
            'Trusted_Connection=yes;'
        )
    return conn
