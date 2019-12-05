import cx_Oracle  #there is also  pyodbc
from pprint import pprint

class OraDBConnect:
 def __init__(self,dbHost,dbUser,dbPass,dbInstance,dbPort):
    # Build a DSN (can be subsitited for a TNS name)
    self.dsn = cx_Oracle.makedsn(dbHost, dbPort, dbInstance)
    self.db = cx_Oracle.connect(dbUser, dbPass, self.dsn)
    print "DB Version" + self.db.version


 def query(self,querySQL):
    cursor = self.db.cursor()
    cursor.execute(querySQL)                #cursor.fetchone()
    print cursor.description
    #for result in cursor:
    #    print result
    #pprint(cursor.fetchall())
    #pprint(cursor.fetchone())
    return cursor.fetchall()
 def __del__(self):
     print ("DB connection   is closing!")
     self.db.cursor().close()
     print ("cursor is closed by DB Desctractor!")
     self.db.close()
     print ("DB is closed by Desctractor!")
"""
 def close(self):
    print ("Close func  is closing!")
    self.db.cursor().close()
    print ("cursor is closed by Close func !")
    self.db.close()
    print ("DB is closed by Close func !")
"""





"""
#con = cx_Oracle.connect('pythonhol/welcome@127.0.0.1/orcl')
con = cx_Oracle.connect('ABPAPP1/ABPAPP1@VFIDB931/orcl')
#con = cx_Oracle.connect('ABPAPP1/ABPAPP1@illinqw931/orcl')
#con = cx_Oracle.connect(dbUserABP+'/' + dbPassABP +'@' + dbHost +'/orcl') #user/password/host/db service name 'orcl'
#Database Resident Connection Pooling ?can be nonpooling and pooling for long lifeprocesses we need to use pooling
print con.version
con.close()
"""
"""
import cx_Oracle
#creating  pooled connection
con = cx_Oracle.connect('pythonhol', 'welcome', '127.0.0.1:/orcl:pooled', 
             cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)

print con.version

con.close()
"""
"""
import cx_Oracle
#simple query
con = cx_Oracle.connect('pythonhol/welcome@127.0.0.1/orcl')

cur = con.cursor()
cur.execute('select * from departments order by department_id')
for result in cur:
    print result

cur.close()
con.close()  

"""

"""
import cx_Oracle, os, sys

def db_connect():
    # Build a DSN (can be subsitited for a TNS name)
    dsn = cx_Oracle.makedsn("ServerName", 1521, "DatabaseName")
    db = cx_Oracle.connect("username", "password", dsn)
    cursor = db.cursor()
    return cursor

def db_lookup(cursor):
    cursor.execute("SELECT SERVICEID FROM SERVICE WHERE STATUS = 0")
    row = cursor.fetchone()
    print row
    return row

cursor = db_connect()
#db_connect()
db_lookup(cursor)
"""

if __name__ == "__main__":
    db=OraDBConnect()
    result = db.query('select MANF_NAME from voucher_manufacturer');
    print result[1][0],type(result[1][0])
    #db.close()  #not needed with __del__



