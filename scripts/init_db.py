import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

from database.database import engine, Base
from database.models import User, UserProfile, Resume, ResumeTemplate
from core.config import settings

# Load environment variables
load_dotenv()

def create_tables():
    """Create all database tables based on SQLAlchemy models."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except SQLAlchemyError as e:
        print(f"Error creating database tables: {e}")
        sys.exit(1)

def check_postgres_connection():
    """Check if we can connect to PostgreSQL."""
    print(f"Trying to connect to PostgreSQL at {settings.POSTGRES_SERVER}...")

    try:
        # Try to execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Successfully connected to PostgreSQL!")
    except SQLAlchemyError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        print("\nPlease check your database settings:")
        print(f"  Server: {settings.POSTGRES_SERVER}")
        print(f"  Database: {settings.POSTGRES_DB}")
        print(f"  User: {settings.POSTGRES_USER}")
        print("  (Password hidden)")
        sys.exit(1)

def create_default_templates():
    """Create default resume templates."""
    from sqlalchemy.orm import Session

    templates = [
        {
            "name": "Modern",
            "description": "A clean, modern design with customizable accent colors.",
            "template_data": {
                "font_family": "Roboto, sans-serif",
                "primary_color": "#2563eb",
                "secondary_color": "#e5e7eb",
                "heading_style": "uppercase",
                "section_spacing": "1.5rem",
                "border_style": "none",
            }
        }
    ]

    # Create a session and add templates
    with Session(engine) as session:
        # Check if templates already exist
        existing_count = session.query(ResumeTemplate).count()
        if existing_count > 0:
            print(f"Found {existing_count} existing templates. Skipping template creation.")
            return
        
        print("Creating default resume templates...")
        for template_data in templates:
            template = ResumeTemplate(**template_data)
            session.add(template)
        
        session.commit()
        print(f"Created {len(templates)} default templates!")


def main():
    """Initialize the database."""
    print("Database initialization starting...")
    check_postgres_connection()
    create_tables()
    create_default_templates()
    print("\nDatabase initialization completed successfully!")

if __name__ == "__main__":
    main()