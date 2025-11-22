import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple
import time
import csv

# Load configuration
def load_config(config_path: str = None) -> Dict:
    """Load configuration from JSON file"""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "menu_config.json")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found at {config_path}, using defaults")
        return {
            "download_settings": {
                "max_workers": 10,
                "timeout": 30,
                "retry_attempts": 3,
                "retry_delay": 2
            },
            "api_settings": {
                "page_size": 100,
                "sorting_method_id": 7,
                "platform_os": "web"
            },
            "output_settings": {
                "output_dir": "muv_menus",
                "save_summary": True,
                "indent": 2
            }
        }

# Load config at module level
CONFIG = load_config()

# Load store IDs from CSV
def load_store_ids(csv_path: str = None) -> List[Dict]:
    """Load store IDs from CSV file"""
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), "storeid_location_list.csv")
    
    stores = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                storeid = row.get('storeid', '').strip()
                if storeid:  # Only include if storeid is not empty
                    stores.append({
                        'location': row['location'],
                        'storeid': storeid
                    })
    except FileNotFoundError:
        print(f"CSV file not found at {csv_path}")
    return stores

# Load stores at module level
STORES = load_store_ids()

def get_muv_products(store_id=None):
    """
    Send a request to the MÜV API to get product list
    
    Args:
        store_id (str, optional): Store ID to include in headers
    
    Returns:
        dict: JSON response from the API
    """
    
    store_urls = [
    "https://muvfl.com/locations/apollo-beach",
    "https://muvfl.com/locations/apopka",
    "https://muvfl.com/locations/auburndale",
    "https://muvfl.com/locations/bonita-springs",
    "https://muvfl.com/locations/boynton-beach",
    "https://muvfl.com/locations/bradenton-75th-west",
    "https://muvfl.com/locations/bradenton",
    "https://muvfl.com/locations/brandon",
    "https://muvfl.com/locations/cape-coral",
    "https://muvfl.com/locations/clearwater",
    "https://muvfl.com/locations/clearwater-roosevelt",
    "https://muvfl.com/locations/crystal-river",
    "https://muvfl.com/locations/deerfield",
    "https://muvfl.com/locations/deltona",
    "https://muvfl.com/locations/fort-myers-beach",
    "https://muvfl.com/locations/ft-myers",
    "https://muvfl.com/locations/fort-myers-cypress",
    "https://muvfl.com/locations/fort-pierce",
    "https://muvfl.com/locations/gainesville",
    "https://muvfl.com/locations/haines-city",
    "https://muvfl.com/locations/hobe-sound",
    "https://muvfl.com/locations/hollywood",
    "https://muvfl.com/locations/jax-beach",
    "https://muvfl.com/locations/jacksonville",
    "https://muvfl.com/locations/jacksonville-skymarks",
    "https://muvfl.com/locations/key-west",
    "https://muvfl.com/locations/lady-lake",
    "https://muvfl.com/locations/lake-city",
    "https://muvfl.com/locations/lakeland",
    "https://muvfl.com/locations/longwood",
    "https://muvfl.com/locations/lutz",
    "https://muvfl.com/locations/marco-island",
    "https://muvfl.com/locations/melbourne",
    "https://muvfl.com/locations/merritt-island",
    "https://muvfl.com/locations/miami-kendall",
    "https://muvfl.com/locations/naranja",
    "https://muvfl.com/locations/navarre",
    "https://muvfl.com/locations/new-smyrna-beach",
    "https://muvfl.com/locations/new-tampa",
    "https://muvfl.com/locations/north-miami",
    "https://muvfl.com/locations/north-miami-beach",
    "https://muvfl.com/locations/north-port",
    "https://muvfl.com/locations/ocala",
    "https://muvfl.com/locations/okeechobee",
    "https://muvfl.com/locations/orange-city",
    "https://muvfl.com/locations/orange-park",
    "https://muvfl.com/locations/orlando-colonial",
    "https://muvfl.com/locations/orlando",
    "https://muvfl.com/locations/orlando-vineland",
    "https://muvfl.com/locations/ormond-beach",
    "https://muvfl.com/locations/palatka",
    "https://muvfl.com/locations/panama-city-beach",
    "https://muvfl.com/locations/pensacola",
    "https://muvfl.com/locations/pinellas-park",
    "https://muvfl.com/locations/port-charlotte",
    "https://muvfl.com/locations/port-orange",
    "https://muvfl.com/locations/port-richey",
    "https://muvfl.com/locations/port-st-lucie",
    "https://muvfl.com/locations/sarasota",
    "https://muvfl.com/locations/sarasota-main",
    "https://muvfl.com/locations/satellite-beach",
    "https://muvfl.com/locations/sebastian",
    "https://muvfl.com/locations/sebring",
    "https://muvfl.com/locations/shalimar",
    "https://muvfl.com/locations/spring-hill",
    "https://muvfl.com/locations/st-augustine",
    "https://muvfl.com/locations/st-petersburg",
    "https://muvfl.com/locations/stuart",
    "https://muvfl.com/locations/tallahassee",
    "https://muvfl.com/locations/tamarac",
    "https://muvfl.com/locations/tampa",
    "https://muvfl.com/locations/tampa-himes",
    "https://muvfl.com/locations/tampa-west-kennedy",
    "https://muvfl.com/locations/titusville",
    "https://muvfl.com/locations/venice",
    "https://muvfl.com/locations/wellington",
    "https://muvfl.com/locations/west-melbourne",
    "https://muvfl.com/locations/west-palm-okeechobee",
    "https://muvfl.com/locations/west-palm-beach",
    "https://muvfl.com/locations/winter-haven",
    "https://muvfl.com/locations/winter-springs",
    "https://muvfl.com/locations/yulee",
    "https://muvfl.com/locations/zephyrhills"
]

def get_muv_products(store_id=None, config: Dict = None):
    """
    Send a request to the MÜV API with specific store ID
    
    Args:
        store_id (str): Store ID to include in headers
        config (dict, optional): Configuration dict, uses global CONFIG if not provided
    """
    if config is None:
        config = CONFIG
        
    url = "https://web-ui-production.sweedpos.com/_api/proxy/Products/GetProductList"
    
    headers = {
        "Content-Type": "application/json",
        "Storeid": store_id,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    
    api_settings = config.get("api_settings", {})
    download_settings = config.get("download_settings", {})
    
    payload = {
        "filters": {"category": [425003]},
        "page": 1,
        "pageSize": api_settings.get("page_size", 100),
        "sortingMethodId": api_settings.get("sorting_method_id", 7),
        "searchTerm": "",
        "platformOs": api_settings.get("platform_os", "web"),
        "sourcePage": 0
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=download_settings.get("timeout", 30))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# Save response to file
def save_muv_response(filename="muv_products.json", store_id=None):
    """
    Get MÜV products and save to JSON file in current directory
    """
    products = get_muv_products(store_id)
    if products:
        current_dir = os.getcwd()
        filepath = os.path.join(current_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"Products saved to {filepath}")
        return True
    return False

def download_store_menu(store: Dict) -> Tuple[str, Optional[Dict], Optional[str]]:
    """
    Download menu for a single store
    
    Args:
        store: Dict with 'location' and 'storeid'
        
    Returns:
        Tuple of (location, menu_data, error_message)
    """
    location = store['location']
    store_id = store['storeid']
    
    try:
        products = get_muv_products(store_id)
        if products:
            return (location, products, None)
        else:
            return (location, None, "Failed to fetch products")
    except Exception as e:
        return (location, None, str(e))

def download_all_stores_parallel(max_workers: int = None, output_dir: str = None, config: Dict = None) -> List[Dict]:
    """
    Download menus from all stores in parallel
    
    Args:
        max_workers: Maximum number of parallel threads (uses config if None)
        output_dir: Directory to save the menu files (uses config if None)
        config: Configuration dict (uses global CONFIG if None)
        
    Returns:
        List of results with store info and status
    """
    if config is None:
        config = CONFIG
    
    # Get settings from config
    download_settings = config.get("download_settings", {})
    output_settings = config.get("output_settings", {})
    
    if max_workers is None:
        max_workers = download_settings.get("max_workers", 10)
    
    if output_dir is None:
        output_dir = output_settings.get("output_dir", "muv_menus")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    successful = 0
    failed = 0
    
    print(f"Starting download of {len(STORES)} stores with {max_workers} parallel workers...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all download tasks
        future_to_store = {executor.submit(download_store_menu, store): store for store in STORES}
        
        # Process completed tasks
        for future in as_completed(future_to_store):
            store = future_to_store[future]
            try:
                location, menu_data, error = future.result()
                
                if menu_data and not error:
                    # Save to file
                    filename = f"{location}.json"
                    filepath = os.path.join(output_dir, filename)
                    indent = output_settings.get("indent", 2)
                
                if menu_data and not error:
                    # Save to file
                    filename = f"{location}.json"
                    filepath = os.path.join(output_dir, filename)
                    indent = output_settings.get("indent", 2)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(menu_data, f, indent=indent, ensure_ascii=False)
                    
                    successful += 1
                    print(f"✓ {location}: Successfully downloaded and saved")
                    results.append({
                        "location": location,
                        "storeid": store['storeid'],
                        "status": "success",
                        "filepath": filepath
                    })
                else:
                    failed += 1
                    print(f"✗ {location}: Failed - {error}")
                    results.append({
                        "location": location,
                        "storeid": store['storeid'],
                        "status": "failed",
                        "error": error
                    })
            except Exception as e:
                failed += 1
                location = store['location']
                print(f"✗ {location}: Exception - {str(e)}")
                results.append({
                    "location": location,
                    "storeid": store['storeid'],
                    "status": "error",
                    "error": str(e)
                })
    
    elapsed_time = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"Download Complete!")
    print(f"Total stores: {len(STORES)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Output directory: {os.path.abspath(output_dir)}")
    print(f"{'='*60}\n")
    
    return results

# Usage examples:
if __name__ == "__main__":
    # Download all stores in parallel (uses config settings)
    results = download_all_stores_parallel()
    
    # Save summary report if enabled in config
    output_settings = CONFIG.get("output_settings", {})
    if output_settings.get("save_summary", True):
        output_dir = output_settings.get("output_dir", "muv_menus")
        summary_file = os.path.join(output_dir, "_download_summary.json")
        indent = output_settings.get("indent", 2)
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=indent, ensure_ascii=False)
        print(f"Summary saved to: {summary_file}")
    
    # Original single store example (commented out)
    # products = get_muv_products("298")
    # save_muv_response("muv_products.json", "298")