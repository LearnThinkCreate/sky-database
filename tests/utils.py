import environ
import google.auth
import io
import os
import pandas as pd

from google.cloud import secretmanager
from sky import Sky

# Saving GCP details to environment
env = environ.Env(DEBUG=(bool, True)) 
_, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

# Loading env variables from google secret manager
client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project_id}/secrets/db_secrets/versions/latest"
payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
env.read_env(io.StringIO(payload))

# Starting sky client
sky = Sky(
    api_key=os.getenv('BB_API_KEY'),
    token_path='/tmp/.sky-token',
    credentials={
        "client_id":os.getenv('CLIENT_ID'),
        "client_secret":os.getenv('CLIENT_SECRET'),
        "redirect_uri":'http://localhost:8080'
    })

def getStudents():
    students = sky.getUsers()

    clean_students = students[[
        'id', 'student_id', 'first_name', 'last_name',
        'preferred_name', 'student_info.grade_level',
        'custom_field_one', 'birth_date'
    ]].rename(columns={
        'student_info.grade_level':'grade_level',
        'custom_field_one':'counselor',
    }).astype({
        'id':'int64',
        'grade_level':'int32'
    })
    
    clean_students.birth_date = pd.to_datetime(clean_students.birth_date, errors = 'coerce')
    clean_students.student_id = pd.to_numeric(clean_students.student_id, errors='coerce')

    clean_students = clean_students.astype(object).where(pd.notnull(clean_students), None)

    return clean_students

def getTeachers():
    teachers = sky.getUsers(['Teacher', 'Advisor'])
    teachers = teachers[['id', 'first_name', 'last_name', 'gender', 'email']]
    teachers = teachers.drop_duplicates().reset_index(drop=True)
    return teachers