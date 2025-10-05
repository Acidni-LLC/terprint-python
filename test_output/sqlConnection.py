"""
Connects to a SQL database using pyodbc
"""
from os import getenv
from dotenv import load_dotenv
import pyodbc
from pyodbc import connect


try:
    load_dotenv()
    #conn = connect(getenv("SQL_CONNECTION_STRING"))
    AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 18 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Uid=jgill@acidnillc.onmicrosoft.com;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryInteractive"
#AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 18 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
#connection_string = AZURE_SQL_CONNECTIONSTRING
    #AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 17 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
    conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
    cursor = conn.cursor()
    print("Connection successful!")

    #You can now execute SQL queries using the cursor
    print("terpeneResults")

    cursor.execute("SELECT * FROM terpeneResults")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.execute("        INSERT INTO [dbo].[cannabinoidResults]            ([batch], [Index], [Cannabinoid], [percent], [milligrams],   [dispensaryId], [createdBy])        VALUES  ('1111' ,1 ,'THC' ,.025 ,.0025 ,1 ,'jgill@acidnillc.onmicrosoft.com')    ")

    print("cannabinoidResults")
    cursor.execute("SELECT * FROM cannabinoidResults")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error connecting to SQL Server: {sqlstate}")

finally:
    if 'cnxn' in locals() and cnxn:
        cnxn.close()