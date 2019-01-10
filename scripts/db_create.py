from migrate.versioning import api
from config import Config
from app import db
import os.path
db.create_all()
if not os.path.exists(Config.SQLALCHEMY_DATABASE_URI):
    api.create(Config.SQLALCHEMY_DATABASE_URI, 'database repository')
    api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_DATABASE_URI)
else:
    api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_DATABASE_URI, api.version(Config.SQLALCHEMY_DATABASE_URI))