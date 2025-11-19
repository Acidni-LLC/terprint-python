import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path to import from menus folder
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the comprehensive debug functions
try:
    from menuTrulieveDebug import (
        test_all_store_configurations, 
        test_specific_config, 
        get_full_product_data,
        STORE_CATEGORY_CONFIG,
        parse_store_config
    )
    print("✅ Successfully imported comprehensive Trulieve debug functions")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure menuTrulieveDebug.py exists in the same directory")
    sys.exit(1)

def collect_all_store_data():
    """Collect data from ALL store/category configurations and combine into one file"""
    
    print("🏪 COLLECTING DATA FROM ALL TRULIEVE STORES")
    print("="*60)
    
    configs = parse_store_config()
    all_store_data = {
        "collection_timestamp": datetime.now().isoformat(),
        "total_stores_attempted": len(configs),
        "successful_stores": 0,
        "failed_stores": 0,
        "stores": {},
        "combined_products": [],
        "summary": {
            "total_products": 0,
            "stores_by_category": {},
            "working_configurations": [],
            "failed_configurations": []
        }
    }
    
    print(f"📋 Testing {len(configs)} store/category combinations:")
    for config in configs:
        print(f"   - {config['config']}")
    
    print("\n" + "="*60)
    print("🚀 STARTING DATA COLLECTION...")
    
    for i, config in enumerate(configs, 1):
        store_id = config['store_id']
        category_id = config['category_id']
        config_name = config['config']
        
        print(f"\n[{i}/{len(configs)}] Collecting: {config_name}")
        print("-" * 50)
        
        # Test if this configuration works
        test_result = test_single_store_quick(store_id, category_id)
        
        if test_result and test_result.get('success'):
            print(f"   ✅ Store working - getting full data...")
            
            # Get full product data
            full_data = get_full_product_data(store_id, category_id, page_size=100)
            
            if full_data and 'data' in full_data and 'products' in full_data['data']:
                products_info = full_data['data']['products']
                items = products_info.get('items', [])
                total_count = products_info.get('total_count', 0)
                
                print(f"   📦 Retrieved {len(items)} products (of {total_count} total)")
                
                # Add store data
                all_store_data['stores'][config_name] = {
                    "store_id": store_id,
                    "category_id": category_id,
                    "success": True,
                    "products_retrieved": len(items),
                    "products_total": total_count,
                    "data": full_data
                }
                
                # Add products to combined list with store info
                for product in items:
                    product_with_store = product.copy()
                    product_with_store['_store_info'] = {
                        "store_id": store_id,
                        "category_id": category_id,
                        "config_name": config_name
                    }
                    all_store_data['combined_products'].append(product_with_store)
                
                # Update summary
                all_store_data['successful_stores'] += 1
                all_store_data['summary']['total_products'] += len(items)
                all_store_data['summary']['working_configurations'].append(config_name)
                
                # Track by category
                if category_id not in all_store_data['summary']['stores_by_category']:
                    all_store_data['summary']['stores_by_category'][category_id] = []
                all_store_data['summary']['stores_by_category'][category_id].append({
                    "store_id": store_id,
                    "config": config_name,
                    "products": len(items)
                })
                
                print(f"   ✅ SUCCESS - {len(items)} products added to collection")
            else:
                print(f"   ❌ Failed to get full product data")
                all_store_data['failed_stores'] += 1
                all_store_data['summary']['failed_configurations'].append(config_name)
                all_store_data['stores'][config_name] = {
                    "store_id": store_id,
                    "category_id": category_id,
                    "success": False,
                    "error": "Failed to retrieve product data"
                }
        else:
            print(f"   ❌ Store configuration not working")
            all_store_data['failed_stores'] += 1
            all_store_data['summary']['failed_configurations'].append(config_name)
            all_store_data['stores'][config_name] = {
                "store_id": store_id,
                "category_id": category_id,
                "success": False,
                "error": "Store configuration failed"
            }
    
    return all_store_data

def test_single_store_quick(store_id, category_id):
    """Quick test of a single store/category combination"""
    
    import requests
    
    url = "https://www.trulieve.com/api/graphql"
    
    headers = {
        "Cookie": f"store_id={store_id}",
        "Store": store_id,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    # Quick test query
    query = """
    query products($searchCriteria:[SearchCriteriaInput!]!,$pageSize:Int=5,$currentPage:Int=1){
        products(searchCriteria:$searchCriteria pageSize:$pageSize currentPage:$currentPage){
            total_count
            items{
                id 
                name 
                sku
            }
        }
    }
    """
    
    variables = {
        "currentPage": 1,
        "pageSize": 5,
        "searchCriteria": [
            {
                "attribute_code": "category_uid",
                "filter_action": "EQ",
                "filter_value": category_id
            }
        ]
    }
    
    body = {
        "query": query,
        "operationName": "products",
        "variables": variables
    }
    
    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if 'data' in result and result['data'] and 'products' in result['data']:
                products = result['data']['products']
                total_count = products.get('total_count', 0)
                if total_count > 0:
                    return {"success": True, "total_count": total_count}
        
        return {"success": False}
        
    except Exception:
        return {"success": False}

def save_combined_data(all_store_data):
    """Save the combined data to files"""
    
    print(f"\n💾 SAVING COMBINED DATA...")
    print("="*40)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save complete combined file
    combined_filename = f"trulieve_all_stores_combined_{timestamp}.json"
    try:
        with open(combined_filename, "w", encoding='utf-8') as f:
            json.dump(all_store_data, f, indent=2, ensure_ascii=False)
        
        file_size = os.path.getsize(combined_filename)
        print(f"✅ Complete data saved to: {combined_filename}")
        print(f"   📏 File size: {file_size:,} bytes")
    except Exception as e:
        print(f"❌ Failed to save complete file: {e}")
        return False
    
    # Save products-only file (for easier analysis)
    products_filename = f"trulieve_products_only_{timestamp}.json"
    try:
        products_only = {
            "collection_timestamp": all_store_data["collection_timestamp"],
            "total_products": len(all_store_data["combined_products"]),
            "working_stores": all_store_data["successful_stores"],
            "summary": all_store_data["summary"],
            "products": all_store_data["combined_products"]
        }
        
        with open(products_filename, "w", encoding='utf-8') as f:
            json.dump(products_only, f, indent=2, ensure_ascii=False)
        
        file_size = os.path.getsize(products_filename)
        print(f"✅ Products-only data saved to: {products_filename}")
        print(f"   📏 File size: {file_size:,} bytes")
    except Exception as e:
        print(f"❌ Failed to save products file: {e}")
    
    # Save summary report
    summary_filename = f"trulieve_summary_report_{timestamp}.json"
    try:
        summary_report = {
            "collection_timestamp": all_store_data["collection_timestamp"],
            "total_stores_attempted": all_store_data["total_stores_attempted"],
            "successful_stores": all_store_data["successful_stores"],
            "failed_stores": all_store_data["failed_stores"],
            "total_products_collected": all_store_data["summary"]["total_products"],
            "working_configurations": all_store_data["summary"]["working_configurations"],
            "failed_configurations": all_store_data["summary"]["failed_configurations"],
            "stores_by_category": all_store_data["summary"]["stores_by_category"],
            "store_performance": {
                store: {
                    "success": data["success"],
                    "products": data.get("products_retrieved", 0) if data["success"] else 0
                }
                for store, data in all_store_data["stores"].items()
            }
        }
        
        with open(summary_filename, "w", encoding='utf-8') as f:
            json.dump(summary_report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Summary report saved to: {summary_filename}")
    except Exception as e:
        print(f"❌ Failed to save summary: {e}")
    
    return True

def print_collection_summary(all_store_data):
    """Print a detailed summary of the data collection"""
    
    print(f"\n📊 COLLECTION SUMMARY")
    print("="*60)
    
    print(f"🏪 Stores Attempted: {all_store_data['total_stores_attempted']}")
    print(f"✅ Successful: {all_store_data['successful_stores']}")
    print(f"❌ Failed: {all_store_data['failed_stores']}")
    print(f"📦 Total Products: {all_store_data['summary']['total_products']}")
    
    if all_store_data['summary']['working_configurations']:
        print(f"\n✅ WORKING CONFIGURATIONS:")
        for config in all_store_data['summary']['working_configurations']:
            store_data = all_store_data['stores'][config]
            products = store_data.get('products_retrieved', 0)
            print(f"   {config} - {products} products")
    
    if all_store_data['summary']['failed_configurations']:
        print(f"\n❌ FAILED CONFIGURATIONS:")
        for config in all_store_data['summary']['failed_configurations']:
            print(f"   {config}")
    
    # Category breakdown
    print(f"\n📋 BY CATEGORY:")
    for category, stores in all_store_data['summary']['stores_by_category'].items():
        total_products = sum(store['products'] for store in stores)
        print(f"   {category}: {len(stores)} stores, {total_products} total products")
        for store in stores:
            print(f"     - {store['config']}: {store['products']} products")

def run_comprehensive_collection():
    """Run comprehensive data collection from all stores"""
    
    print("🚀 COMPREHENSIVE TRULIEVE DATA COLLECTION")
    print("="*60)
    
    # Collect all store data
    all_store_data = collect_all_store_data()
    
    # Print summary
    print_collection_summary(all_store_data)
    
    # Save data
    save_success = save_combined_data(all_store_data)
    
    if save_success and all_store_data['successful_stores'] > 0:
        print(f"\n🎉 COLLECTION SUCCESSFUL!")
        print(f"✅ Collected data from {all_store_data['successful_stores']} stores")
        print(f"📦 Total products: {all_store_data['summary']['total_products']}")
        print("\nFiles created:")
        print("- Complete combined data file")
        print("- Products-only file") 
        print("- Summary report")
        print("\n🚀 Ready for Azure Data Lake upload!")
        return True
    else:
        print(f"\n❌ COLLECTION FAILED")
        print("No working store configurations found")
        return False

if __name__ == "__main__":
    # Run comprehensive collection
    success = run_comprehensive_collection()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. Review the generated JSON files")
        print("2. Update Azure upload script with combined data")
        print("3. Upload to Azure Data Lake")
        print("4. Set up automated collection schedule")
    else:
        print("\n🔧 TROUBLESHOOTING NEEDED:")
        print("1. Check network connectivity")
        print("2. Verify store IDs and category IDs")
        print("3. Check if API requirements have changed")