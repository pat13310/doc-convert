"""
Point d'entrée principal de l'application FastAPI
"""
import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from pathlib import Path

# Import des configurations
from .config import APP_CONFIG, CORS_CONFIG, UPLOADS_DIR, OUTPUT_DIR, TEMP_DIR

# Import des routes
from .routes import convert, extract, pdf_images

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title=APP_CONFIG["title"],
    description=APP_CONFIG["description"],
    version=APP_CONFIG["version"]
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG["allow_origins"],
    allow_credentials=CORS_CONFIG["allow_credentials"],
    allow_methods=CORS_CONFIG["allow_methods"],
    allow_headers=CORS_CONFIG["allow_headers"],
)

# Obtenir le chemin de base de l'application
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Chemin vers les dossiers frontend et static
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR

# Créer les dossiers nécessaires s'ils n'existent pas
os.makedirs(FRONTEND_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Configuration des dossiers statiques
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")
app.mount("/temp", StaticFiles(directory=TEMP_DIR), name="temp")

# Inclusion des routes
app.include_router(convert.router)
app.include_router(extract.router)
app.include_router(pdf_images.router)

# Route pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Renvoie la page d'accueil de l'application
    """
    try:
        with open(os.path.join(FRONTEND_DIR, "index.html"), "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Conversion de Documents</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                    text-align: center;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                }
                .nav {
                    margin-top: 30px;
                }
                .nav a {
                    display: inline-block;
                    margin: 10px;
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                }
                .nav a:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Application de Conversion de Documents</h1>
                <p>Bienvenue dans notre application de conversion et d'extraction de documents.</p>
                
                <div class="nav">
                    <a href="/static/pages/extract.html">Extraction de Texte</a>
                    <a href="/static/pages/convert.html">Conversion de Documents</a>
                    <a href="/static/pages/pdf-to-images.html">PDF vers Images</a>
                </div>
            </div>
        </body>
        </html>
        """)

# Route pour la vérification de santé
@app.get("/health")
async def health_check():
    """
    Vérifie l'état de santé de l'application
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }

# Route pour la documentation API
@app.get("/api/docs")
async def api_docs():
    """
    Redirige vers la documentation de l'API
    """
    return RedirectResponse(url="/docs")

# Route pour télécharger un fichier
@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """
    Télécharge un fichier depuis le dossier de sortie
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(path=file_path, filename=filename)

# Point d'entrée pour l'exécution directe
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
