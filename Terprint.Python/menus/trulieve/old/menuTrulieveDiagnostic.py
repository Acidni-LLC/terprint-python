import requests
import json
import os
from datetime import datetime

def diagnose_trulieve_api():
    """Comprehensive diagnostic of the Trulieve API"""
    
    print("🔍 TRULIEVE API DIAGNOSTIC")
    print("="*50)
    
    base_url = "https://www.trulieve.com/api/graphql"
    
    # Test 1: Basic connectivity
    print("\n🌐 TEST 1: Basic Connectivity")
    print("-" * 30)
    try:
        response = requests.get("https://www.trulieve.com", timeout=10)
        print(f"✅ Trulieve.com reachable: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot reach trulieve.com: {e}")
        return False
    
    # Test 2: GraphQL endpoint
    print("\n📡 TEST 2: GraphQL Endpoint")
    print("-" * 30)
    try:
        response = requests.get(base_url, timeout=10)
        print(f"GraphQL endpoint status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 405:
            print("✅ Endpoint exists (405 Method Not Allowed is expected for GET on GraphQL)")
        elif response.status_code == 200:
            print("✅ Endpoint accessible")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ GraphQL endpoint error: {e}")
    
    # Test 3: Simple GraphQL query without filters
    print("\n🧪 TEST 3: Simple GraphQL Query")
    print("-" * 30)
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    # Very basic query
    simple_query = """
    query {
        __schema {
            types {
                name
            }
        }
    }
    """
    
    try:
        response = requests.post(
            base_url,
            headers=headers,
            json={"query": simple_query},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if 'data' in result:
                print("✅ GraphQL schema accessible")
                schema_types = result.get('data', {}).get('__schema', {}).get('types', [])
                print(f"Found {len(schema_types)} schema types")
                
                # Look for product-related types
                product_types = [t['name'] for t in schema_types if 'product' in t['name'].lower()]
                if product_types:
                    print(f"Product-related types: {product_types}")
            else:
                print(f"❌ No data in response: {result}")
        else:
            print(f"❌ GraphQL query failed: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ GraphQL query error: {e}")
    
    # Test 4: Try different product query approaches
    print("\n🛍️ TEST 4: Product Query Approaches")
    print("-" * 30)
    
    # Approach 1: Without any store/category filters
    print("Approach 1: No filters")
    test_product_query_no_filters()
    
    # Approach 2: Try to discover available categories
    print("\nApproach 2: Category discovery")
    test_category_discovery()
    
    # Approach 3: Try different header combinations
    print("\nApproach 3: Different headers")
    test_different_headers()
    
    return True

def test_product_query_no_filters():
    """Test basic product query without filters"""
    
    url = "https://www.trulieve.com/api/graphql"
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    # Try minimal product query
    query = """
    query products($pageSize: Int = 5) {
        products(pageSize: $pageSize) {
            total_count
            items {
                id
                name
                sku
            }
        }
    }
    """
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json={
                "query": query,
                "variables": {"pageSize": 5}
            },
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Response keys: {list(result.keys())}")
            
            if 'data' in result:
                print("   ✅ Got data response")
                products = result['data'].get('products')
                if products:
                    total = products.get('total_count', 0)
                    items = products.get('items', [])
                    print(f"   📦 Total products: {total}, Items returned: {len(items)}")
                    return True
                else:
                    print("   ⚠️ No products in response")
            
            if 'errors' in result:
                print(f"   ❌ GraphQL errors: {result['errors']}")
        else:
            print(f"   ❌ HTTP error: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    return False

def test_category_discovery():
    """Try to discover available categories"""
    
    url = "https://www.trulieve.com/api/graphql"
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    # Try to get category information
    category_queries = [
        """
        query {
            categories {
                items {
                    id
                    name
                    uid
                }
            }
        }
        """,
        """
        query {
            categoryList {
                id
                name
                uid
            }
        }
        """,
        """
        query {
            storeConfig {
                store_name
                store_code
            }
        }
        """
    ]
    
    for i, query in enumerate(category_queries, 1):
        print(f"   Query {i}:")
        try:
            response = requests.post(
                url,
                headers=headers,
                json={"query": query},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'data' in result and result['data']:
                    print(f"   ✅ Success: {list(result['data'].keys())}")
                    return result['data']
                elif 'errors' in result:
                    print(f"   ❌ Errors: {[e.get('message', str(e)) for e in result['errors']]}")
                else:
                    print("   ⚠️ Empty response")
            else:
                print(f"   ❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    return None

def test_different_headers():
    """Test different header combinations"""
    
    url = "https://www.trulieve.com/api/graphql"
    
    # Different header combinations to try
    header_sets = [
        {
            "name": "Basic",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        },
        {
            "name": "With Referer",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.trulieve.com/",
                "Origin": "https://www.trulieve.com"
            }
        },
        {
            "name": "With Store Cookie",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Cookie": "store_id=palm_coast",
                "Referer": "https://www.trulieve.com/",
                "Origin": "https://www.trulieve.com"
            }
        },
        {
            "name": "Full Browser Simulation",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.trulieve.com/",
                "Origin": "https://www.trulieve.com",
                "Cookie": "store_id=palm_coast",
                "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
            }
        }
    ]
    
    # Simple test query
    query = """
    query {
        __typename
    }
    """
    
    for header_set in header_sets:
        print(f"   {header_set['name']}:")
        try:
            response = requests.post(
                url,
                headers=header_set['headers'],
                json={"query": query},
                timeout=10
            )
            
            print(f"     Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if 'data' in result:
                    print("     ✅ Success")
                elif 'errors' in result:
                    print(f"     ❌ Errors: {[e.get('message', str(e)) for e in result['errors']]}")
            else:
                print(f"     ❌ Failed: {response.text[:100]}")
                
        except Exception as e:
            print(f"     ❌ Exception: {e}")

def test_website_scraping_alternative():
    """Test if we can get product data from the website HTML instead of API"""
    
    print("\n🌐 TEST 5: Website Scraping Alternative")
    print("-" * 30)
    
    # Try to access a product page directly
    test_urls = [
        "https://www.trulieve.com/dispensary/palm-coast/",
        "https://www.trulieve.com/products/",
        "https://www.trulieve.com/shop/",
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for url in test_urls:
        print(f"Testing: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Look for signs of product data
                indicators = [
                    "product", "price", "thc", "cbd", "strain", 
                    "inventory", "menu", "dispensary"
                ]
                
                found_indicators = [ind for ind in indicators if ind in content]
                print(f"   Found indicators: {found_indicators}")
                
                # Look for potential API endpoints in the HTML
                if "graphql" in content:
                    print("   ✅ GraphQL mentioned in page")
                if "api" in content:
                    print("   ✅ API mentioned in page")
                    
                # Check for JavaScript that might make API calls
                if "fetch(" in content or "axios" in content or "xhr" in content:
                    print("   ✅ AJAX/Fetch calls found")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 STARTING COMPREHENSIVE TRULIEVE DIAGNOSTIC")
    print("This will help identify why the API calls are failing")
    print("="*60)
    
    success = diagnose_trulieve_api()
    
    # Also test website scraping as alternative
    test_website_scraping_alternative()
    
    print("\n" + "="*60)
    print("📋 DIAGNOSTIC COMPLETE")
    print("\nNext steps based on results:")
    print("1. If GraphQL works but products don't - API structure changed")
    print("2. If nothing works - Authentication/CORS issues")
    print("3. If website has data - Consider scraping alternative")
    print("4. Check browser network tab for actual API calls")