@echo off
REM Vérifier si Python3 est installé
where py >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python3 n'est pas installe. Veuillez installer Python3.
    exit /b
)

REM Récupérer la version de Python
for /f "delims=" %%I in ('py --version 2^>nul') do set PYTHON_VERSION=%%I

REM Afficher la version récupérée pour le débogage
echo Version de Python detectée: %PYTHON_VERSION%

REM Extraire les parties de la version
for /f "tokens=2 delims= " %%a in ("%PYTHON_VERSION%") do set VERSION=%%a
for /f "tokens=1-3 delims=." %%a in ("%VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
    set PATCH=%%c
)

REM Afficher la version pour débogage
echo Version extraite : %MAJOR%.%MINOR%.%PATCH%

REM Comparer la version de Python
IF %MAJOR% LSS 3 (
    echo La version de Python est inférieure à 3. Veuillez installer Python 3.13 ou supérieur.
    exit /b
) 
IF %MAJOR%==3 IF %MINOR% LSS 13 (
    echo La version de Python est inférieure à 3.13. Veuillez installer Python 3.13 ou supérieur.
    exit /b
)

REM Créer un environnement virtuel dans le répertoire '.venv'
echo Creation de l'environnement virtuel...
py -m venv .venv

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

REM Installation du gestionnaire de dépendences du projet...
py -m pip install pdm

REM Installer les dependances
echo Installation des dependances...
py -m pip install --upgrade pip
pdm install

echo Installation de l'environnement python terminee.
pause
