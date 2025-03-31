import os
import subprocess
from logger import logger

def convert_docx_to_pdf(input_path):
    logger.info(f"Converting DOCX file to PDF: {input_path}")
    output_path = input_path.replace('.docx', '.pdf')
    try:
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(input_path), input_path], check=True)
        logger.info(f"Converted DOCX to PDF: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting DOCX to PDF: {e}")
        raise RuntimeError(f"Conversion failed: {e}")
