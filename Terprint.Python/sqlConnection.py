"""
Connects to a SQL database using pyodbc
"""
from dotenv import load_dotenv
import pyodbc
from pyodbc import connect
from bcolors import bcolors
import COA_MethodDataExtractor
from typing import Optional
from COA_MethodDataExtractor import COA

AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 17 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Uid=adm;Pwd=sql1234%;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def checkCannabinoid(batch: str):    
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
def checkTerpene(batch: str):
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
        batch: str, 
        Index: int, 
        Cannabinoid: str,
        percent: str,
        milligrams: str,  
        dispensaryId: int, 
        createdBy: str,
        batchid: int):
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
        [batchID],
        [created] 
        ) OUTPUT INSERTED.cannabinoidResultId
        VALUES (?, ?, ?, ?,?,?, ?,?,CURRENT_TIMESTAMP)
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
        print(bcolors.FAIL + "insertcannabinoids Error connecting to SQL Server: "+sqlstate)

    finally:
        if 'conn' in locals() and conn:
            conn.close()
def insertstrain(strainName: str):
    strainID = None
    try:    
        print ("Inserting strain")
        load_dotenv()
        conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
        cursor = conn.cursor()
        SQL_STATEMENT = """
        INSERT INTO [dbo].[Strain]
           ([StrainName]
           ,[StrainDescription]
           ,[created])
        OUTPUT INSERTED.StrainID
        VALUES (?,?, CURRENT_TIMESTAMP)
        """
        cursor.execute(
        SQL_STATEMENT,
        (
        strainName,""
        )
        )
        strainID = cursor.fetchval()
        print(f"Inserted StrainID : {strainID} for Strain Name: {strainName}")
        conn.commit()
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        msg = ex.args[1] if len(ex.args) > 1 else ""
        print(bcolors.FAIL + "insertstrain Error connecting to SQL Server: "+sqlstate +" - " +msg)
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return strainID
def getStrainID(strainName):
    strainID = None
    try: 
       # print ("Looking up strain for "+ strainName )
        load_dotenv()
        conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
        cursor = conn.cursor()        
        SQL_STATEMENT = """
        SELECT StrainID FROM Strain WHERE StrainName = ?
        """
        sql = "" 
        cursor.execute(SQL_STATEMENT,(strainName))
        row = cursor.fetchone()
        if row:
            strainID = row[0]
            print(f"Found StrainID: {strainID} for Strain Name: {strainName}")
        else:
            print(f"No StrainID found for Strain Name: {strainName}")
            strainID = insertstrain(strainName)
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        msg = ex.args[1] if len(ex.args) > 1 else ""
        print(bcolors.FAIL + "getStrainID Error connecting to SQL Server: "+sqlstate + " | " + msg)
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return strainID
def getBatchID(batchName: str) -> Optional[int]:
    BatchID = None
    try: 
        print ("Looking up batch")
        load_dotenv()
        conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
        cursor = conn.cursor()
        sql = "SELECT BatchId FROM Batch WHERE Name = ?"
        cursor.execute(sql, (batchName))
        row = cursor.fetchone()
        if row:
           # print ("found batchid "+ str(row[0]))
            BatchID = row[0]
            print(f"Found BatchID: {BatchID} for Batch Name: {batchName}")
        else:
            print(f"No BatchID found for Batch Name: {batchName}")
            BatchID = 0
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(bcolors.FAIL + "getBatchID Error connecting to SQL Server: "+sqlstate)
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return BatchID

def insertBatch(
        coadata:  COA,
        producttype: str,
        dispensaryId: int,       # GrowerID   #1 Trulieve #2 Sunburn
        createdBy: str,        
        jsonstring: str,        
        batchName: str
    ) -> Optional[int]:
    """
    Insert a Batch record and return the inserted BatchID (int) or None on error.
    coadata: instance of COAMethodDataExtractor.COA
    """
    conn = None
    try:
        batchid: Optional[int] = None
        print (batchid)
        batchid =  getBatchID(batchName) 
        print (batchid)
        if batchid == 0:
            print("get straind id for "+ (coadata.product_name or "Unknown"))
            strainid = getStrainID(coadata.product_name)
            load_dotenv()
            conn = pyodbc.connect(AZURE_SQL_CONNECTIONSTRING)
            cursor = conn.cursor()

            SQL_STATEMENT = """
        INSERT INTO [dbo].[Batch]
            ([createdby]
            ,[Name]
            ,[Type]
            ,[Date]
            ,[GrowerID]
            ,[StrainID]
            ,[batchJSON]
            ,[totalTerpenes]
            ,[totalCannabinoids]
            ,[created]
            )
            OUTPUT INSERTED.BatchID
            VALUES (?, ?, ?,?,?, ?,?,?,?,CURRENT_TIMESTAMP)
            """ 
            print("batch sql" + SQL_STATEMENT)
            cursor.execute(
                SQL_STATEMENT,
                (
                    createdBy,
                    batchName,
                    producttype,
                    coadata.production_date,
                    dispensaryId,
                    strainid, 
                    jsonstring,
                    coadata.total_terpenes_percent,
                    coadata.total_cannabinoids_percent
                )
            )
            resultId = cursor.fetchval()
            print(f"Inserted batchid : {resultId}")
            conn.commit()
            batchid = resultId
            print (batchid)
        else: 
            print(bcolors.WARNING + f"Batch '{batchName}' already exists with BatchID: {batchid}. Skipping insert." + bcolors.ENDC)

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        msg = ex.args[1] if len(ex.args) > 1 else ""
        
        print(bcolors.FAIL + "insertBatch Error connecting to SQL Server: " + sqlstate +"-" + msg)

    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return batchid
       

def insertterpenes(
    batch: str,
    Index: int,
    terpene: str,
    percent: str,
    milligrams: str,
    dispensaryId: int,
    createdBy: str,
    batchid: int):
        
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
        VALUES (?, ?, ?, ?,?,CURRENT_TIMESTAMP,?, ?,?)
        """

        cursor.execute(
        SQL_STATEMENT,
        (
        batch, Index, terpene, percent, 
        milligrams, dispensaryId, createdBy, batchid
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
        print(bcolors.FAIL + "insertterpenes Error connecting to SQL Server: "+sqlstate)

    finally:
        if 'conn' in locals() and conn:
            conn.close()