@echo off
REM ============================================================================
REM Git Publishing Script for Customer Segmentation ML Project
REM ============================================================================

echo.
echo ========================================================================
echo  Customer Segmentation ML - GitHub Publishing Script
echo ========================================================================
echo.

REM Check if git is installed
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in PATH!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo After installation, restart this script.
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Check if git is already initialized
if exist .git (
    echo [INFO] Git repository already initialized
    echo.
) else (
    echo [STEP 1] Initializing Git repository...
    git init
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to initialize git repository
        pause
        exit /b 1
    )
    echo [OK] Git repository initialized
    echo.
)

REM Check git configuration
echo [STEP 2] Checking Git configuration...
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Git user name not configured
    echo Please enter your name:
    set /p username="Name: "
    git config --global user.name "!username!"
    echo.
)

git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Git email not configured
    echo Please enter your email:
    set /p useremail="Email: "
    git config --global user.email "!useremail!"
    echo.
)

echo [OK] Git is configured
echo   Name:  
git config user.name
echo   Email: 
git config user.email
echo.

REM Add files
echo [STEP 3] Adding files to Git...
git add .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to add files
    pause
    exit /b 1
)
echo [OK] Files added successfully
echo.

REM Show status
echo [INFO] Repository Status:
git status --short
echo.

REM Commit
echo [STEP 4] Creating commit...
git commit -m "Initial commit: Complete Customer Segmentation ML system - Implemented K-Means, DBSCAN, Hierarchical, and GMM clustering - Complete preprocessing pipeline with feature engineering - Comprehensive evaluation metrics and profiling - Flask REST API for deployment - Jupyter notebooks for analysis - Full documentation and quick start guide"
if %errorlevel% neq 0 (
    echo [WARNING] Commit may have failed or no changes to commit
    echo.
) else (
    echo [OK] Commit created successfully
    echo.
)

REM Check if remote exists
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Remote 'origin' already exists:
    git remote get-url origin
    echo.
    echo Do you want to update it? (Y/N)
    set /p update_remote="Choice: "
    if /i "!update_remote!"=="Y" (
        git remote remove origin
        goto :add_remote
    ) else (
        goto :push
    )
) else (
    :add_remote
    echo [STEP 5] Adding remote repository...
    echo.
    echo Please enter your GitHub repository URL
    echo Example: https://github.com/username/Customer-Segmentation-ML.git
    echo.
    set /p repo_url="Repository URL: "
    
    git remote add origin !repo_url!
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to add remote repository
        pause
        exit /b 1
    )
    echo [OK] Remote repository added
    echo.
)

:push
REM Push to GitHub
echo [STEP 6] Pushing to GitHub...
echo.
echo This will push your code to GitHub.
echo You may be asked for your GitHub credentials.
echo Use your GitHub username and Personal Access Token (not password)
echo.
echo Continue? (Y/N)
set /p confirm_push="Choice: "
if /i "!confirm_push!"=="Y" (
    git branch -M main
    git push -u origin main
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Push failed!
        echo.
        echo Common issues:
        echo 1. Invalid credentials - Use Personal Access Token, not password
        echo 2. Remote repository doesn't exist - Create it on GitHub first
        echo 3. Network connection issues
        echo.
        echo To create a Personal Access Token:
        echo 1. Go to GitHub Settings - Developer settings - Personal access tokens
        echo 2. Generate new token with 'repo' scope
        echo 3. Copy and use it as password when prompted
        echo.
        pause
        exit /b 1
    )
    echo.
    echo ========================================================================
    echo  SUCCESS! Your project has been published to GitHub!
    echo ========================================================================
    echo.
    echo Visit your repository:
    git remote get-url origin
    echo.
    echo Next steps:
    echo 1. Add repository description on GitHub
    echo 2. Add topics/tags for discoverability
    echo 3. Consider adding a license
    echo 4. Share your project!
    echo.
) else (
    echo [INFO] Push cancelled by user
    echo.
    echo Your code is committed locally but not pushed to GitHub.
    echo To push later, run: git push -u origin main
    echo.
)

echo.
echo Script completed!
pause
