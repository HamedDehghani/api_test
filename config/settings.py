# Flask settings
FLASK_SERVER_NAME = 'localhost:5000'
HOST = "localhost"
PORT = 5000
FLASK_DEBUG = False  # Do not use debug mode in production
API_KEY = '8C2995BF5EDB481FB65BEE0551228D26'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
JWT_SECRET_STRING = 'jwt-secret-string'

# SQLAlchemy settings
# SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
