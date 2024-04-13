from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(32) , primary_key=True , unique=True , default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    username = db.Column(db.Text ,unique=True , nullable=False)
    password = db.Column(db.Text , nullable=False)
    is_suspended = db.Column(db.Boolean , nullable=False ,default= False )
    login_attempt = db.Column(db.Integer , nullable=False ,default= 0 )

class AdminUser(db.Model):
    __tablename__ = "admin_users"
    id = db.Column(db.String(32) , primary_key=True , unique=True ,nullable=False)
    AccessLevel = db.Column(db.Enum('SuperAdmin', 'Admin', name='admin_types'), nullable=False)
