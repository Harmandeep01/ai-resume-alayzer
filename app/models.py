from pydantic import BaseModel


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