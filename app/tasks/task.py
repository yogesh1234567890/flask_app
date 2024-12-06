import os
from datetime import datetime
from tabula import read_pdf
from app.celery import celery


@celery.task(name='parse_pdf_task')
def parse_pdf_task(pdf_path, folder_path):
    start_time = datetime.now()  
    try:
        data = read_pdf(pdf_path, stream=True, pages='all')
        for idx, table in enumerate(data):
            print(f"Processing table {idx + 1}")
            csv_path = os.path.join(folder_path, f'table_{idx + 1}.csv')
            table.to_csv(csv_path, index=False)  # Save table to CSV file
        end_time = datetime.now()  
        processing_time = (end_time - start_time).total_seconds()  # Calculate time in seconds
        with open(os.path.join(folder_path, 'processing_time.txt'), 'w') as f:
            f.write(f"Processing time: {processing_time} seconds\n")
            f.write(f"Start Time: {start_time}\n")
            f.write(f"End Time: {end_time}\n")
        print(f"PDF processing complete in {processing_time} seconds")

    except Exception as e:
        error_file_path = os.path.join(folder_path, 'error_log.txt')
        with open(error_file_path, 'w') as error_file:
            error_file.write(str(e))  # Save the error message to a text file
        print(f"Error: {str(e)}")