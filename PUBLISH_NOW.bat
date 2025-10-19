@echo off
REM Simple GitHub Publishing Script for Customer Segmentation ML
REM Just double-click this file to run!

echo ========================================
echo Customer Segmentation ML - GitHub Publisher
echo ========================================
echo.

REM Check if Git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git first:
    echo 1. Download from: https://git-scm.com/download/win
    echo 2. Run installer with default settings
    echo 3. Restart your terminal
    echo 4. Run this script again
    echo.
    echo Opening Git download page in browser...
    start https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Configure Git
echo Configuring Git with your credentials...
git config --global user.name "jeet-pramanik"
git config --global user.email "jeetpramanik516@gmail.com"
echo [OK] Git configured
echo.

REM Check if already a git repo
if exist ".git" (
    echo [INFO] Git repository already exists
    echo.
) else (
    echo Initializing Git repository...
    git init
    echo [OK] Repository initialized
    echo.
)

REM Add files
echo Adding all files to Git...
git add .
echo [OK] Files added
echo.

REM Commit
echo Creating commit...
git commit -m "Initial commit: Complete Customer Segmentation ML System - Implemented data loading with synthetic data generation - Created preprocessing pipeline with feature engineering - Built 4 clustering algorithms (K-Means, DBSCAN, Hierarchical, GMM) - Added comprehensive evaluation metrics - Developed customer profiling and marketing strategies - Created visualization suite - Built Flask REST API for deployment - Added Jupyter notebooks and documentation"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Commit created
) else (
    echo [INFO] No changes to commit or commit already exists
)
echo.

REM Check if remote exists
git remote -v | find "origin" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Remote 'origin' already exists
    git remote -v
    echo.
) else (
    echo Adding GitHub remote...
    git remote add origin https://github.com/jeet-pramanik/Customer-Segmentation-ML.git
    echo [OK] Remote added
    echo.
)

REM Instructions for pushing
echo ========================================
echo READY TO PUSH TO GITHUB!
echo ========================================
echo.
echo IMPORTANT: You need a GitHub Personal Access Token
echo.
echo If you don't have one:
echo 1. Go to: https://github.com/settings/tokens/new
echo 2. Note: "Customer Segmentation ML"
echo 3. Expiration: 90 days
echo 4. Scopes: Select 'repo'
echo 5. Click 'Generate token' and COPY it
echo.
echo When Git asks for password, paste your token
echo.

choice /C YN /M "Do you want to push to GitHub now"
if %ERRORLEVEL% EQU 2 goto :cancel
if %ERRORLEVEL% EQU 1 goto :push

:push
echo.
echo Pushing to GitHub...
echo Username: jeet-pramanik
echo Password: [Paste your Personal Access Token]
echo.
git push -u origin master

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Project published to GitHub!
    echo ========================================
    echo.
    echo Your repository is live at:
    echo https://github.com/jeet-pramanik/Customer-Segmentation-ML
    echo.
    echo Next steps:
    echo 1. Visit your repository
    echo 2. Add topics: machine-learning, clustering, python
    echo 3. Star your repository
    echo 4. Share on LinkedIn or Twitter
    echo.
    
    choice /C YN /M "Open repository in browser"
    if %ERRORLEVEL% EQU 1 (
        start https://github.com/jeet-pramanik/Customer-Segmentation-ML
    )
) else (
    echo.
    echo [ERROR] Push failed!
    echo.
    echo Common issues:
    echo 1. Repository doesn't exist - Create at https://github.com/new
    echo 2. Invalid token - Use Personal Access Token as password
    echo 3. No internet connection
    echo.
    echo For help, see PUBLISH_INSTRUCTIONS.md
)
goto :end

:cancel
echo.
echo Push cancelled. You can run this script again when ready.
echo.
echo Manual push command: git push -u origin master
echo.

:end
echo.
pause
