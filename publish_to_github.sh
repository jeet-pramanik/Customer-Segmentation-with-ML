#!/bin/bash

# ============================================================================
# Git Publishing Script for Customer Segmentation ML Project
# ============================================================================

echo ""
echo "========================================================================"
echo " Customer Segmentation ML - GitHub Publishing Script"
echo "========================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Git is not installed or not in PATH!"
    echo ""
    echo "Please install Git from: https://git-scm.com/download"
    echo "After installation, restart this script."
    echo ""
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Git is installed"
echo ""

# Check if git is already initialized
if [ -d .git ]; then
    echo -e "${YELLOW}[INFO]${NC} Git repository already initialized"
    echo ""
else
    echo "[STEP 1] Initializing Git repository..."
    git init
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Failed to initialize git repository"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} Git repository initialized"
    echo ""
fi

# Check git configuration
echo "[STEP 2] Checking Git configuration..."
if ! git config user.name &> /dev/null; then
    echo ""
    echo -e "${YELLOW}[WARNING]${NC} Git user name not configured"
    read -p "Please enter your name: " username
    git config --global user.name "$username"
    echo ""
fi

if ! git config user.email &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} Git email not configured"
    read -p "Please enter your email: " useremail
    git config --global user.email "$useremail"
    echo ""
fi

echo -e "${GREEN}[OK]${NC} Git is configured"
echo "  Name:  $(git config user.name)"
echo "  Email: $(git config user.email)"
echo ""

# Add files
echo "[STEP 3] Adding files to Git..."
git add .
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Failed to add files"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Files added successfully"
echo ""

# Show status
echo -e "${YELLOW}[INFO]${NC} Repository Status:"
git status --short
echo ""

# Commit
echo "[STEP 4] Creating commit..."
git commit -m "Initial commit: Complete Customer Segmentation ML system

- Implemented K-Means, DBSCAN, Hierarchical, and GMM clustering
- Complete preprocessing pipeline with feature engineering
- Comprehensive evaluation metrics and profiling
- Flask REST API for deployment
- Jupyter notebooks for analysis
- Full documentation and quick start guide"

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Commit may have failed or no changes to commit"
    echo ""
else
    echo -e "${GREEN}[OK]${NC} Commit created successfully"
    echo ""
fi

# Check if remote exists
if git remote get-url origin &> /dev/null; then
    echo -e "${YELLOW}[INFO]${NC} Remote 'origin' already exists:"
    git remote get-url origin
    echo ""
    read -p "Do you want to update it? (y/N): " update_remote
    if [[ $update_remote =~ ^[Yy]$ ]]; then
        git remote remove origin
    else
        # Skip to push
        repo_url=$(git remote get-url origin)
        push_to_github=true
    fi
fi

# Add remote if not already set
if [ -z "$push_to_github" ]; then
    echo "[STEP 5] Adding remote repository..."
    echo ""
    echo "Please enter your GitHub repository URL"
    echo "Example: https://github.com/username/Customer-Segmentation-ML.git"
    echo ""
    read -p "Repository URL: " repo_url
    
    git remote add origin "$repo_url"
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Failed to add remote repository"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} Remote repository added"
    echo ""
fi

# Push to GitHub
echo "[STEP 6] Pushing to GitHub..."
echo ""
echo "This will push your code to GitHub."
echo "You may be asked for your GitHub credentials."
echo "Use your GitHub username and Personal Access Token (not password)"
echo ""
read -p "Continue? (Y/n): " confirm_push

if [[ ! $confirm_push =~ ^[Nn]$ ]]; then
    git branch -M main
    git push -u origin main
    
    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}[ERROR]${NC} Push failed!"
        echo ""
        echo "Common issues:"
        echo "1. Invalid credentials - Use Personal Access Token, not password"
        echo "2. Remote repository doesn't exist - Create it on GitHub first"
        echo "3. Network connection issues"
        echo ""
        echo "To create a Personal Access Token:"
        echo "1. Go to GitHub Settings → Developer settings → Personal access tokens"
        echo "2. Generate new token with 'repo' scope"
        echo "3. Copy and use it as password when prompted"
        echo ""
        exit 1
    fi
    
    echo ""
    echo "========================================================================"
    echo -e " ${GREEN}SUCCESS!${NC} Your project has been published to GitHub!"
    echo "========================================================================"
    echo ""
    echo "Visit your repository:"
    echo "$repo_url"
    echo ""
    echo "Next steps:"
    echo "1. Add repository description on GitHub"
    echo "2. Add topics/tags for discoverability"
    echo "3. Consider adding a license"
    echo "4. Share your project!"
    echo ""
else
    echo -e "${YELLOW}[INFO]${NC} Push cancelled by user"
    echo ""
    echo "Your code is committed locally but not pushed to GitHub."
    echo "To push later, run: git push -u origin main"
    echo ""
fi

echo ""
echo "Script completed!"
