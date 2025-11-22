import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import concurrent.futures
import os

def get_store_id_from_network(url, retry=1):
    for attempt in range(retry + 1):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            driver.get(url + "/menu/menu?filters=%7B%22category%22%3A%5B425003%5D%7D")
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

            logs = driver.get_log("performance")
            for log in logs:
                try:
                    message = json.loads(log["message"])["message"]
                    if message["method"] == "Network.requestWillBeSent":
                        request = message["params"]["request"]
                        if "https://web-ui-production.sweedpos.com/_api/proxy/Products/GetProductList" in request["url"]:
                            headers = request["headers"]
                            if "StoreId" in headers or "storeid" in headers:
                                return headers.get("StoreId") or headers.get("storeid")
                except:
                    continue
            return None
        except Exception as e:
            if attempt < retry:
                continue
            else:
                raise e
        finally:
            driver.quit()
    return None

# List of store URLs
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

if __name__ == "__main__":
    results = {}
    failed_urls = []
    
    # First pass
    print("Running first pass...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(get_store_id_from_network, url): url for url in STORE_URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                store_id = future.result()
                results[url] = store_id
                if store_id is None:
                    failed_urls.append(url)
                print(f"{url}: {store_id}")
            except Exception as exc:
                results[url] = None
                failed_urls.append(url)
                print(f"{url}: Error - {exc}")
    
    # Retry failed ones sequentially
    print(f"\nRetrying {len(failed_urls)} failed URLs...")
    for url in failed_urls:
        try:
            store_id = get_store_id_from_network(url, retry=2)
            results[url] = store_id
            print(f"Retry {url}: {store_id}")
        except Exception as exc:
            print(f"Retry {url}: Still failed - {exc}")
    
    # Save to file
    output_file = "store_ids.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"\nResults saved to {output_file}")
    
    print("\nFinal Summary:")
    for url, store_id in results.items():
        print(f"{url}: {store_id}")