from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
gategory = Table('gategory', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
)

category = Table('category', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
)

team = Table('team', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('key_access', VARCHAR(length=10)),
    Column('event_id', INTEGER),
    Column('gategory_id', INTEGER),
)

team = Table('team', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('key_access', String(length=10)),
    Column('event_id', Integer),
    Column('category_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['gategory'].drop()
    post_meta.tables['category'].create()
    pre_meta.tables['team'].columns['gategory_id'].drop()
    post_meta.tables['team'].columns['category_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['gategory'].create()
    post_meta.tables['category'].drop()
    pre_meta.tables['team'].columns['gategory_id'].create()
    post_meta.tables['team'].columns['category_id'].drop()
