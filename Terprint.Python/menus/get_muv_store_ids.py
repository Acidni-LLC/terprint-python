"""
Script to extract MUV store IDs from their location pages
Outputs a list of store IDs and URLs for use in the downloader
"""
import requests
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple, Optional, Dict
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Store URLs from MUV website
STORE_URLS = [
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

def extract_store_id_from_url(store_url: str, timeout: int = 10, debug: bool = False) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Extract store ID from a MUV store location page
    Args:
        store_url: URL of the store location page
        timeout: Request timeout in seconds
        debug: Enable debug output
    Returns:
        Tuple of (store_url, store_id, error_message)
    """
    store_slug = store_url.split('/')[-1]
    try:
        # Always append the menu page with the specified filters
        menu_url = store_url.rstrip('/') + '/menu/menu?filters=%7B"category"%3A%5B425003%5D%7D'
        if debug:
            print(f"\n[DEBUG] {store_slug}")
            print(f"  Store URL: {store_url}")
            print(f"  Menu URL: {menu_url}")
        
        # Use Selenium to capture network requests
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(menu_url)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        
        logs = driver.get_log("performance")
        driver.quit()
        
        for log in logs:
            try:
                message = json.loads(log["message"])["message"]
                if message["method"] == "Network.requestWillBeSent":
                    request = message["params"]["request"]
                    if "https://web-ui-production.sweedpos.com/_api/proxy/Products/GetProductList" in request["url"]:
                        headers = request["headers"]
                        if "StoreId" in headers or "storeid" in headers:
                            store_id = headers.get("StoreId") or headers.get("storeid")
                            if debug:
                                print(f"  ✓ Found store ID from network: {store_id}")
                            return (store_url, store_id, None)
            except:
                continue
        
        if debug:
            print(f"  ✗ No GetProductList request found")
        
        return (store_url, None, "Store ID not found in network requests")
        
    except Exception as e:
        return (store_url, None, f"Error extracting store ID: {str(e)}")

def get_all_store_ids(max_workers: int = 10) -> Dict:
    """
    Fetch store IDs for all MUV locations by scraping their location pages
    
    Args:
        max_workers: Maximum number of parallel requests
        
    Returns:
        Dictionary with results
    """
    print(f"Fetching store IDs from {len(STORE_URLS)} MUV locations...")
    print(f"Using {max_workers} parallel workers")
    print("=" * 80)
    
    results = {}
    successful = 0
    failed = 0
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {
            executor.submit(extract_store_id_from_url, url): url 
            for url in STORE_URLS
        }
        
        # Process results as they complete
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            store_slug = url.split('/')[-1]
            
            try:
                _, store_id, error = future.result()
                
                if store_id:
                    successful += 1
                    results[store_slug] = {
                        'store_id': store_id,
                        'store_url': url,
                        'store_slug': store_slug,
                        'status': 'success'
                    }
                    print(f"✓ {store_slug:35s} -> Store ID: {store_id}")
                else:
                    failed += 1
                    results[store_slug] = {
                        'store_id': None,
                        'store_url': url,
                        'store_slug': store_slug,
                        'status': 'failed',
                        'error': error
                    }
                    print(f"✗ {store_slug:35s} -> Failed: {error}")
                    
            except Exception as e:
                failed += 1
                results[store_slug] = {
                    'store_id': None,
                    'store_url': url,
                    'store_slug': store_slug,
                    'status': 'error',
                    'error': str(e)
                }
                print(f"✗ {store_slug:35s} -> Error: {str(e)}")
    
    elapsed_time = time.time() - start_time
    
    # Print summary
    print("=" * 80)
    print(f"Store ID Extraction Complete!")
    print(f"Total locations: {len(STORE_URLS)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print("=" * 80)
    
    # Extract and display store IDs list
    store_id_list = [info['store_id'] for slug, info in sorted(results.items()) if info['store_id']]
    
    print(f"\n✓ Found {len(store_id_list)} store IDs\n")
    print("Store IDs List (Python format):")
    print("-" * 80)
    print("muv_store_ids = [")
    for i, store_id in enumerate(store_id_list):
        if i < len(store_id_list) - 1:
            print(f"    '{store_id}',")
        else:
            print(f"    '{store_id}'")
    print("]")
    print("-" * 80)
    
    # Display URL to Store ID mapping
    print("\nStore URL to ID Mapping:")
    print("-" * 80)
    for slug, info in sorted(results.items()):
        if info['store_id']:
            print(f"{info['store_slug']:35s} -> {info['store_id']:5s} ({info['store_url']})")
    print("-" * 80)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'muv_store_ids.json')
    output_data = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_locations': len(STORE_URLS),
        'successful': successful,
        'failed': failed,
        'store_ids': store_id_list,
        'store_mapping': {slug: info for slug, info in results.items() if info['store_id']},
        'failed_stores': {slug: info for slug, info in results.items() if not info['store_id']}
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to: {output_file}\n")
    
    return output_data

if __name__ == "__main__":
    import sys
    
    # Test mode: only test first 2 stores with debug output
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("=" * 80)
        print("TEST MODE: Testing first 2 stores with debug output")
        print("=" * 80)
        
        test_urls = STORE_URLS[:2]
        for url in test_urls:
            store_url, store_id, error = extract_store_id_from_url(url, timeout=15, debug=True)
            print()
        
        print("=" * 80)
        print("Test complete. Run without --test to process all stores.")
        print("=" * 80)
    else:
        results = get_all_store_ids(max_workers=15)
