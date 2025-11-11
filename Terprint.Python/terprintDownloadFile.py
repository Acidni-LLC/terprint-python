import os
import requests
import batchFromUrl
from bcolors import bcolors


def downloadfile(my_list,dispensaryid):
   
    batchescount = 1
    totalbatches = str(len(my_list))
    print(my_list.__len__())
    for item in my_list:
        printstring = f"{bcolors.OKBLUE} batch {bcolors.OKGREEN}  {str(batchescount)} {bcolors.ENDC}  of {bcolors.OKGREEN} {totalbatches} {item+bcolors.ENDC} {item+bcolors.ENDC}"
        print (printstring)
   
    # url = "https://mete.labdrive.net/s/8K4kMmg8nsTGFxt/download/COA_2510CBR0024-004.pdf"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        try: 
            batch = batchFromUrl.batch_from_url(item)
            local_path ='C:/Users/JamiesonGill/source/repos/Acidni-LLC/Terprint/Terprint.Python/files/test_output/'
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
            
                with open(local_path+local_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"File '{local_path+local_filename}' downloaded successfully.")
            
            batchescount=batchescount+1
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
    
            
my_list = [ 'WQiipC7sQpiyojx',
'FW3xYKXr7WnzAWq',
'gFAcXTRYpnfkSfk',
'g47exX3f769D7Np',
'6z63Dpn43BwkggY',
'QpgabPXJzZM7StD',
'g852X8ybqn7w2pL',
'LngeNzi2cfXKMiX',
'33k3sMwNY5TKXTg',
'Ay2ZkZyeQNDjyfa',
'LicBAKgsBwt5GMd',
'6DMQwXFGMqs8zX5',
'rbbr8Ep3qAoPj5y',
'cZLTKTn3yTTJe7P',
'SnFSY86MjSfXyB8',
'gbxxJoq4GqJcnLw',
'SfWBtnDxrN9qs2t',
'czKcWBWzTDyCPdT',
'8K4kMmg8nsTGFxt',
'sGgQEA54cQ3Y9JW',
'rqrTmqqezwBGipR',
'SrGCCkbd2AobjjY',
'JPqWAsffRt99ySJ',
'nP7REAQ5aQ4RYW2',
'jKdbRbwgKFijRtc',
'eWDcrrGNLEmzbs9',
'meg9ZNWmCGESgsC',
'dnyP2drMTRyw87E',
'gZYK5idR4KdJqma',
'L4As3WZDmB5H5y3',
'3qmgeWwcKYRrawa',
'fmNHWqZYycqDAgd',
'n75eWwYNjSbYEqJ',
'DGCc8Jw2HGRKzNx',
'iTCbmGmZEW2KYFw',
'n4MkEi4Afr5bLZZ',
'dB6rS35dyT8pKkS',
'wErCYb5e5NDYAqP',
'QCcQmpq5e7cF3zW',
'DNkcJ3BkcEiSg2b',
'bRRiF8TxnFb7E7A',
'pHX6bxL7C5yFWme',
'8Dp8nq5QiTbAzrC',
'Yad7LeWTiqZc3Jm',
'je5X9ECWdoC6w4o',
'NgBasfHjWkQecKP',
'XF4zAKoQj8yCx3p',
'j5XgcqBirTe85nG',
'zpyWAj3mMeADHCt',
'dfA63am93BqkAeR',
'ABbmjHwkrRK5F4e',
'iCm33pB7LjWnd5q',
'zDF5f7E6ggrca73',
'4REmwgHG6A5fwcL',
'9yWQQm4aaRsgHNa',
'LF66JqZy3mMr4wy',
'r87Bi5xrLPpCSfo',
'xCZ57p6SmP4GkFP',
'dS6zKbP9cGmtNEY',
'y8YBxxsizxsCHRE',
'AfCP8Lj3XkzHems',
'REYxZB8sRQ4KwKG',
'NJiRDgnPDYBtAnX',
'ERHxaFsjM9pyotE',
'KTcZ6JgHdpqoAEx',
'5RzcEb3k8B4ALo4',
'dxDjCKX2xmAwYtW',
'6T5P2wJxs4sBAR4',
'mj6WiyWX8HiAFxE',
'cZLTKTn3yTTJe7P',
'eWDcrrGNLEmzbs9',
'meg9ZNWmCGESgsC',
'dnyP2drMTRyw87E',
'pHX6bxL7C5yFWme',
'8Dp8nq5QiTbAzrC',
'gZYK5idR4KdJqma',
'AfCP8Lj3XkzHems',
'REYxZB8sRQ4KwKG',
'NJiRDgnPDYBtAnX',
'ERHxaFsjM9pyotE',
'KTcZ6JgHdpqoAEx',
'5RzcEb3k8B4ALo4',
'dxDjCKX2xmAwYtW',
'6T5P2wJxs4sBAR4',
'mj6WiyWX8HiAFxE']


local_filename = "COA_2509CBR0194-005.pdf"
url="https://mete.labdrive.net/s/SfWBtnDxrN9qs2t/download/COA_2509CBR0194-005.pdf"

# Define 'item' with the appropriate value before using it


downloadfile(my_list,2)
