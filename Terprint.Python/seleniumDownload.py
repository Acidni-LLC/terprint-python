from selenium import webdriver
from selenium.webdriver.common.by import By

url="https://mete.labdrive.net/s/SfWBtnDxrN9qs2t/download/COA_2509CBR0194-005.pdf"
# Set up the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()

# Open the webpage
driver.get(url)

# Wait for the page to load and interact with it
content = driver.page_source

# Close the browser
driver.quit()

print(content)