from sqlalchemy import Table, Column, MetaData, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, JSON, JSONB, MACADDR, MONEY, NUMERIC, OID, REAL, SMALLINT, TEXT, \
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR


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

academic_enrollment_table = Table(
    "academic_enrollments",
    metadata_obj,
    Column('user_id', ForeignKey('tp_students.id')),
    Column('section_id', ForeignKey('tp_sections.id')),
    Column('period', VARCHAR),
    Column('course_title', VARCHAR),
    Column('term', VARCHAR),
    Column('department', VARCHAR),
    Column('teacher_first', VARCHAR),
    Column('teacher_last', VARCHAR),
    PrimaryKeyConstraint('user_id', 'section_id', name='academic_enrollment_pk')
)

courses_table = Table(
    'tp_courses',
    metadata_obj,
    Column('id', INTEGER, primary_key=True, autoincrement=False, index=True),
    Column('course_code', VARCHAR),
    Column('course_title', VARCHAR),
    Column('level_description', VARCHAR),
    Column('course_length', INTEGER),
    Column('inactive', BOOLEAN)
)

sections_table = Table(
    'tp_sections',
    metadata_obj,
    Column('id', INTEGER, primary_key=True, autoincrement=False, index=True),
    Column('offering_id', ForeignKey('tp_courses.id')),
    Column('term', VARCHAR),
    Column('teacher_id', ForeignKey('tp_teachers.id'))
)

teachers_table = Table(
    'tp_teachers',
    metadata_obj,
    Column('id', INTEGER, primary_key=True, autoincrement=False, index=True),
    Column('first_name', VARCHAR),
    Column('last_name', VARCHAR),
    Column('gender', VARCHAR(1)),
    Column('email', VARCHAR)
)

advisory_enrollment_table = Table(
    "advising_enrollments",
    metadata_obj,
    Column('user_id', ForeignKey('tp_students.id')),
    Column('section_id', ForeignKey('tp_advising_sections.id')),
    PrimaryKeyConstraint('user_id', 'section_id', name='advisory_enrollment_pk')
)

advising_sections_table = Table(
    'tp_advising_sections',
    metadata_obj,
    Column('id', INTEGER, primary_key=True, autoincrement=False),
    Column('advisor_id', ForeignKey('tp_teachers.id')),
    Column('title', VARCHAR),
    Column('course_code', VARCHAR),
    Column('term', VARCHAR),
    Column('advisor_name', VARCHAR),
    Column('school_year', VARCHAR)
)

athletic_enrollment_table = Table(
    "athletic_enrollments",
    metadata_obj,
    Column('user_id', ForeignKey('tp_students.id')),
    Column('sport', VARCHAR),
    Column('coach_first', VARCHAR),
    Column('coach_last', VARCHAR),
    Column('section_id', INTEGER),
    Column('season', VARCHAR),
    PrimaryKeyConstraint('user_id', 'section_id', name='athletic_enrollment_pk')
)

gradebook_table = Table(
    "tp_gradebook_grades",
    metadata_obj,
    Column('grade', FLOAT, nullable=True),
    Column('last_updated', TIMESTAMP),
    Column('term', VARCHAR),
    Column('section_id', ForeignKey('tp_sections.id')),
    Column('user_id', ForeignKey('tp_students.id')),
    PrimaryKeyConstraint('user_id', 'section_id', 'term', name='gradebook_pk')
    
)

historic_grade_table = Table(
    'tp_historic_grades',
    metadata_obj,
    Column('course_code', VARCHAR),
    Column('course_title', VARCHAR, nullable=True),
    Column('credits_attempted', FLOAT),
    Column('credits_earned', FLOAT),
    Column('gpa_points', FLOAT),
    Column('grade', VARCHAR),
    Column('offering_id', INTEGER, nullable=True),
    Column('school_year', VARCHAR, nullable=True),
    Column('term', VARCHAR, nullable=True),
    Column('user_id', ForeignKey('tp_students.id')),
    Column('weight', FLOAT),
    Column('transcript_category', VARCHAR(30), nullable=True),
    PrimaryKeyConstraint('user_id', 'offering_id', 'course_title', 'term', 'school_year', name='historic_grade_pk')
)

psat_table = Table(
    'tp_psat_scores',
    metadata_obj,
    Column('id', INTEGER, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('tp_students.id'), unique=True),
    Column('total_score', INTEGER),
    Column('lang_score', INTEGER),
    Column('math_score', INTEGER)
)

student_gpa_table = Table(
    'tp_gpas',
    metadata_obj,
    Column('id', INTEGER, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('tp_students.id'), unique=True),
    Column('unweighted_gpa', FLOAT),
    Column('weighted_gpa', FLOAT)
)

attendance_table = Table(
    'tp_attendance',
    metadata_obj,
    Column('id', INTEGER, primary_key=True),
    Column('user_id', ForeignKey('tp_students.id')),
    Column('absence_type', VARCHAR),
    Column('absence_date', DATE),
    Column('absence_type_id', INTEGER),
    Column('section_id', VARCHAR),
    Column('term_name', VARCHAR),
    Column('excuse_description', VARCHAR)
)

candidate_table = Table(
    "tp_candidates",
    metadata_obj,
    Column('id', INTEGER, primary_key=True),
    Column('role', VARCHAR),
    Column('grade_level', INTEGER, nullable=True),
    Column('gender', VARCHAR),
    Column('financial_aid', BOOLEAN),
    Column('entering_year', VARCHAR),
    Column('application_status', VARCHAR),
    Column('ethnicity', VARCHAR)
)

contract_table = Table(
    "tp_contracts",
    metadata_obj,
    Column('user_id', INTEGER),
    Column('role', VARCHAR),
    Column('grade_level', INTEGER),
    Column('gender', VARCHAR(10)),
    Column('not_returning', INTEGER),
    Column('payment_plan', VARCHAR),
    Column('ethnicity', VARCHAR),
    Column('contract_year', VARCHAR(11)),
    PrimaryKeyConstraint('user_id', 'contract_year', name='tp_contract_pk')
)

attendance_code_table = Table(
    "tp_attendance_codes",
    metadata_obj,
    Column('id', INTEGER, primary_key=True),
    Column('name', VARCHAR)
)