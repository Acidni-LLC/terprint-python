# Dispensary Orchestrator Changelog

All notable changes to the Dispensary Data Orchestrator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-18

### Added

#### Core Orchestrator (`dispensaryOrchestrator.py`)
- **NEW**: Complete dispensary data orchestration system
- **NEW**: Multi-dispensary support for MÜV, Trulieve, and Sunburn
- **NEW**: Parallel and sequential download modes
- **NEW**: Comprehensive Azure Data Lake integration
- **NEW**: Advanced logging with file and console output
- **NEW**: Detailed error tracking and reporting
- **NEW**: JSON results export with performance metrics
- **NEW**: Command-line interface with multiple options

#### Download Capabilities
- **NEW**: Automated data collection from multiple dispensary APIs
- **NEW**: Local file storage with timestamp-based naming
- **NEW**: Metadata enrichment for downloaded data
- **NEW**: File size tracking and reporting
- **NEW**: Product count validation and logging
- **NEW**: Store/category breakdown reporting (Trulieve)

#### Upload Capabilities  
- **NEW**: Automated Azure Data Lake Gen2 upload
- **NEW**: Directory structure creation and management
- **NEW**: Content type setting for JSON files
- **NEW**: Upload progress tracking with success rates
- **NEW**: Retry logic and error handling
- **NEW**: File verification after upload

#### Configuration System
- **NEW**: Dispensary configuration with enable/disable flags
- **NEW**: Store ID management for multi-location dispensaries
- **NEW**: Flexible output directory configuration
- **NEW**: Azure authentication method selection
- **NEW**: Parallel processing configuration

#### Command Line Interface
- **NEW**: `--dispensary` - Run specific dispensary only
- **NEW**: `--download-only` - Skip Azure upload
- **NEW**: `--no-azure` - Alternative skip Azure option
- **NEW**: `--no-parallel` - Disable parallel processing
- **NEW**: `--output-dir` - Custom output directory
- **NEW**: `--list-dispensaries` - Show available dispensaries

#### Error Handling & Diagnostics
- **NEW**: Module import validation with helpful error messages
- **NEW**: Azure connection testing before upload
- **NEW**: Graceful degradation when modules unavailable
- **NEW**: Detailed file path guidance for troubleshooting
- **NEW**: Import path validation and setup
- **NEW**: Configuration validation before execution

#### Reporting & Monitoring
- **NEW**: Real-time progress logging with emojis
- **NEW**: Phase-based execution reporting (Download → Upload)
- **NEW**: Summary statistics with success rates
- **NEW**: File listing in final summary
- **NEW**: Duration tracking and performance metrics
- **NEW**: Error categorization for troubleshooting

### Changed

#### Import Strategy
- **FIXED**: Moved Azure imports inside methods to prevent early import failures
- **IMPROVED**: Enhanced sys.path setup for reliable module loading
- **IMPROVED**: Better error messages for missing dependencies

#### MÜV Integration
- **ENHANCED**: Added detailed download progress logging
- **ENHANCED**: Improved metadata with raw response size tracking
- **ENHANCED**: Better error handling for API failures
- **ENHANCED**: File size reporting after download

#### Trulieve Integration
- **ENHANCED**: Full store/category combination support
- **ENHANCED**: Detailed store breakdown reporting
- **ENHANCED**: Enhanced metadata with orchestrator version
- **ENHANCED**: Better progress indication during data collection

#### Sunburn Integration
- **ENHANCED**: Anti-bot protection detection and reporting
- **ENHANCED**: Method tracking in metadata
- **ENHANCED**: Graceful handling of blocked requests

#### Azure Integration
- **ENHANCED**: Connection testing before upload attempts
- **ENHANCED**: Better credential handling (CLI vs Service Principal)
- **ENHANCED**: Directory creation with proper error handling
- **ENHANCED**: Content type management for uploaded files
- **ENHANCED**: Upload progress tracking with detailed logging

### Technical Improvements

#### Performance
- **NEW**: Parallel download support with ThreadPoolExecutor
- **NEW**: Configurable worker thread limits
- **NEW**: Efficient file handling with proper encoding
- **NEW**: Memory-conscious JSON processing

#### Security
- **NEW**: Credential validation before execution
- **NEW**: Secure import handling to prevent injection
- **NEW**: Proper file path handling and validation

#### Reliability
- **NEW**: Comprehensive exception handling at all levels
- **NEW**: Retry logic for failed operations
- **NEW**: Graceful degradation when services unavailable
- **NEW**: Proper resource cleanup and management

### Infrastructure

#### Supporting Files
- **NEW**: `orchestrator_config.py` - Centralized configuration management
- **NEW**: `requirements.txt` - Dependency specification
- **NEW**: `run_orchestrator.bat` - Windows batch execution script
- **NEW**: `run_orchestrator.ps1` - PowerShell execution script
- **NEW**: `README.md` - Comprehensive documentation

#### Documentation
- **NEW**: Complete API documentation with examples
- **NEW**: Configuration guide with all options
- **NEW**: Troubleshooting section with common issues
- **NEW**: Usage examples for different scenarios
- **NEW**: File structure documentation

### Dependencies

#### Required Python Packages
- **NEW**: `requests>=2.31.0` - HTTP client for API calls
- **NEW**: `azure-storage-file-datalake>=12.8.0` - Azure Data Lake SDK
- **NEW**: `azure-identity>=1.12.0` - Azure authentication
- **NEW**: `python-dateutil>=2.8.0` - Date/time utilities

#### Optional Dependencies
- **NEW**: `schedule>=1.2.0` - Future scheduling support
- **NEW**: `croniter>=1.3.0` - Cron expression parsing
- **NEW**: Development tools (pytest, black, flake8)

### Integration Points

#### Existing Module Integration
- **INTEGRATED**: `menuMuv.py` - MÜV dispensary API client
- **INTEGRATED**: `menuTrulieveFixed.py` - Trulieve API client with page size optimization
- **INTEGRATED**: `menuSunburn.py` - Sunburn API client with anti-bot handling
- **INTEGRATED**: `azure_config.py` - Azure configuration management
- **INTEGRATED**: `saveJsonToAzureDataLake.py` - Core Azure upload functionality

#### Data Flow
- **NEW**: Dispensary APIs → Local JSON files → Azure Data Lake
- **NEW**: Metadata enrichment at each stage
- **NEW**: Progress tracking throughout pipeline
- **NEW**: Error handling with rollback capabilities

### Output Structure

#### Local Files
```
downloads/
├── orchestrator_results_YYYYMMDD_HHMMSS.json
├── muv_products_store_298_YYYYMMDD_HHMMSS.json
├── trulieve_complete_data_YYYYMMDD_HHMMSS.json
└── sunburn_products_YYYYMMDD_HHMMSS.json
```

#### Azure Data Lake Structure
```
container/
├── muv/
│   └── muv_products_store_298_YYYYMMDD_HHMMSS.json
├── trulieve/
│   └── trulieve_complete_data_YYYYMMDD_HHMMSS.json
└── sunburn/
    └── sunburn_products_YYYYMMDD_HHMMSS.json
```

### Performance Metrics

#### Processing Capabilities
- **NEW**: Parallel processing of multiple dispensaries
- **NEW**: Optimized page size (50) for Trulieve API calls
- **NEW**: Efficient memory usage for large datasets
- **NEW**: Minimal file I/O operations

#### Monitoring
- **NEW**: Real-time progress indicators
- **NEW**: Success rate calculations
- **NEW**: Duration tracking for performance analysis
- **NEW**: File size reporting for storage planning

### Future Roadmap

#### Planned Features
- [ ] Scheduled automated runs with cron support
- [ ] Browser automation for anti-bot protection bypass
- [ ] Real-time monitoring dashboard
- [ ] Data validation and quality checks
- [ ] Power BI refresh integration
- [ ] Additional dispensary integrations

#### Known Issues
- **LIMITATION**: Sunburn dispensary blocked by anti-bot protection
- **ENHANCEMENT**: Browser automation needed for certain APIs
- **IMPROVEMENT**: Retry logic could be more sophisticated

### Usage Examples

#### Basic Operations
```bash
# Download and upload all dispensaries
python dispensaryOrchestrator.py

# Download only (no Azure upload)
python dispensaryOrchestrator.py --download-only

# Run specific dispensary
python dispensaryOrchestrator.py --dispensary trulieve

# Custom output directory
python dispensaryOrchestrator.py --output-dir "C:\MyData"
```

#### Advanced Operations
```bash
# Sequential processing with custom directory
python dispensaryOrchestrator.py --no-parallel --output-dir "C:\DataArchive"

# Trulieve only with no Azure upload
python dispensaryOrchestrator.py --dispensary trulieve --no-azure

# List available dispensaries
python dispensaryOrchestrator.py --list-dispensaries
```

### Migration Notes

#### From Previous Versions
- **BREAKING**: First version - no migration needed
- **NEW**: All functionality is additive to existing codebase
- **COMPATIBLE**: Integrates with existing dispensary API scripts

#### Configuration Changes
- **NEW**: All configuration is new
- **REQUIRED**: Azure configuration must be set up in `azure_config.py`
- **OPTIONAL**: Orchestrator-specific config in `orchestrator_config.py`

---

## Version History

### [1.0.0] - 2025-11-18
- Initial release of Dispensary Data Orchestrator
- Complete multi-dispensary automation pipeline
- Azure Data Lake integration
- Comprehensive error handling and reporting

---

## Contributors

- **AI Assistant (GitHub Copilot)** - Primary development and implementation
- **User (JamiesonGill)** - Requirements definition and testing

## License

This project is part of the Acidni LLC Terprint system.

---

*This changelog follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format for clear and consistent documentation of changes.*