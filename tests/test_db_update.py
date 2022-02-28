from unittest import TestCase
from skydb.classes import Student, Teacher
from skydb.sheets import createSpreadsheet, updateSpreadsheet
from skydb.connections import GooglePsqlConnection
from utils import *
from skydb.update import updateTable
from gspread.spreadsheet import Spreadsheet

class TestAuth(TestCase):
    def test_student_update(self):
        result = updateTable(
            db_class=Student,
            data_function=getStudents,
            table_type='Normal',
            conn=GooglePsqlConnection()
        )
        self.assertTrue(result)
    
    def test_teacher_update(self):
        result = updateTable(
            db_class=Teacher,
            data=getTeachers(),
            table_type='Normal',
        )
        self.assertTrue(result)
        
    def test_create_spreadsheet(self):
        result = createSpreadsheet(sky.getUsers()[['id', 'first_name', 'last_name']], 'Tox Test Spreadsheet')
        self.assertIsInstance(result, Spreadsheet)

    def test_update_spreadsheet(self):
        result = updateSpreadsheet(sky.getUsers('Teacher')[['id', 'first_name', 'last_name']],  sheet_name='Tox Test Spreadsheet')
        self.assertTrue(result)