"""
Fix Azure Data Lake permissions
"""
import subprocess
import json

def assign_storage_permissions():
    """Assign Storage Blob Data Contributor role"""
    try:
        print("🔧 ASSIGNING STORAGE PERMISSIONS")
        print("="*40)
        
        storage_account = "storageacidnidatamover"
        
        print(f"🎯 Target storage account: {storage_account}")
        
        # Get current user
        user_result = subprocess.run(["az", "account", "show", "--query", "user.name", "-o", "tsv"], 
                                   capture_output=True, text=True)
        if user_result.returncode != 0:
            print("❌ Failed to get current user")
            return False
        
        user_name = user_result.stdout.strip()
        print(f"👤 Current user: {user_name}")
        
        # Get subscription ID
        sub_result = subprocess.run(["az", "account", "show", "--query", "id", "-o", "tsv"], 
                                  capture_output=True, text=True)
        subscription_id = sub_result.stdout.strip()
        
        # Get resource group
        rg_result = subprocess.run([
            "az", "storage", "account", "show", 
            "-n", storage_account, 
            "--query", "resourceGroup", 
            "-o", "tsv"
        ], capture_output=True, text=True)
        
        if rg_result.returncode != 0:
            print(f"❌ Storage account '{storage_account}' not found or no access")
            return False
        
        resource_group = rg_result.stdout.strip()
        print(f"📁 Resource group: {resource_group}")
        
        # Build scope
        scope = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Storage/storageAccounts/{storage_account}"
        
        print(f"\n🔐 Assigning 'Storage Blob Data Contributor' role...")
        
        # Assign role
        role_result = subprocess.run([
            "az", "role", "assignment", "create",
            "--assignee", user_name,
            "--role", "Storage Blob Data Contributor", 
            "--scope", scope
        ], capture_output=True, text=True)
        
        if role_result.returncode == 0:
            print("✅ Permissions assigned successfully!")
            
            # Wait a moment for propagation
            print("⏳ Waiting for permissions to propagate...")
            import time
            time.sleep(10)
            
            return True
        else:
            print(f"❌ Failed to assign permissions: {role_result.stderr}")
            
            # Check if already assigned
            if "already exists" in role_result.stderr.lower():
                print("ℹ️  Role already assigned - checking existing permissions...")
                return True
            
            return False
            
    except Exception as e:
        print(f"❌ Error assigning permissions: {e}")
        return False

def verify_permissions():
    """Verify the assigned permissions"""
    try:
        print(f"\n🔍 Verifying permissions...")
        
        # List role assignments for current user on the storage account
        list_result = subprocess.run([
            "az", "role", "assignment", "list",
            "--assignee", "$(az account show --query user.name -o tsv)",
            "--scope", f"/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$(az storage account show -n storageacidnidatamover --query resourceGroup -o tsv)/providers/Microsoft.Storage/storageAccounts/storageacidnidatamover",
            "--query", "[].{Role:roleDefinitionName, Scope:scope}",
            "-o", "table"
        ], shell=True, capture_output=True, text=True)
        
        if list_result.returncode == 0:
            print("📋 Current role assignments:")
            print(list_result.stdout)
            return True
        else:
            print("❌ Could not verify permissions")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying permissions: {e}")
        return False

if __name__ == "__main__":
    success = assign_storage_permissions()
    
    if success:
        verify_permissions()
        print("\n🎉 Permission setup complete!")
        print("🧪 Now try running your upload script again.")
    else:
        print("\n💥 Permission setup failed!")
        print("\n🔧 Manual steps:")
        print("1. Go to Azure Portal")
        print("2. Navigate to your storage account: storageacidnidatamover")
        print("3. Go to Access Control (IAM)")
        print("4. Add role assignment: 'Storage Blob Data Contributor'")
        print("5. Assign to your user account")