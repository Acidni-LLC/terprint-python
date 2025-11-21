# PowerShell script to show all JSON data from Event House table
# This script will execute the show_all_data_detailed.kql query

param(
    [string]$ClusterUri = $env:CLUSTER_URI,
    [string]$Database = $env:DATABASE,
    [string]$KqlFile = "show_all_data_detailed.kql"
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

# Load KQL query from file
$kqlPath = Join-Path $PSScriptRoot $KqlFile
if (-not (Test-Path $kqlPath)) {
    Write-Error "KQL file not found: $kqlPath"
    exit 1
}

$query = Get-Content $kqlPath -Raw
Write-Host "📊 Executing KQL query from $KqlFile..." -ForegroundColor Cyan
Write-Host "Query: $query" -ForegroundColor Gray

# Execute query
$queryUrl = "$ClusterUri/v2/rest/query"
$body = @{ db = $Database; csl = $query; properties = @{ Options = @{ results = 'true' } } } | ConvertTo-Json -Depth 20

try {
    $response = Invoke-RestMethod -Method Post -Uri $queryUrl -Headers @{ Authorization = "Bearer $token" } -ContentType 'application/json' -Body $body
    
    # Display results
    if ($response.Tables -and $response.Tables.Count -gt 0) {
        $table = $response.Tables[0]
        Write-Host "✅ Query executed successfully!" -ForegroundColor Green
        Write-Host "📋 Results:" -ForegroundColor Cyan
        
        # Display column headers
        if ($table.Columns) {
            $headers = $table.Columns | ForEach-Object { $_.ColumnName }
            Write-Host ($headers -join " | ") -ForegroundColor Yellow
            Write-Host ("-" * ($headers -join " | ").Length) -ForegroundColor Yellow
        }
        
        # Display rows
        if ($table.Rows) {
            foreach ($row in $table.Rows) {
                Write-Host ($row -join " | ") -ForegroundColor White
            }
        }
        
        Write-Host "`n📊 Total rows: $($table.Rows.Count)" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️  Query executed but no results returned." -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ Query execution failed: $_" -ForegroundColor Red
    exit 1
}