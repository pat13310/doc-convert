# Application de Conversion de Documents

Une application web complète pour convertir, extraire et manipuler différents formats de documents.

## Fonctionnalités

- **Conversion de Documents**
  - Conversion de DOCX vers PDF
  - Conversion de PDF vers DOCX

- **Extraction de Texte**
  - Extraction à partir de fichiers PDF
  - Extraction à partir de fichiers DOCX
  - Extraction à partir de fichiers XLS/XLSX
  - Extraction à partir de fichiers CSV

- **Conversion de PDF vers Images**
  - Conversion de chaque page d'un PDF en images PNG
  - Compression des images dans un fichier ZIP

## Installation

### Prérequis

- Python 3.7 ou supérieur
- Pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Clonez ce dépôt :
   ```
   git clone <url-du-dépôt>
   cd convert-document-new
   ```

2. Créez un environnement virtuel :
   ```
   python -m venv venv
   ```

3. Activez l'environnement virtuel :
   - Sous Windows :
     ```
     venv\Scripts\activate
     ```
   - Sous Linux/Mac :
     ```
     source venv/bin/activate
     ```

4. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

5. Créez les dossiers nécessaires :
   ```
   mkdir -p backend/uploads backend/output backend/temp
   ```

## Utilisation

1. Démarrez le serveur :
   ```
   uvicorn backend.app.main:app --reload
   ```

2. Ouvrez votre navigateur et accédez à :
   ```
   http://localhost:8000
   ```

3. Utilisez l'interface pour accéder aux différentes fonctionnalités.

## Structure du Projet

```
convert-document-new/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── convert.py
│   │   │   ├── extract.py
│   │   │   └── pdf_images.py
│   │   ├── config.py
│   │   └── main.py
│   ├── services/
│   │   └── document_service.py
│   └── utils/
│       └── file_utils.py
├── frontend/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── scripts.js
│   ├── pages/
│   │   ├── convert.html
│   │   ├── extract.html
│   │   └── pdf-to-images.html
│   └── index.html
├── venv/
├── requirements.txt
└── README.md
```

## Technologies Utilisées

- **Backend** : FastAPI, Python
- **Frontend** : HTML, CSS, JavaScript
- **Bibliothèques principales** :
  - python-docx : Manipulation de fichiers DOCX
  - PyMuPDF (fitz) : Manipulation de fichiers PDF
  - pandas : Traitement de fichiers XLS et CSV
  - reportlab : Génération de PDF

## Contact

Pour toute question ou assistance, veuillez contacter : xenatronics@gmx.fr
