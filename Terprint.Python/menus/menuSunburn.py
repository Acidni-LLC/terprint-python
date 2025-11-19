import requests
import json
import os
import time
import urllib.parse
from datetime import datetime

class SunburnAPIClient:
    """API client for Sunburn dispensary data with multiple request methods"""
    
    def __init__(self):
        self.base_url = "https://sunburn-jacksonvillebeach.dispensary.shop"
        self.session = requests.Session()
        
        # More comprehensive browser headers
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0"
        })
    
    def method_1_direct_api(self, category="Flower", medrec="med", page=1):
        """Method 1: Direct API call (original approach)"""
        
        print("🔄 Method 1: Direct API call")
        
        relative_path = f"/catalog/search?category={category}&medrec={medrec}&order_by=name&order_dir=asc&page={page}&_data=routes%2Fcatalog.search"
        url = self.base_url + relative_path
        
        try:
            response = self.session.get(url, timeout=30)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"   Error: {response.text[:200]}")
                return None
        except Exception as e:
            print(f"   Exception: {e}")
            return None
    
    def method_2_visit_site_first(self, category="Flower", medrec="med", page=1):
        """Method 2: Visit main site first, then make API call"""
        
        print("🔄 Method 2: Visit site first, then API")
        
        try:
            # Step 1: Visit the main site to get cookies/session
            print("   Step 1: Visiting main site...")
            main_response = self.session.get(self.base_url, timeout=30)
            print(f"   Main site status: {main_response.status_code}")
            
            if main_response.status_code != 200:
                return None
            
            # Step 2: Update headers for subsequent requests
            self.session.headers.update({
                "Referer": self.base_url,
                "Accept": "application/json, text/plain, */*",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
            })
            
            # Step 3: Make the API call
            print("   Step 2: Making API call...")
            relative_path = f"/catalog/search?category={category}&medrec={medrec}&order_by=name&order_dir=asc&page={page}&_data=routes%2Fcatalog.search"
            url = self.base_url + relative_path
            
            response = self.session.get(url, timeout=30)
            print(f"   API status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"   API error: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"   Exception: {e}")
            return None
    
    def method_3_catalog_page_first(self, category="Flower", medrec="med", page=1):
        """Method 3: Visit catalog page first, then make API call"""
        
        print("🔄 Method 3: Visit catalog page first")
        
        try:
            # Step 1: Visit the catalog page
            catalog_url = f"{self.base_url}/catalog"
            print(f"   Step 1: Visiting catalog page...")
            catalog_response = self.session.get(catalog_url, timeout=30)
            print(f"   Catalog status: {catalog_response.status_code}")
            
            # Step 2: Visit category-specific page
            category_url = f"{self.base_url}/catalog?category={category}&medrec={medrec}"
            print(f"   Step 2: Visiting category page...")
            category_response = self.session.get(category_url, timeout=30)
            print(f"   Category status: {category_response.status_code}")
            
            # Step 3: Update headers for API call
            self.session.headers.update({
                "Referer": category_url,
                "Accept": "application/json, text/plain, */*",
                "X-Requested-With": "XMLHttpRequest"
            })
            
            # Step 4: Make API call
            print("   Step 3: Making API call...")
            relative_path = f"/catalog/search?category={category}&medrec={medrec}&order_by=name&order_dir=asc&page={page}&_data=routes%2Fcatalog.search"
            url = self.base_url + relative_path
            
            response = self.session.get(url, timeout=30)
            print(f"   API status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"   API error: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"   Exception: {e}")
            return None
    
    def method_4_form_submission(self, category="Flower", medrec="med", page=1):
        """Method 4: Try POST request as form submission"""
        
        print("🔄 Method 4: Form submission approach")
        
        try:
            # Visit main site first
            main_response = self.session.get(self.base_url, timeout=30)
            
            # Prepare for POST request
            self.session.headers.update({
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": self.base_url,
                "Origin": self.base_url
            })
            
            # POST data
            data = {
                "category": category,
                "medrec": medrec,
                "order_by": "name",
                "order_dir": "asc",
                "page": page,
                "_data": "routes/catalog.search"
            }
            
            # Make POST request
            url = f"{self.base_url}/catalog/search"
            response = self.session.post(url, data=data, timeout=30)
            print(f"   POST status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"   POST error: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"   Exception: {e}")
            return None
    
    def method_5_selenium_style(self, category="Flower", medrec="med", page=1):
        """Method 5: Mimic Selenium behavior with delays"""
        
        print("🔄 Method 5: Selenium-style with delays")
        
        try:
            # Step 1: Visit main page and wait
            print("   Visiting main page...")
            self.session.get(self.base_url, timeout=30)
            time.sleep(2)  # Wait like a human would
            
            # Step 2: Visit catalog with search params
            search_params = {
                "category": category,
                "medrec": medrec,
                "order_by": "name",
                "order_dir": "asc",
                "page": page
            }
            
            # Build URL with parameters
            params_str = urllib.parse.urlencode(search_params)
            catalog_url = f"{self.base_url}/catalog?{params_str}"
            
            print("   Visiting catalog with params...")
            catalog_response = self.session.get(catalog_url, timeout=30)
            time.sleep(1)  # Another human-like delay
            
            # Step 3: Try to extract data from the HTML response
            if catalog_response.status_code == 200:
                # Look for JSON data embedded in the HTML
                html_content = catalog_response.text
                
                # Common patterns where JSON might be embedded
                json_patterns = [
                    r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
                    r'window\.__DATA__\s*=\s*({.*?});',
                    r'__remixContext\s*=\s*({.*?});',
                    r'data-json="([^"]*)',
                    r'<script[^>]*>.*?({.*"products".*?})',
                ]
                
                import re
                for pattern in json_patterns:
                    matches = re.search(pattern, html_content, re.DOTALL)
                    if matches:
                        try:
                            json_str = matches.group(1)
                            if json_str.startswith('"') and json_str.endswith('"'):
                                json_str = json_str[1:-1].replace('\\"', '"')
                            return json.loads(json_str)
                        except:
                            continue
                
                print(f"   No JSON found in HTML response")
                return None
            else:
                print(f"   Catalog error: {catalog_response.status_code}")
                return None
                
        except Exception as e:
            print(f"   Exception: {e}")
            return None
    
    def method_6_alternative_endpoints(self, category="Flower", medrec="med", page=1):
        """Method 6: Try alternative API endpoints"""
        
        print("🔄 Method 6: Alternative endpoints")
        
        # Different possible endpoints
        endpoints = [
            f"/api/catalog/search?category={category}&medrec={medrec}&page={page}",
            f"/api/products?category={category}&medrec={medrec}&page={page}",
            f"/_data/catalog/search?category={category}&medrec={medrec}&page={page}",
            f"/catalog/search.json?category={category}&medrec={medrec}&page={page}",
            f"/search?category={category}&medrec={medrec}&page={page}&format=json",
        ]
        
        for endpoint in endpoints:
            try:
                url = self.base_url + endpoint
                print(f"   Trying: {endpoint}")
                
                response = self.session.get(url, timeout=15)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   ✅ Success with {endpoint}")
                        return data
                    except:
                        print(f"   Not JSON response")
                        continue
                        
            except Exception as e:
                print(f"   Error with {endpoint}: {e}")
                continue
        
        return None
    
    def try_all_methods(self, category="Flower", medrec="med", page=1):
        """Try all methods until one works"""
        
        print(f"🚀 TRYING ALL METHODS FOR {category}")
        print("="*50)
        
        methods = [
            self.method_1_direct_api,
            self.method_2_visit_site_first,
            self.method_3_catalog_page_first,
            self.method_4_form_submission,
            self.method_5_selenium_style,
            self.method_6_alternative_endpoints
        ]
        
        for i, method in enumerate(methods, 1):
            print(f"\n🧪 Attempting Method {i}")
            print("-" * 30)
            
            try:
                result = method(category=category, medrec=medrec, page=page)
                
                if result:
                    print(f"✅ Method {i} succeeded!")
                    print(f"Response keys: {list(result.keys())}")
                    
                    # Check if it looks like product data
                    if self._has_product_data(result):
                        print(f"🎉 Found product data with Method {i}!")
                        return result, i
                    else:
                        print(f"⚠️ Method {i} returned data but no products found")
                else:
                    print(f"❌ Method {i} failed")
                    
            except Exception as e:
                print(f"❌ Method {i} exception: {e}")
            
            # Small delay between methods
            time.sleep(1)
        
        print("\n❌ All methods failed")
        return None, 0
    
    def _has_product_data(self, response):
        """Check if response contains product data"""
        
        if not response or not isinstance(response, dict):
            return False
        
        # Check various possible product containers
        product_indicators = [
            'products', 'items', 'data', 'results', 'catalog', 'inventory'
        ]
        
        for indicator in product_indicators:
            if indicator in response:
                data = response[indicator]
                if isinstance(data, list) and len(data) > 0:
                    return True
                elif isinstance(data, dict):
                    # Check for nested product arrays
                    for key, value in data.items():
                        if isinstance(value, list) and len(value) > 0:
                            return True
        
        return False

def test_all_methods():
    """Test all methods to find what works"""
    
    print("🧪 COMPREHENSIVE SUNBURN API TEST")
    print("="*60)
    
    client = SunburnAPIClient()
    
    # Try to get Flower category data
    result, method_num = client.try_all_methods(category="Flower", medrec="med", page=1)
    
    if result:
        print(f"\n🎉 SUCCESS with Method {method_num}!")
        print(f"Response structure: {json.dumps(result, indent=2)[:500]}...")
        
        # Try to extract product count
        product_count = 0
        if 'products' in result:
            product_count = len(result['products'])
        elif 'data' in result and isinstance(result['data'], list):
            product_count = len(result['data'])
        elif 'items' in result:
            product_count = len(result['items'])
        
        print(f"📦 Products found: {product_count}")
        
        # Save the working result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sunburn_working_response_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Working response saved to: {filename}")
        
        return True
    else:
        print(f"\n❌ ALL METHODS FAILED")
        print("The API might require authentication or have anti-bot protection")
        return False

if __name__ == "__main__":
    print("🚀 SUNBURN API - MULTIPLE METHODS TEST")
    print("="*60)
    
    success = test_all_methods()
    
    if success:
        print("\n✅ At least one method worked!")
        print("You can now proceed with data collection")
    else:
        print("\n❌ No methods worked")
        print("\n🔧 Possible issues:")
        print("1. Site requires user authentication")
        print("2. Anti-bot protection (Cloudflare, etc.)")
        print("3. API endpoint has changed")
        print("4. Geographic restrictions")
        print("5. Rate limiting")
        
        print("\n💡 Alternative approaches:")
        print("1. Use a browser automation tool (Selenium)")
        print("2. Check if there's a public API documentation")
        print("3. Try accessing from a different IP/VPN")
        print("4. Use a headless browser service")