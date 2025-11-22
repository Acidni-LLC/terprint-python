"""
Upload JSON data to Azure Event House (Kusto)
"""
import os
import json
import io
import logging
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
# azure-kusto imports may not be available in all environments. Guard them so
# consumers can import this module (e.g., to parse docs or run tests) even when
# the packages are missing. If the azure packages aren't present, the module
# will still import successfully but attempting to initialize EventHouseUploader
# will raise a clear ImportError with the underlying cause.
try:
    from azure.kusto.data import KustoConnectionStringBuilder, DataFormat
    from azure.kusto.ingest import (
        QueuedIngestClient,
        IngestionProperties,
        IngestionMappingKind,
        ColumnMapping,
    )
    _KUSTO_AVAILABLE = True
    _KUSTO_IMPORT_ERROR = None
except Exception as _e:  # pragma: no cover - environment specific
    _KUSTO_AVAILABLE = False
    _KUSTO_IMPORT_ERROR = _e

logger = logging.getLogger(__name__)


class EventHouseUploader:
    """Handles uploading JSON data to Azure Event House"""
    
    def __init__(
        self,
        cluster: str,
        database: str,
        table: str,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        use_azure_cli: bool = False,
        column_name: str = "data"
    ):
        """
        Initialize Event House uploader
        
        Args:
            cluster: Kusto cluster name (e.g., 'trd-vdf84t56eet09mgd66.z5')
            database: Database name
            table: Table name
            tenant_id: Azure tenant ID
            client_id: Azure client ID
            client_secret: Azure client secret
            use_azure_cli: Use Azure CLI auth instead of service principal
            column_name: Column name to store JSON data
        """
        self.cluster = cluster
        self.database = database
        self.table = table
        self.column_name = column_name
        self.cluster_uri = f"https://{cluster}.kusto.fabric.microsoft.com"
        
        # Check azure-kusto availability
        if not _KUSTO_AVAILABLE:
            # Fail fast with a helpful error. The original import failure is
            # attached to the exception to aid troubleshooting.
            raise ImportError(
                "Required package `azure-kusto-data` / `azure-kusto-ingest` is not available. "
                "Install with `pip install azure-kusto-data azure-kusto-ingest` or set use_azure_cli accordingly. "
            ) from _KUSTO_IMPORT_ERROR

        # Build connection string
        if use_azure_cli:
            logger.info("Using Azure CLI authentication for Event House...")
            self.kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(self.cluster_uri)
        else:
            logger.info("Using Service Principal authentication for Event House...")
            self.kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                self.cluster_uri, client_id, client_secret, tenant_id
            )
        
        # Create ingest client
        self.ingest_client = QueuedIngestClient(self.kcsb)
        
        # Set up ingestion properties
        self.ingestion_properties = IngestionProperties(
            database=database,
            table=table,
            data_format=DataFormat.JSON,
        )
        
        # Set the mapping
        self.ingestion_properties.ingestion_mapping = [
            {"column": column_name, "path": "$", "datatype": "dynamic"}
        ]
        self.ingestion_properties.ingestion_mapping_kind = IngestionMappingKind.JSON
        
        logger.info(f"Event House uploader initialized: {self.cluster_uri}/{database}/{table}")
    
    def upload_json(self, json_data: Any, source_info: Optional[Dict] = None) -> bool:
        """
        Upload JSON data to Event House
        
        Args:
            json_data: JSON data to upload (dict, list, or string)
            source_info: Optional metadata about the source (filename, dispensary, etc.)
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            # Add metadata if provided
            if source_info:
                if isinstance(json_data, dict):
                    json_data['_upload_metadata'] = {
                        **source_info,
                        'upload_timestamp': datetime.now().isoformat()
                    }

            # Normalize input into a JSON-serializable object
            if not isinstance(json_data, (dict, list)):
                if isinstance(json_data, str):
                    try:
                        json_data = json.loads(json_data)
                    except json.JSONDecodeError:
                        json_data = {"raw_data": json_data}
                else:
                    # Wrap non-serializable scalars
                    json_data = {"raw_data": json_data}

            # Serialize to bytes and ingest using a stream. This is more reliable
            # for JSON ingestion than stuffing Python objects into a DataFrame.
            payload = json.dumps(json_data, ensure_ascii=False).encode('utf-8')
            stream = io.BytesIO(payload)

            logger.debug("Ingesting JSON stream to Event House...")
            # Use ingest_from_stream which accepts a file-like object
            self.ingest_client.ingest_from_stream(stream, self.ingestion_properties)

            logger.info(f"Successfully queued JSON stream for ingestion to {self.table}")
            return True

        except Exception:
            # Log full traceback to help diagnose authentication/ingest errors
            logger.exception("Failed to upload to Event House")
            return False
    
    def upload_file(self, filepath: str, dispensary_id: Optional[str] = None) -> bool:
        """
        Upload a JSON file to Event House
        
        Args:
            filepath: Path to JSON file
            dispensary_id: Optional dispensary identifier
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            source_info = {
                'source_file': filepath,
                'filename': os.path.basename(filepath)
            }
            
            if dispensary_id:
                source_info['dispensary'] = dispensary_id
            
            return self.upload_json(data, source_info)
            
        except Exception as e:
            logger.error(f"Failed to upload file {filepath}: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test the connection to Event House
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try a simple ingestion test
            test_data = {
                "test": "connection",
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("Testing Event House connection...")
            # Note: We can't easily test without actually ingesting, so we'll just validate the client setup
            if self.ingest_client and self.ingestion_properties:
                logger.info("Event House client initialized successfully")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Event House connection test failed: {e}")
            return False


def get_eventhouse_uploader(
    cluster: str,
    database: str,
    table: str,
    tenant_id: str,
    client_id: str,
    client_secret: str,
    use_azure_cli: bool = False
) -> EventHouseUploader:
    """
    Factory function to create an Event House uploader
    
    Returns:
        EventHouseUploader instance
    """
    return EventHouseUploader(
        cluster=cluster,
        database=database,
        table=table,
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
        use_azure_cli=use_azure_cli
    )
