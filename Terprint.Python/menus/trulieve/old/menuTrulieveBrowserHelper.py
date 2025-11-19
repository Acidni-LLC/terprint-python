"""
Browser inspection helper for Trulieve API
"""

def generate_browser_instructions():
    """Generate instructions for browser-based API inspection"""
    
    instructions = """
🔍 BROWSER INSPECTION INSTRUCTIONS FOR TRULIEVE API
==================================================

To find the correct API endpoints and parameters:

1. OPEN BROWSER DEVELOPER TOOLS:
   - Open Chrome/Edge
   - Go to https://www.trulieve.com/
   - Press F12 to open Developer Tools
   - Click on "Network" tab

2. NAVIGATE TO PRODUCTS:
   - Select a store location (e.g., Palm Coast)
   - Browse to products/menu section
   - Look for AJAX/XHR/Fetch requests in Network tab

3. FIND API CALLS:
   - Look for requests to:
     * /api/graphql
     * /api/products
     * Any endpoints containing "product" or "menu"
   
4. INSPECT THE REQUESTS:
   - Right-click on API calls → Copy → Copy as cURL
   - Note the headers, especially:
     * Authorization headers
     * Store-specific cookies
     * CSRF tokens
     * Session IDs

5. CHECK REQUEST PAYLOAD:
   - Look at the GraphQL query structure
   - Note the exact variable names and values
   - Check for store IDs and category IDs being used

6. SAVE THE WORKING REQUEST:
   - Copy the exact headers
   - Copy the exact GraphQL query
   - Note any authentication requirements

COMMON ISSUES TO CHECK:
======================

❌ Missing Authentication:
   - Look for Authorization headers
   - Check for session cookies
   - CSRF/XSRF tokens

❌ Wrong Parameters:
   - Store IDs might be different format
   - Category IDs might have changed
   - API structure might be different

❌ CORS/Security:
   - API might require specific referrer
   - Browser security headers needed
   - Rate limiting in place

ALTERNATIVE DATA SOURCES:
========================

If API is blocked, check:
1. JSON data embedded in HTML
2. JavaScript variables with product data
3. Alternative endpoints (REST instead of GraphQL)
4. Mobile API endpoints (might be different)

COPY WORKING EXAMPLE:
====================
Once you find a working request in browser, copy:
1. Request URL
2. All request headers
3. Request payload/body
4. Response format

Then we can replicate it in Python!
"""

    print(instructions)
    
    # Save to file for reference
    with open("trulieve_browser_inspection_guide.txt", "w") as f:
        f.write(instructions)
    
    print("\n💾 Instructions saved to 'trulieve_browser_inspection_guide.txt'")

if __name__ == "__main__":
    generate_browser_instructions()