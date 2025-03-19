"""
Point d'entrée pour le déploiement sur Vercel
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import sys
import os
from pathlib import Path
import traceback

# Ajouter le répertoire parent au chemin Python pour pouvoir importer le module principal
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Importer l'application FastAPI depuis le fichier principal
try:
    from backend.app.main import app
except Exception as e:
    # Créer une application de secours en cas d'erreur d'importation
    app = FastAPI()
    
    @app.get("/api/status")
    async def status():
        return {"status": "error", "message": f"Erreur d'importation: {str(e)}"}

# Intercepter les erreurs pour les routes API
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # Journaliser l'erreur
        error_detail = f"Erreur: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        
        # Vérifier si la route est une API
        if request.url.path.startswith("/api/"):
            return JSONResponse(
                status_code=500,
                content={
                    "error": str(e),
                    "message": "Cette fonctionnalité n'est pas disponible dans l'environnement Vercel. Veuillez utiliser l'application en local pour accéder à toutes les fonctionnalités.",
                    "detail": "Les fonctions serverless de Vercel ont des limitations qui empêchent certaines opérations comme la manipulation de fichiers."
                }
            )
        
        # Pour les autres routes, renvoyer une page HTML d'erreur
        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Erreur - Conversion de Documents</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; text-align: center; }}
                    .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #e74c3c; }}
                    .message {{ margin: 20px 0; padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px; color: #721c24; }}
                    .btn {{ display: inline-block; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 4px; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Erreur</h1>
                    <div class="message">
                        <p>Cette fonctionnalité n'est pas disponible dans l'environnement Vercel.</p>
                        <p>Veuillez utiliser l'application en local pour accéder à toutes les fonctionnalités.</p>
                    </div>
                    <a href="/" class="btn">Retour à l'accueil</a>
                </div>
            </body>
            </html>
            """,
            status_code=500
        )

# Définir une route pour la racine qui renvoie une page HTML
@app.get("/", response_class=HTMLResponse)
async def vercel_root():
    """
    Route racine pour Vercel qui renvoie la page d'accueil
    """
    try:
        # Chemin vers le fichier index.html
        index_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
        
        # Lire le contenu du fichier
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
            # Ajouter une bannière d'information
            info_banner = """
            <div style="background-color: #f8f9fa; padding: 10px; margin-bottom: 20px; border-left: 4px solid #007bff; text-align: left;">
                <p style="margin: 0;"><strong>Note:</strong> Certaines fonctionnalités ne sont pas disponibles dans cette version en ligne. 
                Pour accéder à toutes les fonctionnalités, veuillez télécharger et exécuter l'application en local.</p>
            </div>
            """
            
            # Insérer la bannière après la balise <header>
            html_content = html_content.replace("<header>", "<header>" + info_banner)
        
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        # Fallback si le fichier n'existe pas
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
                    border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #2c3e50;
                }
                .info-banner {
                    background-color: #f8f9fa;
                    padding: 10px;
                    margin-bottom: 20px;
                    border-left: 4px solid #007bff;
                    text-align: left;
                }
                .card {
                    margin: 20px 0;
                    padding: 15px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                .btn {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Application de Conversion de Documents</h1>
                
                <div class="info-banner">
                    <p><strong>Note:</strong> Certaines fonctionnalités ne sont pas disponibles dans cette version en ligne. 
                    Pour accéder à toutes les fonctionnalités, veuillez télécharger et exécuter l'application en local.</p>
                </div>
                
                <div class="card">
                    <h2>Fonctionnalités</h2>
                    <p>Cette application vous permet de :</p>
                    <ul style="text-align: left;">
                        <li>Convertir des documents DOCX en PDF</li>
                        <li>Convertir des documents PDF en DOCX</li>
                        <li>Extraire du texte de différents formats de documents</li>
                        <li>Convertir des PDF en images</li>
                    </ul>
                    
                    <div>
                        <a href="/frontend/pages/convert.html" class="btn">Conversion de Documents</a>
                        <a href="/frontend/pages/extract.html" class="btn">Extraction de Texte</a>
                        <a href="/frontend/pages/pdf-to-images.html" class="btn">PDF vers Images</a>
                    </div>
                </div>
                
                <div class="card">
                    <h2>Téléchargement</h2>
                    <p>Pour accéder à toutes les fonctionnalités, téléchargez l'application depuis GitHub :</p>
                    <a href="https://github.com/pat13310/doc-convert" class="btn" target="_blank">Télécharger sur GitHub</a>
                </div>
                
                <footer style="margin-top: 30px; font-size: 0.9em; color: #777;">
                    &copy; 2025 Application de Conversion de Documents. Tous droits réservés.
                </footer>
            </div>
        </body>
        </html>
        """)

# Nécessaire pour Vercel Serverless Functions
handler = app
