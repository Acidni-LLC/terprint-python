import requests
from bs4 import BeautifulSoup

# URL of the webpage containing the download link
webpage_url = "https://mete.labdrive.net/s/Ay2ZkZyeQNDjyfa" 

# Fetch the webpage content
response = requests.get(webpage_url)
response.raise_for_status() # Raise an exception for bad status codes

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find the download link (adjust selector as needed)
# Example: finding a link with specific text or class
download_link_tag = soup.find('a',attrs={'class': 'primary button'}) 
# Or, if the link has a specific attribute:
# download_link_tag = soup.find('a', {'id': 'download-button'})

if download_link_tag:
    file_url = download_link_tag['href']
    # If the href is a relative path, you might need to construct the full URL
    # from urllib.parse import urljoin
    # file_url = urljoin(webpage_url, file_url)
    print("Download link found:", file_url)
    coa = file_url.split('download/')[-1]
    print("File name:", coa)
    batch = coa.split('.')[0]
    print("Batch name:", batch)
else:
    print("Download link not found on the page.")
    file_url = None