"""
Routes pour la conversion de documents
"""
import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import uuid
import shutil

from services.document_service import (
    convert_docx_to_pdf,
    convert_pdf_to_docx,
    convert_pdf_to_images
)
from utils.file_utils import save_upload_file, clean_temp_files
from app.config import UPLOADS_DIR, OUTPUT_DIR, TEMP_DIR

# Configuration du logging
logger = logging.getLogger(__name__)

# Créer le routeur
router = APIRouter(prefix="/api", tags=["conversion"])

@router.post("/convert/docx-to-pdf/")
async def convert_docx_to_pdf_endpoint(file: UploadFile = File(...)):
    """
    Convertit un document DOCX en PDF
    """
    try:
        logger.info(f"Demande de conversion DOCX vers PDF reçue pour le fichier: {file.filename}")
        
        # Vérifier l'extension du fichier
        if not file.filename.lower().endswith(('.docx', '.doc')):
            raise HTTPException(status_code=400, detail="Le fichier doit être au format DOCX ou DOC")
        
        # Sauvegarder le fichier téléchargé
        success, upload_path, original_filename = save_upload_file(file, UPLOADS_DIR)
        
        if not success:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde du fichier: {upload_path}")
        
        # Définir le chemin de sortie pour le fichier PDF
        output_filename = f"{uuid.uuid4()}.pdf"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Convertir le fichier DOCX en PDF
        convert_docx_to_pdf(upload_path, output_path)
        
        # Vérifier si le fichier PDF a été créé
        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="La conversion a échoué, le fichier PDF n'a pas été créé")
        
        # Définir le nom du fichier pour le téléchargement
        download_filename = original_filename.replace('.docx', '.pdf').replace('.doc', '.pdf')
        
        # Renvoyer le fichier PDF
        return FileResponse(
            path=output_path,
            filename=download_filename,
            media_type="application/pdf"
        )
    
    except Exception as e:
        logger.error(f"Erreur lors de la conversion DOCX vers PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la conversion: {str(e)}")

@router.post("/convert/pdf-to-docx/")
async def convert_pdf_to_docx_endpoint(file: UploadFile = File(...)):
    """
    Convertit un document PDF en DOCX
    """
    try:
        logger.info(f"Demande de conversion PDF vers DOCX reçue pour le fichier: {file.filename}")
        
        # Vérifier l'extension du fichier
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Le fichier doit être au format PDF")
        
        # Sauvegarder le fichier téléchargé
        success, upload_path, original_filename = save_upload_file(file, UPLOADS_DIR)
        
        if not success:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde du fichier: {upload_path}")
        
        # Définir le chemin de sortie pour le fichier DOCX
        output_filename = f"{uuid.uuid4()}.docx"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Convertir le fichier PDF en DOCX
        convert_pdf_to_docx(upload_path, output_path)
        
        # Vérifier si le fichier DOCX a été créé
        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="La conversion a échoué, le fichier DOCX n'a pas été créé")
        
        # Définir le nom du fichier pour le téléchargement
        download_filename = original_filename.replace('.pdf', '.docx')
        
        # Renvoyer le fichier DOCX
        return FileResponse(
            path=output_path,
            filename=download_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    except Exception as e:
        logger.error(f"Erreur lors de la conversion PDF vers DOCX: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la conversion: {str(e)}")

@router.post("/convert/pdf-to-images/")
async def convert_pdf_to_images_endpoint(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """
    Convertit un document PDF en images (une image par page)
    """
    try:
        logger.info(f"Demande de conversion PDF vers images reçue pour le fichier: {file.filename}")
        
        # Vérifier l'extension du fichier
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Le fichier doit être au format PDF")
        
        # Sauvegarder le fichier téléchargé
        success, upload_path, original_filename = save_upload_file(file, UPLOADS_DIR)
        
        if not success:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde du fichier: {upload_path}")
        
        # Créer un dossier temporaire pour les images
        temp_dir = os.path.join(TEMP_DIR, str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)
        
        # Convertir le fichier PDF en images
        success, message, image_paths = convert_pdf_to_images(upload_path, temp_dir)
        
        if not success or not image_paths:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la conversion: {message}")
        
        # Créer un fichier ZIP contenant les images
        zip_filename = f"{uuid.uuid4()}.zip"
        zip_path = os.path.join(OUTPUT_DIR, zip_filename)
        
        # Créer le fichier ZIP
        with shutil.ZipFile(zip_path, 'w') as zipf:
            for image_path in image_paths:
                # Ajouter l'image au fichier ZIP
                zipf.write(image_path, os.path.basename(image_path))
        
        # Ajouter une tâche de nettoyage en arrière-plan
        if background_tasks:
            background_tasks.add_task(clean_temp_files, temp_dir)
        
        # Définir le nom du fichier pour le téléchargement
        download_filename = original_filename.replace('.pdf', '_images.zip')
        
        # Renvoyer le fichier ZIP
        return FileResponse(
            path=zip_path,
            filename=download_filename,
            media_type="application/zip"
        )
    
    except Exception as e:
        logger.error(f"Erreur lors de la conversion PDF vers images: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la conversion: {str(e)}")
