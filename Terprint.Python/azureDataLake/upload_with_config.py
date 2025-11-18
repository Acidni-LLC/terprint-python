"""
Upload to Azure Data Lake using azure_config.py settings
"""
import sys
import os
import json

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from azure_config import *
    from saveJsonToAzureDataLake import AzureDataLakeManager, get_credential_from_service_principal
    config_loaded = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    config_loaded = False

def upload_muv_data():
    """Upload MÜV data using configuration from azure_config.py"""
    
    if not config_loaded:
        return False
    
    print("🚀 AZURE DATA LAKE UPLOAD")
    print("="*30)
    
    # Validate configuration
    if not validate_config():
        return False
    
    try:
        # Create credential based on config
        if USE_AZURE_CLI:
            print("🔐 Using Azure CLI authentication...")
            credential = None  # Will use DefaultAzureCredential
        else:
            print("🔐 Using Service Principal authentication...")
            credential = get_credential_from_service_principal(
                tenant_id=AZURE_TENANT_ID,
                client_id=AZURE_CLIENT_ID,
                client_secret=AZURE_CLIENT_SECRET
            )
        
        # Load JSON data
        json_path = r"C:\Users\JamiesonGill\source\repos\Acidni-LLC\Terprint\muv_products.json"
        print(f"📂 Loading JSON from: {json_path}")
        
        if not os.path.exists(json_path):
            print(f"❌ File not found: {json_path}")
            return False
        
        with open(json_path, 'r', encoding='utf-8') as f:
            muv_data = json.load(f)
        
        print(f"✅ Loaded {len(json.dumps(muv_data))} characters")
        
        # Initialize Data Lake manager
        print(f"🔗 Connecting to: {AZURE_STORAGE_ACCOUNT_NAME}")
        dl_manager = AzureDataLakeManager(
            account_name=AZURE_STORAGE_ACCOUNT_NAME,
            container_name=AZURE_CONTAINER_NAME,
            credential=credential
        )
        
        # Generate file path using config
        file_path = get_file_path("muv_products.json", "muv")
        print(f"📤 Uploading to: {file_path}")
        
        # Upload file
        success = dl_manager.save_json_to_data_lake(muv_data, file_path)
        
        if success:
            print("✅ Upload successful!")
            
            # Set content type
            try:
                dl_manager.set_content_properties(file_path, "application/json")
                print("✅ Content type set to application/json")
            except Exception as e:
                print(f"⚠️  Could not set content type: {e}")
            
            # List some files to verify
            try:
                print("\n📁 Recent files in container:")
                files = dl_manager.list_files("muv")
                for file in files[-5:]:  # Show last 5 files
                    print(f"   📄 {file}")
            except Exception as e:
                print(f"⚠️  Could not list files: {e}")
            
            return True
        else:
            print("❌ Upload failed")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Provide guidance based on error type
        error_str = str(e).lower()
        if "authorization" in error_str or "forbidden" in error_str:
            print("\n🔧 Permission issue detected!")
            print("   Run: python fix_permissions.py")
        elif "authentication" in error_str:
            print("\n🔧 Authentication issue!")
            print("   Check your credentials in azure_config.py")
        elif "not found" in error_str:
            print("\n🔧 Resource not found!")
            print("   Check storage account and container names in azure_config.py")
        
        return False

if __name__ == "__main__":
    success = upload_muv_data()
    
    if not success:
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Update azure_config.py with your credentials")
        print("2. Run: python fix_permissions.py")
        print("3. Wait a few minutes for permissions to propagate")
        print("4. Try this script again")