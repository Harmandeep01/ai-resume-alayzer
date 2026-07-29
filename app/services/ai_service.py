import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models import ResumeData

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
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