import os
import uuid
import time
import csv
from celery.result import AsyncResult
from flask import jsonify, abort

from flask import Blueprint, request, jsonify, abort
from app.tasks.task import parse_pdf_task

app_routes = Blueprint('users', __name__)
UPLOAD_FOLDER='static/uploads'

@app_routes.route('/upload', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        abort(400, description="No file provided")

    pdf_file = request.files['file']
    if pdf_file.filename == '':
        abort(400, description="No file selected")

    unique_id = f"{uuid.uuid4().hex[:8]}{int(time.time())}"
    folder_path = os.path.join(UPLOAD_FOLDER, unique_id)
    os.makedirs(folder_path, exist_ok=True)

    pdf_path = os.path.join(folder_path, pdf_file.filename)
    pdf_file.save(pdf_path)

    parse_pdf_task.apply_async(args=[pdf_path, folder_path], task_id=unique_id)

    return jsonify({'message': 'File uploaded', 'id': unique_id}), 202

@app_routes.route('/status/<string:task_id>', methods=['GET'])
def get_status(task_id):
    try:
        result = AsyncResult(task_id)
        if result.status == 'PENDING' or result.status == 'STARTED':
            return jsonify({'status': 'In progress'}), 200

        if result.status == 'SUCCESS':
            task_folder_path = os.path.join(UPLOAD_FOLDER, task_id)
            if os.path.exists(task_folder_path):
                csv_files = [f for f in os.listdir(task_folder_path) if f.endswith('.csv')]
                data = {}
                for csv_file in csv_files:
                    csv_file_path = os.path.join(task_folder_path, csv_file)
                    with open(csv_file_path, 'r') as f:
                        reader = csv.DictReader(f)
                        data[csv_file] = [row for row in reader]
                return jsonify({'status': 'SUCCESS', 'data': data}), 200
            return jsonify({'status': 'SUCCESS', 'data': 'No files found'}), 200

        if result.status == 'FAILURE':
            task_folder_path = os.path.join(UPLOAD_FOLDER, task_id)
            error_log_path = os.path.join(task_folder_path, 'error_log.txt')
            if os.path.exists(error_log_path):
                with open(error_log_path, 'r') as f:
                    error_message = f.read()
                return jsonify({'status': 'FAILED', 'error': error_message}), 200

            return jsonify({'status': 'FAILED', 'error': 'Task failed but no error log found'}), 200

    except Exception as e:
        print(f"Error checking Celery task: {e}")

    task_folder_path = os.path.join(UPLOAD_FOLDER, task_id)
    if os.path.exists(task_folder_path):
        csv_files = [f for f in os.listdir(task_folder_path) if f.endswith('.csv')]
        if csv_files:
            data = {}
            for csv_file in csv_files:
                csv_file_path = os.path.join(task_folder_path, csv_file)
                with open(csv_file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    data[csv_file] = [row for row in reader]
            return jsonify({'status': 'SUCCESS', 'data': data}), 200

        error_log_path = os.path.join(task_folder_path, 'error_log.txt')
        if os.path.exists(error_log_path):
            with open(error_log_path, 'r') as f:
                error_message = f.read()
            return jsonify({'status': 'FAILED', 'error': error_message}), 200

    return jsonify({'status': 'UNKNOWN', 'error': 'Task ID does not exist and no files found'}), 404
