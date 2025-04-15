from .database import get_db, check_postgres_connection, create_tables

check_postgres_connection()
create_tables()
