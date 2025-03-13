import logging
import os
from typing import Dict, Any, List

from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Initialize the LLM
def get_llm():
    """Initialize and return the language model."""
    # api_key = os.getenv("OPENAI_API_KEY")
    # if not api_key:
    #     raise ValueError("OPENAI_API_KEY environment variable not set")
    # return ChatOpenAI(
    #     model="gpt-4o-mini",
    #     temperature=0.2,
    #     api_key=api_key
    # )
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set")

    return init_chat_model(
        "gpt-4o-mini", 
        model_provider="openai",
        temperature = 0.2,
    )

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
            resume_content = self.output_parser.parse(result)
            print(resume_content)
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


def main():
    """Main function to demonstrate resume generation."""
    # Example user profile
    user_profile = {
        "personal_info": {
            "name": "Alex Johnson",
            "email": "alex.johnson@example.com",
            "phone": "123-456-7890",
            "location": "San Francisco, CA",
            "linkedin": "linkedin.com/in/alexjohnson"
        },
        "work_experience": [
            {
                "company": "Tech Solutions Inc.",
                "role": "Senior Software Engineer",
                "duration": "Jan 2019 - Present",
                "location": "San Francisco, CA",
                "achievements": [
                    "Led development of a microservices architecture that improved system response time by 40%",
                    "Implemented CI/CD pipeline reducing deployment time from days to hours",
                    "Mentored 5 junior developers on best practices and design patterns"
                ]
            },
            {
                "company": "Data Innovations",
                "role": "Software Engineer",
                "duration": "Jun 2016 - Dec 2018",
                "location": "Boston, MA",
                "achievements": [
                    "Developed RESTful APIs for data analysis platform used by 500+ clients",
                    "Optimized database queries reducing load time by 30%",
                    "Collaborated with UX team to redesign user interface improving user satisfaction by 25%"
                ]
            }
        ],
        "education": [
            {
                "institution": "MIT",
                "degree": "Master's",
                "field": "Computer Science",
                "graduation_date": "2016",
                "gpa": "3.8/4.0"
            },
            {
                "institution": "University of California, Berkeley",
                "degree": "Bachelor's",
                "field": "Computer Science",
                "graduation_date": "2014",
                "gpa": "3.7/4.0"
            }
        ],
        "skills": [
            "Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes",
            "CI/CD", "Microservices", "REST APIs", "SQL", "NoSQL", "Git", "Agile"
        ],
        "certifications": [
            "AWS Certified Solutions Architect",
            "Certified Kubernetes Administrator (CKA)",
            "Google Professional Cloud Developer"
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Developed a scalable e-commerce platform with payment integration",
                "technologies": ["Python", "Django", "React", "PostgreSQL", "Stripe API"]
            }
        ]
    }
    
    # Example job details
    company_name = "Innovate Tech"
    job_role = "Lead Software Engineer"
    job_description = """
    We're looking for a Lead Software Engineer to join our growing team. The ideal candidate
    has experience with:
    - Python and JavaScript
    - Microservices architecture
    - Cloud platforms (AWS/GCP)
    - Leading development teams
    - CI/CD implementation
    - Agile methodologies
    
    Responsibilities:
    - Design and implement scalable software solutions
    - Lead a team of 3-5 engineers
    - Implement best practices for code quality and testing
    - Work with product managers to define technical requirements
    - Mentor junior engineers
    
    Requirements:
    - 5+ years of software development experience
    - Experience with Python and JavaScript
    - Knowledge of cloud platforms and infrastructure
    - Strong communication skills
    - Bachelor's degree in Computer Science or related field
    """
    
    # Generate resume
    generator = ResumeGenerator()
    resume = generator.generate_resume(
        user_profile=user_profile,
        company_name=company_name,
        job_role=job_role,
        job_description=job_description
    )
    
    # Print result
    if isinstance(resume, Resume):
        print(f"Generated resume for {resume.header.get('name', 'User')}")
        print(f"Summary: {resume.summary[:100]}...")
        print(f"Number of work experience sections: {len(resume.work_experience)}")
        print(f"Skills highlighted: {', '.join(resume.skills[:5])}...")
    else:
        print("Generated resume (raw format):")
        print(resume + "...")

if __name__ == "__main__":
    main()

