"""
Check if data exists in Event House table
"""
import sys
import os
from datetime import datetime, timedelta

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.extend([current_dir, parent_dir])

from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure_config import (
    AZURE_TENANT_ID,
    AZURE_CLIENT_ID,
    AZURE_CLIENT_SECRET,
    USE_AZURE_CLI,
    EVENTHOUSE_CLUSTER,
    EVENTHOUSE_DATABASE,
    EVENTHOUSE_TABLE,
    EVENTHOUSE_COLUMN
)


def check_eventhouse_data():
    """Query Event House to check if data exists"""
    
    # Build connection string
    cluster_uri = f"https://{EVENTHOUSE_CLUSTER}.kusto.fabric.microsoft.com"
    
    if USE_AZURE_CLI:
        print("Using Azure CLI authentication...")
        kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster_uri)
    else:
        print("Using Service Principal authentication...")
        kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
            cluster_uri, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
        )
    
    # Create query client
    client = KustoClient(kcsb)
    
    print(f"\nConnecting to Event House:")
    print(f"  Cluster: {cluster_uri}")
    print(f"  Database: {EVENTHOUSE_DATABASE}")
    print(f"  Table: {EVENTHOUSE_TABLE}")
    print("=" * 60)
    
    # Query 1: Check if table exists
    print("\n1. Checking if table exists...")
    query = f".show tables | where TableName == '{EVENTHOUSE_TABLE}'"
    try:
        response = client.execute(EVENTHOUSE_DATABASE, query)
        if response.primary_results[0].rows_count > 0:
            print(f"   ✅ Table '{EVENTHOUSE_TABLE}' exists")
        else:
            print(f"   ❌ Table '{EVENTHOUSE_TABLE}' NOT found")
            return
    except Exception as e:
        print(f"   ❌ Error checking table: {e}")
        return
    
    # Query 2: Get table schema
    print("\n2. Checking table schema...")
    query = f".show table {EVENTHOUSE_TABLE} schema as json"
    try:
        response = client.execute(EVENTHOUSE_DATABASE, query)
        if response.primary_results[0].rows_count > 0:
            print(f"   ✅ Schema retrieved")
            for row in response.primary_results[0]:
                print(f"      {row['Schema']}")
        else:
            print(f"   ⚠️  No schema information")
    except Exception as e:
        print(f"   ⚠️  Could not get schema: {e}")
    
    # Query 3: Count total rows
    print("\n3. Counting total rows...")
    query = f"{EVENTHOUSE_TABLE} | count"
    try:
        response = client.execute(EVENTHOUSE_DATABASE, query)
        if response.primary_results[0].rows_count > 0:
            count = response.primary_results[0][0]['Count']
            print(f"   ✅ Total rows: {count:,}")
        else:
            print(f"   ⚠️  Table is empty")
    except Exception as e:
        print(f"   ❌ Error counting rows: {e}")
    
    # Query 4: Get recent data (last 24 hours)
    print("\n4. Checking for recent data (last 24 hours)...")
    # Try to query with ingestion_time if it exists
    query = f"""
    {EVENTHOUSE_TABLE}
    | where ingestion_time() > ago(24h)
    | summarize count()
    """
    try:
        response = client.execute(EVENTHOUSE_DATABASE, query)
        if response.primary_results[0].rows_count > 0:
            count = response.primary_results[0][0]['count_']
            print(f"   ✅ Rows ingested in last 24h: {count:,}")
        else:
            print(f"   ⚠️  No recent data found")
    except Exception as e:
        print(f"   ⚠️  Could not check recent data: {e}")
    
    # Query 5: Sample recent data
    print("\n5. Getting sample data (most recent 5 rows)...")
    query = f"{EVENTHOUSE_TABLE} | take 5"
    try:
        response = client.execute(EVENTHOUSE_DATABASE, query)
        if response.primary_results[0].rows_count > 0:
            print(f"   ✅ Found {response.primary_results[0].rows_count} sample rows:")
            for i, row in enumerate(response.primary_results[0], 1):
                print(f"\n   Row {i}:")
                for key, value in row.items():
                    # Truncate long values
                    str_value = str(value)
                    if len(str_value) > 100:
                        str_value = str_value[:100] + "..."
                    print(f"      {key}: {str_value}")
        else:
            print(f"   ⚠️  No data found in table")
    except Exception as e:
        print(f"   ❌ Error querying sample data: {e}")
    
    # Query 6: Check ingestion failures
    print("\n6. Checking for ingestion failures...")
    query = ".show ingestion failures | where FailedOn > ago(24h)"
    try:
        response = client.execute(EVENTHOUSE_DATABASE, query)
        if response.primary_results[0].rows_count > 0:
            print(f"   ⚠️  Found {response.primary_results[0].rows_count} ingestion failures:")
            for row in response.primary_results[0]:
                print(f"      Table: {row.get('Table', 'N/A')}")
                print(f"      Error: {row.get('Details', 'N/A')}")
                print(f"      Time: {row.get('FailedOn', 'N/A')}")
                print()
        else:
            print(f"   ✅ No ingestion failures in last 24h")
    except Exception as e:
        print(f"   ⚠️  Could not check failures: {e}")
    
    # Query 7: Check pending ingestion operations
    print("\n7. Checking pending ingestion operations...")
    query = ".show operations | where State == 'InProgress' and OperationKind == 'DataIngestPull'"
    try:
        response = client.execute(EVENTHOUSE_DATABASE, query)
        if response.primary_results[0].rows_count > 0:
            print(f"   ⏳ Found {response.primary_results[0].rows_count} pending ingestions")
            for row in response.primary_results[0]:
                print(f"      Operation: {row.get('OperationId', 'N/A')}")
                print(f"      Started: {row.get('StartedOn', 'N/A')}")
        else:
            print(f"   ✅ No pending operations")
    except Exception as e:
        print(f"   ⚠️  Could not check pending operations: {e}")
    
    print("\n" + "=" * 60)
    print("Check complete!")


if __name__ == "__main__":
    try:
        check_eventhouse_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
