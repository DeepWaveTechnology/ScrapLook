#!/bin/bash

# Vérifier si Python3 et pip sont installés
if ! command -v python3.13 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "Python3 ou pip3 n'est pas installé. Veuillez installer Python3 et pip3."
    exit 1
fi

# Vérifier la version de Python3
PYTHON_VERSION=$(python3.13 --version 2>&1 | awk '{print $2}')
MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f1)
MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f2)
PATCH_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f3)

# Comparer la version de Python
if [ "$MAJOR_VERSION" -lt 3 ] || { [ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 13 ]; }; then
    echo "La version de Python ($PYTHON_VERSION) est inférieure à 3.13. Veuillez installer Python 3.13 ou supérieur."
    exit 1
fi

# Créer un répertoire pour l'environnement virtuel et les installer dans '.venv'
echo "Création de l'environnement virtuel..."
python3 -m venv .venv

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source .venv/bin/activate

# Installer la librairie pdm
echo "Installation du gestionnaire de dépendences du projet..."
pip install pdm

# Installer les dépendances
echo "Installation des dépendances..."
pdm install

echo "Installation de l'environnement python terminee"
