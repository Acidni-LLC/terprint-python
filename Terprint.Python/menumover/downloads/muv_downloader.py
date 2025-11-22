"""
MÜV Dispensary Download Module
Handles data collection from MÜV dispensary API
"""
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directories to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.extend([current_dir, parent_dir, grandparent_dir, 
                os.path.join(grandparent_dir, "menus")])

class MuvDownloader:
    """MÜV dispensary data downloader"""
    
    def __init__(self, output_dir: str, store_ids: Optional[List[str]] = None):
        self.output_dir = output_dir
        if store_ids is None:
            # Default to all known MÜV store IDs
            self.store_ids = [
                '298', '299', '300', '301', '302', '303', '304', '305', '306', '307',
                '308', '309', '310', '311', '312', '313', '314', '315', '316', '317',
                '318', '319', '320', '321', '322', '323', '324', '325', '326', '327',
                '328', '329', '330', '331', '332', '333', '334', '335', '336', '337',
                '338', '339', '340', '341', '342', '343', '344', '345', '346', '347',
                '348', '349', '350', '351', '352', '353', '354', '355', '356', '357',
                '358', '359', '360', '361', '362', '363', '364', '365', '366', '367',
                '368', '369', '370', '371', '372', '373', '374', '375', '376', '377',
                '378', '379', '380', '381', '382', '383'
            ]
        else:
            self.store_ids = store_ids
        self.dispensary_name = 'MÜV'
        # Create muv subdirectory
        self.muv_dir = os.path.join(output_dir, 'muv')
        os.makedirs(self.muv_dir, exist_ok=True)
        
    def download(self) -> List[Tuple[str, Dict]]:
        """Download MÜV dispensary data"""
        print(f"Starting {self.dispensary_name} download...")
        
        try:
            # Import MÜV module
            from menuMuv import get_muv_products
            
            results = []
            
            def download_store(store_id):
                """Download data for a single store"""
                try:
                    print(f"   Downloading {self.dispensary_name} store {store_id}...")
                    
                    # Get products from API
                    products = get_muv_products(store_id)
                    
                    if products:
                        # Create filename with timestamp
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"muv_products_store_{store_id}_{timestamp}.json"
                        filepath = os.path.join(self.muv_dir, filename)
                        
                        # Add metadata
                        data_with_metadata = {
                            'timestamp': timestamp,
                            'dispensary': 'muv',
                            'store_id': store_id,
                            'download_time': datetime.now().isoformat(),
                            'product_count': len(products.get('data', [])) if isinstance(products.get('data'), list) else 0,
                            'raw_response_size': len(json.dumps(products)) if products else 0,
                            'downloader_version': '1.0',
                            'products': products
                        }
                        
                        # Save downloaded data to local file
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(data_with_metadata, f, indent=2, ensure_ascii=False)
                        
                        file_size = os.path.getsize(filepath)
                        print(f"   SUCCESS: {self.dispensary_name} store {store_id}: {data_with_metadata['product_count']} products downloaded ({file_size:,} bytes)")
                        print(f"      Saved to: {filename}")
                        return (filepath, data_with_metadata)
                        
                    else:
                        error_msg = f"{self.dispensary_name} store {store_id}: No data received from API"
                        print(f"   ERROR: {error_msg}")
                        raise Exception(error_msg)
                        
                except Exception as e:
                    # Log the per-store error but do NOT raise. We want the
                    # overall downloader to continue and return any successful
                    # store downloads so later upload logic can process them.
                    error_msg = f"{self.dispensary_name} store {store_id}: {str(e)}"
                    print(f"   ERROR: {error_msg}")
                    # Return None to indicate this store failed; the caller
                    # will skip None results and continue processing other
                    # stores.
                    return None
            
            # Process stores in parallel if there are multiple stores
            if len(self.store_ids) > 1:
                print(f"   Processing {len(self.store_ids)} stores in parallel...")
                with ThreadPoolExecutor(max_workers=min(5, len(self.store_ids))) as executor:
                    future_to_store = {executor.submit(download_store, store_id): store_id 
                                      for store_id in self.store_ids}
                    
                    for future in as_completed(future_to_store):
                        store_id = future_to_store[future]
                        try:
                            result = future.result()
                            if result:
                                results.append(result)
                            else:
                                print(f"   WARNING: {self.dispensary_name} store {store_id} failed and returned no result")
                        except Exception as e:
                            # Avoid failing the entire downloader if one store
                            # raised an exception at runtime — just record and
                            # continue so other stores still return their data.
                            print(f"   ERROR processing store {store_id}: {e}")
                            continue
            else:
                # Single store - no need for parallel processing
                for store_id in self.store_ids:
                    result = download_store(store_id)
                    if result:
                        results.append(result)
                    else:
                        print(f"   WARNING: {self.dispensary_name} store {store_id} failed and returned no result (continuing)")
            
            return results
            
        except ImportError as e:
            error_msg = f"Could not import {self.dispensary_name} module: {e}"
            print(f"ERROR: {error_msg}")
            print(f"   Check that menuMuv.py exists in: {os.path.join(grandparent_dir, 'menus')}")
            raise ImportError(error_msg)
        except Exception as e:
            error_msg = f"{self.dispensary_name} download failed: {e}"
            print(f"ERROR: {error_msg}")
            raise Exception(error_msg)
    
    def get_config(self) -> Dict:
        """Get downloader configuration"""
        return {
            'name': self.dispensary_name,
            'store_ids': self.store_ids,
            'output_dir': self.output_dir,
            'enabled': True
        }