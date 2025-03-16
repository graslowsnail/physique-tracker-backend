from enum import unique
from app.models.db import db
from datetime import datetime


# user forgien key to define data relations
##collaborator_user_id = Column(Integer, ForeignKey("collaborators.user_id"), nullable=False)


class User(db.Model):
    __tablename__ = "users" # defines the table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    
    # Relationship with projects
    projects = db.relationship('Project', backref='owner', lazy=True, cascade="all, delete-orphan")

    # debugging 
    def __repr__(self):
        return f"<User {self.name}>"

def get_db():
    from app import db
    return db

