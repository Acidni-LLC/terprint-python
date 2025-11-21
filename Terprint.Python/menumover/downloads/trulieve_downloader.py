"""
Trulieve Dispensary Download Module
Handles data collection from Trulieve dispensary API using menuTrulieveFixed
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
                os.path.join(grandparent_dir, "menus"),
                os.path.join(grandparent_dir, "menus", "trulieve")])

class TrulieveDownloader:
    """Trulieve dispensary data downloader using menuTrulieveFixed"""
    
    def __init__(self, output_dir: str, dev_mode: bool = False):
        self.output_dir = output_dir
        self.dispensary_name = 'Trulieve'
        self.dev_mode = dev_mode
        # Create trulieve subdirectory
        self.trulieve_dir = os.path.join(output_dir, 'trulieve')
        os.makedirs(self.trulieve_dir, exist_ok=True)
        
    def download(self) -> List[Tuple[str, Dict]]:
        """Download Trulieve dispensary data and split into separate files by store and category"""
        mode_name = "DEVELOPMENT" if self.dev_mode else "PRODUCTION"
        print(f"Starting {self.dispensary_name} download ({mode_name} mode)...")
        
        try:
            # Import ONLY the working collection function - no fallbacks, no other methods
            print(f"   Importing menuTrulieveFixed.collect_all_trulieve_data_browser_format...")
            from menuTrulieveFixed import collect_all_trulieve_data_browser_format
            print(f"   ✓ Import successful")
            
            results = []
            
            # Call ONLY the working function with dev_mode parameter
            print(f"   Calling collect_all_trulieve_data_browser_format(dev_mode={self.dev_mode})...")
            all_data = collect_all_trulieve_data_browser_format(dev_mode=self.dev_mode)
            print(f"   ✓ Function call completed")
            
            # Check if we got valid data
            if not all_data:
                raise Exception("collect_all_trulieve_data_browser_format returned None")
            
            if not isinstance(all_data, dict):
                raise Exception(f"Expected dict, got {type(all_data)}")
            
            summary = all_data.get('summary', {})
            total_products = summary.get('total_products', 0)
            
            print(f"   ✓ Received data with {total_products} total products")
            
            if total_products > 0:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Create separate files for each store/category combination
                stores_data = all_data.get('stores', {})
                print(f"   Creating separate files for {len(stores_data)} store/category combinations...")
                
                for config, store_data in stores_data.items():
                    if not store_data.get('success', False):
                        continue
                    
                    store_id = store_data.get('store_id', 'unknown')
                    category_id = store_data.get('category_id', 'unknown')
                    products = store_data.get('products', [])
                    
                    if not products:
                        continue
                    
                    # Create filename: trulieve_products_store-{name}_cat-{id}_{timestamp}.json
                    filename = f"trulieve_products_store-{store_id}_cat-{category_id}_{timestamp}.json"
                    filepath = os.path.join(self.trulieve_dir, filename)
                    
                    # Create file data structure
                    file_data = {
                        'timestamp': timestamp,
                        'dispensary': 'trulieve',
                        'store_id': store_id,
                        'category_id': category_id,
                        'config': config,
                        'download_time': datetime.now().isoformat(),
                        'downloader_version': '1.0',
                        'download_method': 'menuTrulieveFixed_browser_format',
                        'products_count': len(products),
                        'total_available': store_data.get('total_available', len(products)),
                        'products': products
                    }
                    
                    # Save to file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(file_data, f, indent=2, ensure_ascii=False)
                    
                    file_size = os.path.getsize(filepath)
                    print(f"      ✓ {config}: {len(products)} products saved ({file_size:,} bytes)")
                    
                    results.append((filepath, file_data))
                
                # Also create a summary file with metadata
                summary_filename = f"trulieve_products_summary_{timestamp}.json"
                summary_filepath = os.path.join(self.trulieve_dir, summary_filename)
                
                summary_data = {
                    'timestamp': timestamp,
                    'dispensary': 'trulieve',
                    'download_time': datetime.now().isoformat(),
                    'downloader_version': '1.0',
                    'download_method': 'menuTrulieveFixed_browser_format',
                    'total_products': total_products,
                    'successful_stores': summary.get('successful_stores', 0),
                    'failed_stores': summary.get('failed_stores', 0),
                    'working_configurations': summary.get('working_configurations', []),
                    'failed_configurations': summary.get('failed_configurations', []),
                    'files_created': len(results),
                    'collection_timestamp': all_data.get('collection_timestamp')
                }
                
                with open(summary_filepath, 'w', encoding='utf-8') as f:
                    json.dump(summary_data, f, indent=2, ensure_ascii=False)
                
                print(f"   ✓ Summary saved to: {summary_filename}")
                results.append((summary_filepath, summary_data))
                
                print(f"   SUCCESS: {self.dispensary_name}: {len(results)-1} store/category files + 1 summary file created")
                print(f"      Total products: {total_products} from {summary.get('successful_stores', 0)} store/category combinations")
                
                return results
                
            else:
                # No products collected
                error_msg = f"No products collected (successful_stores: {summary.get('successful_stores', 0)}, failed_stores: {summary.get('failed_stores', 0)})"
                failed_configs = summary.get('failed_configurations', [])
                if failed_configs:
                    error_msg += f", first few failed: {failed_configs[:3]}"
                
                print(f"   ERROR: {error_msg}")
                raise Exception(error_msg)
            
        except ImportError as e:
            error_msg = f"Could not import menuTrulieveFixed: {e}"
            print(f"ERROR: {error_msg}")
            
            # List available files for debugging
            trulieve_dir = os.path.join(grandparent_dir, "menus", "trulieve")
            if os.path.exists(trulieve_dir):
                files = [f for f in os.listdir(trulieve_dir) if f.endswith('.py')]
                print(f"   Available Python files in trulieve dir: {files}")
            
            raise ImportError(error_msg)
        
        except Exception as e:
            error_msg = f"{self.dispensary_name} download failed: {e}"
            print(f"ERROR: {error_msg}")
            print(f"   Error type: {type(e).__name__}")
            print(f"   Error details: {str(e)}")
            raise Exception(error_msg)
    
    def get_config(self) -> Dict:
        """Get downloader configuration"""
        return {
            'name': self.dispensary_name,
            'output_dir': self.output_dir,
            'enabled': True,
            'method': 'menuTrulieveFixed_browser_format_only'
        }

    def test_download(self) -> bool:
        """Test if the Trulieve download function is available"""
        try:
            print(f"Testing {self.dispensary_name} function availability...")
            
            # Test import only
            from menuTrulieveFixed import collect_all_trulieve_data_browser_format
            print(f"   ✓ Successfully imported collect_all_trulieve_data_browser_format")
            
            # Check if it's callable
            if callable(collect_all_trulieve_data_browser_format):
                print(f"   ✓ Function is callable")
                return True
            else:
                print(f"   ✗ Function is not callable")
                return False
            
        except ImportError as e:
            print(f"   ✗ Import failed: {e}")
            return False
        except Exception as e:
            print(f"   ✗ Test failed: {e}")
            return False