import logging
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from init_llm import get_llm
from Schema.resume_Schema import Resume


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Create a resume generator class
class ResumeGenerator:
    """Generate tailored resumes based on user data and job details."""
    
    def __init__(self):
        self.llm = get_llm()
        self.output_parser = PydanticOutputParser(pydantic_object=Resume)
    
    def _create_resume_prompt(self):
        """Create the prompt template for resume generation."""
        template = """
        You are an expert resume writer with years of experience creating tailored, ATS-friendly resumes.
        
        # USER PROFILE
        {user_profile}
        
        # JOB DETAILS
        Company: {company_name}
        Role: {job_role}
        
        # JOB DESCRIPTION
        {job_description}
        
        Create a tailored, professional resume that highlights the most relevant skills and experiences 
        for this specific job. Focus on quantifiable achievements and use strong action verbs.
        Make sure the resume is ATS-friendly and optimized with relevant keywords from the job description.
        
        Limit the resume to one page worth of content and prioritize the most relevant information.
        
        {format_instructions}
        """
        
        return ChatPromptTemplate.from_template(template)
    
    def generate_resume(
        self, 
        user_profile: Dict[str, Any], 
        company_name: str, 
        job_role: str, 
        job_description: str
    ) -> Resume:
        """
        Generate a tailored resume.
        
        Args:
            user_profile: Dictionary containing user's data (experience, education, skills, etc.)
            company_name: Name of the company being applied to
            job_role: The role being applied for
            job_description: Full job description
            
        Returns:
            Resume object with tailored content
        """
        prompt = self._create_resume_prompt()
        chain = prompt | self.llm 
        
        # Format user profile for the prompt
        user_profile_text = self._format_user_profile(user_profile)
        
        result = chain.invoke({
            "user_profile": user_profile_text,
            "company_name": company_name,
            "job_role": job_role,
            "job_description": job_description,
            "format_instructions": self.output_parser.get_format_instructions()
        })
        
        try:
            # Try to parse the structured output
            resume_content = self.output_parser.parse(result.content)
            return resume_content
        except Exception as e:
            logger.error(f"Error parsing output: {e}")
            # Fallback: return raw text
            logger.info("Falling back to raw output")
            return result.content
    
    def _format_user_profile(self, user_profile: Dict[str, Any]) -> str:
        """Format user profile data for inclusion in the prompt."""
        sections = []
        
        # Personal Info
        if "personal_info" in user_profile:
            pi = user_profile["personal_info"]
            personal_info = [
                "## PERSONAL INFORMATION",
                f"Name: {pi.get('name', 'Not provided')}",
                f"Email: {pi.get('email', 'Not provided')}",
                f"Phone: {pi.get('phone', 'Not provided')}",
                f"Location: {pi.get('location', 'Not provided')}",
                f"LinkedIn: {pi.get('linkedin', 'Not provided')}"
            ]
            sections.append("\n".join(personal_info))
        
        # Work Experience
        if "work_experience" in user_profile:
            work_exp = ["## WORK EXPERIENCE"]
            for job in user_profile["work_experience"]:
                job_details = [
                    f"Company: {job.get('company', 'Not provided')}",
                    f"Role: {job.get('role', 'Not provided')}",
                    f"Duration: {job.get('duration', 'Not provided')}",
                    f"Location: {job.get('location', 'Not provided')}",
                    "Responsibilities and Achievements:"
                ]
                
                for item in job.get("achievements", []):
                    job_details.append(f"- {item}")
                
                work_exp.append("\n".join(job_details) + "\n")
            
            sections.append("\n".join(work_exp))
        
        # Education
        if "education" in user_profile:
            edu = ["## EDUCATION"]
            for school in user_profile["education"]:
                edu_details = [
                    f"Institution: {school.get('institution', 'Not provided')}",
                    f"Degree: {school.get('degree', 'Not provided')}",
                    f"Field: {school.get('field', 'Not provided')}",
                    f"Graduation Date: {school.get('graduation_date', 'Not provided')}",
                    f"GPA: {school.get('gpa', 'Not provided')}"
                ]
                edu.append("\n".join(edu_details) + "\n")
            
            sections.append("\n".join(edu))
        
        # Skills
        if "skills" in user_profile:
            skills = ["## SKILLS"]
            skills.append(", ".join(user_profile["skills"]))
            sections.append("\n".join(skills))
        
        # Certifications
        if "certifications" in user_profile:
            certs = ["## CERTIFICATIONS"]
            for cert in user_profile["certifications"]:
                certs.append(f"- {cert}")
            sections.append("\n".join(certs))
        
        # Projects
        if "projects" in user_profile:
            projs = ["## PROJECTS"]
            for project in user_profile["projects"]:
                proj_details = [
                    f"Name: {project.get('name', 'Not provided')}",
                    f"Description: {project.get('description', 'Not provided')}",
                    "Technologies: " + ", ".join(project.get("technologies", []))
                ]
                projs.append("\n".join(proj_details) + "\n")
            
            sections.append("\n".join(projs))
        
        return "\n\n".join(sections)