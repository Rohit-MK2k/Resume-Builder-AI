from .database import get_db, check_postgres_connection, create_tables
from .models.user import User
from .models.profile import UserProfile
from .models.resume import Resume
from .models.templete import ResumeTemplate

check_postgres_connection()
create_tables()
