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
    absences = relationship('Attendance', back_populates='student', cascade='delete')

    def __repr__(self):
        return f"Student({self.first_name!r} {self.last_name!r} - {self.student_id!r})"


class AcademicEnrollment(Base):
    __table__ = academic_enrollment_table

    student = relationship('Student', back_populates='classes')
    section = relationship('Section', back_populates='enrollment')

    def __repr__(self):
        return f"AcademicEnrollment({self.user_id!r} - {self.section_id!r} - {self.teacher_last!r})"


class Course(Base):
    __table__ = courses_table

    sections = relationship('Section', back_populates='course_info')

    def __repr__(self):
        return f"Course({self.course_title!r})"


class Section(Base):
    __table__ = sections_table

    course_info = relationship('Course', back_populates='sections')
    teacher = relationship('Teacher', back_populates='classes')
    gradebook_grades = relationship('GradebookGrades', back_populates='section')
    enrollment = relationship('AcademicEnrollment', back_populates='section')

    def __repr__(self):
        return f"Section({self.id!r} - {self.term!r})"


class Teacher(Base):
    __table__ = teachers_table

    advising = relationship('AdvisingSection', back_populates='advisor')
    classes = relationship('Section', back_populates='teacher')

    def __repr__(self):
        return f"Teacher({self.first_name} {self.last_name})"


class AdvisoryEnrollment(Base):
    __table__ = advisory_enrollment_table

    advisee = relationship('Student', back_populates='advising_section')
    section = relationship('AdvisingSection', back_populates='advisees')

    def __repr__(self):
        return f"AdvisoryEnrollment({self.user_id!r} - {self.section_id!r})"


class AdvisingSection(Base):
    __table__ = advising_sections_table

    advisees = relationship('AdvisoryEnrollment', back_populates='section')
    advisor = relationship('Teacher', back_populates='advising')

    def __repr__(self):
        return f"AdvisingSection({self.title!r})"


class AthleticEnrollment(Base):
    __table__ = athletic_enrollment_table

    athlete = relationship('Student', back_populates='sports')

    def __repr__(self):
        return f"AthleticEnrollment({self.user_id!r} - {self.sport!r} - {self.season!r})"


class GradebookGrades(Base):
    __table__ = gradebook_table

    section = relationship('Section', back_populates='gradebook_grades')
    student = relationship('Student', back_populates='gradebook_grades')

    def __repr__(self):
        return f"GradebookGrades({self.user_id!r} - {self.section_id!r} - Grade: {self.grade!r})"

class HistoricGrades(Base):
    __table__ = historic_grade_table
    
    student = relationship('Student', back_populates='historic_grades')

    def __repr__(self):
        return f"HistoricGrades({self.user_id!r} - {self.course_title!r} - {self.grade!r})"

class GPA(Base):
    __table__ = student_gpa_table
    
    student = relationship('Student', back_populates='gpa')

    def __repr__(self):
        return f"GPA({self.user_id!r} - {self.unweighted_gpa!r} - {self.weighted_gpa!r})"

class Psat(Base):
    __table__ = psat_table
    
    student = relationship('Student', back_populates='psat_score')

    def __repr__(self):
        return f"Psat({self.user_id!r} - {self.total_score!r})"


class Attendance(Base):
    __table__ = attendance_table

    student = relationship('Student', back_populates='absences')
    
    def __repr__(self):
        return f"Attendance({self.user_id!r} - {self.excuse_description!r} on {self.absence_date!r})"


class Candidate(Base):
    __table__ = candidate_table

    def __repr__(self):
        return f"Candidate({self.user_id!r} - {self.gender!r} {self.grade_level!r}th grader)"


class Contract(Base):
    __table__ = contract_table

    def __repr__(self):
        return f"Contract({self.user_id} - {self.grade_level!r} - returning: {self.returning!r})"

class AttendanceCode(Base):
    __table__ = attendance_code_table

    def __repr__(self):
        return f"AttendanceCode({self.excuse_name} ({self.excuse_id}))"