"""
Connects to a SQL database using pyodbc
"""
from os import getenv
from dotenv import load_dotenv
import pyodbc
from pyodbc import connect
from bcolors import bcolors

AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 17 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Uid=adm;Pwd=sql1234%;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def checkCannabinoid(batch):    
    load_dotenv()
    returnvalue = False
    conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
    cursor = conn.cursor()    
    sql = "SELECT * FROM vw_cannabinoidResults WHERE batch like '%"+batch+"%'"
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(bcolors.OKGREEN + batch +" cannabinoid record exisits" + bcolors.ENDC)
        returnvalue = True   
        break 
    return returnvalue
def checkTerpene(batch):
    load_dotenv()
    returnvalue = False
    conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
    cursor = conn.cursor()
    sql = "SELECT * FROM vw_terpeneResults WHERE batch like '%"+batch+"%'"
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        returnvalue = True    
        print(bcolors.OKGREEN + batch +" terpene record exisits" + bcolors.ENDC)
        break
    return returnvalue

def insertcannabinoids( 
        batch, 
        Index, 
        Cannabinoid,
        percent,
        milligrams,  
        dispensaryId, 
        createdBy):
    try: 
       # print("C variables in"+ batch+"|"+str(Index)+"|"+Cannabinoid+"|"+percent+"|"+milligrams+"|"+str(dispensaryId)+"|"+createdBy)
    
        load_dotenv()
        conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
        cursor = conn.cursor()
        # print("Connection successful!")

        #You can now execute SQL queries using the cursor
    

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
        
    # print(SQL_STATEMENT)    
        #print (str(Index) +"---"+batch + "," +        str(Index)  + "," +        Cannabinoid + "," +        percent + "," +        milligrams + "," +          str(dispensaryId) + "," +        createdBy+"---")
        cursor.execute(
        SQL_STATEMENT,
        (
            batch, 
        Index, 
        Cannabinoid,
        percent,
        milligrams,  
        dispensaryId, 
        createdBy
        )
        )
        resultId = cursor.fetchval()
        print(f"Inserted cannabinoidResultId : {resultId}")
        conn.commit()

        

        # print("cannabinoidResults")
        # cursor.execute("SELECT * FROM cannabinoidResults")
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)

    # cursor.close()
        #conn.close()
        

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(bcolors.FAIL + "Error connecting to SQL Server: "+sqlstate)

    finally:
        if 'conn' in locals() and conn:
            conn.close()

def insertterpenes(
    batch           ,
    Index           ,
    terpene           ,
    percent           ,
    milligrams           ,
    dispensaryId        ,
    createdBy):
        
    try: 
        #print("T variables in"+ batch+"|"+str(Index)+"|"+terpene+"|"+percent+"|"+milligrams+"|"+str(dispensaryId)+"|"+createdBy)
        load_dotenv()
        conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
        cursor = conn.cursor()
    # print("Connection successful!")

        #You can now execute SQL queries using the cursor
    # print("terpeneResults")
    #Terprintpw13579$
        # cursor.execute("SELECT * FROM terpeneResults")
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)

        SQL_STATEMENT = """
        INSERT INTO [dbo].[terpeneResults]
        ([batch]
        ,[Index]
        ,[terpene]
        ,[percent]
        ,[milligrams]
        ,[created]
        ,[dispensaryId]
        ,[createdBy])
        OUTPUT INSERTED.terpeneResultId
        VALUES (?, ?, ?, ?,?,CURRENT_TIMESTAMP,?, ?)
        """

        cursor.execute(
        SQL_STATEMENT,
        (
        batch           ,Index           ,terpene           ,percent           ,milligrams           ,dispensaryId        ,createdBy
        )
        )
        resultId = cursor.fetchval()
        print(f"Inserted terpeneResultId : {resultId}")
        conn.commit()

        

        # print("terpeneResults")
        # cursor.execute("SELECT * FROM terpeneResults")
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)

    #cursor.close()
        #conn.close()
       
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(bcolors.FAIL + "Error connecting to SQL Server: "+sqlstate)

    finally:
        if 'conn' in locals() and conn:
            conn.close()