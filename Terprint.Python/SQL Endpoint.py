##SQL Endpoint

from azure.identity import InteractiveBrowserCredential
import requests
import json

# Acquire a token
# DO NOT USE IN PRODUCTION.
# Below code to acquire token is for development purpose only to test the GraphQL endpoint
# For production, always register an application in a Microsoft Entra ID tenant and use the appropriate client_id and scopes
# https://learn.microsoft.com/en-us/fabric/data-engineering/connect-apps-api-graphql#create-a-microsoft-entra-app

app = InteractiveBrowserCredential()
scp = 'https://analysis.windows.net/powerbi/api/user_impersonation'
result = app.get_token(scp)

if not result.token:
    print('Error:', "Could not get access token")

# Prepare headers
headers = {
    'Authorization': f'Bearer {result.token}',
    'Content-Type': 'application/json'
}

endpoint = 'https://8924d1b786b445db883f591262eaffee.z89.graphql.fabric.microsoft.com/v1/workspaces/8924d1b7-86b4-45db-883f-591262eaffee/graphqlapis/a68c4c2c-ecc4-4b13-8ff4-3bcd07376433/graphql'
query = """
    query {
  inverterEnergyInfos(first: 10) {
     items {
        id
        deviceId
        energyProduced
        timestamp
     }
  }
}
"""

variables = {

  }
  

# Issue GraphQL request
try:
    response = requests.post(endpoint, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=4))
except Exception as error:
    print(f"Query failed with error: {error}")
