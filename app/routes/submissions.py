from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.db.supabase_client import supabase
from app.services.model1_ocr import run_ocr
from app.services.model2_similarity import run_similarity
import uuid, tempfile, os, traceback

router = APIRouter()
MAX_SIZE = 10 * 1024 * 1024


@router.post("/submit-answer")
def submit_answer(
    exam_id: str = Form(...),
    student_id: str = Form(...),
    question_id: str = Form(...),
    file: UploadFile = File(...),
):
    try:
        # Validate file type
        if file.content_type != "application/pdf" or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDFs are allowed")

        content = file.file.read()  # read ONCE

        if len(content) > MAX_SIZE:
            raise HTTPException(status_code=400, detail="Upload a smaller file")

        submission_id = str(uuid.uuid4())
        file_path = f"{submission_id}_{file.filename}"

        # 1. Upload PDF to Supabase Storage
        print(f"[STEP 1] Uploading PDF to storage: {file_path}")
        supabase.storage.from_("answer-sheets").upload(file_path, content)
        print("[STEP 1] ✅ Upload done")

        # 2. Save temp file to run OCR on
        print("[STEP 2] Running OCR...")
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        # 3. Call Model 1 (OCR) → get extracted text
        extracted_text = run_ocr(tmp_path)
        os.unlink(tmp_path)
        print(f"[STEP 2] ✅ OCR done: {extracted_text[:80]}...")

        # 4. Store submission with extracted text
        print("[STEP 3] Inserting into submissions table...")
        supabase.table("submissions").insert({
            "id": submission_id,
            "exam_id": exam_id,
            "student_id": student_id,
            "pdf_path": file_path,
            "extracted_text": extracted_text,
        }).execute()
        print("[STEP 3] ✅ Submission stored")

        # 5. Fetch answer key for this exam + question
        print(f"[STEP 4] Fetching answer key for exam={exam_id}, question={question_id}...")
        answer_key_resp = (
            supabase.table("answer_keys")
            .select("answer_text")
            .eq("exam_id", exam_id)
            .eq("question_id", question_id)
            .limit(1)
            .execute()
        )

        if not answer_key_resp.data:
            raise HTTPException(
                status_code=404,
                detail=f"No answer key found for exam_id='{exam_id}', question_id='{question_id}'. Please insert one first."
            )

        answer_key_text = answer_key_resp.data[0]["answer_text"]
        print(f"[STEP 4] ✅ Answer key found: {answer_key_text[:80]}...")

        # 6. Call Model 2 (Similarity + Keywords)
        print("[STEP 5] Running similarity model...")
        results = run_similarity(extracted_text, answer_key_text)
        print(f"[STEP 5] ✅ Score: {results['similarity_score']}%")

        # 7. Store evaluation results
        print("[STEP 6] Storing evaluation results...")
        eval_id = str(uuid.uuid4())
        supabase.table("evaluation_results").insert({
            "id": eval_id,
            "submission_id": submission_id,
            "question_id": question_id,
            "keywords": results["keywords"],
            "similarity_score": results["similarity_score"],
            "missing_keywords": results["missing_keywords"],
        }).execute()
        print("[STEP 6] ✅ Evaluation stored")

        return {
            "status": "completed",
            "submission_id": submission_id,
            "extracted_text": extracted_text,
            "evaluation": results,
        }

    except HTTPException:
        raise  # re-raise 400/404 as-is
    except Exception as e:
        traceback.print_exc()  # prints full traceback to terminal
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/{submission_id}")
def get_results(submission_id: str):
    submission = (
        supabase.table("submissions")
        .select("*")
        .eq("id", submission_id)
        .single()
        .execute()
    )

    if not submission.data:
        raise HTTPException(status_code=404, detail="Submission not found")

    evaluation = (
        supabase.table("evaluation_results")
        .select("*")
        .eq("submission_id", submission_id)
        .execute()
    )

    return {
        "submission_id": submission_id,
        "extracted_text": submission.data["extracted_text"],
        "results": evaluation.data,
    }
