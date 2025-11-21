"""
Clear all data from Event House table
"""
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from azure_config import (
    EVENTHOUSE_CLUSTER,
    EVENTHOUSE_DATABASE,
    EVENTHOUSE_TABLE,
)

def clear_table():
    """Delete all data from the Event House table"""
    cluster_uri = f"https://{EVENTHOUSE_CLUSTER}.kusto.fabric.microsoft.com"
    
    # Use Azure CLI authentication
    kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster_uri)
    client = KustoClient(kcsb)
    
    print(f"🗑️  CLEARING EVENT HOUSE TABLE")
    print("=" * 60)
    print(f"Cluster: {cluster_uri}")
    print(f"Database: {EVENTHOUSE_DATABASE}")
    print(f"Table: {EVENTHOUSE_TABLE}")
    print()
    
    try:
        # Check current row count
        query = f"{EVENTHOUSE_TABLE} | count"
        response = client.execute(EVENTHOUSE_DATABASE, query)
        current_count = list(response.primary_results[0])[0]['Count']
        print(f"📊 Current rows in table: {current_count}")
        
        if current_count == 0:
            print("✅ Table is already empty!")
            return
        
        # Clear the table
        print(f"\n🗑️  Deleting all {current_count} rows...")
        clear_command = f".clear table {EVENTHOUSE_TABLE} data"
        response = client.execute_mgmt(EVENTHOUSE_DATABASE, clear_command)
        
        print("✅ Table cleared successfully!")
        
        # Verify it's empty
        response = client.execute(EVENTHOUSE_DATABASE, query)
        new_count = list(response.primary_results[0])[0]['Count']
        print(f"📊 Rows after clearing: {new_count}")
        
    except KustoServiceError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    clear_table()
