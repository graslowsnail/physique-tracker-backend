from app.models.db import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = "projects"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Unique folder ID for storage
    folder_id = db.Column(db.String(255), nullable=False)
    
    # Relationship with PDF pages
    pdf_pages = db.relationship('PDFPage', backref='project', lazy=True)
    
    image_path = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f"<Project {self.id}: {self.title}>"


class PDFPage(db.Model):
    __tablename__ = "pdf_pages"
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PDFPage {self.id}: Project {self.project_id}, Page {self.page_number}>" 