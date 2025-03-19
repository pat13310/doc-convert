"""
Point d'entrée pour le déploiement sur Vercel
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au chemin Python pour pouvoir importer le module principal
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Importer l'application FastAPI depuis le fichier principal
from backend.app.main import app

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

# Nécessaire pour Vercel Serverless Functions
handler = app
