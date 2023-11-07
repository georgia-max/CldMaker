import os

import psycopg2


def get_connection():
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    # TODO, uncomment when you have a database user and password
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        # user=db_user,
        # password=db_password
    )

    return conn
