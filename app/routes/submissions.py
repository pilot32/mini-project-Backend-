from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.db.supabase_client import supabase
import uuid

router = APIRouter()

MAX_SIZE = 10 * 1024 * 1024


@router.post("/submit-answer")
def submit_answer(
    exam_id: str = Form(...), student_id: str = Form(...), file: UploadFile = File(...)
):
    # validatng the file type

    if file.content_type != "application/pdf" or not file.filename.lower().endswith(
        ".pdf"
    ):
        raise HTTPException(status_code=400, details="Only PDFs are allowed")
    content = file.file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status=400, detial="upload lower size file")
    submission_id = str(uuid.uuid4())

    file_path = f"{submission_id}_{file.filename}"

    # Read the file synchronously
    content = file.file.read()

    # upload to supabase storage
    supabase.storage.from_("answer-sheets").upload(file_path, content)

    # insert into database
    supabase.table("submissions").insert(
        {
            "id": submission_id,
            "exam_id": exam_id,
            "student_id": student_id,
            "pdf_path": file_path,
        }
    ).execute()

    return {"message": "upload successful", "submission_id": submission_id}
