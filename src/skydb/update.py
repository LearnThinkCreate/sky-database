from .connections import GooglePsqlConnection

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


def updateTable(db_class, data_function=None, data=None, table_type="Normal", conn=GooglePsqlConnection()):
    if not hasattr(conn, 'init_db_engine') and callable(getattr(conn, 'init_db_engine')):
        raise NotImplementedError('Connection class must have valid init_db_engine method')
    # Intializing session
    session = Session(conn.init_db_engine())
    
    # Enrollment data is passed directly into func
    if isinstance(data, type(None)):
        # Getting data as pandas df
        data = data_function()

    # Making sure there's data to upload
    if data.empty:
        session.close()
        return False
    
    # Deleting old students, etc.
    if table_type == "Normal":
        delete_q = db_class.__table__.delete().where(~db_class.id.in_(data.id.tolist()))

        try:
            session.execute(delete_q)
            session.commit()

        except Exception as e:
            print(e)
            print()
            print('Delete failed')
            print()
            return False

    # Inserting/Uploading
    while not data.empty:
        if len(data) > 999:
            # Uploading max amount of data possible at once
            upload_data = data[:1000]
            # Reseting the value for data
            data = data[1001:]
        else:
            upload_data = data
            # Making data null
            data = data[0:0]

        # Insert statement
        stmt = insert(db_class).values(upload_data.to_dict(orient='records'))

        # Updating old data if there's a conflict
        if table_type == 'Normal':
            stmt = stmt.on_conflict_do_update(
                index_elements=['id'], set_=dict(stmt.excluded)
            ).returning(db_class)

        if table_type == 'Grades':
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id', 'section_id', 'term'], set_=dict(stmt.excluded)
            ).returning(db_class)

        if table_type == 'FinalGrades':
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id', 'section_id', 'term', 'grade_plan'], set_=dict(stmt.excluded)
            ).returning(db_class)

        if table_type == 'HistoricGrades':
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id', 'offering_id', 'course_title', 'term', 'school_year'], set_=dict(stmt.excluded)
            ).returning(db_class)

        if table_type == 'Enrollment':
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id', 'section_id'], set_=dict(stmt.excluded)
            ).returning(db_class)

        if table_type == 'Contracts':
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id', 'contract_year'], set_=dict(stmt.excluded)
            ).returning(db_class)        

        if table_type == 'User':
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id'], set_=dict(stmt.excluded)
            ).returning(db_class)   

        # Making statement orm friendly for session
        orm_stmt = (
            select(db_class)
            .from_statement(stmt)
            .execution_options(populate_existing=True)
        )

        # Executing the insert/deletes
        try:
            session.execute(
                orm_stmt,
            )
            session.commit()

        except Exception as e:
            print(e)
            session.close()
            return False
    print('-------------------------')
    print('Table updated')
    print()

    session.close()
    return True
