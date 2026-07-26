from fastapi import FastAPI
from app.models import Student, Book
from app.routers.health import router as health_router
from app.routers.resume import router as resume_router
app = FastAPI()


@app.get("/")
def home():
    return {"message":"Welcome"}


app.include_router(health_router)
app.include_router(resume_router)