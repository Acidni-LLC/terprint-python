import requests
import json
import os

def get_trulieve_products(store_id=None, category_uid=None, page_size=100, current_page=1):
    """
    Send a GraphQL request to the Trulieve API to get product list
    
    Args:
        store_id (str, optional): Store ID to include in headers
        category_uid (str, optional): Category UID filter
        page_size (int): Number of products per page (default: 100)
        current_page (int): Current page number (default: 1)
    
    Returns:
        dict: JSON response from the API
    """
    
    url = "https://www.trulieve.com/api/graphql"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    
    # Add store-specific headers if provided
    if store_id:
        headers["Cookie"] = f"store_id={store_id}"
        headers["Store"] = store_id
    
    # GraphQL query
    query = """
    query products($searchCriteria:[SearchCriteriaInput!]!,$pageSize:Int=100,$currentPage:Int=1,$sort:ProductAttributeSortInput={}){
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
    }
    """
    
    # Variables for the GraphQL query
    variables = {
        "currentPage": current_page,
        "pageSize": page_size,
        "searchCriteria": [],
        "sort": {}
    }
    
    # Add category filter if provided
    if category_uid:
        variables["searchCriteria"].append({
            "attribute_code": "category_uid",
            "filter_action": "EQ",
            "filter_value": category_uid
        })
    
    # Request body
    body = {
        "query": query,
        "operationName": "products",
        "variables": variables
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=30
        )
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Return JSON response
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None

def get_trulieve_products_all_pages(store_id=None, category_uid=None, page_size=100):
    """
    Get all products from all pages
    
    Args:
        store_id (str, optional): Store ID
        category_uid (str, optional): Category UID filter
        page_size (int): Products per page
        
    Returns:
        dict: Combined results from all pages
    """
    all_products = []
    current_page = 1
    total_pages = 1
    
    while current_page <= total_pages:
        print(f"Fetching page {current_page}...")
        
        response = get_trulieve_products(
            store_id=store_id,
            category_uid=category_uid,
            page_size=page_size,
            current_page=current_page
        )
        
        if response and 'data' in response and 'products' in response['data']:
            products_data = response['data']['products']
            
            # Update total pages from response
            if 'page_info' in products_data:
                total_pages = products_data['page_info'].get('total_pages', 1)
            
            # Add items to our collection
            if 'items' in products_data:
                all_products.extend(products_data['items'])
                print(f"  Got {len(products_data['items'])} products")
            
            current_page += 1
        else:
            print(f"Failed to fetch page {current_page}")
            break
    
    return {
        "total_products": len(all_products),
        "products": all_products,
        "store_id": store_id,
        "category_uid": category_uid
    }

def save_trulieve_response(filename="trulieve_products.json", store_id=None, category_uid=None, get_all_pages=False):
    """
    Get Trulieve products and save to JSON file
    
    Args:
        filename (str): Output filename
        store_id (str, optional): Store ID
        category_uid (str, optional): Category UID filter  
        get_all_pages (bool): Whether to fetch all pages
    """
    if get_all_pages:
        products = get_trulieve_products_all_pages(store_id, category_uid)
    else:
        products = get_trulieve_products(store_id, category_uid)
    
    if products:
        # Ensure we're saving to the repo root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.join(current_dir, "..", "..")  # Go up to Terprint folder
        filepath = os.path.join(repo_root, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"Products saved to {filepath}")
        return True
    return False

# Usage examples:
if __name__ == "__main__":
    # Example 1: Get products without any filters
    print("Getting Trulieve products...")
    products = get_trulieve_products()
    if products:
        print("Success! Received products")
        print(f"Response keys: {list(products.keys())}")
    
    # Example 2: Get products with store ID
    print("\nGetting products for store...")
    products_with_store = get_trulieve_products(store_id="palm_coast")  # Adjust store_id as needed
    
    # Example 3: Save to file
    print("\nSaving products to file...")
    save_trulieve_response("trulieve_products.json", store_id="palm_coast", get_all_pages=True)
    
    # Example 4: Get products with category filter
    # You would need to find the correct category_uid for the products you want
    # products_category = get_trulieve_products(category_uid="some_category_id")
