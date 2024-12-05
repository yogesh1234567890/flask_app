import os
import uuid
import time
import csv

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

    parse_pdf_task.apply_async(args=[pdf_path, folder_path], task_id=unique_id)

    return jsonify({'message': 'File uploaded', 'id': unique_id}), 202

@app_routes.route('/status/<string:task_id>', methods=['GET'])
def get_status(task_id):
    code_path = os.path.join(UPLOAD_FOLDER, task_id)
    if not os.path.exists(code_path):
        return jsonify({'error': 'Task not found'}), 404
    
    if os.path.exists(os.path.join(code_path, 'error_log.txt')):
        with open(os.path.join(code_path, 'error_log.txt'), 'r') as f:
            error_message = f.read()
        return jsonify({'status': 'failed', 'error': error_message}), 200
    
    elif os.path.exists(code_path):
        csv_files = [f for f in os.listdir(code_path) if f.endswith('.csv')]
        data = {}
        for csv_file in csv_files:
            csv_file_path = os.path.join(code_path, csv_file)

            with open(csv_file_path, 'r') as f:
                reader = csv.DictReader(f)  
                data[csv_file] = [row for row in reader]  

        return jsonify({'status': 'completed', 'data': data}), 200
    else:
        return jsonify({'status': 'pending'}), 200