import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_DRIVER = "postgresql+psycopg2"
if os.environ.get('GAE_ENV') == 'standard':
    db_user = os.environ.get('CLOUD_SQL_USERNAME')
    db_pass = os.environ.get('CLOUD_SQL_PASSWORD')
    db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
    db_conn_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
else:
    db_user = "postgres"
    db_pass = "hacksc1"
    db_name = "college-data-db"
    db_conn_name = "fluent-plate-266907:us-west1:college-data"


url = f"{DB_DRIVER}://{db_user}:{db_pass}@/?host=/cloudsql/{db_conn_name}"
engine = create_engine(url, connect_args={'database': db_name})
db_session = scoped_session(sessionmaker(bind=engine))
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # import models
    Base.metadata.create_all(bind=engine)
