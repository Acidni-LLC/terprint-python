"""
Dispensary Data Orchestrator
Automatically downloads data from multiple dispensaries and uploads to Azure Data Lake
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

# Import Azure config after setting up paths
try:
    from azure_config import *
except ImportError:
    # Will be imported later in upload method
    pass

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
    
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or os.path.join(current_dir, "downloads")
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
        self.downloaders = self._init_downloaders()
        
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
            # MUV Downloader
            logger.info("Initializing MUV downloader...")
            downloaders['muv'] = {
                'name': 'MUV',
                'enabled': True,
                'downloader': MuvDownloader(
                    output_dir=self.output_dir,
                    store_ids=['298']  # Add more store IDs as needed
                )
            }
            
            # Trulieve Downloader  
            logger.info("Initializing Trulieve downloader...")
            downloaders['trulieve'] = {
                'name': 'Trulieve',
                'enabled': True,
                'downloader': TrulieveDownloader(
                    output_dir=self.output_dir
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
        logger.info(f"Download mode: {'Parallel' if parallel else 'Sequential'}")
        
        download_results = {}
        
        if parallel and len(enabled_dispensaries) > 1:
            # Parallel downloads using ONLY modular downloaders
            logger.info("Starting parallel downloads...")
            with ThreadPoolExecutor(max_workers=3) as executor:
                # Submit download tasks
                future_to_dispensary = {}
                for dispensary_id, config in self.downloaders.items():
                    if config.get('enabled', True):
                        downloader = config['downloader']
                        future = executor.submit(downloader.download)
                        future_to_dispensary[future] = dispensary_id
                
                # Collect results
                for future in as_completed(future_to_dispensary):
                    dispensary_id = future_to_dispensary[future]
                    try:
                        results = future.result()
                        download_results[dispensary_id] = results
                        self.results['downloads'][dispensary_id] = {
                            'success': True,
                            'files': len(results),
                            'files_list': [os.path.basename(filepath) for filepath, _ in results]
                        }
                        logger.info(f"SUCCESS: {dispensary_id} parallel download completed: {len(results)} files")
                    except Exception as e:
                        logger.error(f"ERROR: {dispensary_id} parallel download failed: {e}")
                        download_results[dispensary_id] = []
                        self.results['downloads'][dispensary_id] = {
                            'success': False,
                            'error': str(e)
                        }
                        self.results['errors'].append(f"{dispensary_id}: {str(e)}")
        else:
            # Sequential downloads using ONLY modular downloaders
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
    
    def upload_to_azure(self, download_results: Dict[str, List[Tuple[str, Dict]]]) -> bool:
        """Upload downloaded files to Azure Data Lake"""
        logger.info("\nSTARTING AZURE DATA LAKE UPLOAD")
        logger.info("=" * 60)
        
        try:
            # Import Azure modules here to avoid early import issues
            from saveJsonToAzureDataLake import AzureDataLakeManager, get_credential_from_service_principal
            
            # Validate configuration
            if not validate_config():
                logger.error("Azure configuration validation failed")
                return False
            
            # Create credential
            if USE_AZURE_CLI:
                logger.info("Using Azure CLI authentication...")
                credential = None
            else:
                logger.info("Using Service Principal authentication...")
                credential = get_credential_from_service_principal(
                    tenant_id=AZURE_TENANT_ID,
                    client_id=AZURE_CLIENT_ID,
                    client_secret=AZURE_CLIENT_SECRET
                )
            
            # Initialize Data Lake manager
            logger.info(f"Connecting to: {AZURE_STORAGE_ACCOUNT_NAME}")
            dl_manager = AzureDataLakeManager(
                account_name=AZURE_STORAGE_ACCOUNT_NAME,
                container_name=AZURE_CONTAINER_NAME,
                credential=credential
            )
            
            # Test connection
            logger.info("Testing Azure connection...")
            container_info = dl_manager.get_container_info()
            if not container_info:
                logger.error("Could not connect to Azure container")
                return False
            
            logger.info(f"Connected to container: {container_info['name']}")
            
            # Upload files for each dispensary
            upload_success = True
            total_uploads = 0
            successful_uploads = 0
            
            for dispensary_id, files in download_results.items():
                if not files:
                    logger.info(f"Skipping {dispensary_id}: No files to upload")
                    continue
                
                logger.info(f"Uploading {dispensary_id} files...")
                dispensary_results = {'success': True, 'files': []}
                
                for filepath, data in files:
                    try:
                        total_uploads += 1
                        
                        # Generate Azure path
                        filename = os.path.basename(filepath)
                        azure_path = get_file_path(filename, dispensary_id)
                        
                        logger.info(f"   Uploading {filename} to {azure_path}")
                        
                        # Ensure directory exists
                        directory_path = "/".join(azure_path.split("/")[:-1])
                        if directory_path:
                            dl_manager.ensure_directory_exists(directory_path)
                        
                        # Upload file
                        success = dl_manager.save_json_to_data_lake(data, azure_path)
                        
                        if success:
                            successful_uploads += 1
                            
                            # Set content type
                            try:
                                dl_manager.set_content_properties(azure_path, "application/json")
                            except Exception as e:
                                logger.warning(f"Could not set content type for {azure_path}: {e}")
                            
                            # Get file size for logging
                            file_size = os.path.getsize(filepath)
                            logger.info(f"   SUCCESS: {filename} uploaded successfully ({file_size:,} bytes)")
                            
                            dispensary_results['files'].append({
                                'filename': filename,
                                'azure_path': azure_path,
                                'local_path': filepath,
                                'file_size': file_size,
                                'success': True
                            })
                        else:
                            logger.error(f"   ERROR: Failed to upload {filename}")
                            dispensary_results['files'].append({
                                'filename': filename,
                                'azure_path': azure_path,
                                'local_path': filepath,
                                'success': False,
                                'error': 'Upload failed'
                            })
                            dispensary_results['success'] = False
                            upload_success = False
                            
                    except Exception as e:
                        logger.error(f"   ERROR: Error uploading {os.path.basename(filepath)}: {e}")
                        dispensary_results['files'].append({
                            'filename': os.path.basename(filepath),
                            'local_path': filepath,
                            'success': False,
                            'error': str(e)
                        })
                        dispensary_results['success'] = False
                        upload_success = False
                
                self.results['uploads'][dispensary_id] = dispensary_results
            
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
    
    def run_full_pipeline(self, parallel_downloads: bool = True, upload_to_azure: bool = True) -> Dict:
        """Run the complete dispensary data pipeline"""
        start_time = time.time()
        
        logger.info("DISPENSARY DATA ORCHESTRATOR")
        logger.info("=" * 60)
        logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info(f"Parallel downloads: {parallel_downloads}")
        logger.info(f"Upload to Azure: {upload_to_azure}")
        logger.info(f"Using modular downloaders: {MODULAR_DOWNLOADERS_AVAILABLE}")
        
        # Phase 1: Download from dispensaries
        logger.info("\nPHASE 1: DOWNLOADING DATA")
        download_results = self.download_all_dispensaries(parallel=parallel_downloads)
        
        # Phase 2: Upload to Azure (if enabled)
        azure_success = True
        if upload_to_azure:
            logger.info("\nPHASE 2: UPLOADING TO AZURE")
            azure_success = self.upload_to_azure(download_results)
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
        """Save orchestrator results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_filename = f"orchestrator_results_{timestamp}.json"
        results_filepath = os.path.join(self.output_dir, results_filename)
        
        with open(results_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to: {results_filename}")
    
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
    parser.add_argument('--no-parallel', action='store_true', help='Disable parallel downloads')
    parser.add_argument('--no-azure', action='store_true', help='Skip Azure upload')
    parser.add_argument('--dispensary', '-d', choices=['muv', 'trulieve', 'sunburn'], 
                       help='Run only specific dispensary')
    parser.add_argument('--list-dispensaries', action='store_true', help='List available dispensaries')
    parser.add_argument('--download-only', action='store_true', help='Download only, skip Azure upload')
    
    args = parser.parse_args()
    
    if args.list_dispensaries:
        print("\nAvailable dispensaries:")
        orchestrator = DispensaryOrchestrator()
        for dispensary_id, config in orchestrator.downloaders.items():
            status = "Enabled" if config.get('enabled', True) else "Disabled"
            print(f"   - {config['name']} ({dispensary_id}): {status}")
        return
    
    # Create orchestrator
    orchestrator = DispensaryOrchestrator(args.output_dir)
    
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