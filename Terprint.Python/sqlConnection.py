"""
Connects to a SQL database using pyodbc
"""
from os import getenv
from dotenv import load_dotenv
import pyodbc
from pyodbc import connect
from bcolors import bcolors
import COAMethodDataExtractor
from typing import Optional
from COAMethodDataExtractor import COA

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
        createdBy,
        batchid):
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
        [created] ,
        [batchID]
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
        createdBy,
        batchid
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
def insertstrain(
    strainName):
    strainID = None
    try:    
        load_dotenv()
        conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
        cursor = conn.cursor()
        SQL_STATEMENT = """
        INSERT INTO [dbo].[Strain]
           ([Name]
           ,[created])
        OUTPUT INSERTED.StrainID
        VALUES (?, CURRENT_TIMESTAMP)
        """
        cursor.execute(
        SQL_STATEMENT,
        (
        strainName,
        )
        )
        strainID = cursor.fetchval()
        print(f"Inserted StrainID : {strainID} for Strain Name: {strainName}")
        conn.commit()
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(bcolors.FAIL + "Error connecting to SQL Server: "+sqlstate)
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return strainID
def getStrainID(strainName):
    strainID = None
    try: 
        load_dotenv()
        conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
        cursor = conn.cursor()
        sql = "SELECT StrainID FROM Strain WHERE Name = ?"
        cursor.execute(sql, (strainName))
        row = cursor.fetchone()
        if row:
            strainID = row.StrainID
            print(f"Found StrainID: {strainID} for Strain Name: {strainName}")
        else:
            print(f"No StrainID found for Strain Name: {strainName}")
            strainID = insertstrain(strainName)
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(bcolors.FAIL + "Error connecting to SQL Server: "+sqlstate)
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return strainID

def insertBatch(
        coadata:  COA,
        producttype: str,
        dispensaryId: int,       # GrowerID   #1 Trulieve #2 Sunburn
        createdBy: str
    ) -> Optional[int]:
    """
    Insert a Batch record and return the inserted BatchID (int) or None on error.
    coadata: instance of COAMethodDataExtractor.COA
    """
    batchid: Optional[int] = None
    try:
        strainid = getStrainID(coadata.strainName if getattr(coadata, "strainName", None) else "Unknown")
        load_dotenv()
        conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
        cursor = conn.cursor()

        SQL_STATEMENT = """
       INSERT INTO [dbo].[Batch]
           ([created]
           ,[createdby]
           ,[Name]
           ,[Type]
           ,[Date]
           ,[GrowerID]
           ,[StrainID]
           ,[batchJSON])
        OUTPUT INSERTED.BatchID
        VALUES (CURRENT_TIMESTAMP, ?, ?, ?,?,?, ?)
        """

        cursor.execute(
            SQL_STATEMENT,
            (
                createdBy,
                coadata.batchNumber,
                producttype,
                coadata.batchDate,
                dispensaryId,
                strainid,
                coadata.to_json()
            )
        )
        resultId = cursor.fetchval()
        print(f"Inserted batchid : {resultId}")
        conn.commit()
        batchid = resultId

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(bcolors.FAIL + "Error connecting to SQL Server: " + sqlstate)

    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return batchid
       

def insertterpenes(
    batch           ,
    Index           ,
    terpene           ,
    percent           ,
    milligrams           ,
    dispensaryId        ,
    createdBy,
    batchid)  :
        
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
        ,[createdBy]
        ,[batchID])
        OUTPUT INSERTED.terpeneResultId
        VALUES (?, ?, ?, ?,?,CURRENT_TIMESTAMP,?, ?)
        """

        cursor.execute(
        SQL_STATEMENT,
        (
        batch, Index, terpene, percent, milligrams, dispensaryId, createdBy, batchid
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