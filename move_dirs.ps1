# PowerShell script to move terprint.powerbi and terprint.python to new GitHub repositories and remove from current repo.
# Run this from your current repository's root directory.
# Prerequisites: Git installed, Chocolatey (choco) installed for automatic gh installation.
# Update variables below with your actual values.

# Set variables
$CurrentRepoPath = Get-Location
$GitHubUsername = "Acidni-LLC"  # Acidni-LLC is the only organization used for creating new repos
$NewRepo1Name = "terprint-powerbi"
$NewRepo2Name = "terprint-python"
$Dir1 = "terprint.powerbi"
$Dir2 = "terprint.python"

# Check and install GitHub CLI if not present
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "GitHub CLI (gh) not found. Installing via Chocolatey..."
    # Run choco install as admin if possible, or ensure choco is in PATH
    try {
        choco install gh -y
    } catch {
        Write-Host "Failed to install gh. Ensure Chocolatey is installed and run as Administrator."
        exit
    }
    # Refresh PATH in the current session to recognize newly installed gh
    $chocoPath = "$env:ProgramData\chocolatey\bin"
    if (-not ($env:PATH -split ';' | Where-Object { $_ -eq $chocoPath })) {
        $env:PATH += ";$chocoPath"
    }
    # Verify gh is now available
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        Write-Host "gh still not found after install. Restart PowerShell or add $chocoPath to your system PATH manually."
        exit
    }
    # Prompt for authentication with the Acidni-LLC organization
    Write-Host "Authenticating GitHub CLI with Acidni-LLC organization..."
    gh auth login --hostname github.com --web  # Use web-based login for org access
}

# Function to create repo and move directory
function Move-Dir {
    param (
        [string]$Dir,
        [string]$RepoName
    )
    
    $FullRepoName = "$GitHubUsername/$RepoName"  # Specify org in repo name to create under Acidni-LLC
    $RepoUrl = "https://github.com/$FullRepoName.git"
    
    if (-not (Test-Path $Dir)) {
        Write-Host "Directory $Dir not found. Skipping."
        return
    }
    
    # Create new GitHub repo under Acidni-LLC organization (requires gh auth)
    gh repo create $FullRepoName --public --confirm  # Change --public to --private if needed
    
    # Extract directory to new repo using git subtree
    git subtree push --prefix=$Dir $RepoUrl main
    
    # Remove from current repo
    git rm -r $Dir
    git commit -m "Remove $Dir directory (moved to $RepoName repo)"
}

# Move each directory
Move-Dir -Dir $Dir1 -RepoName $NewRepo1Name
Move-Dir -Dir $Dir2 -RepoName $NewRepo2Name

# Push changes to current repo
git push origin main

Write-Host "Done! Directories moved to new repos. Check for any remaining references in your Blazor project and update as needed."