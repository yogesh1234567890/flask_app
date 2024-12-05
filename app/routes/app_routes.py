import os
import uuid
import time

from flask import Blueprint, request, jsonify
from app.tasks.task import parse_pdf_task

app_routes = Blueprint('users', __name__)
UPLOAD_FOLDER='static/uploads'

@app_routes.route('/upload', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    pdf_file = request.files['file']
    if pdf_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    unique_id = f"{uuid.uuid4().hex[:8]}{int(time.time())}"
    folder_path = os.path.join(UPLOAD_FOLDER, unique_id)
    os.makedirs(folder_path, exist_ok=True)

    pdf_path = os.path.join(folder_path, pdf_file.filename)
    pdf_file.save(pdf_path)

    parse_pdf_task(pdf_path, folder_path)

    return jsonify({'message': 'File uploaded', 'id': unique_id}), 202