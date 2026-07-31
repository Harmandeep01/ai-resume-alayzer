from google.genai import types

from app.core.llm import client
from app.models import AnalysisResult


def analyze_resume_with_jd(
    resume_text: str,
    job_description: str
) -> AnalysisResult:

   prompt = f"""
   You are a resume-to-job matching system.

   Analyze the candidate's resume against the provided job description.

   RESUME:
   {resume_text}

   JOB DESCRIPTION:
   {job_description}

   MATCHING RULES:

   1. Identify REQUIRED and PREFERRED skills separately from the job description.

   2. For every job skill, search the ENTIRE resume for evidence, including:
      - skills section
      - project technology stacks
      - project descriptions
      - professional experience
      - education where relevant

   3. Match skills semantically, not only by exact string equality.

   Examples:
   - "Retrieval-Augmented Generation" matches "RAG" or "RAG Pipelines"
   - "Large Language Models" matches "LLM" or "LLM APIs"
   - "Vector Databases" can match ChromaDB, Pinecone, Weaviate, or Qdrant
   - "Embeddings" can match Sentence Transformers
   - "AWS" can match explicit AWS services such as AWS Bedrock, S3,
   Lambda, EC2, ECS, or other AWS technologies

   4. A skill is matched only when the resume contains direct or clearly
      equivalent evidence.

   5. A skill is missing only when no supporting evidence exists anywhere
      in the resume.

   6. Do NOT infer unrelated skills.

   Examples:
   - FastAPI does NOT imply Docker
   - Git does NOT imply CI/CD
   - Kubernetes does NOT imply AWS
   - Python does NOT imply machine learning

   7. Required skills MUST be placed only in:
      - matched_required_skills
      - missing_required_skills

   8. Preferred skills MUST be placed only in:
      - matched_preferred_skills
      - missing_preferred_skills

   9. Before marking a skill as missing, verify that no direct,
      synonymous, parent/child technology, or concrete-tool evidence
      exists anywhere in the resume.

   10. Evaluate the candidate's experience match from 0 to 100.
      Base this only on relevant professional/project experience
      compared with the job requirements.

   11. Evaluate education match from 0 to 100.
      100 means the candidate fully satisfies the stated education requirement.

   12. Evaluate overall role relevance from 0 to 100.
      Consider how strongly the candidate's projects, technical background,
      and demonstrated work align with this specific role.

   13. Strengths and weaknesses must specifically relate to this job.

   14. Recommendations must address genuine gaps.
      Never recommend adding a skill already evidenced in the resume.

   15. Never invent skills, experience, education, deployments,
      or achievements.
   """
   response = client.models.generate_content(
      model="gemini-3.1-flash-lite",
      contents=prompt,
      config=types.GenerateContentConfig(
         response_mime_type="application/json",
         response_schema=AnalysisResult
      ),
   )

   return AnalysisResult.model_validate_json(response.text)