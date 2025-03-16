# controllers/pdf_controller.py
import os
import tempfile
import uuid
from pdf2image import convert_from_path
from flask import current_app
from PIL import Image
from app.models.db import db
from app.models.project import Project, PDFPage

def convert_pdf_to_images(pdf_file, user_id, title=None, description=None, dpi=300):
    """
    Convert an uploaded PDF file to images, save them to the static folder,
    and create database records for the project and pages.
    
    Args:
        pdf_file: The uploaded PDF file
        user_id: The ID of the user who uploaded the file
        title: Optional title for the project (defaults to filename)
        description: Optional description for the project
        dpi: DPI for the image conversion
        
    Returns:
        A dictionary containing project info and a list of image URLs.
    """
    Image.MAX_IMAGE_PIXELS = None  # Disable the limit (use with caution)
    
    # Save the uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        pdf_file.save(temp_pdf.name)
        temp_pdf_path = temp_pdf.name

    try:
        # Create a unique folder name for this upload
        unique_id = str(uuid.uuid4())
        static_folder = os.path.join(current_app.static_folder, 'uploads', unique_id)
        os.makedirs(static_folder, exist_ok=True)
        
        # Set default title if not provided
        if title is None:
            title = pdf_file.filename or "Untitled Project"
        
        # Create a new project in the database
        project = Project(
            title=title,
            description=description,
            user_id=user_id,
            folder_id=unique_id
        )
        db.session.add(project)
        db.session.flush()  # Get the project ID without committing
        
        # Convert PDF pages to images using pdf2image
        images = convert_from_path(temp_pdf_path, dpi=dpi)
        
        image_urls = []
        pdf_pages = []
        
        for i, image in enumerate(images):
            page_number = i + 1
            image_filename = f'page_{page_number}.png'
            image_path = os.path.join(static_folder, image_filename)
            image.save(image_path, format="PNG")
            print(f"Saved image: {image_path}")  # Debugging line
            
            # Create a URL relative to the static folder
            image_url = f'/static/uploads/{unique_id}/{image_filename}'
            image_urls.append(image_url)
            
            # Create a database record for this page
            pdf_page = PDFPage(
                project_id=project.id,
                page_number=page_number,
                image_path=image_url
            )
            pdf_pages.append(pdf_page)
        
        # Add all pages to the database
        db.session.add_all(pdf_pages)
        db.session.commit()
        
        print("Generated image URLs:", image_urls)  # Debugging line
        
        return {
            'project_id': project.id,
            'title': project.title,
            'folder_id': unique_id,
            'page_count': len(images),
            'image_urls': image_urls
        }
    
    except Exception as e:
        # Handle exceptions related to image processing
        print(f"Error processing images: {e}")
        db.session.rollback()
        # Clean up the folder if it was created
        if os.path.exists(static_folder):
            import shutil
            shutil.rmtree(static_folder)
        raise e
    
    finally:
        # Remove the temporary file
        os.remove(temp_pdf_path)
