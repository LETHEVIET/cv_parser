from pydantic import BaseModel
from typing import List, Optional

class ContactInformation(BaseModel):
    name: str
    phone_number: str
    email: str
    linkedin_profile: Optional[str] = None

class WorkExperience(BaseModel):
    company_name: str
    job_title: str
    dates_of_employment: str
    responsibilities: str
    achievements: Optional[str] = None

class Education(BaseModel):
    institution_name: str
    degree: str
    dates_of_attendance: str
    relevant_coursework: Optional[str] = None

class Skills(BaseModel):
    technical_skills: List[str]
    soft_skills: List[str]

class Project(BaseModel):
    project_name: str
    description: str
    technologies_used: List[str]
    outcome: Optional[str] = None

class DeveloperResume(BaseModel):
    contact_information: ContactInformation
    resume_summary: Optional[str] = None
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: Skills
    certifications: Optional[List[str]] = None
    projects: Optional[List[Project]] = None
    languages_and_technologies: Optional[List[str]] = None
    extracurricular_activities: Optional[List[str]] = None
    interests: Optional[List[str]] = None

