"""
Script to help gather Azure Data Lake credentials and configuration
"""

def print_azure_info_guide():
    print("=== AZURE DATA LAKE SETUP GUIDE ===\n")
    
    print("1. STORAGE ACCOUNT INFORMATION:")
    print("   - Go to Azure Portal (portal.azure.com)")
    print("   - Navigate to 'Storage accounts'")
    print("   - Find your Data Lake Gen2 storage account")
    print("   - Copy the 'Storage account name' (e.g., 'mystorageaccount')")
    print("   - Note: Full URL will be: https://{account-name}.dfs.core.windows.net\n")
    
    print("2. CONTAINER/FILESYSTEM:")
    print("   - In your storage account, go to 'Containers' or 'Data Lake Storage' > 'Containers'")
    print("   - Copy the container name (e.g., 'data', 'raw-data', etc.)\n")
    
    print("3. AUTHENTICATION METHODS:")
    print("   Choose ONE of the following:\n")
    
    print("   OPTION A: Azure CLI (Easiest for development)")
    print("   - Install Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli")
    print("   - Run: az login")
    print("   - This will use your current Azure login\n")
    
    print("   OPTION B: Service Principal (Best for production)")
    print("   - Go to Azure Portal > Azure Active Directory > App registrations")
    print("   - Click 'New registration'")
    print("   - Give it a name (e.g., 'Terprint-DataLake-Access')")
    print("   - After creation, note:")
    print("     * Application (client) ID")
    print("     * Directory (tenant) ID")
    print("   - Go to 'Certificates & secrets' > 'New client secret'")
    print("   - Copy the secret value (you can't see it again!)")
    print("   - Go back to your Storage Account > Access Control (IAM)")
    print("   - Add role assignment: 'Storage Blob Data Contributor' to your app\n")
    
    print("   OPTION C: Managed Identity (For Azure VMs/Functions)")
    print("   - Enable managed identity on your Azure resource")
    print("   - Grant it 'Storage Blob Data Contributor' role on the storage account\n")

def create_config_template():
    """Create a configuration template file"""
    config_content = """# Azure Data Lake Configuration
# Update these values with your actual Azure information

# Storage Account Information
AZURE_STORAGE_ACCOUNT_NAME = "your-storage-account-name"  # e.g., "terprintdatalake"
AZURE_CONTAINER_NAME = "your-container-name"             # e.g., "raw-data" or "json-files"

# Authentication Method 1: Service Principal (Recommended for production)
AZURE_TENANT_ID = "your-tenant-id"                       # Directory (tenant) ID
AZURE_CLIENT_ID = "your-client-id"                       # Application (client) ID  
AZURE_CLIENT_SECRET = "your-client-secret"               # Client secret value

# Authentication Method 2: Azure CLI (For development)
# Just run 'az login' and set USE_AZURE_CLI = True
USE_AZURE_CLI = False

# File paths and naming
BASE_PATH = "dispensaries/muv"                           # Base folder in container
INCLUDE_DATE_FOLDERS = True                              # Create YYYY/MM/DD subfolders
"""
    
    with open("azure_config.py", "w") as f:
        f.write(config_content)
    
    print("4. CONFIGURATION FILE CREATED:")
    print("   - Created 'azure_config.py' template")
    print("   - Update the values in this file with your Azure information\n")

def test_azure_cli_login():
    """Test if Azure CLI is installed and logged in"""
    import subprocess
    import json
    
    try:
        # Check if Azure CLI is installed
        result = subprocess.run(["az", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Azure CLI is not installed")
            return False
        
        print("✅ Azure CLI is installed")
        
        # Check if logged in
        result = subprocess.run(["az", "account", "show"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not logged into Azure CLI. Run: az login")
            return False
        
        # Parse account info
        account_info = json.loads(result.stdout)
        print(f"✅ Logged into Azure CLI")
        print(f"   Account: {account_info.get('user', {}).get('name', 'Unknown')}")
        print(f"   Subscription: {account_info.get('name', 'Unknown')}")
        print(f"   Tenant: {account_info.get('tenantId', 'Unknown')}")
        
        return True
        
    except FileNotFoundError:
        print("❌ Azure CLI is not installed")
        return False
    except json.JSONDecodeError:
        print("❌ Error parsing Azure CLI output")
        return False
    except Exception as e:
        print(f"❌ Error checking Azure CLI: {e}")
        return False

def list_storage_accounts():
    """List storage accounts if Azure CLI is available"""
    import subprocess
    import json
    
    try:
        result = subprocess.run(
            ["az", "storage", "account", "list", "--query", "[].{Name:name, ResourceGroup:resourceGroup, Location:location}"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            accounts = json.loads(result.stdout)
            if accounts:
                print("📋 AVAILABLE STORAGE ACCOUNTS:")
                for account in accounts:
                    print(f"   Name: {account['Name']}")
                    print(f"   Resource Group: {account['ResourceGroup']}")
                    print(f"   Location: {account['Location']}")
                    print()
            else:
                print("No storage accounts found")
        else:
            print("Could not list storage accounts")
            
    except Exception as e:
        print(f"Error listing storage accounts: {e}")

if __name__ == "__main__":
    print_azure_info_guide()
    print("\n" + "="*60 + "\n")
    
    # Test Azure CLI
    print("TESTING AZURE CLI:")
    cli_available = test_azure_cli_login()
    
    if cli_available:
        print("\n" + "="*60 + "\n")
        list_storage_accounts()
    
    print("\n" + "="*60 + "\n")
    create_config_template()
    
    print("NEXT STEPS:")
    print("1. Update azure_config.py with your values")
    print("2. Run test_connection.py to verify setup")