# controllers/pdf_controller.py
import os
import tempfile
import uuid
from pdf2image import convert_from_path
from flask import current_app

def convert_pdf_to_images(pdf_file, dpi=300):
    """
    Convert an uploaded PDF file to images and save them to the static folder.
    Returns a list of image URLs.
    """
    # Save the uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        pdf_file.save(temp_pdf.name)
        temp_pdf_path = temp_pdf.name

    try:
        # Create a unique folder name for this upload
        unique_id = str(uuid.uuid4())
        static_folder = os.path.join(current_app.static_folder, 'uploads', unique_id)
        os.makedirs(static_folder, exist_ok=True)
        
        # Convert PDF pages to images using pdf2image
        images = convert_from_path(temp_pdf_path, dpi=dpi)
        
        image_urls = []
        for i, image in enumerate(images):
            image_path = os.path.join(static_folder, f'page_{i+1}.png')
            image.save(image_path, format="PNG")
            # Create a URL relative to the static folder
            image_url = f'/static/uploads/{unique_id}/page_{i+1}.png'
            image_urls.append(image_url)
            
        return image_urls
    finally:
        # Remove the temporary file
        os.remove(temp_pdf_path)
