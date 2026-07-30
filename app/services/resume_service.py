import re
from google.genai import types

from app.models import ResumeData
from app.core.llm import client

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


def extract_resume_with_ai(text: str)->ResumeData:
    prompt = f"""
        Extract structured information from the resume below.

        Rules:
        - Extract only information explicitly present in the resume.
        - Do not invent missing information.
        - If a scalar field is unavailable, return null.
        - If a list field has no information, return an empty list.

        RESUME:
        {text}
        """
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=ResumeData
        ),
    )

    return ResumeData.model_validate_json(
        response.text
    )

# def extract_resume_skills(text: str) -> list[str]:
#     text_lower = text.lower()

#     found_skills = []

#     for skill in SKILLS:

#         if skill.lower() in text_lower:
#             found_skills.append(skill)

#     return sorted(found_skills)