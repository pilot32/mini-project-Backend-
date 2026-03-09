from fastapi import APIRouter, UploadFile, File, Form
from app.db.supabase_client import supabase
import uuid

router = APIRouter()


@router.post("/submit-answer")
def submit_answer(
    exam_id: str = Form(...), student_id: str = Form(...), file: UploadFile = File(...)
):

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
