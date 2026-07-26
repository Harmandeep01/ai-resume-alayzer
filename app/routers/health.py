from fastapi import APIRouter
from app.models import Student, Book
router = APIRouter(prefix="/health")

@router.get("")
def health():

    return {
        "status": "Health OK"
    }

@router.get("/name")
def name():
    return {"name":"Harmann"}


@router.get("/college")
def college():
    return {"college":"SMDRSD College"}


@router.get("/skills")
def skills():
    return {
        "skills":[
            "Python",
            "FastAPI",
            "AI"
        ]
    }

@router.get("/hello")
def hello():

    return {"name":"Harmann"}

    return {"age":25}


@router.get("/projects")
def projects():

    return {

        "projects":[
            "Resume Analyzer",
            "F1 GPT",
            "Weather App"
        ]

    }


@router.post("/student")
def create_student(student:Student):

    return student


@router.post("/book", response_model=Book)
def books(book: Book):
    return book