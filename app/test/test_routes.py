import os
import uuid
import pytest
import time
from flask import jsonify
from unittest.mock import patch
from run import create_app

UPLOAD_FOLDER = "/tmp/test_uploads"

@pytest.fixture
def client():
    """Fixture for Flask test client"""
    app, _ = create_app()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_celery_task(mocker):
    """Mock the Celery task"""
    return mocker.patch('app.routes.app_routes.parse_pdf_task.apply_async', return_value=None)

def test_upload_file_no_file(client):
    """Test upload when no file is provided"""
    response = client.post('/api/v1/upload')
    assert response.status_code == 400
    assert b"No file provided" in response.data

# def test_upload_file_no_filename(client):
#     """Test upload when an empty file is provided"""
#     data = {'file': (b'', '')}  # Empty file
#     response = client.post('/api/v1/upload', data=data, content_type='multipart/form-data')
#     assert response.status_code == 400
#     assert b"No file selected" in response.data

# def test_upload_file_success(client, mock_celery_task):
#     """Test a successful file upload"""
#     data = {'file': (open(__file__, 'rb'), 'test.pdf')}  # Use this script as a fake file
#     response = client.post('/api/v1/upload', data=data, content_type='multipart/form-data')
#     assert response.status_code == 202
#     assert b"File uploaded" in response.data

#     response_json = response.get_json()
#     assert 'id' in response_json

#     folder_path = os.path.join(UPLOAD_FOLDER, response_json['id'])
#     assert os.path.exists(folder_path)

# def test_upload_file_task_triggered(client, mock_celery_task):
#     """Ensure Celery task is triggered on file upload"""
#     data = {'file': (open(__file__, 'rb'), 'test.pdf')}
#     response = client.post('/api/v1/upload', data=data, content_type='multipart/form-data')
#     assert response.status_code == 202

#     response_json = response.get_json()
#     unique_id = response_json['id']

#     mock_celery_task.assert_called_once_with(
#         args=[os.path.join(UPLOAD_FOLDER, unique_id, 'test.pdf'), os.path.join(UPLOAD_FOLDER, unique_id)],
#         task_id=unique_id
#     )

# def test_upload_file_directory_created(client, mock_celery_task):
#     """Verify the upload folder is created after file upload"""
#     data = {'file': (open(__file__, 'rb'), 'test.pdf')}
#     response = client.post('/api/v1/upload', data=data, content_type='multipart/form-data')
#     assert response.status_code == 202

#     response_json = response.get_json()
#     unique_id = response_json['id']

#     folder_path = os.path.join(UPLOAD_FOLDER, unique_id)
#     assert os.path.exists(folder_path)

# def test_upload_file_cleanup(client, mock_celery_task):
#     """Verify cleanup logic, if any, can be triggered after a file upload"""
#     data = {'file': (open(__file__, 'rb'), 'test.pdf')}
#     response = client.post('/api/v1/upload', data=data, content_type='multipart/form-data')
#     assert response.status_code == 202

#     response_json = response.get_json()
#     folder_path = os.path.join(UPLOAD_FOLDER, response_json['id'])

#     # Assuming some cleanup logic can be triggered here
#     os.rmdir(folder_path)  # Clean up the directory for the test
#     assert not os.path.exists(folder_path)
