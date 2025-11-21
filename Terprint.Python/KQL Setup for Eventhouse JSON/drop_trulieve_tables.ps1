# PowerShell script to drop all tables containing "trulieve" in the name
# This script will automatically find and drop all matching tables

param(
    [string]$ClusterUri = $env:CLUSTER_URI,
    [string]$Database = $env:DATABASE
)

# Load .env file if it exists
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    Write-Host "Loading environment from .env file" -ForegroundColor Cyan
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            if ($key -eq 'CLUSTER_URI' -and -not $PSBoundParameters.ContainsKey('ClusterUri')) {
                $ClusterUri = $value
            }
            if ($key -eq 'DATABASE' -and -not $PSBoundParameters.ContainsKey('Database')) {
                $Database = $value
            }
        }
    }
}

if (-not $ClusterUri) { Write-Error 'CLUSTER_URI env var not set.'; exit 1 }
if (-not $Database) { Write-Error 'DATABASE env var not set.'; exit 1 }

Write-Host "🔍 Finding tables with 'trulieve' in the name..." -ForegroundColor Cyan

# Load service principal credentials from azure_config.py
$configPath = Join-Path $PSScriptRoot "..\menumover\azure_config.py"
if (Test-Path $configPath) {
    $config = Get-Content $configPath | Select-String -Pattern '(AZURE_TENANT_ID|AZURE_CLIENT_ID|AZURE_CLIENT_SECRET)\s*=\s*"([^"]+)"'
    $tenantId = ($config | Where-Object { $_ -match 'AZURE_TENANT_ID' } | ForEach-Object { $_.Matches.Groups[2].Value })
    $clientId = ($config | Where-Object { $_ -match 'AZURE_CLIENT_ID' } | ForEach-Object { $_.Matches.Groups[2].Value })
    $clientSecret = ($config | Where-Object { $_ -match 'AZURE_CLIENT_SECRET' } | ForEach-Object { $_.Matches.Groups[2].Value })
    
    if ($tenantId -and $clientId -and $clientSecret) {
        Write-Host "  Found credentials in azure_config.py" -ForegroundColor Gray
        
        # Get token using service principal
        $tokenBody = @{
            grant_type    = "client_credentials"
            client_id     = $clientId
            client_secret = $clientSecret
            resource      = "https://api.fabric.microsoft.com"
        }
        
        $tokenUrl = "https://login.microsoftonline.com/$tenantId/oauth2/token"
        
        # Try Fabric resource first
        try {
            $tokenResponse = Invoke-RestMethod -Method Post -Uri $tokenUrl -Body $tokenBody -ContentType "application/x-www-form-urlencoded"
            $token = $tokenResponse.access_token
            Write-Host "  ✓ Token acquired via Service Principal" -ForegroundColor Green
        }
        catch {
            Write-Warning "Failed to get token with Fabric resource, trying Kusto resource..."
            # Try Kusto resource as fallback
            try {
                $tokenBody.resource = "https://kusto.kusto.windows.net"
                $tokenResponse = Invoke-RestMethod -Method Post -Uri $tokenUrl -Body $tokenBody -ContentType "application/x-www-form-urlencoded"
                $token = $tokenResponse.access_token
                Write-Host "  ✓ Token acquired via Service Principal (Kusto)" -ForegroundColor Green
            }
            catch {
                Write-Warning "Service Principal authentication failed: $_"
            }
        }
    }
}

# Fallback to Azure CLI if service principal fails
if (-not $token) {
    Write-Warning "Service Principal auth failed, trying Azure CLI..."
    try {
        $token = (az account get-access-token --resource https://api.fabric.microsoft.com | ConvertFrom-Json).accessToken
    }
    catch {
        Write-Warning "Azure CLI Fabric auth failed, trying Kusto resource..."
        try {
            $token = (az account get-access-token --resource https://kusto.kusto.windows.net | ConvertFrom-Json).accessToken
        }
        catch {
            Write-Warning "Azure CLI authentication also failed: $_"
        }
    }
}

if (-not $token) { Write-Error 'Failed to acquire token.'; exit 1 }

# Query to find tables with "trulieve" in the name
$query = ".show tables | where TableName contains `"trulieve`" | project TableName"
$mgmt = "$ClusterUri/v1/rest/mgmt"
$body = @{ db = $Database; csl = $query; properties = @{ Options = @{ results = 'true' } } } | ConvertTo-Json -Depth 20

Write-Host "Querying for tables with 'trulieve' in the name..." -ForegroundColor Cyan
$response = Invoke-RestMethod -Method Post -Uri $mgmt -Headers @{ Authorization = "Bearer $token" } -ContentType 'application/json' -Body $body

# Extract table names from response
$tablesToDrop = @()
if ($response.Tables) {
    foreach ($table in $response.Tables) {
        if ($table.TableName) {
            $tablesToDrop += $table.TableName
        }
    }
}

if ($tablesToDrop.Count -eq 0) {
    Write-Host "✅ No tables found with 'trulieve' in the name." -ForegroundColor Green
    exit 0
}

Write-Host "🗑️  Found $($tablesToDrop.Count) table(s) to drop:" -ForegroundColor Yellow
foreach ($table in $tablesToDrop) {
    Write-Host "  - $table" -ForegroundColor Yellow
}

# Confirm before dropping
$confirmation = Read-Host "⚠️  This will permanently delete these tables and all their data. Continue? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Operation cancelled." -ForegroundColor Gray
    exit 0
}

# Drop each table
foreach ($table in $tablesToDrop) {
    Write-Host "Dropping table: $table..." -ForegroundColor Cyan
    
    $dropCommand = ".drop table $table ifexists"
    $body = @{ db = $Database; csl = $dropCommand; properties = @{ Options = @{ results = 'true' } } } | ConvertTo-Json -Depth 20
    
    try {
        $response = Invoke-RestMethod -Method Post -Uri $mgmt -Headers @{ Authorization = "Bearer $token" } -ContentType 'application/json' -Body $body
        Write-Host "  ✅ Dropped table: $table" -ForegroundColor Green
    }
    catch {
        Write-Host "  ❌ Failed to drop table $table : $_" -ForegroundColor Red
    }
}

Write-Host "🎉 Table cleanup complete!" -ForegroundColor Green