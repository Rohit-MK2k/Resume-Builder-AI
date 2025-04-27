from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Use relative import for Base
from ..database import Base

class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    # Correct FK definition for one-to-many
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Review if external_user_id is still needed or should be user_id
    # If it's a separate ID from another system, keep it.
    # If it was meant to be the link to User, remove it.
    external_user_id = Column(String, unique=True, index=True, nullable=False) # Assuming this is still needed

    personal_info = Column(JSONB, nullable=False)
    work_experience = Column(JSONB, nullable=False)
    education = Column(JSONB, nullable=False)
    skills = Column(JSONB, nullable=False)
    certifications = Column(JSONB, nullable=True)
    projects = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship - Use string references "User" and "Resume"
    # Correct back_populates to User.profiles
    user = relationship("User", back_populates="profiles")
    resumes = relationship("Resume", back_populates="profile", cascade="all, delete-orphan")
