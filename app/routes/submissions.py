from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.db.supabase_client import supabase
from app.services.model1_ocr import run_ocr
import uuid, tempfile, os

router = APIRouter()
MAX_SIZE = 10 * 1024 * 1024


@router.post("/submit-answer")
def submit_answer(
    exam_id: str = Form(...), student_id: str = Form(...), file: UploadFile = File(...)
):
    if file.content_type != "application/pdf" or not file.filename.lower().endswith(
        ".pdf"
    ):
        raise HTTPException(status_code=400, detail="Only PDFs are allowed")

    content = file.file.read()  # read ONCE

    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="Upload a smaller file")

    submission_id = str(uuid.uuid4())
    file_path = f"{submission_id}_{file.filename}"

    # 1. Upload to Supabase Storage
    supabase.storage.from_("answer-sheets").upload(file_path, content)

    # 2. Save temp file to run OCR on
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # 3. Call Model 1 (OCR)
    extracted_text = run_ocr(tmp_path)
    os.unlink(tmp_path)  # cleanup

    # 4. Insert into DB with extracted_text
    supabase.table("submissions").insert(
        {
            "id": submission_id,
            "exam_id": exam_id,
            "student_id": student_id,
            "pdf_path": file_path,
            "extracted_text": extracted_text,
        }
    ).execute()

    return {
        "status": "processing",
        "submission_id": submission_id,
        "extracted_text": extracted_text,
    }
