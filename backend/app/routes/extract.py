"""
Routes pour l'extraction de texte des documents
"""
import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Form
from fastapi.responses import JSONResponse
import uuid
import json
from typing import Optional

from backend.services.document_service import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_xlsx,
    extract_text_from_xls,
    extract_text_from_csv,
    extract_text_from_file
)
from backend.utils.file_utils import save_upload_file, get_file_extension
from backend.app.config import UPLOADS_DIR, OUTPUT_DIR

# Configuration du logging
logger = logging.getLogger(__name__)

# Créer le routeur
router = APIRouter(prefix="/api", tags=["extraction"])

@router.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    """
    Extrait le texte d'un document (PDF, DOCX, Excel, etc.)
    """
    try:
        logger.info(f"Demande d'extraction de texte reçue pour le fichier: {file.filename}")
        
        # Sauvegarder le fichier téléchargé
        success, upload_path, original_filename = save_upload_file(file, UPLOADS_DIR)
        
        if not success:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde du fichier: {upload_path}")
        
        # Déterminer l'extension du fichier
        file_extension = get_file_extension(original_filename)
        
        # Extraire le texte en fonction du type de fichier
        if file_extension == 'pdf':
            text = extract_text_from_pdf(upload_path)
        elif file_extension in ['docx', 'doc']:
            text = extract_text_from_docx(upload_path)
        elif file_extension == 'xlsx':
            text = extract_text_from_xlsx(upload_path)
        elif file_extension == 'xls':
            text = extract_text_from_xls(upload_path)
        elif file_extension == 'csv':
            text = extract_text_from_csv(upload_path)
        else:
            # Pour les autres types de fichiers, utiliser la méthode générique
            text = extract_text_from_file(upload_path)
        
        # Sauvegarder le texte extrait dans un fichier JSON
        output_filename = f"texte_extrait_{uuid.uuid4()}.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"text": text}, f, ensure_ascii=False, indent=2)
        
        # Renvoyer le texte extrait
        return JSONResponse(content={"text": text})
    
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction de texte: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction de texte: {str(e)}")

@router.post("/extract-text-unified/")
async def extract_text_unified(file: UploadFile = File(...)):
    """
    Extrait le texte d'un document en détectant automatiquement son type (PDF, DOCX, etc.)
    """
    try:
        logger.info(f"Demande d'extraction de texte unifiée reçue pour le fichier: {file.filename}")
        
        # Sauvegarder le fichier téléchargé
        success, upload_path, original_filename = save_upload_file(file, UPLOADS_DIR)
        
        if not success:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde du fichier: {upload_path}")
        
        # Extraire le texte en utilisant la méthode générique
        text = extract_text_from_file(upload_path)
        
        # Sauvegarder le texte extrait dans un fichier JSON
        output_filename = f"texte_extrait_{uuid.uuid4()}.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"text": text}, f, ensure_ascii=False, indent=2)
        
        # Renvoyer le texte extrait
        return JSONResponse(content={"text": text})
    
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction de texte unifiée: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction de texte: {str(e)}")

@router.post("/text-to-csv/")
async def text_to_csv_endpoint(
    request: Request,
    text: str = Form(...),
    delimiter: str = Form("auto"),
    has_header: bool = Form(True)
):
    """
    Convertit du texte en CSV avec détection automatique du séparateur
    """
    try:
        logger.info(f"Demande de conversion de texte en CSV reçue avec délimiteur: {delimiter}")
        
        # Générer un nom de fichier unique pour le CSV
        output_filename = f"converted_{uuid.uuid4()}.csv"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Convertir le texte en CSV
        convert_text_to_csv(text, output_path, delimiter, has_header)
        
        # Lire le contenu du fichier CSV pour le renvoyer
        with open(output_path, 'r', encoding='utf-8') as f:
            csv_content = f.read()
        
        # Renvoyer le contenu du fichier CSV et le chemin du fichier
        return JSONResponse(content={
            "success": True,
            "message": "Conversion réussie",
            "csv_content": csv_content,
            "file_path": output_path,
            "download_url": f"/api/download/{output_filename}"
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de la conversion de texte en CSV: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Erreur lors de la conversion: {str(e)}"
            }
        )

@router.post("/text-to-csv-interactive/")
async def text_to_csv_interactive_endpoint(
    request: Request,
    text: str = Form(...),
    delimiter: str = Form(","),
    has_header: bool = Form(True)
):
    """
    Convertit du texte en CSV de manière interactive
    """
    try:
        logger.info(f"Demande de conversion interactive de texte en CSV reçue avec délimiteur: {delimiter}")
        
        # Générer un nom de fichier unique pour le CSV
        output_filename = f"converted_{uuid.uuid4()}.csv"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Convertir le texte en CSV
        convert_text_to_csv_interactive(text, output_path, delimiter, has_header)
        
        # Lire le contenu du fichier CSV pour le renvoyer
        with open(output_path, 'r', encoding='utf-8') as f:
            csv_content = f.read()
        
        # Renvoyer le contenu du fichier CSV et le chemin du fichier
        return JSONResponse(content={
            "success": True,
            "message": "Conversion réussie",
            "csv_content": csv_content,
            "file_path": output_path,
            "download_url": f"/api/download/{output_filename}"
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de la conversion interactive de texte en CSV: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Erreur lors de la conversion: {str(e)}"
            }
        )

@router.post("/extract-text-from-csv/")
async def extract_text_from_csv_endpoint(
    request: Request, 
    file: UploadFile = File(...), 
    delimiter: str = Form("keep")
):
    """
    Extrait le texte d'un fichier CSV en conservant ou modifiant le séparateur
    """
    try:
        logger.info(f"Demande d'extraction de texte CSV reçue pour le fichier: {file.filename}")
        
        # Vérifier l'extension du fichier
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(status_code=400, detail="Le fichier doit être au format CSV")
        
        # Sauvegarder le fichier téléchargé
        success, upload_path, original_filename = save_upload_file(file, UPLOADS_DIR)
        
        if not success:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde du fichier: {upload_path}")
        
        # Extraire le texte du fichier CSV
        text = extract_text_from_csv(upload_path)
        
        # Renvoyer le texte extrait
        return JSONResponse(content={"text": text})
    
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction de texte CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction de texte: {str(e)}")
