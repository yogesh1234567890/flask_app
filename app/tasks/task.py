import os
import pandas as pd
from tabula import read_pdf
from app.celery import celery


# @celery.task
def parse_pdf_task(pdf_path, folder_path):
    try:
        data = read_pdf(pdf_path, stream=True, pages='all')
        for idx, table in enumerate(data):
            print(f"Processing table {idx + 1}")
            csv_path = os.path.join(folder_path, f'table_{idx + 1}.csv')
            table.to_csv(csv_path, index=False)  # Save table to CSV file

        print("PDF processing complete")

    except Exception as e:
        error_file_path = os.path.join(folder_path, 'error_log.txt')
        with open(error_file_path, 'w') as error_file:
            error_file.write(str(e))  # Save the error message to a text file
        print(f"Error: {str(e)}")