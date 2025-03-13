from typing import List, Dict
from pydantic import BaseModel, Field



# Define the resume schema
class ResumeSection(BaseModel):
    """Schema for a section of the resume."""
    title: str = Field(description="Title of the section")
    content: List[str] = Field(description="List of bullet points or paragraphs for this section")

class Resume(BaseModel):
    """Schema for the complete resume."""
    header: Dict[str, str] = Field(
        description="Header information like name, email, phone, LinkedIn, etc."
    )
    summary: str = Field(description="Professional summary paragraph")
    work_experience: List[ResumeSection] = Field(description="Work experience sections")
    skills: List[str] = Field(description="List of relevant skills")
    education: List[ResumeSection] = Field(description="Education sections")
    additional_sections: List[ResumeSection] = Field(
        description="Additional sections like certifications, projects, etc."
    )