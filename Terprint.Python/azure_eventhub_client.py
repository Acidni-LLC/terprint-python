# filepath suggestion: c:\Users\JamiesonGill\source\repos\Acidni-LLC\Terprint\Terprint.Python\azure_eventhub_client.py
from typing import Optional
import os
import json
from azure.eventhub import EventData, EventHubProducerClient
from azure.eventhub.exceptions import EventHubError

# If you use your COA class:
from COAMethodDataExtractor import COA

def _get_conn_info(conn_env: str = "EVENTHUB_CONN_STR", hub_env: str = "EVENTHUB_NAME"):
    conn_str = os.getenv(conn_env)
    hub_name = os.getenv(hub_env)
    if not conn_str or not hub_name:
        raise RuntimeError(f"Missing env var(s): {conn_env} or {hub_env}")
    return conn_str, hub_name

def send_json_to_eventhub(
    json_text: str,
    conn_str_env: str = "EVENTHUB_CONN_STR",
    hub_name_env: str = "EVENTHUB_NAME",
    partition_key: Optional[str] = None,
) -> None:
    """
    Send a JSON string to Azure Event Hubs (sync).
    - json_text: JSON payload text (should be UTF-8)
    - read connection string & hub name from env vars by default
    - partition_key: optional partition key for ordering
    """
    conn_str, hub_name = _get_conn_info(conn_str_env, hub_name_env)

    producer = EventHubProducerClient.from_connection_string(conn_str, eventhub_name=hub_name)
    try:
        # Create a batch and add the event (producer will auto-split large batches)
        with producer:
            event_data = EventData(json_text)
            # You can add metadata as properties if desired:
            # event_data.properties = {"source": "Terprint", "type": "coa"}
            event_batch = producer.create_batch(partition_key=partition_key)
            # If payload exceeds batch limits producer.create_batch + add may raise ValueError.
            try:
                event_batch.add(event_data)
            except ValueError:
                # payload too large for single event-batch; fallback: send single EventData without batch
                # (rare: Event Hubs limits event size; consider storing large payload in blob and sending pointer)
                producer.send_batch([event_data])
            else:
                producer.send_batch(event_batch)
    except EventHubError as ex:
        # handle Azure EventHub specific errors
        raise
    finally:
        producer.close()


def send_coa_to_eventhub(
    coa: COA,
    conn_str_env: str = "EVENTHUB_CONN_STR",
    hub_name_env: str = "EVENTHUB_NAME",
    partition_key: Optional[str] = None,
) -> None:
    """
    Convert COA to JSON and send to Event Hubs.
    Uses COA.to_json() if present, otherwise uses to_dict().
    """
    # Prefer COA.to_json() if available
    if hasattr(coa, "to_json"):
        json_text = coa.to_json()
    else:
        payload = getattr(coa, "to_dict", None)
        if callable(payload):
            json_text = json.dumps(payload())
        else:
            # last resort: serialize __dict__
            json_text = json.dumps(coa.__dict__, default=str)

    send_json_to_eventhub(json_text, conn_str_env=conn_str_env, hub_name_env=hub_name_env, partition_key=partition_key)