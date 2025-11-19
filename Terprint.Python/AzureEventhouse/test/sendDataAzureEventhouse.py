import json
import pandas as pd
from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.ingest import QueuedIngestClient, IngestionProperties, DataFormat, IngestionMapping, IngestionMappingKind
from azureDataLake.azure_config import AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, USE_AZURE_CLI, validate_config

def send_json_to_eventhouse(
    json_data,
    cluster="solareventhouse",
    database="terprinteventhouse", 
    table="onelakejsonparser",
    column="data"
):
    """
    Send JSON data to Azure Eventhouse (Kusto) database.
    
    Args:
        json_data: The JSON data to send (dict, list, or string)
        cluster: The Kusto cluster name (default: solareventhouse)
        database: The database name (default: terprinteventhouse)
        table: The table name (default: onelakejsonparser)
        column: The column name to store the data (default: data)
    """
    # Validate configuration
    if not validate_config():
        raise ValueError("Azure configuration validation failed")
    
    # Serialize json_data to string if it's not already
    if isinstance(json_data, (dict, list)):
        json_string = json.dumps(json_data)
    else:
        json_string = str(json_data)
    
    # Create DataFrame with the JSON string
    df = pd.DataFrame({column: [json_string]})
    
    # Build connection string using configured authentication method
    cluster_uri = f"https://{cluster}.kusto.windows.net"
    
    if USE_AZURE_CLI:
        print("Using Azure CLI authentication...")
        kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster_uri)
    else:
        print("Using Service Principal authentication...")
        kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
            cluster_uri, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
        )
    
    # Create ingest client
    ingest_client = QueuedIngestClient(kcsb)
    
    # Define ingestion mapping for JSON format
    ingestion_mapping = IngestionMapping(
        kind=IngestionMappingKind.JSON,
        ingestion_mapping={"Column": column, "DataType": "string", "Properties": {"path": f"$.{column}"}}
    )
    
    # Set ingestion properties
    ingestion_properties = IngestionProperties(
        database=database,
        table=table,
        data_format=DataFormat.JSON,
        ingestion_mapping=ingestion_mapping
    )
    
    # Perform the ingestion
    ingest_client.ingest_from_dataframe(df, ingestion_properties)
    
    print(f"Successfully sent JSON data to {cluster}/{database}/{table}")

# Example usage:
if __name__ == "__main__":
    # Load the newest Trulieve products file
    file_path = r"C:\Users\JamiesonGill\source\repos\Acidni-LLC\Terprint\Terprint.Python\menus\trulieve\trulieve_products_20251118_191253.json"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            trulieve_data = json.load(f)
        
        print(f"Loaded Trulieve data with {trulieve_data.get('total_products', 'unknown')} products")
        send_json_to_eventhouse(trulieve_data)
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Error: {e}")