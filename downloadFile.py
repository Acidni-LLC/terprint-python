import os
import requests
import batchFromUrl
from bcolors import bcolors


def downloadfile(my_list,dispensaryid):
   
    batchescount = 1
    totalbatches = str(len(my_list))
    print(my_list.__len__())
    for item in my_list:
        print (bcolors.OKBLUE+"batch "+ bcolors.OKGREEN+  str(batchescount) +bcolors.ENDC + " of " +bcolors.OKGREEN+   totalbatches + item+bcolors.ENDC+ item+bcolors.ENDC)
   
    # url = "https://mete.labdrive.net/s/8K4kMmg8nsTGFxt/download/COA_2510CBR0024-004.pdf"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        try: 
            batch = batchFromUrl.batch_from_url(item)
            local_path ='C:/Users/JamiesonGill/source/repos/Terprint/test_output/'
            local_filename =  batch + ".pdf"
            if os.path.exists(local_filename):
                print(f"File '{batch}' already exists.")
            # continue
                # If you want to redownload the file even if it exists, set redownload to 1
                # redownload = 1
            else:
                print(f"File '{batch}' does not exist. It will be downloaded.")
                missingfile = 1
                url="https://mete.labdrive.net/s/"+item+"/download/"+batch +".pdf"
                print (url)
                response = requests.get(url, headers=headers, stream=True, timeout=10)  # Use stream=True for large files
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            
                with open(local_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"File '{local_path}' downloaded successfully.")
            
            batchescount=batchescount+1
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
    

my_list = ["gbxxJoq4GqJcnLw","3LpRC3Ckz5XjF6w","L4As3WZDmB5H5y3","WQiipC7sQpiyojx","czKcWBWzTDyCPdT","8K4kMmg8nsTGFxt","3qmgeWwcKYRrawa","fmNHWqZYycqDAgd","n75eWwYNjSbYEqJ","DGCc8Jw2HGRKzNx","g47exX3f769D7Np","6z63Dpn43BwkggY","QpgabPXJzZM7StD","iTCbmGmZEW2KYFw","sGgQEA54cQ3Y9JW","rqrTmqqezwBGipR","SrGCCkbd2AobjjY","n4MkEi4Afr5bLZZ","g852X8ybqn7w2pL","dB6rS35dyT8pKkS","wErCYb5e5NDYAqP","QCcQmpq5e7cF3zW","DNkcJ3BkcEiSg2b","33k3sMwNY5TKXTg","Ay2ZkZyeQNDjyfa","nP7REAQ5aQ4RYW2","6DMQwXFGMqs8zX5","bRRiF8TxnFb7E7A","cZLTKTn3yTTJe7P","eWDcrrGNLEmzbs9","meg9ZNWmCGESgsC","dnyP2drMTRyw87E","pHX6bxL7C5yFWme","8Dp8nq5QiTbAzrC","gZYK5idR4KdJqma"]


local_filename = "COA_2509CBR0194-005.pdf"
url="https://mete.labdrive.net/s/SfWBtnDxrN9qs2t/download/COA_2509CBR0194-005.pdf"

# Define 'item' with the appropriate value before using it


downloadfile(my_list,2)
