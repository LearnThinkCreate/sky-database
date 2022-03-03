# skydb

## About

Library for creating and maintaining k-12 data in conjunction with the Blackbaud information system.

## Goals 

Create library for setting up and maintaining Tampa Preparatory school's data warehouse with latest data from Blackbaud.

## Examples

``` Python
from utils import getStudents
from skydb.tables import student_table, metadata_obj
from skydb.classes import Student
from skydb.sheets import *
from skydb.connections import GooglePsqlConnection
from skydb.sheets.style import BaseStyle
from gspread_formatting import *

# Creating a single table 
student_table.create(GooglePsqlConnection().init_db_engine())

# Dropping a table
student_table.drop(GooglePsqlConnection().init_db_engine())

# Creating all the tables 
metadata_obj.create_all(GooglePsqlConnection().init_db_engine())

# Reading a spreadsheet
counselors = readSpreadsheet(sheet_name='Tampa Prep Counselors')

# Creating a google sheets style class
class HysonFireStyle(BaseStyle):
    def style(self, ncol=100):
        set_frozen(self.worksheet, rows=1, cols=2)
        """ Body """
        self.worksheet.format(':', {
                'horizontalAlignment': 'CENTER',
                'textFormat':{
                    'fontSize': 14
                },
            #  'wrapStrategy': 'WRAP',
            })

        """ Header """
        # Bold
        self.worksheet.format('1:', {'textFormat': {'bold': True, 'fontSize':12}})
        # Background color
        self.worksheet.format('1:', self.mplColorConverter(color='lightgrey'))

        self.worksheet.columns_auto_resize(0, ncol)
        
# Updating a spreadsheet with a custom class
updateSpreadsheet(getStudents().fillna(''), 
                  sheet_name='Student Spreadsheet',
                  styleClass=HysonFireStyle
                 )
```

## Connection Classes & sqlalchemy

In order to set up and update the database I elected to use [sqlalchemy](https://docs.sqlalchemy.org/en/14/tutorial/index.html). 

There are 4 main steps in creating/maintaining a database with sqlalchemy
1. [The engine](https://github.com/LearnThinkCreate/sky-database/blob/main/src/skydb/connections.py)
    1. [sqlalchemy docs](https://docs.sqlalchemy.org/en/14/tutorial/engine.html)
    2. To create a standard method for connecting and updating the data, I've used connection classes
2. [The tables](https://github.com/LearnThinkCreate/sky-database/blob/main/src/skydb/tables.py)
    1. [sqlalchemy docs](https://docs.sqlalchemy.org/en/14/tutorial/metadata.html)
4. [The classes](https://github.com/LearnThinkCreate/sky-database/blob/main/src/skydb/classes.py)
    1. [sqlalchemy docs](https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#declaring-mapped-classes)
6. [The update function](https://github.com/LearnThinkCreate/sky-database/blob/main/src/skydb/update.py)


## skydb.tables

``` Python
# Object for creating each table
metadata_obj = MetaData()

student_table = Table(
    "tp_students",
    metadata_obj,
    Column('id', INTEGER, primary_key=True, autoincrement=False, index=True),
    Column('student_id', FLOAT, autoincrement=True, index=True),
    Column('first_name', VARCHAR),
    Column('last_name', VARCHAR),
    Column('preferred_name', VARCHAR),
    Column('grade_level', VARCHAR, index=True),
    Column('counselor', VARCHAR),
    Column('birth_date', TIMESTAMP, nullable=True)
)
```

## skydb.classes


``` Python  
from sqlalchemy.orm import declarative_base, relationship
# Db tables, engine, and MetaData object
from .tables import *

# Connecting to sqlite db for testing
# engine = create_engine("sqlite+pysqlite:///sky_test.db",  future=True, echo=True)

Base = declarative_base()


class Student(Base):
    __table__ = student_table

    classes = relationship("AcademicEnrollment",  back_populates="student", cascade='delete')
    sports = relationship("AthleticEnrollment", back_populates='athlete', cascade='delete')
    advising_section = relationship('AdvisoryEnrollment', back_populates='advisee', cascade='delete')
    gradebook_grades = relationship('GradebookGrades', back_populates='student', cascade='delete')
    historic_grades = relationship('HistoricGrades', back_populates='student', cascade='delete')
    gpa = relationship('GPA', back_populates='student', cascade='delete')
    psat_score = relationship('Psat', back_populates='student', cascade='delete')
    final_grades = relationship('FinalGrades', back_populates='student', cascade='delete')
    absences = relationship('Attendance', back_populates='student', cascade='delete')

    def __repr__(self):
        return f"Student({self.first_name!r} {self.last_name!r} - {self.student_id!r})"
```

## skydb.sheets

Inspired by [this guide](https://levelup.gitconnected.com/python-pandas-google-spreadsheet-476bd6a77f2b) on using pandas and gspread, 
this script provides 3 helper functions that make working with Google Sheets 
really easy -- `readSpreadsheet`, `updateSpreadsheet`, and `createSpreadsheet`. 
I've also added style classes into the mix in order to provide some flair.

These functions are just convenient wrappers around the [gspread library](https://docs.gspread.org/en/latest/oauth2.html). 
I highly recommend checking out these resources if you'd like to use Google Sheets and Python as a part of your 
schools reporting solution 


Example:
``` Python
from skydb.sheets import *
# grades is a padas.DataFrame object
from utils import grades

counselors = readSpreadsheet(sheet_name='Tampa Prep Counselors')
updateSpreadsheet(grades.astype(str), sheet_name = "Sky Grades")
```
