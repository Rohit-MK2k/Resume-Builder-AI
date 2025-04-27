# database/resume_template.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship # Keep if you add relationships FROM template
from sqlalchemy.sql import func

# Use relative import for Base
from ..database import Base

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

    # Add relationships here if a template needs to link to other models
    # Example: resumes = relationship("Resume", back_populates="template")
