"""
List all tables in Event House database and create the target table if needed
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
    EVENTHOUSE_COLUMN
)


def manage_eventhouse_table():
    """List tables and create the target table if it doesn't exist"""
    
    cluster_uri = f"https://{EVENTHOUSE_CLUSTER}.kusto.fabric.microsoft.com"
    
    print("Using Azure CLI authentication...")
    print("(Make sure you've run 'az login' first)\n")
    
    kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster_uri)
    client = KustoClient(kcsb)
    
    print(f"Connecting to Event House:")
    print(f"  Cluster: {cluster_uri}")
    print(f"  Database: {EVENTHOUSE_DATABASE}")
    print("=" * 60)
    
    # Step 1: List all existing tables
    print("\n1. Listing all tables in database...")
    query = ".show tables"
    
    try:
        response = client.execute(EVENTHOUSE_DATABASE, query)
        if response.primary_results[0].rows_count > 0:
            print(f"   Found {response.primary_results[0].rows_count} tables:")
            table_exists = False
            for row in response.primary_results[0]:
                table_name = row['TableName']
                print(f"      - {table_name}")
                if table_name == EVENTHOUSE_TABLE:
                    table_exists = True
            
            if table_exists:
                print(f"\n   ✅ Target table '{EVENTHOUSE_TABLE}' already exists!")
                return True
            else:
                print(f"\n   ⚠️  Target table '{EVENTHOUSE_TABLE}' NOT found")
        else:
            print("   No tables found in database")
    except Exception as e:
        print(f"   ❌ Error listing tables: {e}")
        return False
    
    # Step 2: Create the table
    print(f"\n2. Creating table '{EVENTHOUSE_TABLE}'...")
    
    # Create table with a dynamic column to store JSON data
    create_command = f"""
    .create table {EVENTHOUSE_TABLE} (
        {EVENTHOUSE_COLUMN}: dynamic
    )
    """
    
    try:
        response = client.execute(EVENTHOUSE_DATABASE, create_command)
        print(f"   ✅ Table '{EVENTHOUSE_TABLE}' created successfully!")
        
        # Enable streaming ingestion for better performance
        print(f"\n3. Enabling streaming ingestion...")
        enable_streaming = f".alter table {EVENTHOUSE_TABLE} policy streamingingestion enable"
        try:
            client.execute(EVENTHOUSE_DATABASE, enable_streaming)
            print(f"   ✅ Streaming ingestion enabled")
        except Exception as e:
            print(f"   ⚠️  Could not enable streaming: {e}")
        
        # Set retention policy (optional)
        print(f"\n4. Setting retention policy (365 days)...")
        retention_command = f"""
        .alter table {EVENTHOUSE_TABLE} policy retention 
        ```
        {{
            "SoftDeletePeriod": "365.00:00:00",
            "Recoverability": "Enabled"
        }}
        ```
        """
        try:
            client.execute(EVENTHOUSE_DATABASE, retention_command)
            print(f"   ✅ Retention policy set")
        except Exception as e:
            print(f"   ⚠️  Could not set retention policy: {e}")
        
        print(f"\n" + "=" * 60)
        print(f"✅ Table setup complete!")
        print(f"\nYou can now run the orchestrator to upload data:")
        print(f"   python dispensaryOrchestrator.py --dev")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating table: {e}")
        print(f"\nYou may need admin permissions to create tables.")
        print(f"Ask your admin to create the table with this command:")
        print(f"\n{create_command}")
        return False


if __name__ == "__main__":
    try:
        manage_eventhouse_table()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
