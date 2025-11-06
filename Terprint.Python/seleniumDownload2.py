from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

local_filename = "COA_2509CBR0194-005.pdf"
url="https://mete.labdrive.net/s/SfWBtnDxrN9qs2t/download/COA_2509CBR0194-005.pdf"
# Set up ChromeOptions for headless mode (optional)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless") # Run in headless mode

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.get(url) # Replace with your URL

    # Example: Find a download button and click it
    download_button = driver.find_element(By.CSS_SELECTOR, 'primary button')
    download_button.click()

    # You might need to wait for the download to complete or handle file saving
    # ...

finally:
    driver.quit()