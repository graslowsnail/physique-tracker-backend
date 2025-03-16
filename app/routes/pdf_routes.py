# routes/pdf_routes.py
from flask import Blueprint, request, jsonify, render_template, render_template_string
from app.controllers.pdf_controller import convert_pdf_to_images
from app.models.project import Project, PDFPage
from app.models.db import db
from app.models.user import User

pdf_routes = Blueprint('pdf_bp', __name__)

@pdf_routes.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    # First, ensure we have a test user
    test_user = User.query.first()
    if not test_user:
        # Create a test user if none exists
        test_user = User(
            name="Test User",
            email="test@example.com",
            username="testuser"
        )
        db.session.add(test_user)
        db.session.commit()
    
    # Check if the 'pdf' file part is present in the request
    if 'pdf' not in request.files:
        print(" empty request.files", request.files)
        return jsonify({'error': 'No file part in the request'}), 400
    
    pdf_file = request.files['pdf']
    # Check if a file was selected
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Use the test user's ID instead of hardcoded 2
        result = convert_pdf_to_images(pdf_file, user_id=test_user.id)
        image_urls = result['image_urls']
        print("Generated image URLs:", image_urls)
        
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
                img { max-width: 300px; height: auto; border: 1px solid #ddd; }
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


@pdf_routes.route('/user-projects/<int:user_id>', methods=['GET'])
def user_projects(user_id):
    # Fetch all projects for the given user ID
    projects = Project.query.filter_by(user_id=user_id).all()
    
    # Generate a simple HTML response to display the projects
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Projects</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .project-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
            .project-card { border: 1px solid #ddd; padding: 10px; text-align: center; }
            .project-card a { text-decoration: none; color: #333; }
            .project-card img { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>Your Projects</h1>
        <div class="project-grid">
            {% for project in projects %}
                <div class="project-card">
                    <a href="/project/{{ project.id }}">
                        <h2>{{ project.title }}</h2>
                        <img src="{{ project.image_path }}" alt="{{ project.title }}">
                    </a>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_content, projects=projects)

@pdf_routes.route('/project/<int:project_id>', methods=['GET'])
def project_detail(project_id):
    # Fetch the project by ID
    project = Project.query.get_or_404(project_id)
    
    # Fetch the associated images (assuming you have a relationship set up)
    images = project.pdf_pages  # Adjust this based on your model relationships
    
    # Generate HTML to display the images
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ project.title }}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .image-container { display: flex; flex-wrap: wrap; gap: 10px; }
            img { max-width: 150px; height: auto; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>{{ project.title }}</h1>
        <div class="image-container">
            {% for image in images %}
                <img src="{{ image.image_path }}" alt="Page {{ loop.index }}">
            {% endfor %}
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_content, project=project, images=images)