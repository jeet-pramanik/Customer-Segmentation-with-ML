# Customer Segmentation ML - GitHub Publishing Script
# PowerShell Script for Windows
# Author: GitHub Copilot
# Date: October 19, 2025

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Customer Segmentation ML - GitHub Publisher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
Write-Host "Checking Git installation..." -ForegroundColor Yellow
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git first:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "2. Run the installer with default settings" -ForegroundColor White
    Write-Host "3. Restart your terminal and run this script again" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to open Git download page..."
    Start-Process "https://git-scm.com/download/win"
    exit 1
}

Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
Write-Host ""

# Configure Git
Write-Host "Configuring Git..." -ForegroundColor Yellow
git config --global user.name "jeet-pramanik"
git config --global user.email "jeetpramanik516@gmail.com"
Write-Host "✅ Git configured successfully" -ForegroundColor Green
Write-Host ""

# Check if repository already exists
if (Test-Path ".git") {
    Write-Host "⚠️  Git repository already exists!" -ForegroundColor Yellow
    $response = Read-Host "Do you want to continue? This will add new changes. (y/n)"
    if ($response -ne "y") {
        Write-Host "Operation cancelled." -ForegroundColor Red
        exit 0
    }
} else {
    # Initialize Git repository
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Repository initialized" -ForegroundColor Green
    Write-Host ""
}

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files added" -ForegroundColor Green
Write-Host ""

# Check if there are changes to commit
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "⚠️  No changes to commit!" -ForegroundColor Yellow
    Write-Host "All files are already committed." -ForegroundColor White
} else {
    # Create commit
    Write-Host "Creating commit..." -ForegroundColor Yellow
    $commitMessage = @"
Initial commit: Complete Customer Segmentation ML System

- Implemented data loading with synthetic data generation
- Created preprocessing pipeline with feature engineering
- Built 4 clustering algorithms (K-Means, DBSCAN, Hierarchical, GMM)
- Added comprehensive evaluation metrics
- Developed customer profiling and marketing strategies
- Created visualization suite (matplotlib, seaborn, plotly)
- Built Flask REST API for deployment
- Added Jupyter notebooks for interactive analysis
- Complete documentation and quickstart guides
"@
    git commit -m $commitMessage
    Write-Host "✅ Commit created" -ForegroundColor Green
    Write-Host ""
}

# Check if remote already exists
$remoteExists = git remote -v 2>&1 | Select-String "origin"
if ($remoteExists) {
    Write-Host "ℹ️  Remote 'origin' already exists" -ForegroundColor Cyan
    git remote -v
    Write-Host ""
} else {
    # Add remote
    Write-Host "Adding GitHub remote..." -ForegroundColor Yellow
    $repoUrl = "https://github.com/jeet-pramanik/Customer-Segmentation-ML.git"
    git remote add origin $repoUrl
    Write-Host "✅ Remote added: $repoUrl" -ForegroundColor Green
    Write-Host ""
}

# Push to GitHub
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ready to push to GitHub!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  IMPORTANT: You need a GitHub Personal Access Token" -ForegroundColor Yellow
Write-Host ""
Write-Host "If you don't have one yet:" -ForegroundColor White
Write-Host "1. Go to: https://github.com/settings/tokens/new" -ForegroundColor White
Write-Host "2. Note: 'Customer Segmentation ML Project'" -ForegroundColor White
Write-Host "3. Expiration: 90 days" -ForegroundColor White
Write-Host "4. Scopes: Select 'repo'" -ForegroundColor White
Write-Host "5. Click 'Generate token' and COPY it" -ForegroundColor White
Write-Host ""
Write-Host "When Git asks for password, paste your Personal Access Token" -ForegroundColor Yellow
Write-Host ""

$proceed = Read-Host "Do you want to push to GitHub now? (y/n)"
if ($proceed -eq "y") {
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
    Write-Host "Username: jeet-pramanik" -ForegroundColor Cyan
    Write-Host "Password: [Your Personal Access Token]" -ForegroundColor Cyan
    Write-Host ""
    
    git push -u origin master
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "✅ SUCCESS! Project published to GitHub!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your repository is now live at:" -ForegroundColor White
        Write-Host "https://github.com/jeet-pramanik/Customer-Segmentation-ML" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Visit your repository and add topics (machine-learning, clustering, python)" -ForegroundColor White
        Write-Host "2. Star your repository ⭐" -ForegroundColor White
        Write-Host "3. Share it on LinkedIn or Twitter" -ForegroundColor White
        Write-Host "4. Continue development with remaining notebooks" -ForegroundColor White
        Write-Host ""
        
        $openBrowser = Read-Host "Do you want to open your repository in browser? (y/n)"
        if ($openBrowser -eq "y") {
            Start-Process "https://github.com/jeet-pramanik/Customer-Segmentation-ML"
        }
    } else {
        Write-Host ""
        Write-Host "❌ Push failed!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Common issues:" -ForegroundColor Yellow
        Write-Host "1. Repository doesn't exist on GitHub - Create it first at https://github.com/new" -ForegroundColor White
        Write-Host "2. Invalid credentials - Make sure to use Personal Access Token as password" -ForegroundColor White
        Write-Host "3. No internet connection - Check your network" -ForegroundColor White
        Write-Host ""
        Write-Host "For help, see: PUBLISH_INSTRUCTIONS.md" -ForegroundColor Cyan
    }
} else {
    Write-Host ""
    Write-Host "Push cancelled. You can run this script again when ready." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual push command:" -ForegroundColor Cyan
    Write-Host "git push -u origin master" -ForegroundColor White
}

Write-Host ""
Write-Host "Press Enter to exit..."
Read-Host
