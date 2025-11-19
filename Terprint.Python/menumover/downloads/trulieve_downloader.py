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
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.dispensary_name = 'Trulieve'
        
    def download(self) -> List[Tuple[str, Dict]]:
        """Download Trulieve dispensary data using ONLY the working menuTrulieveFixed function"""
        print(f"Starting {self.dispensary_name} download...")
        
        try:
            # Import ONLY the working collection function - no fallbacks, no other methods
            print(f"   Importing menuTrulieveFixed.collect_all_trulieve_data_browser_format...")
            from menuTrulieveFixed import collect_all_trulieve_data_browser_format
            print(f"   ✓ Import successful")
            
            results = []
            
            # Call ONLY the working function - no TrulieveAPIClient, no other methods
            print(f"   Calling collect_all_trulieve_data_browser_format()...")
            all_data = collect_all_trulieve_data_browser_format()
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
                # Create output file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"trulieve_complete_data_{timestamp}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                # Create enhanced data structure for orchestrator compatibility
                enhanced_data = {
                    # Orchestrator metadata
                    'timestamp': timestamp,
                    'dispensary': 'trulieve',
                    'download_time': datetime.now().isoformat(),
                    'downloader_version': '1.0',
                    'download_method': 'menuTrulieveFixed_browser_format',
                    
                    # Summary data for compatibility
                    'total_products': total_products,
                    'successful_stores': summary.get('successful_stores', 0),
                    'failed_stores': summary.get('failed_stores', 0),
                    'working_configurations': summary.get('working_configurations', []),
                    'failed_configurations': summary.get('failed_configurations', []),
                    
                    # Main products data
                    'products': all_data.get('combined_products', []),
                    
                    # Store breakdown
                    'stores': all_data.get('stores', {}),
                    
                    # For backward compatibility
                    'store_categories': summary.get('working_configurations', []),
                    
                    # Include ALL original data
                    'original_data': all_data
                }
                
                # Save to file
                print(f"   Saving to: {filename}")
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
                
                file_size = os.path.getsize(filepath)
                print(f"   SUCCESS: {self.dispensary_name}: {enhanced_data['total_products']} products from {enhanced_data['successful_stores']} stores downloaded ({file_size:,} bytes)")
                print(f"      Saved to: {filename}")
                
                # Show breakdown
                working_configs = enhanced_data['working_configurations']
                failed_configs = enhanced_data['failed_configurations']
                
                if working_configs:
                    print(f"      Working configurations: {len(working_configs)}")
                    # Show first few
                    for config in working_configs[:3]:
                        store_data = enhanced_data['stores'].get(config, {})
                        product_count = store_data.get('products_count', 0)
                        print(f"         {config}: {product_count} products")
                    if len(working_configs) > 3:
                        print(f"         ... and {len(working_configs) - 3} more")
                
                if failed_configs:
                    print(f"      Failed configurations: {len(failed_configs)}")
                
                results.append((filepath, enhanced_data))
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