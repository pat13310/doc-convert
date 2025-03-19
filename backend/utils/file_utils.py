"""
Utilitaires pour la gestion des fichiers
"""
import os
import uuid
import shutil
import logging
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile

logger = logging.getLogger(__name__)

def save_upload_file(upload_file: UploadFile, destination_folder: Path) -> Tuple[bool, str, str]:
    """
    Sauvegarde un fichier téléchargé dans le dossier de destination
    
    Args:
        upload_file: Fichier téléchargé via FastAPI
        destination_folder: Dossier de destination
        
    Returns:
        Tuple contenant:
        - bool: Succès ou échec
        - str: Chemin du fichier sauvegardé ou message d'erreur
        - str: Nom original du fichier
    """
    try:
        # Créer le dossier de destination s'il n'existe pas
        os.makedirs(destination_folder, exist_ok=True)
        
        # Générer un nom de fichier unique
        file_extension = os.path.splitext(upload_file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(destination_folder, unique_filename)
        
        # Sauvegarder le fichier
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
        logger.info(f"Fichier sauvegardé: {file_path}")
        return True, file_path, upload_file.filename
    
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du fichier: {str(e)}")
        return False, str(e), upload_file.filename

def clean_temp_files(directory: Path, exclude_files: Optional[list] = None) -> None:
    """
    Nettoie les fichiers temporaires d'un répertoire
    
    Args:
        directory: Répertoire à nettoyer
        exclude_files: Liste de fichiers à exclure du nettoyage
    """
    exclude_files = exclude_files or []
    try:
        if not os.path.exists(directory):
            return
            
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and file_path not in exclude_files:
                os.remove(file_path)
                logger.info(f"Fichier temporaire supprimé: {file_path}")
    
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des fichiers temporaires: {str(e)}")

def get_file_extension(filename: str) -> str:
    """
    Récupère l'extension d'un fichier
    
    Args:
        filename: Nom du fichier
        
    Returns:
        Extension du fichier en minuscules (sans le point)
    """
    return os.path.splitext(filename)[1].lower().lstrip('.')
