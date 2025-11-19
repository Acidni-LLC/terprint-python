"""
Upload Trulieve products data to Azure Data Lake
"""
import sys
import os
import json

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from azure_config import *
    from saveJsonToAzureDataLake import AzureDataLakeManager, get_credential_from_service_principal
    config_loaded = True
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    config_loaded = False

def upload_trulieve_products():
    """Upload Trulieve products JSON to Azure Data Lake"""
    
    if not config_loaded:
        return False
    
    print("🚀 TRULIEVE TO AZURE DATA LAKE UPLOAD")
    print("="*50)
    
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
        
        # Find the Trulieve products file in the trulieve subdirectory
        trulieve_files = []
        trulieve_dir = os.path.join(current_dir, "..", "menus", "trulieve")
        
        if not os.path.exists(trulieve_dir):
            print(f"❌ Trulieve directory not found: {trulieve_dir}")
            return False
        
        print(f"📂 Looking for Trulieve files in: {trulieve_dir}")
        
        # Look for Trulieve JSON files in the trulieve directory
        for file in os.listdir(trulieve_dir):
            if file.startswith("trulieve_") and file.endswith(".json"):
                file_path = os.path.join(trulieve_dir, file)
                trulieve_files.append(file_path)
                print(f"   Found: {file}")
        
        if not trulieve_files:
            print("❌ No Trulieve JSON files found")
            print(f"   Looking in: {trulieve_dir}")
            return False
        
        # Use the most recent file
        latest_file = max(trulieve_files, key=os.path.getmtime)
        print(f"📂 Using latest file: {os.path.basename(latest_file)}")
        
        # Load Trulieve data
        with open(latest_file, 'r', encoding='utf-8') as f:
            trulieve_data = json.load(f)
        
        # Show file info
        data_str = json.dumps(trulieve_data)
        print(f"✅ Loaded {len(data_str):,} characters")
        
        if 'products' in trulieve_data:
            products = trulieve_data['products']
            print(f"📦 Found {len(products)} products")
            
            # Show sample product info
            if products:
                sample = products[0]
                store_info = sample.get('_store_info', {})
                print(f"📋 Sample: {sample.get('name', 'No name')}")
                print(f"🏪 Store: {store_info.get('store_id', 'Unknown')}")
                print(f"📂 Category: {store_info.get('category_id', 'Unknown')}")
        
        # Initialize Data Lake manager
        print(f"🔗 Connecting to: {AZURE_STORAGE_ACCOUNT_NAME}")
        dl_manager = AzureDataLakeManager(
            account_name=AZURE_STORAGE_ACCOUNT_NAME,
            container_name=AZURE_CONTAINER_NAME,
            credential=credential
        )
        
        # Test connection
        print("🔍 Testing connection...")
        container_info = dl_manager.get_container_info()
        if container_info:
            print(f"✅ Connected to container: {container_info['name']}")
        else:
            print("❌ Could not connect to container")
            return False
        
        # Generate file path for Trulieve data
        file_path = get_file_path("trulieve_products.json", "trulieve")
        print(f"📤 Uploading to: {file_path}")
        
        # Ensure the directory exists
        directory_path = "/".join(file_path.split("/")[:-1])  # Remove filename
        if directory_path:
            print(f"📁 Ensuring directory exists: {directory_path}")
            dl_manager.ensure_directory_exists(directory_path)
        
        # Upload file
        success = dl_manager.save_json_to_data_lake(trulieve_data, file_path)
        
        if success:
            print("✅ Upload successful!")
            
            # Set content type
            try:
                dl_manager.set_content_properties(file_path, "application/json")
                print("✅ Content type set to application/json")
            except Exception as e:
                print(f"⚠️  Could not set content type: {e}")
            
            # Verify the uploaded file exists
            try:
                if dl_manager.file_exists(file_path):
                    print(f"✅ Confirmed file exists: {file_path}")
                else:
                    print(f"⚠️  File check failed: {file_path}")
            except Exception as e:
                print(f"⚠️  Could not verify file: {e}")
            
            # List files to verify
            try:
                print("\n📁 Files in container:")
                
                # List root files
                print("   Checking root directory...")
                root_files = dl_manager.list_files("")
                if root_files:
                    print("   Root files found:")
                    for file in root_files[:5]:
                        print(f"     📄 {file}")
                
                # List trulieve directory
                print("   Checking trulieve directory...")
                try:
                    trulieve_files = dl_manager.list_files("trulieve")
                    if trulieve_files:
                        print("   Trulieve directory files:")
                        for file in trulieve_files:
                            print(f"     📄 {file}")
                    else:
                        print("   📁 trulieve directory exists but may be empty")
                except Exception:
                    print("   📁 trulieve directory structure may still be propagating...")
                
            except Exception as e:
                print(f"⚠️  Could not list files: {e}")
            
            # Show summary
            print("\n📊 UPLOAD SUMMARY")
            print("="*30)
            if 'products' in trulieve_data:
                print(f"📦 Products uploaded: {len(trulieve_data['products'])}")
            if 'successful_stores' in trulieve_data:
                print(f"🏪 Stores: {trulieve_data['successful_stores']}")
            print(f"📁 Azure path: {file_path}")
            print(f"🕒 Timestamp: {trulieve_data.get('timestamp', 'Unknown')}")
            
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

def upload_specific_trulieve_file(file_path):
    """Upload a specific Trulieve JSON file to Azure Data Lake"""
    
    if not config_loaded:
        return False
    
    print(f"🚀 UPLOADING SPECIFIC TRULIEVE FILE")
    print(f"File: {file_path}")
    print("="*50)
    
    # Check if it's a relative path and make it absolute
    if not os.path.isabs(file_path):
        # Check if it's just a filename, look in trulieve directory
        if os.path.basename(file_path) == file_path:
            trulieve_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "menus", "trulieve")
            file_path = os.path.join(trulieve_dir, file_path)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        
        # Show available files in trulieve directory
        trulieve_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "menus", "trulieve")
        if os.path.exists(trulieve_dir):
            print(f"\n📂 Available files in {trulieve_dir}:")
            for file in os.listdir(trulieve_dir):
                if file.endswith('.json'):
                    print(f"   📄 {file}")
        
        return False
    
    # Validate configuration
    if not validate_config():
        return False
    
    try:
        # Create credential
        if USE_AZURE_CLI:
            credential = None
        else:
            credential = get_credential_from_service_principal(
                tenant_id=AZURE_TENANT_ID,
                client_id=AZURE_CLIENT_ID,
                client_secret=AZURE_CLIENT_SECRET
            )
        
        # Load the file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Loaded file: {os.path.basename(file_path)}")
        
        # Initialize Data Lake manager
        dl_manager = AzureDataLakeManager(
            account_name=AZURE_STORAGE_ACCOUNT_NAME,
            container_name=AZURE_CONTAINER_NAME,
            credential=credential
        )
        
        # Test connection
        container_info = dl_manager.get_container_info()
        if not container_info:
            print("❌ Could not connect to container")
            return False
        
        # Generate Azure path
        filename = os.path.basename(file_path)
        azure_file_path = get_file_path(filename, "trulieve")
        
        # Upload
        success = dl_manager.save_json_to_data_lake(data, azure_file_path)
        
        if success:
            print(f"✅ Upload successful!")
            print(f"📁 Azure path: {azure_file_path}")
            return True
        else:
            print("❌ Upload failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def list_available_trulieve_files():
    """List all available Trulieve JSON files"""
    
    trulieve_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "menus", "trulieve")
    
    if not os.path.exists(trulieve_dir):
        print(f"❌ Trulieve directory not found: {trulieve_dir}")
        return []
    
    json_files = []
    print(f"📂 Trulieve files in {trulieve_dir}:")
    
    for file in sorted(os.listdir(trulieve_dir)):
        if file.endswith('.json'):
            file_path = os.path.join(trulieve_dir, file)
            file_size = os.path.getsize(file_path)
            file_time = os.path.getmtime(file_path)
            
            from datetime import datetime
            time_str = datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"   📄 {file}")
            print(f"      Size: {file_size:,} bytes")
            print(f"      Modified: {time_str}")
            
            json_files.append(file)
    
    return json_files

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Upload Trulieve products to Azure Data Lake')
    parser.add_argument('--file', '-f', help='Specific file to upload (can be just filename if in trulieve directory)')
    parser.add_argument('--list', '-l', action='store_true', help='List available Trulieve files')
    args = parser.parse_args()
    
    if args.list:
        # List available files
        list_available_trulieve_files()
    elif args.file:
        # Upload specific file
        success = upload_specific_trulieve_file(args.file)
    else:
        # Upload latest Trulieve products file
        success = upload_trulieve_products()
    
    if not args.list:
        if success:
            print("\n🎉 TRULIEVE UPLOAD SUCCESS!")
            print("Your Trulieve products data is now in Azure Data Lake!")
            print("\n🔗 Next steps:")
            print("1. Verify data in Azure Storage Explorer")
            print("2. Connect Power BI to the new data source")
            print("3. Set up automated data refresh schedule")
        else:
            print("\n❌ UPLOAD FAILED")
            print("\n🔧 Troubleshooting:")
            print("1. Check azure_config.py credentials")
            print("2. Run permission fix script if needed")
            print("3. Verify network connectivity")
            print("4. Use --list to see available files")
            print("5. Use --file filename.json to upload specific file")