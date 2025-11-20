from flask import Flask, request, send_from_directory, abort
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Detecta si está en Docker (usando variable de entorno o existencia de /uploads)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Si existe /uploads (volumen de Docker), usar esa ruta
# Si no, usar ./uploads (desarrollo local)
if os.path.exists('/uploads') and os.environ.get('ENV') == 'production':
    UPLOAD_FOLDER = '/uploads'
else:
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    # Crea el directorio si no existe (solo en desarrollo local)
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    except PermissionError:
        print(f"Error: No se tienen permisos para crear {UPLOAD_FOLDER}")
        exit(1)

print(f"Usando UPLOAD_FOLDER: {UPLOAD_FOLDER}")

def validate_filename(filename):
    """Valida que el filename no contenga path traversal attacks"""
    if not filename or filename == '':
        return False
    # secure_filename elimina caracteres peligrosos y path traversal
    safe_name = secure_filename(filename)
    # Verifica que el filename no fue modificado (no contenía caracteres sospechosos)
    if safe_name != filename:
        return False
    # Verifica que el archivo existe en UPLOAD_FOLDER
    filepath = os.path.join(UPLOAD_FOLDER, safe_name)
    # Previene path traversal verificando que la ruta real está dentro de UPLOAD_FOLDER
    real_path = os.path.realpath(filepath)
    real_upload = os.path.realpath(UPLOAD_FOLDER)
    if not real_path.startswith(real_upload):
        return False
    return True

@app.route('/')
def index():
    # Usa BASE_DIR para asegurar que encuentra el archivo
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/files')
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return {'files': files}, 200
    except Exception as e:
        return {'error': str(e), 'files': []}, 500

@app.route('/download/<filename>')
def download_file(filename):
    if not validate_filename(filename):
        abort(400, 'Invalid filename')
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        abort(404, 'File not found')
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST', 'DELETE'])
def delete_file(filename):
    if not validate_filename(filename):
        abort(400, 'Invalid filename')
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        return {'message': 'File deleted successfully'}, 200
    return {'error': 'File not found'}, 404

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    # Sanitiza el filename para prevenir path traversal
    filename = secure_filename(file.filename)
    if not filename:
        return 'Invalid filename', 400
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return 'File uploaded successfully', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



