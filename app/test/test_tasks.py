import os
from unittest.mock import patch, mock_open
from app.tasks.task import parse_pdf_task

def test_parse_pdf_success(tmp_path):
    """Test successful PDF processing"""
    folder_path = tmp_path / "task_id"
    folder_path.mkdir()
    pdf_path = folder_path / "test.pdf"
    pdf_path.write_text("Fake PDF content")

    with patch('app.tasks.task.read_pdf') as mock_read_pdf, patch('builtins.open', mock_open()) as mock_file:
        # Mock `read_pdf` to return dummy data
        mock_read_pdf.return_value = [{'data': 'dummy_table'}]

        # Call the task
        parse_pdf_task(str(pdf_path), str(folder_path))

        # Assert CSV was created
        csv_path = folder_path / "table_1.csv"
        assert csv_path.exists()

        # Assert log file was created
        log_path = folder_path / "processing_time.txt"
        assert log_path.exists()
        mock_file().write.assert_any_call("Processing time")

def test_parse_pdf_error_handling(tmp_path):
    """Test error handling in parse_pdf_task"""
    folder_path = tmp_path / "task_id"
    folder_path.mkdir()
    pdf_path = folder_path / "test.pdf"
    pdf_path.write_text("Fake PDF content")

    with patch('app.tasks.task.read_pdf', side_effect=Exception("Test error")) as mock_read_pdf:
        # Call the task
        parse_pdf_task(str(pdf_path), str(folder_path))

        # Assert error log was created
        error_log_path = folder_path / "error_log.txt"
        assert error_log_path.exists()
        with open(error_log_path) as f:
            assert "Test error" in f.read()
