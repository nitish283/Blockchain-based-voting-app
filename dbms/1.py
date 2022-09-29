import psycopg2
import datetime
from user import *
from psycopg2 import Error
from blockchain import *

f = open("db.key","r")
usr = f.readline()[:-1]
password = f.readline()[:-1]
host = f.readline()[:-1]
port = f.readline()[:-1]
database = f.readline()
connection = psycopg2.connect(user=usr,
                            password=password,
                            host=host,
                            port=port,
                            database=database)
connection.autocommit = True

cursor = connection.cursor()
print(connection.get_dsn_parameters(), "\n")

cursor.execute("select * from p2pr230924_votechain where id = " + str(1) + ";")

print(cursor.fetchall())

cursor.close()
connection.close()

