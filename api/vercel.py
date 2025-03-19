from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import os
from pathlib import Path

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Gère les requêtes GET"""
        print(f"Requête GET reçue pour le chemin: {self.path}")
        
        if self.path == '/' or self.path == '/index.html':
            # Servir la page d'accueil
            self.serve_static_file('index.html')
        elif self.path.startswith('/api/status'):
            # Renvoyer le statut de l'API
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'ok',
                'message': 'API opérationnelle',
                'version': '1.0.0',
                'limitations': 'Cette version déployée sur Vercel a des fonctionnalités limitées. Pour une expérience complète, utilisez l\'application en local.'
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith('/frontend/'):
            # Servir les fichiers statiques du frontend
            file_path = self.path[1:]  # Enlever le / initial
            self.serve_static_file(file_path)
        else:
            # Pour toutes les autres requêtes GET, essayer de servir un fichier statique
            file_path = self.path[1:] if self.path.startswith('/') else self.path
            if self.serve_static_file(file_path, send_404_if_not_found=False):
                return
                
            # Si le fichier n'existe pas, renvoyer une erreur 404
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'error': 'Page non trouvée',
                'message': f'La ressource demandée "{self.path}" n\'existe pas',
                'suggestion': 'Essayez d\'accéder à la page d\'accueil via /'
            }
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Gère les requêtes POST"""
        print(f"Requête POST reçue pour le chemin: {self.path}")
        
        if self.path.startswith('/api/extract-text') or self.path.startswith('/api/convert'):
            # Pour les requêtes d'extraction de texte ou de conversion, renvoyer un message d'erreur
            self.send_response(501)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'error': 'Fonctionnalité non disponible',
                'message': 'Cette fonctionnalité n\'est pas disponible dans l\'environnement Vercel.',
                'detail': 'Les fonctions serverless de Vercel ont des limitations qui empêchent certaines opérations comme la manipulation de fichiers.',
                'solution': 'Pour utiliser cette fonctionnalité, veuillez télécharger et exécuter l\'application en local.'
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            # Pour toutes les autres requêtes POST, renvoyer une erreur 404
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'error': 'Endpoint non trouvé',
                'message': f'L\'API demandée "{self.path}" n\'existe pas'
            }
            self.wfile.write(json.dumps(response).encode())
    
    def serve_static_file(self, file_path, send_404_if_not_found=True):
        """Sert un fichier statique"""
        try:
            # Déterminer le chemin du fichier
            if file_path == 'index.html':
                # Servir la page d'accueil
                html_content = """
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
                """
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode())
                return True
            
            # Pour les autres fichiers, vérifier s'ils existent
            base_path = Path(__file__).resolve().parent.parent
            full_path = base_path / file_path
            
            # Vérifier si le fichier existe
            if not os.path.isfile(full_path):
                if send_404_if_not_found:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'error': 'Fichier non trouvé',
                        'message': f'Le fichier "{file_path}" n\'existe pas'
                    }
                    self.wfile.write(json.dumps(response).encode())
                return False
            
            # Déterminer le type MIME
            content_type = self.get_content_type(file_path)
            
            # Lire et servir le fichier
            with open(full_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
            return True
            
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier: {str(e)}")
            if send_404_if_not_found:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'error': 'Erreur serveur',
                    'message': f'Une erreur est survenue lors de la lecture du fichier: {str(e)}'
                }
                self.wfile.write(json.dumps(response).encode())
            return False
    
    def get_content_type(self, file_path):
        """Détermine le type MIME d'un fichier"""
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        return content_types.get(ext, 'application/octet-stream')

def handler(event, context):
    """Fonction de gestion pour Vercel"""
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    # Créer une réponse par défaut
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': '<html><body><h1>Application de Conversion de Documents</h1><p>Bienvenue sur notre application.</p></body></html>'
    }
    
    # Journaliser la requête
    print(f"Requête reçue: {method} {path}")
    
    # Rediriger vers la page d'accueil
    if path == '/':
        response['statusCode'] = 302
        response['headers']['Location'] = '/index.html'
    
    return response
