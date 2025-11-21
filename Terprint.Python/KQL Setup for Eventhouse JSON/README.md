
# Event House KQL Scripts and Tools

This directory contains KQL (Kusto Query Language) scripts and PowerShell tools for managing your Event House data after migrating from Azure Data Lake.

## 📋 Available Scripts

### KQL Query Files
- `Trulieve_Fabric_Setup.kql` – Tables + Update Policies parsing JSON from `onelakejsonparser(data)`, filtered to `dispensary == "trulieve"`
- `show_all_data.kql` - Basic query to show all JSON data ordered by ingestion time
- `show_all_data_detailed.kql` - Detailed query extracting metadata (filename, dispensary, upload_timestamp)
- `show_raw_json.kql` - Simple query showing raw JSON data with limit
- `drop_trulieve_tables.kql` - Lists tables with "trulieve" in name and generates drop commands
- `drop_trulieve_tables_manual.kql` - Manual drop commands with safety warnings

### PowerShell Tools
- `deploy.ps1` – Generic KQL deployment script (loads any .kql file)
- `show_eventhouse_data.ps1` - Execute and display results from show_all_data_detailed.kql
- `drop_trulieve_tables.ps1` - Automatically find and drop all tables containing "trulieve"

### Other Files
- `deploy.sh` – Bash equivalent of deploy.ps1
- `.vscode/tasks.json` – VS Code tasks to run the deployment from the Command Palette
- `.env.example` – Sample environment variables; copy to `.env` and set values

## 🚀 Quick Start

### 1. Configure Environment
Create a `.env` file in this directory:
```
CLUSTER_URI=https://trd-vdf84t56eet09mgd66.z5.kusto.fabric.microsoft.com
DATABASE=terprinteventhouse
```

### 2. View Your Data
```powershell
# Show all JSON data with metadata
.\show_eventhouse_data.ps1

# Or use the generic deploy script
.\deploy.ps1 -KqlFile "show_all_data_detailed.kql"
```

### 3. Clean Up Old Tables (if needed)
```powershell
# Automatically drop all tables with "trulieve" in the name
.\drop_trulieve_tables.ps1
```

## 🔧 Authentication

Scripts automatically try authentication in this order:
1. Service Principal (from `..\menumover\azure_config.py`)
2. Azure CLI (Fabric resource)
3. Azure CLI (Kusto resource)

## 📊 KQL Query Examples

### Show All Data
```kql
onelakejsonparser
| order by ingestion_time() desc
| project data
```

### Show Data with Metadata
```kql
onelakejsonparser
| extend
    filename = data.filename,
    dispensary = data.dispensary,
    upload_timestamp = data.upload_timestamp
| order by ingestion_time() desc
| project ingestion_time(), filename, dispensary, data
```

### Find Tables to Drop
```kql
.show tables
| where TableName contains "trulieve"
| project TableName, drop_command = strcat(".drop table ", TableName, " ifexists")
```

## 🛠️ Manual Operations

If you prefer to run KQL directly in Azure Portal or Azure CLI:

```bash
# Using Azure CLI
az kusto query --cluster-name "trd-vdf84t56eet09mgd66.z5" \
               --database-name "terprinteventhouse" \
               --query-file "show_all_data_detailed.kql"
```

## 📁 File Structure
```
KQL Setup for Eventhouse JSON/
├── .env                           # Environment configuration
├── Trulieve_Fabric_Setup.kql      # Original Trulieve setup
├── show_all_data.kql             # Basic data display
├── show_all_data_detailed.kql    # Detailed data with metadata
├── show_raw_json.kql             # Raw JSON display
├── drop_trulieve_tables.kql      # Table cleanup query
├── drop_trulieve_tables_manual.kql # Manual drop commands
├── deploy.ps1                    # Generic KQL deployment
├── deploy.sh                     # Bash deployment
├── show_eventhouse_data.ps1      # Data display tool
├── drop_trulieve_tables.ps1      # Automated table cleanup
├── .vscode/tasks.json            # VS Code tasks
└── .env.example                  # Environment template
```

## ⚠️ Safety Notes

- **Table Deletion**: The `drop_trulieve_tables.ps1` script will permanently delete tables and all their data
- **Authentication**: Ensure your Service Principal or Azure CLI has appropriate permissions
- **Testing**: Always test queries in a development environment first

## 🔍 Troubleshooting

### No Data Appearing
- Check table name case sensitivity (`onelakejsonparser` vs `OnelakeJsonParser`)
- Verify streaming ingestion is enabled on the table
- Check authentication permissions

### Authentication Issues
- Ensure Service Principal credentials are in `azure_config.py`
- Try `az login` if using Azure CLI
- Check tenant ID, client ID, and client secret

### Query Errors
- Verify cluster URI and database name in `.env`
- Check KQL syntax in the query files
- Ensure table exists: `.show tables`

## 📞 Support

If you encounter issues:
1. Check the PowerShell error messages
2. Verify your `.env` configuration
3. Test authentication separately
4. Review the KQL syntax in Azure Portal
