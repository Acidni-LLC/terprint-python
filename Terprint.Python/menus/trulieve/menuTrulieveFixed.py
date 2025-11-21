import requests
import json
import os
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

class TrulieveAPIClient:
    """Automated Trulieve API client using working browser request format"""
    
    def __init__(self, default_store_id="palm_coast"):
        self.base_url = "https://www.trulieve.com/api/graphql"
        self.default_store_id = default_store_id
        self.session = requests.Session()
        
        # Use the exact headers from the working browser request
        self.session.headers.update({
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "checkouttype": "pickup",
            "priority": "u=1, i",
            "referer": "https://www.trulieve.com/category/flower",
            "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
            "x-pylot-backend": "trulieve_prod",
            "x-pylot-query": "products"
        })
        
        # Base cookies - we'll update store-specific ones as needed
        self.base_cookies = {
            "trulieve_fe_url": "true",
            "trulieve_fe_cluster": "live",
            "state_name": "FL",
            "checkouttype": "pickup"
        }
    
    def set_store(self, store_id):
        """Set the store ID for requests"""
        self.session.headers["store"] = store_id
        
        # Update cookies with store ID
        cookies = self.base_cookies.copy()
        cookies["store_id"] = store_id
        
        # Convert cookies to cookie string
        cookie_string = "; ".join([f"{k}={v}" for k, v in cookies.items()])
        self.session.headers["cookie"] = cookie_string
    
    def get_products_url_encoded(self, store_id=None, category_uid=None, page_size=50, current_page=1):
        """Get products using URL-encoded GET request like the browser"""
        
        if store_id:
            self.set_store(store_id)
        elif self.default_store_id:
            self.set_store(self.default_store_id)
        
        # Build search criteria
        search_criteria = []
        if category_uid and category_uid.strip():
            search_criteria.append({
                "attribute_code": "category_uid",
                "filter_action": "EQ",
                "filter_value": category_uid
            })
        
        # GraphQL query (matching the working browser request)
        query = """
        query products($searchCriteria:[SearchCriteriaInput!]!,$pageSize:Int=50,$currentPage:Int=1,$sort:ProductAttributeSortInput={}){
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
                    available_quantity
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
        }
        """
        
        # Variables (matching the working browser request)
        variables = {
            "currentPage": current_page,
            "pageSize": page_size,
            "searchCriteria": search_criteria,
            "sort": {}
        }
        
        # URL encode the parameters like the browser does
        params = {
            "query": query,
            "operationName": "products",
            "variables": json.dumps(variables)
        }
        
        try:
            print(f"    Debug: Making GET request to GraphQL endpoint")
            print(f"    Debug: store_id={store_id}, category_uid={category_uid}")
            print(f"    Debug: page_size={page_size}, search_criteria={search_criteria}")
            
            # Use GET request like the browser
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=30
            )
            
            print(f"    Debug: Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"    Debug: Response keys: {list(result.keys())}")
                
                if 'data' in result and result['data'] and 'products' in result['data']:
                    products = result['data']['products']
                    print(f"    Debug: Products keys: {list(products.keys()) if products else 'None'}")
                    return products
                elif 'errors' in result:
                    print(f"    GraphQL errors: {result['errors']}")
                    return None
                else:
                    print(f"    Unexpected response structure: {result}")
                    return None
            else:
                print(f"    HTTP error {response.status_code}: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"    Error getting products: {e}")
            import traceback
            print(f"    Traceback: {traceback.format_exc()}")
            return None
    
    def get_all_products_for_store(self, store_id, category_uid=None, max_pages=20):
        """Get all products for a store across all pages"""
        
        all_products = []
        current_page = 1
        total_pages = 1
        
        while current_page <= total_pages and current_page <= max_pages:
            print(f"  Fetching page {current_page}...")
            
            products_data = self.get_products_url_encoded(
                store_id=store_id,
                category_uid=category_uid,
                current_page=current_page,
                page_size=50  # Updated to 50
            )
            
            if products_data and isinstance(products_data, dict):
                # Update total pages
                page_info = products_data.get('page_info', {})
                if page_info:
                    total_pages = page_info.get('total_pages', 1)
                    print(f"    Total pages: {total_pages}")
                
                # Add items
                items = products_data.get('items', [])
                if items:
                    all_products.extend(items)
                    print(f"    Got {len(items)} products")
                else:
                    print(f"    No items in response")
                
                current_page += 1
            else:
                print(f"    Failed to get page {current_page}")
                break
        
        print(f"  Total collected: {len(all_products)} products")
        return all_products

# Store configurations from your config file
# Set DEV_MODE = True to use only test stores, False for all stores
DEV_MODE = os.getenv('TRULIEVE_DEV_MODE', 'false').lower() == 'true'

# Development test stores (for faster testing)
DEV_STORE_CATEGORY_CONFIG = [
    "palatka:MjA4",
    "palm_coast_sr100:MjA4"
    "palm_coast:MjA4",
    "st_augustine_a1a:MjA4",
    "st_augustine_two:MjA4"
]

# Production - all store configurations
PROD_STORE_CATEGORY_CONFIG = [
    "palatka:MjA4",
    "palm_coast:MjA4", 
    "st_augustine_a1a:MjA4",
    "st_augustine_two:MjA4",
    "palm_coast_sr100:MjA4",
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
    "oakland_park:MjA4",
    "palatka:MjM3",
    "palm_coast:MjM3", 
    "st_augustine_a1a:MjM3",
    "st_augustine_two:MjM3",
    "palm_coast_sr100:MjM3",
    "palatka:MjM3",
    "palm_coast:MjM3",
    "st_augustine_a1a:MjM3",
    "st_augustine_two:MjM3",
    "palm_coast_sr100:MjM3",
    "jacksonville_southside:MjM3",
    "jacksonville_beach:MjM3",
    "jacksonville_arrowhead:MjM3",
    "jacksonville_baymeadows:MjM3",
    "daytona_beach:MjM3",
    "port_orange:MjM3",
    "oakland_park:MjM3"
]

# Select configuration based on mode
STORE_CATEGORY_CONFIG = DEV_STORE_CATEGORY_CONFIG if DEV_MODE else PROD_STORE_CATEGORY_CONFIG

def test_browser_format():
    """Test using the exact browser request format"""
    
    print("🧪 TESTING BROWSER FORMAT")
    print("="*40)
    
    client = TrulieveAPIClient()
    
    # Test the specific working example from your browser
    print("\n🎯 Testing palm_coast:MjA3 (from browser example)")
    print("-" * 40)
    
    # Use the exact parameters from the working browser request
    products = client.get_products_url_encoded(
        store_id="palm_coast",
        category_uid="MjA3",  # This was in your working browser request
        page_size=50,  # Updated to 50
        current_page=1
    )
    
    if products:
        total_count = products.get('total_count', 0)
        items = products.get('items', [])
        
        print(f"✅ SUCCESS! Found {total_count} total products")
        print(f"📦 Retrieved {len(items)} products in this page")
        
        if items:
            sample = items[0]
            print(f"📋 Sample product: {sample.get('name', 'No name')}")
            print(f"🏷️  SKU: {sample.get('sku', 'No SKU')}")
            print(f"💰 Price: {sample.get('price_range', {}).get('minimum_price', {}).get('final_price', {}).get('value', 'No price')}")
            
            # Check for terpene data
            if 'variants' in sample and sample['variants']:
                variant = sample['variants'][0]
                thc = variant.get('product', {}).get('thc_percentage', 'N/A')
                terpenes = variant.get('product', {}).get('total_terpene_percentage', 'N/A')
                print(f"🌿 THC: {thc}%, Terpenes: {terpenes}%")
        
        return True
    else:
        print("❌ Failed to get products with browser format")
        return False

def collect_all_trulieve_data_browser_format(dev_mode=None):
    """Collect data using the browser request format
    
    Args:
        dev_mode: Override DEV_MODE setting. True for dev stores only, False for all stores, None to use env setting
    """
    
    print("🚀 COLLECTING TRULIEVE DATA (BROWSER FORMAT)")
    print("="*60)
    
    # Determine which config to use
    if dev_mode is not None:
        use_dev = dev_mode
        config_list = DEV_STORE_CATEGORY_CONFIG if dev_mode else PROD_STORE_CATEGORY_CONFIG
    else:
        use_dev = DEV_MODE
        config_list = STORE_CATEGORY_CONFIG
    
    mode_name = "DEVELOPMENT" if use_dev else "PRODUCTION"
    print(f"📋 MODE: {mode_name} ({len(config_list)} store/category combinations)")
    
    client = TrulieveAPIClient()
    
    # First test the known working configuration
    if not test_browser_format():
        print("❌ Browser format test failed, stopping")
        return None
    
    all_store_data = {
        "collection_timestamp": datetime.now().isoformat(),
        "stores": {},
        "combined_products": [],
        "summary": {
            "total_products": 0,
            "successful_stores": 0,
            "failed_stores": 0,
            "working_configurations": [],
            "failed_configurations": []
        }
    }
    
    print(f"\n🏪 Processing {len(config_list)} store configurations in parallel...")
    
    # Thread-safe lock for updating shared data
    data_lock = Lock()
    
    def process_store_category(config, index):
        """Process a single store/category combination"""
        store_id, category_id = config.split(":")
        
        # Create a separate client for this thread
        thread_client = TrulieveAPIClient()
        
        print(f"\n[{index}/{len(config_list)}] {config}")
        print("-" * 50)
        
        result = {
            'config': config,
            'store_id': store_id,
            'category_id': category_id,
            'success': False
        }
        
        try:
            # Test with a small request first
            test_products = thread_client.get_products_url_encoded(
                store_id=store_id,
                category_uid=category_id,
                page_size=50,  # Small test size
                current_page=1
            )
            
            if test_products and isinstance(test_products, dict):
                total_count = test_products.get('total_count', 0)
                items = test_products.get('items', [])
                
                if total_count > 0 or len(items) > 0:
                    print(f"  ✅ Working! Found {total_count} products, got {len(items)} items")
                    
                    # Get more products for this store/category
                    all_products = thread_client.get_all_products_for_store(store_id, category_id)
                    
                    if all_products:
                        # Add store info to each product
                        for product in all_products:
                            product['_store_info'] = {
                                "store_id": store_id,
                                "category_id": category_id,
                                "config": config
                            }
                        
                        result.update({
                            'success': True,
                            'products_count': len(all_products),
                            'total_available': total_count,
                            'products': all_products
                        })
                        
                        print(f"  ✅ Collected {len(all_products)} products")
                    else:
                        print(f"  ⚠️ Test worked but full collection failed")
                        result['error'] = 'Full collection failed'
                else:
                    print(f"  ⚠️ No products found (total: {total_count}, items: {len(items)})")
                    result['error'] = 'No products found'
            else:
                print(f"  ❌ Invalid response: {test_products}")
                result['error'] = 'Invalid response'
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            result['error'] = str(e)
        
        return result
    
    # Process all store/category combinations in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_config = {
            executor.submit(process_store_category, config, i): config 
            for i, config in enumerate(config_list, 1)
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_config):
            config = future_to_config[future]
            try:
                result = future.result()
                
                # Thread-safe update of shared data structure
                with data_lock:
                    all_store_data['stores'][config] = {
                        "store_id": result['store_id'],
                        "category_id": result['category_id'],
                        "success": result['success']
                    }
                    
                    if result['success']:
                        all_store_data['stores'][config].update({
                            "products_count": result['products_count'],
                            "total_available": result['total_available'],
                            "products": result['products']
                        })
                        all_store_data['combined_products'].extend(result['products'])
                        all_store_data['summary']['total_products'] += result['products_count']
                        all_store_data['summary']['successful_stores'] += 1
                        all_store_data['summary']['working_configurations'].append(config)
                    else:
                        all_store_data['stores'][config]['error'] = result.get('error', 'Unknown error')
                        all_store_data['summary']['failed_stores'] += 1
                        all_store_data['summary']['failed_configurations'].append(config)
                        
            except Exception as e:
                print(f"  ❌ Exception processing {config}: {e}")
                with data_lock:
                    all_store_data['stores'][config] = {
                        "store_id": config.split(':')[0],
                        "category_id": config.split(':')[1],
                        "success": False,
                        "error": str(e)
                    }
                    all_store_data['summary']['failed_stores'] += 1
                    all_store_data['summary']['failed_configurations'].append(config)
    
    return all_store_data

def save_trulieve_data(data):
    """Save the collected data to files"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save complete data
    filename = f"trulieve_complete_data_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Complete data saved to: {filename}")
    
    # Save products-only file
    products_filename = f"trulieve_products_{timestamp}.json"
    products_data = {
        "timestamp": data["collection_timestamp"],
        "total_products": len(data["combined_products"]),
        "successful_stores": data["summary"]["successful_stores"],
        "products": data["combined_products"]
    }
    
    with open(products_filename, 'w', encoding='utf-8') as f:
        json.dump(products_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Products-only saved to: {products_filename}")
    
    return filename, products_filename

if __name__ == "__main__":
    print("🧪 Testing Trulieve API with exact browser format...")
    
    # Collect data using browser format
    all_data = collect_all_trulieve_data_browser_format()
    
    if all_data:
        # Print summary
        print(f"\n📊 COLLECTION SUMMARY")
        print("="*40)
        print(f"✅ Successful stores: {all_data['summary']['successful_stores']}")
        print(f"❌ Failed stores: {all_data['summary']['failed_stores']}")
        print(f"📦 Total products: {all_data['summary']['total_products']}")
        
        if all_data['summary']['working_configurations']:
            print(f"\n🎉 Working configurations:")
            for config in all_data['summary']['working_configurations']:
                store_data = all_data['stores'][config]
                print(f"   {config}: {store_data['products_count']} products")
        
        # Save data
        if all_data['summary']['total_products'] > 0:
            complete_file, products_file = save_trulieve_data(all_data)
            print(f"\n🚀 SUCCESS! Data collection complete.")
            print(f"Ready for Azure Data Lake upload!")
        else:
            print(f"\n⚠️ No products collected")
    else:
        print(f"\n❌ Collection failed")