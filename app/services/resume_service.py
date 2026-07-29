import re
import spacy

from app.models import ResumeData
from app.data.skills import SKILLS
from app.services.ai_service import extract_resume_with_ai

nlp = spacy.load('en_core_web_sm')

TECH_WORDS = {
    "RAG",
    "LLM",
    "MCP",
    "LangChain",
    "LangGraph",
    "LlamaIndex",
    "FastAPI",
    "Python",
    "Java",
    "JavaScript",
    "React",
    "Node",
    "NodeJS",
    "Express",
    "Docker",
    "Kubernetes",
    "TensorFlow",
    "PyTorch",
    "AWS",
    "Azure",
    "GCP",
    "Gemini",
    "ChromaDB",
    "Redis",
    "MongoDB",
    "PostgreSQL",
    "Git",
    "REST",
    "API",
}

BAD_WORDS = {
    "Resume",
    "Curriculum",
    "Vitae",
    "CV",
    "Engineer",
    "Developer",
    "Intern",
    "Manager",
    "Portfolio",
    "Github",
    "GitHub",
    "LinkedIn",
    "India",
}

def extract_email(text):

    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}", text)
    if email:
        # print(email)
        # print(email.group())
        # print(email.start())
        # print(email.end())
        # print(type(email))
        return email.group()
    return None

def extract_phone_number(text):
    ph_number = re.search(r"(?<!\w)\+?\d{10,15}(?!\w)", text)
    if ph_number:
        return ph_number.group()
    return None


def extract_resume_information(text: str) -> ResumeData:
    ai_resume = extract_resume_with_ai(text)
    email = extract_email(text)
    phone = extract_phone_number(text)

    print(f"Deterministic Email: {email}")
    print(f"Deterministic Phone: {phone}")

    return ResumeData(
    name=ai_resume.name,
    email=email or ai_resume.email,
    phone=phone or ai_resume.phone,
    skills=ai_resume.skills,
    education=ai_resume.education,
    experience=ai_resume.experience,
    projects=ai_resume.projects,
)

def extract_resume_skills(text: str) -> list[str]:
    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return sorted(found_skills)