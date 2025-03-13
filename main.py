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

from Schema.resume_Schema import Resume
from resumeGenerator import ResumeGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


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
        print(f"Generated resume for {resume.header.get('Name', 'User')}")
        print(f"Summary: {resume.summary[:100]}...")
        print(f"Number of work experience sections: {len(resume.work_experience)}")
        print(f"Skills highlighted: {', '.join(resume.skills[:5])}...")
        print(resume)
    else:
        print("Generated resume (raw format):")
        print(resume + "...")

if __name__ == "__main__":
    main()

