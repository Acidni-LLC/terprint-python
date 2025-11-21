# Deploy KQL script to Azure Data Explorer / Fabric RTA using VS Code
# Requires: Azure CLI (az) logged in with access to the cluster
# Env vars used (set via .env or VS Code tasks):
#   CLUSTER_URI   e.g., https://<cluster>.<region>.kusto.windows.net
#   DATABASE      e.g., YourDatabase
#   KQL_FILE      default: Trulieve_Fabric_Setup.kql
#   DO_BACKFILL   optional: true/false (not used in this simple run)

param(
    [string]$ClusterUri = $env:CLUSTER_URI,
    [string]$Database = $env:DATABASE,
    [string]$KqlFile = $(if ($env:KQL_FILE) { $env:KQL_FILE } else { 'Trulieve_Fabric_Setup.kql' })
)

# Load .env file if it exists and override param defaults
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    Write-Host "Loading environment from .env file" -ForegroundColor Cyan
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            Write-Host "  Set $key" -ForegroundColor Gray
            
            # Override parameters if not explicitly provided
            if ($key -eq 'CLUSTER_URI' -and -not $PSBoundParameters.ContainsKey('ClusterUri')) {
                $ClusterUri = $value
            }
            if ($key -eq 'DATABASE' -and -not $PSBoundParameters.ContainsKey('Database')) {
                $Database = $value
            }
            if ($key -eq 'KQL_FILE' -and -not $PSBoundParameters.ContainsKey('KqlFile')) {
                $KqlFile = $value
            }
        }
    }
}

if (-not $ClusterUri) { Write-Error 'CLUSTER_URI env var not set.'; exit 1 }
if (-not $Database) { Write-Error 'DATABASE env var not set.'; exit 1 }
if (-not (Test-Path $KqlFile)) { Write-Error "KQL file not found: $KqlFile"; exit 1 }

Write-Host "Reading KQL from $KqlFile" -ForegroundColor Cyan
$csl = Get-Content -Raw -Path $KqlFile

Write-Host "Getting access token via Service Principal..." -ForegroundColor Cyan

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
            Write-Host "  OK Token acquired via Service Principal" -ForegroundColor Green
        }
        catch {
            Write-Warning "Failed to get token with Fabric resource, trying Kusto resource..."
            # Try Kusto resource as fallback
            try {
                $tokenBody.resource = "https://kusto.kusto.windows.net"
                $tokenResponse = Invoke-RestMethod -Method Post -Uri $tokenUrl -Body $tokenBody -ContentType "application/x-www-form-urlencoded"
                $token = $tokenResponse.access_token
                Write-Host "  OK Token acquired via Service Principal (Kusto)" -ForegroundColor Green
            }
            catch {
                Write-Warning "Service Principal authentication failed: $_"
            }
        }
    }
    else {
        Write-Warning "Service Principal credentials not found or incomplete in azure_config.py"
    }
}
else {
    Write-Warning "azure_config.py not found, cannot attempt Service Principal authentication."
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

$mgmt = "$ClusterUri/v1/rest/mgmt"

# Split the KQL script into individual control commands and post each separately
# Control commands typically start with a leading dot (e.g. .create, .alter)
$lines = $csl -split "`r?`n"
$commands = @()
$current = ""
foreach ($line in $lines) {
    if ($line -match '^\s*\.') {
        if ($current -ne "") { $commands += $current.TrimEnd() }
        $current = $line + "`n"
    }
    else {
        if ($current -ne "") { $current += $line + "`n" }
    }
}
if ($current -ne "") { $commands += $current.TrimEnd() }

if ($commands.Count -eq 0) {
    Write-Warning "No control commands found in KQL file; posting entire script as one command."
    $commands = @($csl)
}

Write-Host "Posting $($commands.Count) command(s) to $mgmt (database: $Database)" -ForegroundColor Cyan

$responses = @()
foreach ($cmd in $commands) {
    $firstLine = ($cmd -split "`n")[0]
    Write-Host "Posting command: $firstLine" -ForegroundColor Cyan
    $body = @{ db = $Database; csl = $cmd; properties = @{ Options = @{ results = 'true' } } } | ConvertTo-Json -Depth 20
    try {
        $resp = Invoke-RestMethod -Method Post -Uri $mgmt -Headers @{ Authorization = "Bearer $token" } -ContentType 'application/json' -Body $body
        $responses += $resp
        Write-Host "  ✓ Success" -ForegroundColor Green
    }
    catch {
        Write-Warning "Command failed (continuing): $_"
        continue
    }
}

Write-Host 'Deployment complete.' -ForegroundColor Green
Write-Output $responses

# Deploy KQL script to Azure Data Explorer / Fabric RTA using VS Code
# Requires: Azure CLI (az) logged in with access to the cluster
# Env vars used (set via .env or VS Code tasks):
#   CLUSTER_URI   e.g., https://<cluster>.<region>.kusto.windows.net
#   DATABASE      e.g., YourDatabase
#   KQL_FILE      default: Trulieve_Fabric_Setup.kql
#   DO_BACKFILL   optional: true/false (not used in this simple run)

param(
    [string]$ClusterUri = $env:CLUSTER_URI,
    [string]$Database = $env:DATABASE,
    [string]$KqlFile = $(if ($env:KQL_FILE) { $env:KQL_FILE } else { 'Trulieve_Fabric_Setup.kql' })
)

# Load .env file if it exists and override param defaults
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    Write-Host "Loading environment from .env file" -ForegroundColor Cyan
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            Write-Host "  Set $key" -ForegroundColor Gray
            
            # Override parameters if not explicitly provided
            if ($key -eq 'CLUSTER_URI' -and -not $PSBoundParameters.ContainsKey('ClusterUri')) {
                $ClusterUri = $value
            }
            if ($key -eq 'DATABASE' -and -not $PSBoundParameters.ContainsKey('Database')) {
                $Database = $value
            }
            if ($key -eq 'KQL_FILE' -and -not $PSBoundParameters.ContainsKey('KqlFile')) {
                $KqlFile = $value
            }
        }
    }
}

if (-not $ClusterUri) { Write-Error 'CLUSTER_URI env var not set.'; exit 1 }
if (-not $Database) { Write-Error 'DATABASE env var not set.'; exit 1 }
if (-not (Test-Path $KqlFile)) { Write-Error "KQL file not found: $KqlFile"; exit 1 }

Write-Host "Reading KQL from $KqlFile" -ForegroundColor Cyan
$csl = Get-Content -Raw -Path $KqlFile

Write-Host "Getting access token via Service Principal..." -ForegroundColor Cyan

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
            Write-Host "  âœ“ Token acquired via Service Principal" -ForegroundColor Green
        }
        catch {
            Write-Warning "Failed to get token with Fabric resource, trying Kusto resource..."
            # Try Kusto resource as fallback
            try {
                $tokenBody.resource = "https://kusto.kusto.windows.net"
                $tokenResponse = Invoke-RestMethod -Method Post -Uri $tokenUrl -Body $tokenBody -ContentType "application/x-www-form-urlencoded"
                $token = $tokenResponse.access_token
                Write-Host " Token acquired via Service Principal (Kusto)" -ForegroundColor Green
            }
            catch {
                Write-Warning "Service Principal authentication failed: $_"
            }
        }
    }
    else {
        Write-Warning "Service Principal credentials not found or incomplete in azure_config.py"
    }
}
else {
    Write-Warning "azure_config.py not found, cannot attempt Service Principal authentication."
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

$mgmt = "$ClusterUri/v1/rest/mgmt"

# Split the KQL script into individual control commands and post each separately
# Control commands typically start with a leading dot (e.g. .create, .alter)
$lines = $csl -split "`r?`n"
$commands = @()
$current = ""
foreach ($line in $lines) {
    if ($line -match '^\s*\.') {
        if ($current -ne "") { $commands += $current.TrimEnd() }
        $current = $line + "`n"
    }
    else {
        if ($current -ne "") { $current += $line + "`n" }
    }
}
if ($current -ne "") { $commands += $current.TrimEnd() }

if ($commands.Count -eq 0) {
    Write-Warning "No control commands found in KQL file; posting entire script as one command."
    $commands = @($csl)
}

Write-Host "Posting $($commands.Count) command(s) to $mgmt (database: $Database)" -ForegroundColor Cyan

$responses = @()
foreach ($cmd in $commands) {
    $firstLine = ($cmd -split "`n")[0]
    Write-Host "Posting command: $firstLine" -ForegroundColor Cyan
    $body = @{ db = $Database; csl = $cmd; properties = @{ Options = @{ results = 'true' } } } | ConvertTo-Json -Depth 20
    try {
        $resp = Invoke-RestMethod -Method Post -Uri $mgmt -Headers @{ Authorization = "Bearer $token" } -ContentType 'application/json' -Body $body
        $responses += $resp
        Write-Host "  ✓ Success" -ForegroundColor Green
    }
    catch {
        Write-Warning "Command failed (continuing): $_"
        continue
    }
}

Write-Host 'Deployment complete.' -ForegroundColor Green
Write-Output $responses
