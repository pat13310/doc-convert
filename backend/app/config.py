"""
Configuration de l'application
"""
import os
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Chemin de base de l'application
BASE_DIR = Path(__file__).resolve().parent.parent

# Dossiers de données
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
OUTPUT_DIR = DATA_DIR / "output"
TEMP_DIR = DATA_DIR / "temp"

# Vérifier si nous sommes sur Vercel (utiliser les variables d'environnement définies dans vercel.json)
if os.environ.get("UPLOAD_FOLDER") and os.environ.get("OUTPUT_FOLDER") and os.environ.get("TEMP_FOLDER"):
    logger.info("Utilisation des chemins configurés pour Vercel")
    UPLOADS_DIR = Path(os.environ.get("UPLOAD_FOLDER"))
    OUTPUT_DIR = Path(os.environ.get("OUTPUT_FOLDER"))
    TEMP_DIR = Path(os.environ.get("TEMP_FOLDER"))

# Créer les dossiers nécessaires s'ils n'existent pas
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Configuration de l'application
APP_CONFIG = {
    "title": "API de Conversion de Documents",
    "description": "API pour convertir et extraire du texte de différents formats de documents",
    "version": "1.0.0",
}

# Configuration CORS
CORS_CONFIG = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
