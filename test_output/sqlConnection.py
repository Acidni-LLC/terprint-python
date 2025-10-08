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
    #AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 18 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Uid=jgill@acidnillc.onmicrosoft.com;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryInteractive"
    AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 18 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Uid=adm;Pwd=sql1234%;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    ss="Driver={ODBC Driver 17 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Uid=afb576e9-40702int;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
#connection_string = AZURE_SQL_CONNECTIONSTRING
    #AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 17 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
    conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
    cursor = conn.cursor()
    print("Connection successful!")

    #You can now execute SQL queries using the cursor
    print("terpeneResults")
#Terprintpw13579$
    cursor.execute("SELECT * FROM terpeneResults")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    SQL_STATEMENT = """
    INSERT INTO [dbo].[cannabinoidResults]  (
    [batch], 
    [Index], 
    [Cannabinoid],
    [percent],
    [milligrams],  
    [dispensaryId], 
    [createdBy] ,
    [created]
    ) OUTPUT INSERTED.cannabinoidResultId
    VALUES (?, ?, ?, ?,?,?, ?,CURRENT_TIMESTAMP)
    """

    cursor.execute(
    SQL_STATEMENT,
    (
        '1111' ,
        1 ,
        'THC' ,
        .025 ,
        .0025 ,
        1 ,
        'jgill@acidnillc.onmicrosoft.com'
    )
    )
    resultId = cursor.fetchval()
    print(f"Inserted cannabinoidResultId : {resultId}")
    conn.commit()

    

    print("cannabinoidResults")
    cursor.execute("SELECT * FROM cannabinoidResults")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    conn.close()

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error connecting to SQL Server: {sqlstate}")

finally:
    if 'cnxn' in locals() and cnxn:
        cnxn.close()