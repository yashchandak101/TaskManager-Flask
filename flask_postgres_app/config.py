import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/taskdb'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
