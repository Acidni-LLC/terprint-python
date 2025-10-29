import requests

# Replace with your values
workspace_id = "your_workspace_id"
eventhouse_id = "your_eventhouse_id"
access_token = "your_access_token"

url = f"https://api.fabric.microsoft.com/eventhouse/{workspace_id}/{eventhouse_id}/items"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Rows retrieved successfully!")
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
