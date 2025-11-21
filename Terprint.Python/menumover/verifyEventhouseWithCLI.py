"""
Verify Event House ingestion is working by checking the last upload
This uses Azure CLI authentication which may have more permissions
"""
import sys
import os

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.extend([current_dir, parent_dir])

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure_config import (
    EVENTHOUSE_CLUSTER,
    EVENTHOUSE_DATABASE,
    EVENTHOUSE_TABLE,
)


def verify_ingestion_with_cli():
    """Try to verify ingestion using Azure CLI authentication"""
    
    cluster_uri = f"https://{EVENTHOUSE_CLUSTER}.kusto.fabric.microsoft.com"
    
    print("Attempting to use Azure CLI authentication...")
    print("Make sure you've run 'az login' first!")
    print()
    
    kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster_uri)
    client = KustoClient(kcsb)
    
    print(f"Connecting to Event House:")
    print(f"  Cluster: {cluster_uri}")
    print(f"  Database: {EVENTHOUSE_DATABASE}")
    print(f"  Table: {EVENTHOUSE_TABLE}")
    print("=" * 60)
    
    # Try to count rows
    print("\nAttempting to count rows in table...")
    query = f"{EVENTHOUSE_TABLE} | count"
    
    try:
        response = client.execute(EVENTHOUSE_DATABASE, query)
        if response.primary_results[0].rows_count > 0:
            count = response.primary_results[0][0]['Count']
            print(f"✅ SUCCESS! Total rows in table: {count:,}")
            
            # Try to get sample data
            print("\nGetting sample data (5 rows)...")
            query = f"{EVENTHOUSE_TABLE} | take 5"
            response = client.execute(EVENTHOUSE_DATABASE, query)
            
            if response.primary_results[0].rows_count > 0:
                print(f"✅ Found {response.primary_results[0].rows_count} rows:")
                for i, row in enumerate(response.primary_results[0], 1):
                    print(f"\n   Row {i}:")
                    for key, value in row.items():
                        str_value = str(value)
                        if len(str_value) > 200:
                            str_value = str_value[:200] + "..."
                        print(f"      {key}: {str_value}")
        else:
            print("⚠️  Table appears to be empty")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPossible solutions:")
        print("1. Run 'az login' to authenticate with Azure CLI")
        print("2. Grant your user account 'Viewer' or 'Admin' permissions on the Event House database")
        print("3. Ask your admin to grant read permissions to the Service Principal")


if __name__ == "__main__":
    try:
        verify_ingestion_with_cli()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
