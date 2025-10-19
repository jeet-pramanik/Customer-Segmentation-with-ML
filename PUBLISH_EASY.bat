@echo off
REM ============================================================================
REM Quick Git Publishing Script for jeet-pramanik
REM Customer Segmentation ML Project
REM ============================================================================

echo.
echo ========================================================================
echo  Customer Segmentation ML - GitHub Publishing
echo  User: jeet-pramanik
echo ========================================================================
echo.

REM Check if git is installed
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    echo After installation:
    echo 1. Restart your terminal
    echo 2. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed
git --version
echo.

REM Configure Git if not already done
echo [STEP 1] Configuring Git...
git config --global user.name "jeet-pramanik"
git config --global user.email "jeetpramanik516@gmail.com"
echo [OK] Git configured as:
echo   Name:  jeet-pramanik
echo   Email: jeetpramanik516@gmail.com
echo.

REM Initialize git if needed
if exist .git (
    echo [INFO] Git repository already initialized
    echo.
) else (
    echo [STEP 2] Initializing Git repository...
    git init
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to initialize git
        pause
        exit /b 1
    )
    echo [OK] Git initialized
    echo.
)

REM Add files
echo [STEP 3] Adding files to Git...
git add .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to add files
    pause
    exit /b 1
)
echo [OK] Files added
echo.

REM Show what will be committed
echo [INFO] Files ready to commit:
git status --short
echo.

REM Commit
echo [STEP 4] Creating commit...
git commit -m "Initial commit: Complete Customer Segmentation ML system - Implemented K-Means, DBSCAN, Hierarchical, and GMM clustering - Complete preprocessing pipeline with feature engineering - Comprehensive evaluation metrics and profiling - Flask REST API for deployment - Jupyter notebooks for analysis - Full documentation and quick start guide"
if %errorlevel% neq 0 (
    echo [WARNING] Nothing to commit or commit failed
    echo.
) else (
    echo [OK] Commit created successfully
    echo.
)

REM Check if remote exists
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Remote repository already configured:
    git remote get-url origin
    echo.
    set /p update_remote="Do you want to update it? (Y/N): "
    if /i "%update_remote%"=="Y" (
        git remote remove origin
        goto :add_remote
    ) else (
        goto :push
    )
) else (
    :add_remote
    echo [STEP 5] Adding GitHub repository...
    echo.
    echo Default repository URL for jeet-pramanik:
    echo https://github.com/jeet-pramanik/Customer-Segmentation-ML.git
    echo.
    set /p use_default="Use this URL? (Y/N): "
    
    if /i "%use_default%"=="Y" (
        set repo_url=https://github.com/jeet-pramanik/Customer-Segmentation-ML.git
    ) else (
        echo.
        echo Enter your GitHub repository URL:
        set /p repo_url="URL: "
    )
    
    git remote add origin %repo_url%
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to add remote
        pause
        exit /b 1
    )
    echo [OK] Remote added: %repo_url%
    echo.
)

:push
echo [STEP 6] Pushing to GitHub...
echo.
echo ========================================================================
echo  IMPORTANT: Authentication Required
echo ========================================================================
echo.
echo When prompted for credentials, use:
echo   Username: jeet-pramanik
echo   Password: [Your Personal Access Token]
echo.
echo NOTE: Use your GitHub Personal Access Token as password, NOT your
echo       GitHub account password!
echo.
echo To create a Personal Access Token:
echo 1. Go to: https://github.com/settings/tokens
echo 2. Click "Generate new token (classic)"
echo 3. Give it a name: "Customer Segmentation ML"
echo 4. Select scope: "repo" (full control)
echo 5. Click "Generate token"
echo 6. COPY the token immediately (you won't see it again!)
echo 7. Use it as your password below
echo.
echo ========================================================================
echo.
set /p confirm_push="Ready to push to GitHub? (Y/N): "

if /i "%confirm_push%"=="Y" (
    git branch -M main
    git push -u origin main
    
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Push failed!
        echo.
        echo Common solutions:
        echo 1. Make sure you created the repository on GitHub first
        echo    Go to: https://github.com/new
        echo.
        echo 2. Use Personal Access Token as password, not your GitHub password
        echo    Create one at: https://github.com/settings/tokens
        echo.
        echo 3. Check the repository URL is correct
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo ========================================================================
    echo  SUCCESS! Project published to GitHub!
    echo ========================================================================
    echo.
    echo Your repository is now at:
    git remote get-url origin
    echo.
    echo View it in browser:
    echo https://github.com/jeet-pramanik/Customer-Segmentation-ML
    echo.
    echo Next steps:
    echo 1. Add topics/tags on GitHub for discoverability
    echo 2. Add a license (MIT recommended)
    echo 3. Pin the repository to your profile
    echo 4. Share on LinkedIn, Twitter, portfolio
    echo.
    echo ========================================================================
    echo.
) else (
    echo.
    echo [INFO] Push cancelled
    echo.
    echo Your code is committed locally but not pushed to GitHub.
    echo To push later, run: git push -u origin main
    echo.
)

echo.
echo Press any key to exit...
pause >nul
