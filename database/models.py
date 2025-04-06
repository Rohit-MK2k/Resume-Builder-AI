from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class User(Base):
    """User model for authentication and basic user info."""
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # OAuth related fields
    oauth_provider = Column(String, nullable=True)  # e.g., 'google', 'linkedin'
    oauth_user_id = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    external_user_id = Column(String, unique=True, index=True, nullable=False)

    personal_info = Column(JSONB, nullable=False)
    work_experience = Column(JSONB, nullable=False)
    education = Column(JSONB, nullable=False)
    skills = Column(JSONB, nullable=False)
    certifications = Column(JSONB, nullable=True)
    projects = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    resumes = relationship("Resume", back_populates="profile", cascade="all, delete-orphan")

class Resume(Base):
    __tablename__ = "resume"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False) #name of the resume
    template_id = Column(Integer, ForeignKey("resume_templates.id"), nullable=True)

    # Store the job details this resume was generated for
    target_job = Column(JSONB, nullable=True)

    
    resume_data = Column(JSONB, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    profile = relationship("UserProfile", back_populates="resumes")
    template = relationship("ResumeTemplate")
    
class ResumeTemplate(Base):
    """Model for storing resume templates."""
    __tablename__ = "resume_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Template configuration
    template_data = Column(JSONB, nullable=False)  # Stores styling and structure information
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())