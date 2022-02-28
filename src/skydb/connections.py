import os
import sqlalchemy
import pg8000
import os

from google.cloud.sql.connector import connector
from sqlalchemy import create_engine

class GooglePsqlConnection:
    def __init__(
        self,
        username=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        instance=os.environ.get('INSTANCE_CONNECTION_NAME'),
        db=os.environ.get('DB_NAME')
    ):
        self.username = username
        self.password = password
        self.instance = instance
        self.db = db
    
    def getconn(self):
        conn: pg8000.dbapi.Connection = connector.connect(
            os.getenv("INSTANCE_CONNECTION_NAME"),
            "pg8000",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            db=os.getenv("DB_NAME"),
        )
        return conn

    def init_db_engine(self):
        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=self.getconn,
        )
        engine.dialect.description_encoding = None
        return engine     

class SqlLiteConnection:
    def init_db_engine(db_name="sky_test"):
        return create_engine(f"sqlite+pysqlite:///{db_name}.db",  future=True, echo=True)
