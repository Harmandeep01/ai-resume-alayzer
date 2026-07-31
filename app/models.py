from pydantic import BaseModel, Field


class Student(BaseModel):

    name:str
    age:int
    college:str


class Book(BaseModel):
    name: str
    author: str
    price: int


class ResumeData(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    skills: list[str] = []
    education: list[str] = []
    experience: list[str] = []
    projects: list[str] = []


class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)


class JobDescription(BaseModel):
    job_title: str | None = None

    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)

    minimum_experience_years: float | None = None

    education: str | None = None

class SkillMatch(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]


class AnalysisResult(BaseModel):
    job_title: str | None = None

    matched_required_skills: list[str]
    missing_required_skills: list[str]

    matched_preferred_skills: list[str]
    missing_preferred_skills: list[str]

    required_experience_years: float
    candidate_experience_years: float

    education_match: bool

    relevant_projects: int
    total_projects: int

    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]

    experience_match: str
    education_match_reason: str