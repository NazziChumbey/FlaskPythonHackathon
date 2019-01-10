#!flask/bin/python
import imp
from migrate.versioning import api
from app import db
from config import Config
migration = Config.SQLALCHEMY_DATABASE_URI + '/versions/%03d_migration.py' % (api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_DATABASE_URI) + 1)
tmp_module = imp.new_module('old_model')
old_model = api.create_model(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_DATABASE_URI)
exec (old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_DATABASE_URI, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_DATABASE_URI)
print ('New migration saved as ' + migration)
print ('Current database version: ' + str(api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_DATABASE_URI)))