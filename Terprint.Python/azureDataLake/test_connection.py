"""
Test Azure Data Lake connection and credentials
"""
import sys
import os
from datetime import datetime

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from azure_config import *
    config_loaded = True
except ImportError:
    print("❌ azure_config.py not found. Run get_azure_info.py first.")
    config_loaded = False

def test_connection():
    if not config_loaded:
        return False
    
    try:
        from azure.storage.filedatalake import DataLakeServiceClient
        from azure.identity import DefaultAzureCredential, ClientSecretCredential
        
        print("Testing Azure Data Lake connection...\n")
        
        # Choose authentication method
        if USE_AZURE_CLI:
            print("🔐 Using Azure CLI authentication")
            credential = DefaultAzureCredential()
        else:
            print("🔐 Using Service Principal authentication")
            if not all([AZURE_TENANT_ID != "your-tenant-id", 
                       AZURE_CLIENT_ID != "your-client-id",
                       AZURE_CLIENT_SECRET != "your-client-secret"]):
                print("❌ Please update Service Principal credentials in azure_config.py")
                return False
            
            credential = ClientSecretCredential(
                tenant_id=AZURE_TENANT_ID,
                client_id=AZURE_CLIENT_ID,
                client_secret=AZURE_CLIENT_SECRET
            )
        
        # Test storage account name
        if AZURE_STORAGE_ACCOUNT_NAME == "your-storage-account-name":
            print("❌ Please update AZURE_STORAGE_ACCOUNT_NAME in azure_config.py")
            return False
        
        if AZURE_CONTAINER_NAME == "your-container-name":
            print("❌ Please update AZURE_CONTAINER_NAME in azure_config.py")
            return False
        
        # Create service client
        account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net"
        service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
        
        print(f"📡 Connecting to: {account_url}")
        print(f"📁 Container: {AZURE_CONTAINER_NAME}")
        
        # Test connection by getting filesystem client
        file_system_client = service_client.get_file_system_client(file_system=AZURE_CONTAINER_NAME)
        
        # Try to list paths to verify access
        print("🔍 Testing access...")
        paths = list(file_system_client.get_paths(max_results=5))
        
        print("✅ Connection successful!")
        print(f"📊 Found {len(paths)} items in container")
        
        if paths:
            print("📄 Sample files/folders:")
            for i, path in enumerate(paths[:3]):
                file_type = "📁 Folder" if path.is_directory else "📄 File"
                print(f"   {file_type}: {path.name}")
        
        # Test write permission with a small test file
        test_data = {
            "test": True,
            "timestamp": datetime.now().isoformat(),
            "message": "Connection test successful"
        }
        
        test_path = f"test/connection_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            import json
            file_client = file_system_client.get_file_client(test_path)
            file_client.upload_data(
                data=json.dumps(test_data, indent=2),
                overwrite=True
            )
            print(f"✅ Write test successful: {test_path}")
            
            # Clean up test file
            file_client.delete_file()
            print("🧹 Test file cleaned up")
            
        except Exception as e:
            print(f"⚠️  Write test failed: {e}")
            print("   (Read access works, but write access may be limited)")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        
        # Provide specific error guidance
        error_str = str(e).lower()
        if "authentication" in error_str or "unauthorized" in error_str:
            print("\n💡 Authentication issue. Try:")
            print("   1. Run 'az login' if using Azure CLI")
            print("   2. Check Service Principal credentials")
            print("   3. Verify permissions on the storage account")
        elif "not found" in error_str:
            print("\n💡 Resource not found. Check:")
            print("   1. Storage account name is correct")
            print("   2. Container name exists")
            print("   3. You have access to the subscription")
        elif "network" in error_str or "timeout" in error_str:
            print("\n💡 Network issue. Check:")
            print("   1. Internet connection")
            print("   2. Firewall settings")
            print("   3. VPN if required")
        
        return False

def show_current_config():
    if not config_loaded:
        return
    
    print("CURRENT CONFIGURATION:")
    print(f"  Storage Account: {AZURE_STORAGE_ACCOUNT_NAME}")
    print(f"  Container: {AZURE_CONTAINER_NAME}")
    print(f"  Auth Method: {'Azure CLI' if USE_AZURE_CLI else 'Service Principal'}")
    print(f"  Base Path: {BASE_PATH}")
    print(f"  Date Folders: {INCLUDE_DATE_FOLDERS}")
    print()

if __name__ == "__main__":
    if config_loaded:
        show_current_config()
    
    success = test_connection()
    
    if success:
        print("\n🎉 Setup complete! You can now use the Data Lake integration.")
    else:
        print("\n🔧 Please fix the issues above and try again.")
        print("   Run get_azure_info.py for setup guidance.")