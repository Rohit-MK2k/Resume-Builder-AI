# database/user.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from passlib.context import CryptContext

# Use relative import for Base
from ..database import Base

# Define pwd_context here or import from a central config/utils file if preferred
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    """User model for authentication and basic user info."""
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # OAuth related fields
    oauth_provider = Column(String, nullable=True)  # e.g., 'google', 'linkedin'
    oauth_user_id = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships - Use string reference "UserProfile"
    profiles = relationship("UserProfile", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        # Extract the plain password and remove it from kwargs
        plain_password = kwargs.pop('password', None)

        # Initialize the SQLAlchemy part with the remaining valid arguments
        super().__init__(**kwargs)

        # If a plain password was provided, store it temporarily for hashing
        if plain_password:
            self._password = plain_password

# Event listener for before insert
@event.listens_for(User, 'before_insert')
def hash_password_before_insert(mapper, connection, target):
    if hasattr(target, '_password') and target._password:
        target.hashed_password = pwd_context.hash(target._password)
        delattr(target, '_password')

# Event listener for before update
@event.listens_for(User, 'before_update')
def hash_password_before_update(mapper, connection, target):
    if hasattr(target, '_password') and target._password:
        target.hashed_password = pwd_context.hash(target._password)
        delattr(target, '_password')
