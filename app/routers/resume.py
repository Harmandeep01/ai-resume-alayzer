from fastapi import APIRouter, UploadFile, File, HTTPException, Form

from app.services.parser import extract_text_from_pdf
from app.services.resume_service import extract_resume_information
from app.services.jd_service import extract_job_information
from app.services.ats import calculate_ats_score
from app.services.analyzer_service import analyze_resume_with_jd
from app.models import Resume

router = APIRouter()

PDF_CONTENT_TYPE = "application/pdf"

@router.post("/upload-resume", response_model=Resume)
def resume_upload(file: UploadFile = File(...)):
    try:
        if file.content_type != PDF_CONTENT_TYPE:
            raise HTTPException(
                status_code=415,
                detail="Only PDF files are allowed."
            )
        extracted_text = extract_text_from_pdf(file.file)
        # print(extracted_text)
        resume = extract_resume_information(extracted_text)

        return resume
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/analyze")
def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        if file.content_type != PDF_CONTENT_TYPE:
            raise HTTPException(
                status_code=415,
                detail="Only PDF files are allowed."
            )
        resume_text = extract_text_from_pdf(file.file)
        print(resume_text)
        analysis = analyze_resume_with_jd(
        resume_text=resume_text,
        job_description=job_description
    )

        score = calculate_ats_score(analysis)
        return {
        "score": score,
        "analysis": analysis
    }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )