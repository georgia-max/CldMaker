import os

DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DB_USER'],
    dbpass=os.environ['DB_PASS'],
    dbhost=os.environ['DB_HOST'],
    dbname=os.environ['DB_NAME']
)