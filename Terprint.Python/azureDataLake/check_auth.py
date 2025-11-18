"""
Check Azure authentication and permissions
"""
import subprocess
import json
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

def check_azure_cli():
    """Check Azure CLI authentication"""
    try:
        print("🔍 Checking Azure CLI authentication...")
        
        # Check if logged in
        result = subprocess.run(["az", "account", "show"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not logged into Azure CLI")
            print("   Run: az login")
            return False
        
        account_info = json.loads(result.stdout)
        print(f"✅ Logged into Azure CLI")
        print(f"   User: {account_info.get('user', {}).get('name', 'Unknown')}")
        print(f"   Subscription: {account_info.get('name', 'Unknown')}")
        print(f"   Tenant: {account_info.get('tenantId', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking Azure CLI: {e}")
        return False

def check_storage_permissions():
    """Check permissions on the storage account"""
    try:
        print("\n🔍 Checking storage account permissions...")
        
        storage_account = "storageacidnidatamover"
        
        # List role assignments
        cmd = f'az role assignment list --scope "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$(az storage account show -n {storage_account} --query resourceGroup -o tsv)/providers/Microsoft.Storage/storageAccounts/{storage_account}" --assignee "$(az account show --query user.name -o tsv)" --query "[].roleDefinitionName" -o tsv'
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            roles = result.stdout.strip().split('\n')
            print(f"✅ Found roles on storage account:")
            for role in roles:
                print(f"   • {role}")
            return True
        else:
            print(f"❌ No roles found on storage account: {storage_account}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking permissions: {e}")
        return False

def test_data_lake_connection():
    """Test basic Data Lake connection"""
    try:
        print("\n🔍 Testing Data Lake connection...")
        
        credential = DefaultAzureCredential()
        account_url = "https://storageacidnidatamover.dfs.core.windows.net"
        
        service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
        file_system_client = service_client.get_file_system_client("jsonfiles")
        
        # Try to list files (read permission)
        print("   Testing read permissions...")
        paths = list(file_system_client.get_paths(max_results=1))
        print("   ✅ Read permissions OK")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔐 AZURE AUTHENTICATION DIAGNOSTICS")
    print("="*50)
    
    cli_ok = check_azure_cli()
    
    if cli_ok:
        perms_ok = check_storage_permissions()
        conn_ok = test_data_lake_connection()
        
        if not perms_ok:
            print("\n🔧 PERMISSION FIX NEEDED:")
            print("Run this command to assign permissions:")
            print('az role assignment create \\')
            print('  --assignee "$(az account show --query user.name -o tsv)" \\')
            print('  --role "Storage Blob Data Contributor" \\')
            print('  --scope "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$(az storage account show -n storageacidnidatamover --query resourceGroup -o tsv)/providers/Microsoft.Storage/storageAccounts/storageacidnidatamover"')
    else:
        print("\n🔧 AUTHENTICATION FIX NEEDED:")
        print("Run: az login")