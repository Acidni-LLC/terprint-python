import requests
import json
import os

def get_muv_products(store_id=None):
    """
    Send a request to the MÜV API to get product list
    
    Args:
        store_id (str, optional): Store ID to include in headers
    
    Returns:
        dict: JSON response from the API
    """
    
    url = "https://web-ui-production.sweedpos.com/_api/proxy/Products/GetProductList"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    
    # Add store ID to headers if provided
    if store_id:
        headers["Storeid"] = store_id
    
    # Request body
    body = {
        "filters": {
            "category": [425003]
        },
        "page": 1,
        "pageSize": 100,
        "sortingMethodId": 7,
        "searchTerm": "",
        "platformOs": "web",
        "sourcePage": 0
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=body,  # This automatically converts dict to JSON and sets Content-Type
            timeout=30
        )
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Return JSON response
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e} {e.message if hasattr(e, 'message') else ''}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e} {e.msg if hasattr(e, 'msg') else ''}")
        return None


# Usage examples:
if __name__ == "__main__":
    # Without store ID
    products = get_muv_products()
    if products:
        print("Success! Received products:")
        print(json.dumps(products, indent=2))
    
    # With store ID
    products_with_store = get_muv_products(store_id="your_store_id_here")
    if products_with_store:
        print("Success with store ID!")

# Alternative version if you want to specify the store ID directly:
def get_muv_products_with_store(store_id):
    """
    Send a request to the MÜV API with specific store ID
    """
    url = "https://web-ui-production.sweedpos.com/_api/proxy/Products/GetProductList"
    
    headers = {
        "Content-Type": "application/json",
        "Storeid": store_id,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    
    payload = {
        "filters": {"category": [425003]},
        "page": 1,
        "pageSize": 50,
        "sortingMethodId": 7,
        "searchTerm": "",
        "platformOs": "web",
        "sourcePage": 0
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
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

# Usage examples:
# With store ID
#products = get_muv_products("298")

#print(products)
# Save to file
save_muv_response("muv_products.json", "298")