from flask import Flask, request, send_from_directory, abort
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    return send_from_directory('.', 'index.html')

@app.route('/files')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return {'files': files}, 200

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



