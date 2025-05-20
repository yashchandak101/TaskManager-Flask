from flask import Flask
from app.models import db
from app.routes import bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)


    app.register_blueprint(bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
