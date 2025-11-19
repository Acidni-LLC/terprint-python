import requests
import json
import os

# Store and category configuration from your config file
STORE_CATEGORY_CONFIG = [
    "palatka:MjEy",
    "palm_coast:MjEy", 
    "st_augustine_a1a:MjEy",
    "st_augustine_two:MjEy",
    "palm_coast_sr100:MjEy",
    "palatka:MjA4",
    "palm_coast:MjA4",
    "st_augustine_a1a:MjA4",
    "st_augustine_two:MjA4",
    "palm_coast_sr100:MjA4",
    "jacksonville_southside:MjA4",
    "jacksonville_beach:MjA4",
    "jacksonville_arrowhead:MjA4",
    "jacksonville_baymeadows:MjA4",
    "daytona_beach:MjA4",
    "port_orange:MjA4",
    "oakland_park:MjA4"
]

def parse_store_config():
    """Parse the store:category configuration"""
    configs = []
    for config in STORE_CATEGORY_CONFIG:
        store_id, category_id = config.split(":")
        configs.append({
            "store_id": store_id,
            "category_id": category_id,
            "config": config
        })
    return configs

def test_single_store_category(store_id, category_id, config_name):
    """Test a single store/category combination"""
    
    url = "https://www.trulieve.com/api/graphql"
    
    print(f"🏬 Testing: {config_name}")
    print(f"   Store ID: {store_id}")
    print(f"   Category ID: {category_id}")
    
    headers = {
        "Cookie": f"store_id={store_id}",
        "Store": store_id,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    # Simplified GraphQL query for testing
    query = """
    query products($searchCriteria:[SearchCriteriaInput!]!,$pageSize:Int=10,$currentPage:Int=1,$sort:ProductAttributeSortInput={}){
        products(searchCriteria:$searchCriteria pageSize:$pageSize currentPage:$currentPage sort:$sort){
            __typename
            total_count
            page_info{
                __typename 
                total_pages 
                current_page
            }
            items{
                __typename 
                id 
                name 
                sku
                stock_status
                price_range{
                    __typename 
                    minimum_price{
                        __typename 
                        regular_price{
                            __typename 
                            value
                        }
                        final_price{
                            __typename 
                            value
                        }
                    }
                }
                categories{
                    name 
                    url_path
                }
            }
        }
    }
    """
    
    variables = {
        "currentPage": 1,
        "pageSize": 10,  # Small number for testing
        "searchCriteria": [
            {
                "attribute_code": "category_uid",
                "filter_action": "EQ",
                "filter_value": category_id
            }
        ],
        "sort": {}
    }
    
    body = {
        "query": query,
        "operationName": "products",
        "variables": variables
    }
    
    try:
        response = requests.post(url, headers=headers, json=body, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'data' in result and result['data'] and 'products' in result['data']:
                products = result['data']['products']
                total_count = products.get('total_count', 0)
                items = products.get('items', [])
                
                if total_count > 0 or len(items) > 0:
                    print(f"   ✅ SUCCESS! Found {total_count} products ({len(items)} in response)")
                    
                    if items:
                        sample = items[0]
                        print(f"   📋 Sample: {sample.get('name', 'No name')}")
                        print(f"   🏷️ SKU: {sample.get('sku', 'No SKU')}")
                        categories = sample.get('categories', [])
                        if categories:
                            cat_names = [cat.get('name', 'No name') for cat in categories]
                            print(f"   🏪 Categories: {', '.join(cat_names)}")
                    
                    return {
                        "success": True,
                        "store_id": store_id,
                        "category_id": category_id,
                        "config": config_name,
                        "total_count": total_count,
                        "items_count": len(items),
                        "data": result
                    }
                else:
                    print(f"   ⚠️ No products found")
            else:
                print(f"   ❌ Invalid response structure")
                if 'errors' in result:
                    print(f"   🚨 GraphQL Errors: {result['errors']}")
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text[:100]}")
            
        return {"success": False, "store_id": store_id, "category_id": category_id, "config": config_name}
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {"success": False, "store_id": store_id, "category_id": category_id, "config": config_name, "error": str(e)}

def test_all_store_configurations():
    """Test all store/category configurations from your config file"""
    
    print("🚀 TESTING ALL TRULIEVE STORE CONFIGURATIONS")
    print("="*60)
    
    configs = parse_store_config()
    results = []
    successful_configs = []
    
    print(f"📋 Found {len(configs)} configurations to test:")
    for config in configs:
        print(f"   - {config['config']}")
    
    print("\n" + "="*60)
    print("🧪 STARTING TESTS...")
    
    for i, config in enumerate(configs, 1):
        print(f"\n[{i}/{len(configs)}] Testing: {config['config']}")
        print("-" * 40)
        
        result = test_single_store_category(
            config['store_id'], 
            config['category_id'], 
            config['config']
        )
        
        results.append(result)
        
        if result['success']:
            successful_configs.append(result)
    
    # Summary report
    print("\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)
    
    successful_count = len(successful_configs)
    total_count = len(results)
    
    print(f"✅ Successful: {successful_count}/{total_count}")
    print(f"❌ Failed: {total_count - successful_count}/{total_count}")
    
    if successful_configs:
        print(f"\n🎉 WORKING CONFIGURATIONS:")
        print("-" * 30)
        for config in successful_configs:
            print(f"✅ {config['config']} - {config['total_count']} products")
        
        # Save the first working configuration for further use
        best_config = successful_configs[0]
        print(f"\n🎯 RECOMMENDED CONFIGURATION:")
        print(f"   Store ID: {best_config['store_id']}")
        print(f"   Category ID: {best_config['category_id']}")
        print(f"   Configuration: {best_config['config']}")
        print(f"   Products Available: {best_config['total_count']}")
        
        # Save working response
        try:
            with open("trulieve_working_response.json", "w") as f:
                json.dump(best_config['data'], f, indent=2)
            print(f"💾 Saved working response to 'trulieve_working_response.json'")
        except Exception as e:
            print(f"⚠️ Could not save response: {e}")
        
        return best_config
    else:
        print(f"\n❌ NO WORKING CONFIGURATIONS FOUND")
        print("All store/category combinations failed.")
        print("\nPossible issues:")
        print("- API endpoint has changed")
        print("- Authentication requirements have changed") 
        print("- Store IDs or category IDs are incorrect")
        print("- Network/firewall restrictions")
        
        return None

def test_specific_config(config_string):
    """Test a specific store:category configuration"""
    
    print(f"🎯 TESTING SPECIFIC CONFIGURATION: {config_string}")
    print("="*50)
    
    try:
        store_id, category_id = config_string.split(":")
        result = test_single_store_category(store_id, category_id, config_string)
        
        if result['success']:
            print(f"\n✅ SUCCESS!")
            print(f"Configuration {config_string} is working!")
            return result
        else:
            print(f"\n❌ FAILED!")
            print(f"Configuration {config_string} did not work.")
            return None
            
    except ValueError:
        print(f"❌ Invalid configuration format. Expected 'store_id:category_id'")
        return None

def get_full_product_data(store_id, category_id, page_size=100):
    """Get full product data for a working configuration"""
    
    url = "https://www.trulieve.com/api/graphql"
    
    print(f"📦 GETTING FULL PRODUCT DATA")
    print(f"Store: {store_id}, Category: {category_id}")
    print("-" * 40)
    
    headers = {
        "Cookie": f"store_id={store_id}",
        "Store": store_id,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    # Full GraphQL query with all the fields from your Power BI query
    query = '''query products($searchCriteria:[SearchCriteriaInput!]!,$pageSize:Int=100,$currentPage:Int=1,$sort:ProductAttributeSortInput={}){
        products(searchCriteria:$searchCriteria pageSize:$pageSize currentPage:$currentPage sort:$sort){
            aggregations{
                __typename 
                attribute_code 
                count 
                label 
                options{
                    __typename 
                    count 
                    label 
                    value
                }
            }
            __typename 
            sort_fields{
                __typename 
                default 
                options{
                    __typename 
                    label 
                    value
                }
            }
            items{
                __typename 
                id 
                name 
                stock_status 
                custom_attributes_product{
                    label 
                    code 
                    value
                }
                last_chance 
                opps_promo{
                    promo_id 
                    promo_name
                }
                price_range{
                    __typename 
                    minimum_price{
                        __typename 
                        regular_price{
                            __typename 
                            value
                        }
                        final_price{
                            __typename 
                            value
                        }
                        discount{
                            __typename 
                            amount_off
                        }
                    }
                }
                sku 
                small_image{
                    __typename 
                    url
                }
                url_key 
                categories{
                    name 
                    url_path
                }
                ... on ConfigurableProduct{
                    configurable_options{
                        __typename 
                        attribute_code 
                        label 
                        values{
                            __typename 
                            value_index 
                            label 
                            uid 
                            swatch_data{
                                __typename 
                                value
                                ... on ImageSwatchData{
                                    thumbnail 
                                    __typename
                                }
                            }
                        }
                    }
                    variants{
                        __typename 
                        attributes{
                            __typename 
                            code 
                            value_index 
                            label 
                            uid
                        }
                        product{
                            __typename 
                            id 
                            small_image{
                                __typename 
                                url
                            }
                            price_range{
                                __typename 
                                minimum_price{
                                    __typename 
                                    regular_price{
                                        __typename 
                                        value
                                    }
                                    final_price{
                                        __typename 
                                        value
                                    }
                                    discount{
                                        __typename 
                                        amount_off
                                    }
                                }
                            }
                        }
                        sku 
                        stock_status 
                        thc_percentage 
                        dominant_terpene 
                        dominant_terpene_percentage 
                        secondary_terpene 
                        secondary_terpene_percentage 
                        terciary_terpene 
                        terciary_terpene_percentage 
                        total_terpene_percentage
                    }
                    __typename
                }
            }
            page_info{
                __typename 
                total_pages 
                current_page
            }
            total_count
        }
    }'''
    
    variables = {
        "currentPage": 1,
        "pageSize": page_size,
        "searchCriteria": [
            {
                "attribute_code": "category_uid",
                "filter_action": "EQ",
                "filter_value": category_id
            }
        ],
        "sort": {}
    }
    
    body = {
        "query": query,
        "operationName": "products",
        "variables": variables
    }
    
    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'data' in result and result['data'] and 'products' in result['data']:
                products = result['data']['products']
                total_count = products.get('total_count', 0)
                items = products.get('items', [])
                
                print(f"✅ Retrieved {len(items)} products out of {total_count} total")
                
                if items:
                    sample = items[0]
                    print(f"📋 Sample product: {sample.get('name', 'No name')}")
                    print(f"🏷️ SKU: {sample.get('sku', 'No SKU')}")
                    
                    # Check for terpene data
                    if 'variants' in sample and sample['variants']:
                        variant = sample['variants'][0]
                        thc = variant.get('thc_percentage', 'N/A')
                        terpenes = variant.get('total_terpene_percentage', 'N/A')
                        print(f"🌿 THC: {thc}%, Terpenes: {terpenes}%")
                
                return result
            else:
                print(f"❌ Invalid response structure")
                return None
        else:
            print(f"❌ HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Legacy function aliases for backward compatibility
def debug_trulieve_api_palm_coast():
    """Legacy function - now tests palm_coast:MjEy configuration"""
    return test_specific_config("palm_coast:MjEy")

def test_palm_coast_variations():
    """Legacy function - now tests all Palm Coast configurations"""
    palm_coast_configs = [config for config in STORE_CATEGORY_CONFIG if config.startswith("palm_coast")]
    
    print("🏬 TESTING ALL PALM COAST CONFIGURATIONS")
    print("="*40)
    
    for config in palm_coast_configs:
        result = test_specific_config(config)
        if result:
            return result['data']
    
    return None

if __name__ == "__main__":
    print("🚀 TRULIEVE API TESTER")
    print("="*60)
    
    print("\nSelect testing mode:")
    print("1. Test all configurations (recommended)")
    print("2. Test specific configuration")
    print("3. Test all Palm Coast configurations")
    print("4. Get full product data for working config")
    
    choice = input("\nEnter choice (1-4) or press Enter for option 1: ").strip()
    
    if choice == "2":
        config_input = input("Enter store:category configuration (e.g., palm_coast:MjEy): ").strip()
        if config_input:
            test_specific_config(config_input)
        else:
            print("No configuration provided")
    
    elif choice == "3":
        test_palm_coast_variations()
    
    elif choice == "4":
        store_input = input("Enter store ID: ").strip()
        category_input = input("Enter category ID: ").strip()
        if store_input and category_input:
            result = get_full_product_data(store_input, category_input)
            if result:
                filename = f"trulieve_{store_input}_{category_input}_full.json"
                with open(filename, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"💾 Saved full data to {filename}")
        else:
            print("Store ID and Category ID required")
    
    else:  # Default to option 1
        working_config = test_all_store_configurations()
        
        if working_config:
            print(f"\n🎉 READY FOR INTEGRATION!")
            print(f"Use store_id='{working_config['store_id']}' and category_id='{working_config['category_id']}'")
        else:
            print(f"\n🔧 NO WORKING CONFIGURATIONS")
            print("Need to investigate API requirements")