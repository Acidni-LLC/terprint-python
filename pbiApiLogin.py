import msal
from bcolors import bcolors

def get_token_for_client(scope):
 client_id = "8cd148e2-a21e-4522-9180-541c6b10f955"
 authority_url = "https://login.microsoftonline.com/fa959b35-58f5-4816-9511-a6ead495f2e5"
 client_secret = ""
 app = msal.ConfidentialClientApplication(client_id,authority=authority_url,client_credential=client_secret)
 result = app.acquire_token_for_client(scopes=scope)
 if 'access_token' in result:
  return(result['access_token'])
 else:
  print(bcolors.FAIL + 'Error in get_token_username_password:' + result.get("error") + " " + result.get("error_description") + bcolors.ENDC)

scope =['https://analysis.windows.net/powerbi/api/.default']
token = get_token_for_client(scope)
print(bcolors.OKGREEN + token + bcolors.ENDC)
