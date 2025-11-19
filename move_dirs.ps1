# PowerShell script to move terprint.pwoerbi and terprint.python to new GitHub repositories and remove from current repo.
# Run this from your current repository's root directory.
# Prerequisites: Git installed, GitHub CLI (gh) installed and authenticated (run 'gh auth login' if needed).
# Update variables below with your actual values.

# Set variables
$CurrentRepoPath = Get-Location
$GitHubUsername = "acidni-llc"  # Replace with your GitHub username or org
$NewRepo1Name = "terprint-pwoerbi"
$NewRepo2Name = "terprint-python"
$Dir1 = "terprint.pwoerbi"
$Dir2 = "terprint.python"

# Function to create repo and move directory
function Move-Dir {
    param (
        [string]$Dir,
        [string]$RepoName
    )
    
    $RepoUrl = "https://github.com/$GitHubUsername/$RepoName.git"
    
    if (-not (Test-Path $Dir)) {
        Write-Host "Directory $Dir not found. Skipping."
        return
    }
    
    # Create new GitHub repo (requires gh auth)
    gh repo create $RepoName --public --confirm  # Change --public to --private if needed
    
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