# routes/pdf_routes.py
from flask import Blueprint, request, jsonify, render_template, render_template_string
from app.controllers.pdf_controller import convert_pdf_to_images

pdf_routes = Blueprint('pdf_bp', __name__)

@pdf_routes.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    # Check if the 'pdf' file part is present in the request.
    if 'pdf' not in request.files:
        print(" empty request.files", request.files)
        return jsonify({'error': 'No file part in the request'}), 400
    
    pdf_file = request.files['pdf']
    # Check if a file was selected.
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        image_urls = convert_pdf_to_images(pdf_file)
        
        # Generate a simple HTML response to display the images
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>PDF to Images</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                .page { margin-bottom: 20px; }
                img { max-width: 100%; border: 1px solid #ddd; }
                .page-number { font-weight: bold; margin-bottom: 5px; }
            </style>
        </head>
        <body>
            <h1>Converted PDF Pages</h1>
            {% for url in image_urls %}
                <div class="page">
                    <div class="page-number">Page {{ loop.index }}</div>
                    <img src="{{ url }}" alt="Page {{ loop.index }}">
                </div>
            {% endfor %}
        </body>
        </html>
        """
        
        return render_template_string(html_content, image_urls=image_urls)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add a GET route for a simple upload form
@pdf_routes.route('/upload-form', methods=['GET'])
def upload_form():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PDF Upload Form</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            form { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>Upload a PDF File</h1>
        <form action="/upload-pdf" method="post" enctype="multipart/form-data">
            <input type="file" name="pdf" accept="application/pdf" required>
            <button type="submit">Convert to Images</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html_content)