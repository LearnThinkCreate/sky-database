from sqlalchemy.engine.base import Engine as psqlEngine
from sqlalchemy.future.engine import Engine as sqlliteEngine
from unittest import TestCase

import environ
import google.auth
import io
import os

from google.cloud import secretmanager
from skydb.connections import GooglePsqlConnection, SqlLiteConnection

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials/service_account.json'

# Saving GCP details to environment
env = environ.Env(DEBUG=(bool, True)) 
_, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

# Loading env variables from google secret manager
client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project_id}/secrets/skydb-connection/versions/latest"
payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
env.read_env(io.StringIO(payload))

class TestAuth(TestCase):

    def test_psql_connection(self):
        engine = GooglePsqlConnection().init_db_engine()
        self.assertIsInstance(engine, psqlEngine)
    
    def test_sqlite_connection(self):
        engine = SqlLiteConnection.init_db_engine()
        self.assertIsInstance(engine, sqlliteEngine)