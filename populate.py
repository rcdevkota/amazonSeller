import psycopg2 as pg
import os
import json
from dotenv import load_dotenv
from .models import Subcategory,SellerInfo  
import psycopg2 as pg
import os

load_dotenv()

# Connect to an existing database
conn = pg.connect(dbname=os.environ["DATABASE_NAME"], user=os.environ["DATABASE_USER"], host=os.environ["DATABASE_HOST"], password=os.environ["DATABASE_PASSWORD"], port=os.environ["DATABASE_PORT"])

# Open a cursor to perform database operations
cur = conn.cursor()
conn.autocommit = True

cur.execute("insert into reference_app_uitext('' ) values('')")



# for language in language_detals:
#     cur.execute("INSERT INTO reference_app_language (language_id, language_name) VALUES (%s, %s)", (language["language_id"], language["language_name"]))

# cur.execute("insert into reference_app_tablename(table_name) values('Customer')")   
# cur.execute("insert into reference_app_tablename(table_name) values('UI')")  



if conn is not None:
    conn.close()
