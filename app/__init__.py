from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import settings
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['HOST'] = settings.HOST
app.config['PORT'] = settings.PORT
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_STRING

db = SQLAlchemy(app)
db.init_app(app)
jwt = JWTManager(app)


def create_app():
    return app
