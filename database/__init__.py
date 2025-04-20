from .database import get_db, check_postgres_connection, create_tables
from .models import User, UserProfile, Resume, ResumeTemplate

check_postgres_connection()
create_tables()
