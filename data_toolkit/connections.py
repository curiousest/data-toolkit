from sqlalchemy import Column, Integer, MetaData, Table, create_engine, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import select


ENGINE = "postgres"
HOST = "somehost.com"
USER = "postgres"
PASSWORD = "postgres"
DB_NAME = "dbname"


engine = create_engine('{}://{}:{}@{}:5432/{}'.format(
    ENGINE,
    USER,
    PASSWORD,
    HOST,
    DB
), client_encoding='utf8')
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

metadata = MetaData()
metadata.reflect(engine, only=['tablename',])
Base = automap_base(metadata=metadata)
Base.prepare()

TableName = Base.classes.tablename


def get_db_session():
    return db_session


def first_tablename():
    s = select([TableName]).where(TableName.id > 1)
    return db_session.execute(s).first()

