"""
Dispensary Data Orchestrator
Automatically downloads data from multiple dispensaries and uploads to Azure Event House
"""
import os
import sys
import json
import time
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple
from azure_config import *

# Add parent directories to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.extend([current_dir, parent_dir, os.path.join(parent_dir, "menus"), 
                os.path.join(parent_dir, "menus", "trulieve"), 
                os.path.join(parent_dir, "azureDataLake")])


# Import download modules - these are the ONLY methods we'll use
try:
    from downloads import MuvDownloader, TrulieveDownloader, SunburnDownloader
    MODULAR_DOWNLOADERS_AVAILABLE = True
    print("✓ Modular downloaders imported successfully")
except ImportError as e:
    print(f"✗ Could not import modular downloaders: {e}")
    MODULAR_DOWNLOADERS_AVAILABLE = False

# Configure logging with proper encoding for Windows
class UnicodeFileHandler(logging.FileHandler):
    """Custom file handler that handles Unicode properly on Windows"""
    def __init__(self, filename, mode='a', encoding='utf-8', delay=False):
        super().__init__(filename, mode, encoding, delay)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        UnicodeFileHandler(os.path.join(current_dir, 'orchestrator.log')),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set console encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

class DispensaryOrchestrator:
    """Main orchestrator for dispensary data collection and upload"""
    
    def __init__(self, output_dir: Optional[str] = None, dev_mode: bool = False):
        self.output_dir = output_dir or os.path.join(current_dir, "downloads")
        self.dev_mode = dev_mode
        self.ensure_output_dir()
        
        # Results tracking
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'downloads': {},
            'uploads': {},
            'errors': [],
            'summary': {}
        }
        
        # Initialize downloaders - ONLY use modular downloaders, no fallbacks
        try:
            self.downloaders = self._init_downloaders()
        except Exception as e:
            logger.error(f"Failed to initialize downloaders: {e}")
            self.downloaders = {}

    def find_all_muv_json_files(self):
        """Recursively find all muv*.json files in downloads/ and downloads/muv/"""
        muv_files = []
        search_dirs = [self.output_dir, os.path.join(self.output_dir, 'muv')]
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                for root, dirs, files in os.walk(search_dir):
                    for file in files:
                        if file.startswith('muv') and file.endswith('.json'):
                            muv_files.append(os.path.join(root, file))
        return muv_files
        
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Output directory: {self.output_dir}")
    
    def _init_downloaders(self) -> Dict:
        """Initialize dispensary downloaders - MODULAR ONLY"""
        downloaders = {}
        
        if not MODULAR_DOWNLOADERS_AVAILABLE:
            logger.error("Modular downloaders not available! Check downloads/ directory and imports.")
            return {}
        
        try:
            # MUV Downloader - Using all known store IDs
            # Based on MUV's 86 Florida locations
            muv_store_ids = [
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
            
            logger.info("Initializing MUV downloader...")
            logger.info(f"MUV: Configured to download from {len(muv_store_ids)} stores")
            downloaders['muv'] = {
                'name': 'MUV',
                'enabled': True,
                'downloader': MuvDownloader(
                    output_dir=self.output_dir,
                    store_ids=muv_store_ids
                )
            }
            
            # Trulieve Downloader  
            logger.info("Initializing Trulieve downloader...")
            
            # Load Trulieve config from menu_config.json
            trulieve_store_ids = None
            trulieve_category_ids = None
            try:
                config_path = os.path.join(parent_dir, "menus", "menu_config.json")
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    
                    trulieve_settings = config.get('trulieve_settings', {})
                    trulieve_store_ids_csv = trulieve_settings.get('store_ids_csv')
                    trulieve_category_ids = trulieve_settings.get('category_ids', [])
                    
                    if trulieve_store_ids_csv and os.path.exists(trulieve_store_ids_csv):
                        import csv
                        with open(trulieve_store_ids_csv, 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            next(reader, None)  # Skip header
                            trulieve_store_ids = [row[0] for row in reader if row]
                        
                        logger.info(f"Trulieve: Loaded {len(trulieve_store_ids)} store IDs from CSV")
                        logger.info(f"Trulieve: Using {len(trulieve_category_ids)} category IDs from config")
                    else:
                        logger.warning("Trulieve: Could not load store IDs from CSV or config")
                else:
                    logger.warning("Trulieve: menu_config.json not found")
            except Exception as e:
                logger.error(f"Trulieve: Error loading config: {e}")
            
            downloaders['trulieve'] = {
                'name': 'Trulieve',
                'enabled': True,
                'downloader': TrulieveDownloader(
                    output_dir=self.output_dir,
                    dev_mode=self.dev_mode,
                    store_ids=trulieve_store_ids if not self.dev_mode else None,
                    category_ids=trulieve_category_ids if not self.dev_mode else None
                )
            }
            
            # Sunburn Downloader
            logger.info("Initializing Sunburn downloader...")
            downloaders['sunburn'] = {
                'name': 'Sunburn',
                'enabled': False,  # Disabled due to anti-bot protection
                'downloader': SunburnDownloader(
                    output_dir=self.output_dir
                )
            }
            
            logger.info(f"Successfully initialized {len(downloaders)} modular downloaders")
            

        except Exception as e:
            logger.error(f"Failed to initialize modular downloaders: {e}")
            return {}
            
        return downloaders
    
    def download_all_dispensaries(self, parallel: bool = True) -> Dict[str, List[Tuple[str, Dict]]]:
        """Download data from all enabled dispensaries using ONLY modular downloaders"""
        logger.info("STARTING DISPENSARY DATA DOWNLOAD")
        logger.info("=" * 60)
        
        if not self.downloaders:
            logger.error("No downloaders available! Cannot proceed.")
            return {}
        
        enabled_dispensaries = [d_id for d_id, config in self.downloaders.items() if config.get('enabled', True)]
        logger.info(f"Enabled dispensaries: {', '.join(enabled_dispensaries)}")
        logger.info("Download mode: Sequential (ensuring all dispensaries complete before uploads)")
        
        download_results = {}
        
        # Always process dispensaries sequentially to ensure complete processing before uploads
        logger.info("Starting sequential downloads...")
        for dispensary_id, config in self.downloaders.items():
            if config.get('enabled', True):
                try:
                    downloader = config['downloader']
                    results = downloader.download()
                    
                    download_results[dispensary_id] = results
                    self.results['downloads'][dispensary_id] = {
                        'success': True,
                        'files': len(results),
                        'files_list': [os.path.basename(filepath) for filepath, _ in results]
                    }
                    logger.info(f"SUCCESS: {dispensary_id} download completed: {len(results)} files")
                except Exception as e:
                    logger.error(f"ERROR: {dispensary_id} download failed: {e}")
                    download_results[dispensary_id] = []
                    self.results['downloads'][dispensary_id] = {
                        'success': False,
                        'error': str(e)
                    }
                    self.results['errors'].append(f"{dispensary_id}: {str(e)}")
        
        # Summary of downloads
        total_files = sum(len(files) for files in download_results.values())
        successful_dispensaries = sum(1 for files in download_results.values() if files)
        
        logger.info(f"\nDOWNLOAD SUMMARY:")
        logger.info(f"   Dispensaries processed: {successful_dispensaries}/{len(enabled_dispensaries)}")
        logger.info(f"   Total files downloaded: {total_files}")
        
        return download_results
    
    def upload_to_azure(self, download_results: Dict[str, List[Tuple[str, Dict]]], delete_after_upload: bool = False, dry_run: bool = False) -> bool:
        """Upload downloaded files to Azure Event House"""
        logger.info("\nSTARTING AZURE EVENT HOUSE UPLOAD")
        logger.info("=" * 60)
        
        try:
            # Import Event House uploader
            from uploadToEventhouse import EventHouseUploader
            
            # Validate configuration
            if not validate_config():
                logger.error("Azure configuration validation failed")
                return False
            
            # Initialize Event House uploader
            logger.info(f"Connecting to Event House: {EVENTHOUSE_CLUSTER}")
            logger.info(f"Database: {EVENTHOUSE_DATABASE}, Table: {EVENTHOUSE_TABLE}")
            
            uploader = EventHouseUploader(
                cluster=EVENTHOUSE_CLUSTER,
                database=EVENTHOUSE_DATABASE,
                table=EVENTHOUSE_TABLE,
                tenant_id=AZURE_TENANT_ID,
                client_id=AZURE_CLIENT_ID,
                client_secret=AZURE_CLIENT_SECRET,
                use_azure_cli=USE_AZURE_CLI,
                column_name=EVENTHOUSE_COLUMN
            )
            
            # Test connection
            logger.info("Testing Event House connection...")
            if not uploader.test_connection():
                logger.error("Could not connect to Event House")
                return False
            
            logger.info("Connected to Event House successfully")
            
            # Collect all files to upload
            all_files_to_upload = []
            for dispensary_id, files in download_results.items():
                if not files:
                    logger.info(f"Skipping {dispensary_id}: No files to upload")
                    continue
                    
                for filepath, data in files:
                    all_files_to_upload.append((dispensary_id, filepath, data))
            
            if not all_files_to_upload:
                logger.info("No files to upload")
                return True
            
            logger.info(f"Uploading {len(all_files_to_upload)} files in parallel...")
            
            # Upload files in parallel
            upload_success = True
            total_uploads = len(all_files_to_upload)
            successful_uploads = 0
            
            def upload_single_file(upload_tuple):
                """Upload a single file to Event House"""
                dispensary_id, filepath, data = upload_tuple
                filename = os.path.basename(filepath)
                
                try:
                    logger.info(f"   Uploading {filename} to Event House...")
                    
                    # Add source metadata
                    source_info = {
                        'dispensary': dispensary_id,
                        'filename': filename,
                        'local_path': filepath,
                        'file_size': os.path.getsize(filepath) if os.path.exists(filepath) else 0
                    }
                    
                    # Upload to Event House (or simulate if dry_run)
                    if dry_run:
                        logger.info(f"   DRY-RUN: Simulating upload of {filename}")
                        success = True
                    else:
                        success = uploader.upload_json(data, source_info)
                    
                    if success:
                        file_size = source_info['file_size']
                        logger.info(f"   SUCCESS: {filename} queued for ingestion ({file_size:,} bytes)")
                        # Delete file after successful upload if requested
                        if delete_after_upload and os.path.exists(filepath) and not dry_run:
                            try:
                                os.remove(filepath)
                                logger.info(f"   Deleted local file after upload: {filename}")
                            except Exception as e:
                                logger.warning(f"   Could not delete {filename}: {e}")
                        return True
                    else:
                        logger.error(f"   ERROR: Failed to upload {filename}")
                        return False
                        
                except Exception as e:
                    logger.error(f"   ERROR: Error uploading {filename}: {e}")
                    return False
            
            # Process uploads in parallel
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_file = {
                    executor.submit(upload_single_file, upload_tuple): upload_tuple[1]
                    for upload_tuple in all_files_to_upload
                }
                
                for future in as_completed(future_to_file):
                    filepath = future_to_file[future]
                    try:
                        success = future.result()
                        if success:
                            successful_uploads += 1
                        else:
                            upload_success = False
                    except Exception as e:
                        logger.error(f"   ERROR: Exception uploading {os.path.basename(filepath)}: {e}")
                        upload_success = False
            
            # Upload summary
            logger.info(f"\nUPLOAD SUMMARY:")
            logger.info(f"   Files uploaded: {successful_uploads}/{total_uploads}")
            logger.info(f"   Upload success rate: {(successful_uploads/total_uploads*100):.1f}%" if total_uploads > 0 else "   No files to upload")
            
            return upload_success
            
        except ImportError as e:
            logger.error(f"Could not import Azure modules: {e}")
            logger.error(f"   Check that azure_config.py and saveJsonToAzureDataLake.py exist in: {os.path.join(parent_dir, 'azureDataLake')}")
            self.results['errors'].append(f"Azure import error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Azure upload failed: {e}")
            self.results['errors'].append(f"Azure upload: {str(e)}")
            return False
    
    def upload_existing_files(self) -> bool:
        """Upload existing downloaded files from the output directory to Azure Event House"""
        logger.info("UPLOADING EXISTING FILES TO AZURE EVENT HOUSE")
        logger.info("=" * 60)
        
        try:
            # Import Event House uploader
            logger.info("Importing EventHouseUploader...")
            try:
                from uploadToEventhouse import EventHouseUploader
                logger.info("✓ EventHouseUploader imported successfully")
            except ImportError as import_e:
                logger.error(f"✗ Failed to import EventHouseUploader: {import_e}")
                logger.error("Check that uploadToEventhouse.py exists and azure-kusto packages are installed")
                return False
            
            # Validate configuration
            logger.info("Validating Azure configuration...")
            if not validate_config():
                logger.error("Azure configuration validation failed")
                return False
            logger.info("✓ Azure configuration validated successfully")
            
            # Initialize Event House uploader
            logger.info(f"Connecting to Event House: {EVENTHOUSE_CLUSTER}")
            logger.info(f"Database: {EVENTHOUSE_DATABASE}, Table: {EVENTHOUSE_TABLE}")
            
            try:
                uploader = EventHouseUploader(
                    cluster=EVENTHOUSE_CLUSTER,
                    database=EVENTHOUSE_DATABASE,
                    table=EVENTHOUSE_TABLE,
                    tenant_id=AZURE_TENANT_ID,
                    client_id=AZURE_CLIENT_ID,
                    client_secret=AZURE_CLIENT_SECRET,
                    use_azure_cli=USE_AZURE_CLI,
                    column_name=EVENTHOUSE_COLUMN
                )
                logger.info("✓ EventHouseUploader initialized")
            except Exception as init_e:
                logger.error(f"✗ Failed to initialize EventHouseUploader: {init_e}")
                logger.error("This could be due to invalid credentials, network issues, or Event House service problems")
                return False
            
            # Test connection
            logger.info("Testing Event House connection...")
            try:
                if not uploader.test_connection():
                    logger.error("Could not connect to Event House")
                    logger.error("Possible causes: invalid credentials, network issues, or Event House service unavailable")
                    return False
                logger.info("✓ Connected to Event House successfully")
            except Exception as conn_e:
                logger.error(f"✗ Event House connection test failed: {conn_e}")
                logger.error("Check your Azure credentials and Event House configuration")
                return False
            
            # Find the most recent download files
            all_files_to_upload = []
            
            # Look for JSON files in subdirectories (muv, trulieve, etc.)
            if os.path.exists(self.output_dir):
                for root, dirs, files in os.walk(self.output_dir):
                    for file in files:
                        if file.endswith('.json'):
                            filepath = os.path.join(root, file)
                            
                            # Determine dispensary from directory structure
                            relative_path = os.path.relpath(root, self.output_dir)
                            dispensary_id = relative_path.split(os.sep)[0] if os.sep in relative_path else 'unknown'
                            
                            try:
                                # Load JSON data
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                
                                all_files_to_upload.append((dispensary_id, filepath, data))
                                logger.info(f"Found file to upload: {os.path.basename(filepath)} ({dispensary_id})")
                                
                            except Exception as e:
                                logger.warning(f"Could not load {filepath}: {e}")
                                continue
            
            if not all_files_to_upload:
                logger.info("No JSON files found to upload")
                return True
            
            logger.info(f"Uploading {len(all_files_to_upload)} existing files in parallel...")
            
            # Upload files in parallel
            upload_success = True
            total_uploads = len(all_files_to_upload)
            successful_uploads = 0
            
            def upload_single_file(upload_tuple):
                """Upload a single file to Event House"""
                dispensary_id, filepath, data = upload_tuple
                filename = os.path.basename(filepath)
                
                try:
                    logger.info(f"   Uploading {filename} to Event House...")
                    
                    # Add source metadata
                    source_info = {
                        'dispensary': dispensary_id,
                        'filename': filename,
                        'local_path': filepath,
                        'file_size': os.path.getsize(filepath) if os.path.exists(filepath) else 0
                    }
                    
                    # Upload to Event House
                    success = uploader.upload_json(data, source_info)
                    
                    if success:
                        file_size = source_info['file_size']
                        logger.info(f"   SUCCESS: {filename} queued for ingestion ({file_size:,} bytes)")
                        return True
                    else:
                        logger.error(f"   ERROR: Failed to upload {filename}")
                        return False
                        
                except Exception as e:
                    logger.error(f"   ERROR: Error uploading {filename}: {e}")
                    return False
            
            # Process uploads in parallel
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_file = {
                    executor.submit(upload_single_file, upload_tuple): upload_tuple[1]
                    for upload_tuple in all_files_to_upload
                }
                
                for future in as_completed(future_to_file):
                    filepath = future_to_file[future]
                    try:
                        success = future.result()
                        if success:
                            successful_uploads += 1
                        else:
                            upload_success = False
                    except Exception as e:
                        logger.error(f"   ERROR: Exception uploading {os.path.basename(filepath)}: {e}")
                        upload_success = False
            
            # Upload summary
            logger.info(f"\nUPLOAD SUMMARY:")
            logger.info(f"   Files uploaded: {successful_uploads}/{total_uploads}")
            logger.info(f"   Upload success rate: {(successful_uploads/total_uploads*100):.1f}%" if total_uploads > 0 else "   No files to upload")
            
            return upload_success
            
        except ImportError as e:
            logger.error(f"Could not import Azure modules: {e}")
            logger.error(f"   Check that azure_config.py and saveJsonToAzureDataLake.py exist in: {os.path.join(parent_dir, 'azureDataLake')}")
            return False
        except Exception as e:
            logger.error(f"Azure upload failed: {e}")
            return False
    
    def run_full_pipeline(self, parallel_downloads: bool = True, upload_to_azure: bool = True) -> Dict:
        """Run the complete dispensary data pipeline"""
        start_time = time.time()
        
        mode_name = "DEVELOPMENT" if self.dev_mode else "PRODUCTION"
        logger.info("DISPENSARY DATA ORCHESTRATOR")
        logger.info("=" * 60)
        logger.info(f"Mode: {mode_name}")
        logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info("Dispensary processing: Sequential (all complete before uploads)")
        logger.info(f"Upload to Azure: {upload_to_azure}")
        logger.info(f"Using modular downloaders: {MODULAR_DOWNLOADERS_AVAILABLE}")
        
        # Phase 1: Download from dispensaries
        logger.info("\nPHASE 1: DOWNLOADING DATA")
        download_results = self.download_all_dispensaries(parallel=parallel_downloads)
        
        # Phase 2: Upload to Azure (if enabled)
        azure_success = True
        if upload_to_azure:
            logger.info("\nPHASE 2: UPLOADING TO AZURE")
            # pass deletion and dry-run flags from self if present
            delete_flag = getattr(self, 'delete_after_upload', False)
            dry_run_flag = getattr(self, 'dry_run_upload', False)
            azure_success = self.upload_to_azure(download_results, delete_after_upload=delete_flag, dry_run=dry_run_flag)
        else:
            logger.info("\nPHASE 2: SKIPPING AZURE UPLOAD (DISABLED)")
        
        # Calculate summary
        end_time = time.time()
        duration = end_time - start_time
        
        total_files = sum(len(files) for files in download_results.values())
        successful_downloads = sum(1 for dispensary_id, files in download_results.items() 
                                 if files and self.results['downloads'].get(dispensary_id, {}).get('success', False))
        
        self.results['summary'] = {
            'start_time': datetime.fromtimestamp(start_time).isoformat(),
            'end_time': datetime.fromtimestamp(end_time).isoformat(),
            'duration_seconds': round(duration, 2),
            'total_dispensaries': len([d for d in self.downloaders.values() if d.get('enabled', True)]),
            'successful_downloads': successful_downloads,
            'total_files_downloaded': total_files,
            'azure_upload_attempted': upload_to_azure,
            'azure_upload_success': azure_success,
            'overall_success': successful_downloads > 0 and (not upload_to_azure or azure_success),
            'modular_downloaders_used': MODULAR_DOWNLOADERS_AVAILABLE
        }
        
        # Save results to file
        self._save_results()
        
        # Print final summary
        self._print_summary()
        
        return self.results
    
    def _save_results(self):
        """Save orchestrator results to JSON files - overall and per dispensary/category"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save overall results
        results_filename = f"orchestrator_results_{timestamp}.json"
        results_filepath = os.path.join(self.output_dir, results_filename)
        
        with open(results_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Overall results saved to: {results_filename}")
        
        # Save separate files for each category (downloads/uploads)
        # Save per-dispensary downloads
        for dispensary_id, info in self.results.get('downloads', {}).items():
            try:
                downloads_filename = f"{dispensary_id}_downloads_{timestamp}.json"
                downloads_filepath = os.path.join(self.output_dir, downloads_filename)
                with open(downloads_filepath, 'w', encoding='utf-8') as f:
                    json.dump(info, f, indent=2, ensure_ascii=False)
                logger.info(f"   {dispensary_id} downloads saved to: {downloads_filename}")
            except Exception as e:
                logger.error(f"Failed to save downloads for {dispensary_id}: {e}")

        # Save per-dispensary uploads if present
        for dispensary_id, info in self.results.get('uploads', {}).items():
            try:
                uploads_filename = f"{dispensary_id}_uploads_{timestamp}.json"
                uploads_filepath = os.path.join(self.output_dir, uploads_filename)
                with open(uploads_filepath, 'w', encoding='utf-8') as f:
                    json.dump(info, f, indent=2, ensure_ascii=False)
                logger.info(f"   {dispensary_id} uploads saved to: {uploads_filename}")
            except Exception as e:
                logger.error(f"Failed to save uploads for {dispensary_id}: {e}")
    
    def _print_summary(self):
        """Print final summary"""
        logger.info("\n" + "=" * 60)
        logger.info("FINAL SUMMARY")
        logger.info("=" * 60)
        
        summary = self.results['summary']
        
        logger.info(f"Duration: {summary['duration_seconds']} seconds")
        logger.info(f"Dispensaries processed: {summary['successful_downloads']}/{summary['total_dispensaries']}")
        logger.info(f"Files downloaded: {summary['total_files_downloaded']}")
        logger.info(f"Modular downloaders: {'YES' if summary['modular_downloaders_used'] else 'NO'}")
        
        if summary['azure_upload_attempted']:
            status = "SUCCESS" if summary['azure_upload_success'] else "FAILED"
            logger.info(f"Azure upload: {status}")
        else:
            logger.info("Azure upload: SKIPPED")
        
        if self.results['errors']:
            logger.info(f"Errors: {len(self.results['errors'])}")
            for error in self.results['errors']:
                logger.info(f"   - {error}")
        
        overall_status = "SUCCESS" if summary['overall_success'] else "FAILED"
        logger.info(f"\nOverall status: {overall_status}")
        
        if summary['overall_success']:
            logger.info("\nPIPELINE COMPLETED SUCCESSFULLY!")
            logger.info("Your dispensary data has been collected and uploaded to Azure Data Lake!")
            logger.info(f"Local files saved in: {self.output_dir}")
        else:
            logger.info("\nPIPELINE COMPLETED WITH ERRORS")
            logger.info("Check the logs above for troubleshooting information.")
        
        # Show file listing
        if os.path.exists(self.output_dir):
            try:
                files = [f for f in os.listdir(self.output_dir) if f.endswith('.json')]
                if files:
                    logger.info(f"\nDownloaded files ({len(files)}):")
                    for file in sorted(files):
                        file_path = os.path.join(self.output_dir, file)
                        file_size = os.path.getsize(file_path)
                        logger.info(f"   {file} ({file_size:,} bytes)")
            except Exception as e:
                logger.warning(f"Could not list output directory: {e}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Dispensary Data Orchestrator')
    parser.add_argument('--output-dir', '-o', help='Output directory for downloaded files')
    parser.add_argument('--no-parallel', action='store_true', help='(Deprecated) Dispensaries are always processed sequentially')
    parser.add_argument('--no-azure', action='store_true', help='Skip Azure upload')
    parser.add_argument('--upload-only', action='store_true', help='Upload existing files only, skip downloading')
    parser.add_argument('--dispensary', '-d', choices=['muv', 'trulieve', 'sunburn'], 
                       help='Run only specific dispensary')
    parser.add_argument('--list-dispensaries', action='store_true', help='List available dispensaries')
    parser.add_argument('--download-only', action='store_true', help='Download only, skip Azure upload')
    parser.add_argument('--dev', '--dev-mode', action='store_true', dest='dev_mode',
                       help='Development mode - use only test stores for Trulieve (faster testing)')
    parser.add_argument('--delete-after-upload', action='store_true', help='Delete local files after successful upload')
    parser.add_argument('--test-stores', type=int, default=0, help='Limit downloads per-dispensary to N stores for testing')
    parser.add_argument('--dry-run', action='store_true', help='Simulate uploads (no network calls, no deletions)')
    
    args = parser.parse_args()
    
    if args.list_dispensaries:
        print("\nAvailable dispensaries:")
        orchestrator = DispensaryOrchestrator()
        for dispensary_id, config in orchestrator.downloaders.items():
            status = "Enabled" if config.get('enabled', True) else "Disabled"
            print(f"   - {config['name']} ({dispensary_id}): {status}")
        return
    
    # Show mode
    if args.dev_mode:
        print("🔧 DEVELOPMENT MODE - Using test stores only")
        print("   Trulieve: port_orange and oakland_park only")
    
    # Create orchestrator
    orchestrator = DispensaryOrchestrator(args.output_dir, dev_mode=args.dev_mode)
    # Attach flags to orchestrator for use during run
    orchestrator.delete_after_upload = args.delete_after_upload
    orchestrator.dry_run_upload = args.dry_run
    
    # Check if we have working downloaders
    if not orchestrator.downloaders:
        print("ERROR: No working downloaders available!")
        print("Check the downloads/ directory and ensure all modules are properly installed.")
        sys.exit(1)
    
    # Filter dispensaries if specific one requested
    if args.dispensary:
        for dispensary_id in list(orchestrator.downloaders.keys()):
            if dispensary_id != args.dispensary:
                orchestrator.downloaders[dispensary_id]['enabled'] = False
        logger.info(f"Running only {args.dispensary}")
    
    # Determine if we should upload to Azure
    upload_to_azure = not (args.no_azure or args.download_only)

    # If test-stores specified, limit store_ids for downloaders that support it
    if args.test_stores and args.test_stores > 0:
        for d_id, cfg in orchestrator.downloaders.items():
            dl = cfg.get('downloader')
            if hasattr(dl, 'store_ids') and isinstance(dl.store_ids, list) and len(dl.store_ids) > args.test_stores:
                original = dl.store_ids
                dl.store_ids = dl.store_ids[:args.test_stores]
                logger.info(f"Limiting {d_id} stores from {len(original)} to {len(dl.store_ids)} for test run")
    
    # Handle upload-only mode
    if args.upload_only:
        logger.info("UPLOAD-ONLY MODE: Uploading existing files without downloading")
        orchestrator = DispensaryOrchestrator(args.output_dir, dev_mode=args.dev_mode)
        upload_success = orchestrator.upload_existing_files()
        exit_code = 0 if upload_success else 1
        sys.exit(exit_code)
    
    # Run the pipeline
    results = orchestrator.run_full_pipeline(
        parallel_downloads=not args.no_parallel,
        upload_to_azure=upload_to_azure
    )
    
    # Exit with appropriate code
    exit_code = 0 if results['summary']['overall_success'] else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()