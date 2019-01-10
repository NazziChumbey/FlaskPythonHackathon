#!flask/bin/python
from migrate.versioning import api
from config import Config

v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_DATABASE_URI)
api.downgrade(Config.SQLALCHEMY_DATABASE_URI,Config.SQLALCHEMY_DATABASE_URI, v - 1)
print ('Current database version: ' + str(api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_DATABASE_URI)))