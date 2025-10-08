
from os import getenv
from dotenv import load_dotenv
import pyodbc
from pyodbc import connect

# Replace with your own server and database names
server_name = "tcp:acidni-sql.database.windows.net,1433"
database_name = "terprint"
client_id = "de9598fc-7ece-4da1-8df7-20d9b4f9ad81"

load_dotenv()

AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 18 for SQL Server};Server=tcp:acidni-sql.database.windows.net,1433;Database=terprint;Encrypt=yes;TrustServerCertificate=no;Authentication=ActiveDirectoryMsi;Connection Timeout=30"
# Connection string using system-assigned managed identity
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={server_name};"
    f"Database={database_name};"
    f"UID={client_id};"
    "Authentication=ActiveDirectoryMsi;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    #"TrustServerCertificate=yes;"
)

try:
    with pyodbc.connect(AZURE_SQL_CONNECTIONSTRING) as cnxn:
        cursor = cnxn.cursor()
        print("Connection successful!")
        
        # Example query
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        if row:
            print(f"SQL Server version: {row[0]}")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Connection failed with error: {sqlstate}")