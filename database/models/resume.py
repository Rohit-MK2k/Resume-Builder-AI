from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Use relative import for Base
from ..database import Base

class Resume(Base):
    __tablename__ = "resume"

    id = Column(Integer, primary_key=True, index=True)
    # Add user_id FK based on the change to UserProfile
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(Integer, ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False) #name of the resume
    template_id = Column(Integer, ForeignKey("resume_templates.id"), nullable=True)

    # Store the job details this resume was generated for
    target_job = Column(JSONB, nullable=True)

    resume_data = Column(JSONB, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship - Use string references "UserProfile" and "ResumeTemplate"
    profile = relationship("UserProfile", back_populates="resumes")
    template = relationship("ResumeTemplate") # Assuming ResumeTemplate doesn't back-populate
