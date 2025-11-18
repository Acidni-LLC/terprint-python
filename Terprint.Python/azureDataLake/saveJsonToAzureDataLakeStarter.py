from saveJsonToAzureDataLake import AzureDataLakeManager
import json

# Load your MÜV products JSON
with open(r"C:\Users\JamiesonGill\source\repos\Acidni-LLC\Terprint\muv_products.json", 'r') as f:
    muv_data = json.load(f)

# Initialize and save
dl_manager = AzureDataLakeManager("your_storage_account", "your_container")
success = dl_manager.save_json_with_timestamp(muv_data, "muv_products")

if success:
    print("Successfully saved to Azure Data Lake!")
else:
    print("Failed to save to Azure Data Lake")