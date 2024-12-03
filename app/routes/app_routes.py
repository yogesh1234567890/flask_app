import os
import uuid

from flask import Blueprint, request, jsonify

app_routes = Blueprint('users', __name__)
UPLOAD_FOLDER='static/uploads'

@app_routes.route('/upload', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    pdf_file = request.files['file']
    if pdf_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Generate unique ID
    unique_id = str(uuid.uuid4())
    folder_path = os.path.join(UPLOAD_FOLDER, unique_id)
    os.makedirs(folder_path, exist_ok=True)

    # Save PDF to the folder
    pdf_path = os.path.join(folder_path, pdf_file.filename)
    pdf_file.save(pdf_path)

    # # Start background processing
    # parse_pdf_task.delay(pdf_path, folder_path)

    return jsonify({'message': 'File uploaded', 'id': unique_id}), 202
