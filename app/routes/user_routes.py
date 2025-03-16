from flask import Blueprint, request, jsonify, render_template, render_template_string
from app.models.project import Project, PDFPage
from app.models.db import db

user_routes = Blueprint("user", __name__)

@user_routes.route("/users", methods=["POST"])
def create_user():
    from app.models.user import User
    from app import db

    data = request.get_json()
    new_user = User(name=data["name"], email=data["email"], username=data["username"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

@user_routes.route("/users", methods=["GET"])
def get_users():
    from app.models.user import User

    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email, "username": u.username} for u in users])


@user_routes.route('/user-projects/<int:user_id>', methods=['GET'])
def user_projects(user_id):
    """
    Fetch all projects for a specific user and display them in a grid layout.
    
    Args:
        user_id: The ID of the user whose projects to fetch.
        
    Returns:
        HTML page displaying the user's projects in a grid.
    """
    try:
        # Fetch all projects for the given user ID
        projects = Project.query.filter_by(user_id=user_id).all()
        
        if not projects:
            # If no projects are found, display a message
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>User Projects</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; }
                    .message { text-align: center; margin-top: 50px; color: #666; }
                    .upload-link { display: block; text-align: center; margin-top: 20px; }
                </style>
            </head>
            <body>
                <h1>Your Projects</h1>
                <div class="message">
                    <p>You don't have any projects yet.</p>
                </div>
                <a class="upload-link" href="/upload-form">Upload a PDF to create a new project</a>
            </body>
            </html>
            """
        else:
            # Generate HTML to display the projects in a grid
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>User Projects</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; }
                    .project-grid { 
                        display: grid; 
                        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); 
                        gap: 20px; 
                        margin-top: 20px;
                    }
                    .project-card { 
                        border: 1px solid #ddd; 
                        border-radius: 8px;
                        overflow: hidden;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        transition: transform 0.3s ease;
                    }
                    .project-card:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                    }
                    .project-card a { 
                        text-decoration: none; 
                        color: #333;
                        display: block;
                    }
                    .project-image {
                        width: 100%;
                        height: 150px;
                        background-color: #f5f5f5;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        overflow: hidden;
                    }
                    .project-image img { 
                        width: 100%; 
                        height: 100%;
                        object-fit: cover;
                    }
                    .project-info {
                        padding: 15px;
                    }
                    .project-title {
                        margin: 0 0 10px 0;
                        font-size: 18px;
                    }
                    .project-meta {
                        color: #666;
                        font-size: 14px;
                    }
                    .upload-link {
                        display: inline-block;
                        margin-top: 20px;
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px 15px;
                        text-decoration: none;
                        border-radius: 4px;
                    }
                    .upload-link:hover {
                        background-color: #45a049;
                    }
                </style>
            </head>
            <body>
                <h1>Your Projects</h1>
                <a class="upload-link" href="/upload-form">Upload New PDF</a>
                <div class="project-grid">
                    {% for project in projects %}
                        <div class="project-card">
                            <a href="/project/{{ project.id }}">
                                <div class="project-image">
                                    {% if project.pdf_pages and project.pdf_pages|length > 0 %}
                                        <img src="{{ project.pdf_pages[0].image_path }}" alt="{{ project.title }}">
                                    {% else %}
                                        <div style="text-align: center; padding: 20px;">No preview available</div>
                                    {% endif %}
                                </div>
                                <div class="project-info">
                                    <h2 class="project-title">{{ project.title }}</h2>
                                    <div class="project-meta">
                                        {{ project.pdf_pages|length }} page(s)
                                        {% if project.description %}
                                            <p>{{ project.description }}</p>
                                        {% endif %}
                                    </div>
                                </div>
                            </a>
                        </div>
                    {% endfor %}
                </div>
            </body>
            </html>
            """
        
        return render_template_string(html_content, projects=projects)
    
    except Exception as e:
        # Log the error and return an error message
        print(f"Error fetching projects: {e}")
        return jsonify({'error': str(e)}), 500

