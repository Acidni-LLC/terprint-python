import requests
from msal import ConfidentialClientApplication
import json

# https://learn.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal?tabs=azure-portal

# --- CONFIGURATION ---
# #Savitas
client_id = "8cf359c9-690d-4d76-9dcf-c2e4dc71e975"
authority_url = "https://login.microsoftonline.com/fa959b35-58f5-4816-9511-a6ead495f2e5"
client_secret = "goj8Q~tXbST6NX58rNqrW-h9bBlPTOz2P1Tmxcx~"
workspace_id = "b264f22b-fe0d-415f-81ae-d81dea949918"  # Replace with your workspace ID
dataset_id = "9ab5c5c4-95d4-4902-9de0-74fc45ae7757"      # Replace with yowhere pythonur dataset ID
TENANT_ID = 'fa959b35-58f5-4816-9511-a6ead495f2e5'
CLIENT_ID = client_id
CLIENT_SECRET = client_secret
WORKSPACE_ID = workspace_id
DATASET_ID = dataset_id
# Acidni

# client_id = "7fb0cb5d-19e8-4de2-a636-0ebd1903d7b5"
# authority_url = "https://login.microsoftonline.com/3278dcb1-0a18-42e7-8acf-d3b5f8ae33cd"
# client_secret = "G3k8Q~inwFNyuAPbyPH9bkBGuA6KfLgj4qQDBaR."
# # https://app.powerbi.com/groups/bd4ce79f-9b33-4970-acbb-3a6fed220f16/datasets/1aa05732-eaaf-40b0-a6b2-3766025168e8/details?ctid=3278dcb1-0a18-42e7-8acf-d3b5f8ae33cd&experience=power-bi
# workspace_id = "bd4ce79f-9b33-4970-acbb-3a6fed220f16"  # Replace with your workspace ID
# dataset_id = "1aa05732-eaaf-40b0-a6b2-3766025168e8"      # Replace with yowhere pythonur dataset ID
# TENANT_ID = '3278dcb1-0a18-42e7-8acf-d3b5f8ae33cd'
# CLIENT_ID = client_id
# CLIENT_SECRET = client_secret
# WORKSPACE_ID = workspace_id
# DATASET_ID = dataset_id



# --- MSAL SETUP ---
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPE = ['https://analysis.windows.net/powerbi/api/.default']

app = ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

# --- Acquire Token ---
result = app.acquire_token_for_client(scopes=SCOPE)
if "access_token" not in result:
    raise Exception(f"Failed to get token: {result.get('error_description')}")

# --- Request Setup ---
url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/datasets/{DATASET_ID}/executeQueries"
headers = {
    'Authorization': f"Bearer {result['access_token']}",
    'Content-Type': 'application/json'
}
payload = {
    "queries": [
        {
            "query": "EVALUATE VALUES(sku 1)"
        }
    ],
    "serializerSettings": {
        "includeNulls": True
    },
    
}

# --- Send POST Request ---
response = requests.post(url, headers=headers, json=payload)

# --- Handle Response ---
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Error {response.status_code}: {response.text}")