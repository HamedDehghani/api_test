import sqlalchemy as db
from config import settings

engine = db.create_engine(settings.SQLALCHEMY_DATABASE_URI)
