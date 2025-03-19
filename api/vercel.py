from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Gère les requêtes GET"""
        if self.path == '/':
            # Rediriger vers la page d'accueil
            self.send_response(302)
            self.send_header('Location', '/frontend/index.html')
            self.end_headers()
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
        else:
            # Pour toutes les autres requêtes GET, renvoyer une erreur 404
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'error': 'Page non trouvée',
                'message': 'La ressource demandée n\'existe pas'
            }
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Gère les requêtes POST"""
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
                'message': 'L\'API demandée n\'existe pas'
            }
            self.wfile.write(json.dumps(response).encode())
