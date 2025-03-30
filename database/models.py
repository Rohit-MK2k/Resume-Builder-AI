from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

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
    
    resume_data = Column(JSONB, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    profile = relationship("UserProfile", back_populates="resumes")
    
