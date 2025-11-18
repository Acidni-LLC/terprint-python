from saveJsonToAzureDataLake import AzureDataLakeManager
import json
import subprocess
import time

def check_prerequisites():
    """Check if authentication and permissions are set up"""
    try:
        # Check Azure CLI login
        result = subprocess.run(["az", "account", "show"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Please run: az login")
            return False
        
        print("✅ Azure CLI authenticated")
        return True
        
    except Exception:
        print("❌ Azure CLI not available or not logged in")
        return False

def test_upload_with_retry():
    """Test upload with retry logic for permission propagation"""
    
    if not check_prerequisites():
        return False
    
    print("🚀 Loading MÜV products JSON...")
    
    # Load your MÜV products JSON
    try:
        with open(r"C:\Users\JamiesonGill\source\repos\Acidni-LLC\Terprint\muv_products.json", 'r') as f:
            muv_data = json.load(f)
        print(f"✅ Loaded JSON data ({len(json.dumps(muv_data))} characters)")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return False
    
    # Initialize Data Lake manager
    print("🔗 Connecting to Azure Data Lake...")
    dl_manager = AzureDataLakeManager("storageacidnidatamover", "jsonfiles")
    
    # Try upload with retries (permissions may need time to propagate)
    max_retries = 3
    retry_delay = 15  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"📤 Upload attempt {attempt + 1}/{max_retries}...")
            
            success = dl_manager.save_json_with_timestamp(muv_data, "muv_products")
            
            if success:
                print("✅ Successfully saved to Azure Data Lake!")
                
                # Try to set content type
                try:
                    dl_manager.set_content_properties(success, "application/json")
                    print("✅ Content type set to application/json")
                except Exception as e:
                    print(f"⚠️  Could not set content type: {e}")
                
                return True
            else:
                print(f"❌ Upload attempt {attempt + 1} failed")
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Upload attempt {attempt + 1} failed: {error_msg}")
            
            # Check for specific permission errors
            if "AuthorizationPermissionMismatch" in error_msg:
                print("🔐 Permission issue detected")
                
                if attempt == 0:
                    print("🔧 Attempting to fix permissions...")
                    # Try to assign permissions
                    try:
                        import fix_permissions
                        fix_success = fix_permissions.assign_storage_permissions()
                        if fix_success:
                            print("✅ Permissions assigned, retrying...")
                        else:
                            print("❌ Could not assign permissions automatically")
                    except ImportError:
                        print("⚠️  Run fix_permissions.py manually")
                
                if attempt < max_retries - 1:
                    print(f"⏳ Waiting {retry_delay} seconds for permission propagation...")
                    time.sleep(retry_delay)
            else:
                # For other errors, don't retry
                break
    
    print("💥 All upload attempts failed!")
    return False

if __name__ == "__main__":
    print("🔄 Testing Azure Data Lake upload with permission handling...")
    
    success = test_upload_with_retry()
    
    if not success:
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Run: python check_auth.py")
        print("2. Run: python fix_permissions.py") 
        print("3. Wait 5-10 minutes for permission propagation")
        print("4. Try this script again")
        print("\n📖 Manual permission assignment:")
        print("   • Go to Azure Portal > Storage Account > Access Control (IAM)")
        print("   • Add role assignment: 'Storage Blob Data Contributor'")
        print("   • Assign to your user account")