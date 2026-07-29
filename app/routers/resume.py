from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.parser import extract_text_from_pdf
from app.services.resume_service import extract_resume_information

router = APIRouter()

PDF_CONTENT_TYPE = "application/pdf"

@router.post("/upload-resume")
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