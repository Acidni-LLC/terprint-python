import msal
from pbipy import PowerBI, datasets, groups
import requests2
from bcolors import bcolors

#https://learn.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal?tabs=azure-portal
2
def get_token_for_client(scope):
 client_id = "de9598fc-7ece-4da1-8df7-20d9b4f9ad81" #TerprintPrincipal
 #client_id = "8cf359c9-690d-4d76-9dcf-c2e4dc71e975" #terprint2
 authority_url = "https://login.microsoftonline.com/3278dcb1-0a18-42e7-8acf-d3b5f8ae33cd"
 client_secret = "icJ8Q~1Zl9upHqQsXNYyJ_Oxaz1GYyTjklNnbaAl" #TerprintPrincipal
 #client_secret="DoI8Q~2lmPcLBzy6-i52kLAPV.kK5DGVvQFFCbfO" #terprint2
 app = msal.ConfidentialClientApplication(client_id,authority=authority_url,client_credential=client_secret)
 result = app.acquire_token_for_client(scopes=scope)
 if 'access_token' in result:
  return(result['access_token'])
 else:
  print(bcolors.FAIL + 'Error in get_token_username_password:' + result.get("error") + " " + result.get("error_description") + bcolors.ENDC)

scope =['https://analysis.windows.net/powerbi/api/.default']
bearer_token =''
bearer_token = get_token_for_client(scope)
print(bcolors.OKGREEN + str(bearer_token) + bcolors.ENDC +'\n')

# # Example: Get datasets in a workspace
# url = "https://app.powerbi.com/groups/b264f22b-fe0d-415f-81ae-d81dea949918/datasets"
# headers = {"Authorization": f"Bearer {bearer_token}"}

# response = requests.get(url, headers=headers)
# print('\n'+str(response.json())+'\n')

pbi = PowerBI(bearer_token)
workspace_id = "bd4ce79f-9b33-4970-acbb-3a6fed220f16"  # Replace with your workspace ID
#
dataset_id = "1aa05732-eaaf-40b0-a6b2-3766025168e8"      # Replace with your dataset ID
# Example: List datasets in a workspace
datasets = pbi.datasets(group=workspace_id)
dataset = pbi.dataset(dataset_id,workspace_id)
for dataset in datasets:
 print(dataset)

dataset = pbi.dataset(dataset_id,workspace_id)

print(dataset.raw)

# Authenticate with Power BI (ensure you have set up authentication properly)
# Removed PowerBIClient() since it's not defined; use PowerBI instance 'pbi' instead.

# Specify the workspace (group) and dataset ID

# API endpoint to get dataset records
url = f"https://api.fabric.microsoft.com/eventhouse/{workspace_id}/{dataset_id}/items"

headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Rows retrieved successfully!")
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")


