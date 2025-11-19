"""
Sunburn Dispensary Download Module
Handles data collection from Sunburn dispensary API
"""
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Tuple

# Add parent directories to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.extend([current_dir, parent_dir, grandparent_dir, 
                os.path.join(grandparent_dir, "menus")])

class SunburnDownloader:
    """Sunburn dispensary data downloader"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.dispensary_name = 'Sunburn'
        
    def download(self) -> List[Tuple[str, Dict]]:
        """Download Sunburn dispensary data"""
        print(f"Starting {self.dispensary_name} download...")
        
        try:
            # Import Sunburn module
            from menuSunburn import SunburnAPIClient
            
            results = []
            
            # Initialize client
            print(f"   Initializing {self.dispensary_name} API client...")
            client = SunburnAPIClient()
            
            # Try to get products
            print(f"   Attempting {self.dispensary_name} data collection (trying all methods)...")
            products = client.try_all_methods()
            
            if products:
                # Create filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sunburn_products_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                # Add metadata
                data_with_metadata = {
                    'timestamp': timestamp,
                    'dispensary': 'sunburn',
                    'download_time': datetime.now().isoformat(),
                    'downloader_version': '1.0',
                    'product_count': len(products) if isinstance(products, list) else 0,
                    'method_used': 'try_all_methods',
                    'products': products
                }
                
                # Save downloaded data to local file
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data_with_metadata, f, indent=2, ensure_ascii=False)
                
                file_size = os.path.getsize(filepath)
                print(f"   SUCCESS: {self.dispensary_name}: {data_with_metadata['product_count']} products downloaded ({file_size:,} bytes)")
                print(f"      Saved to: {filename}")
                results.append((filepath, data_with_metadata))
                
            else:
                error_msg = f"{self.dispensary_name}: No data received (likely blocked by anti-bot protection)"
                print(f"   WARNING: {error_msg}")
                # Don't raise exception for Sunburn since it's expected to fail
                return []
            
            return results
            
        except ImportError as e:
            error_msg = f"Could not import {self.dispensary_name} module: {e}"
            print(f"ERROR: {error_msg}")
            print(f"   Check that menuSunburn.py exists in: {os.path.join(grandparent_dir, 'menus')}")
            raise ImportError(error_msg)
        except Exception as e:
            error_msg = f"{self.dispensary_name} download failed: {e}"
            print(f"WARNING: {error_msg}")
            # Don't raise exception for Sunburn since it's expected to fail
            return []
    
    def get_config(self) -> Dict:
        """Get downloader configuration"""
        return {
            'name': self.dispensary_name,
            'output_dir': self.output_dir,
            'enabled': False  # Disabled by default due to anti-bot protection
        }