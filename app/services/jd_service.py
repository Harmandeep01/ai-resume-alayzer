from google.genai import types

from app.core.llm import client
from app.models import JobDescription

def extract_job_information(job_description: str) -> JobDescription:
        prompt = f"""
        Extract structured information from the job description below.

        Rules:
        - Extract only information explicitly present in the job description.
        - Do not invent missing information.
        - dont make assumptions
        -use the schema to return the response appropriately

        RESUME:
        {job_description}
        """

        response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                    response_schema=JobDescription
                ),
            )

        return JobDescription.model_validate_json(
                response.text
        )