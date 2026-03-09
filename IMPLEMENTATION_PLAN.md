# 📋 AI EVALUATION SYSTEM - IMPLEMENTATION PLAN

## 🎯 PROJECT UNDERSTANDING (CORRECTED)

### Flow Overview:
```
Student Handwritten Answer Sheet (PDF/Image)
        ↓
    Model 1 (External/Hosted)
        • Extract text from handwriting
        • Convert to English text
        • Output: Plain English text
        ↓
Backend API (Minimal Processing)
        • Receive text from Model 1
        • Store extracted text in database
        • Pass to Model 2
        ↓
Model 2 (External/Hosted)
        • Receive extracted text from Model 1
        • Compare with answer key
        • Generate: Keywords, Similarity Scores
        ↓
Backend API (Store Results)
        • Receive Model 2 output
        • Store 3 things for each answer:
          1. Keywords extracted
          2. Similarity score with answer key
          3. (Missing concepts/keywords optional)
        ↓
Database (Supabase)
        • Student answers (extracted text)
        • Model 2 results (keywords + scores)
        • Teacher can review
```

---

## 🏗️ ARCHITECTURE (NO BACKEND PROCESSING)

### Layer 1: Models (External Hosted - Do ALL Processing)
```
MODEL 1 (OCR + Text Extraction):
├─ Input: PDF/Image of handwritten answer sheet
├─ Processing:
│  ├─ OCR (Handwriting → Text)
│  ├─ Text cleaning
│  └─ Language detection/correction
└─ Output: Plain English text

MODEL 2 (Text Analysis + Comparison):
├─ Input: 
│  ├─ Extracted text from Model 1
│  └─ Answer key (reference text)
├─ Processing:
│  ├─ Keyword extraction from student answer
│  ├─ Keyword extraction from answer key
│  ├─ Similarity comparison
│  └─ Calculate similarity score
└─ Output:
   ├─ Keywords found in student answer
   ├─ Similarity score (0-100%)
   └─ Missing keywords/concepts
```

### Layer 2: Backend (MINIMAL - Only Receive & Store)
```
FastAPI Backend:
├─ Endpoint 1: POST /upload-answer-sheet
│  ├─ Receive: PDF from student
│  ├─ Action: Send to Model 1
│  └─ Store: Raw PDF in Supabase Storage
│
├─ Endpoint 2: Receive Model 1 output
│  ├─ Receive: Extracted text
│  ├─ Action: Store in database + Pass to Model 2
│  └─ Store: Extracted text in Supabase
│
└─ Endpoint 3: Receive Model 2 output
   ├─ Receive: Keywords + Similarity Scores
   ├─ Action: Store in database
   └─ Store: Results in Supabase
```

### Layer 3: Database (Storage Only)
```
Supabase Tables:
├─ student_submissions
│  ├─ submission_id
│  ├─ student_id
│  ├─ pdf_file_path (Supabase Storage)
│  ├─ extracted_text (from Model 1)
│  └─ created_at
│
└─ evaluation_results
   ├─ submission_id (FK)
   ├─ question_id
   ├─ extracted_answer (from Model 1)
   ├─ keywords (from Model 2) - JSON array
   ├─ similarity_score (from Model 2) - float
   ├─ missing_keywords (from Model 2) - JSON array
   └─ created_at
```

---

## 🔄 COMPLETE DATA FLOW (STEP BY STEP)

### STEP 1: Student Uploads Handwritten Answer Sheet
```
Action: Teacher/Student uploads PDF
Input: PDF file (handwritten answers)
Backend: 
  ├─ Receive PDF
  ├─ Save to Supabase Storage
  └─ Extract file path
Output: File stored, ready for Model 1
```

### STEP 2: Model 1 Processes (OCR + Text Extraction)
```
Action: Backend calls Model 1 API
Input: PDF file path or file data
Model 1 (Hosted on HF/Replicate):
  ├─ Read PDF
  ├─ Apply OCR (handwriting → text)
  ├─ Clean text
  └─ Return English text
Output: Plain English text
  Example: "The operating system manages hardware resources 
            and provides services to applications"
```

### STEP 3: Backend Stores Model 1 Output
```
Action: Receive extracted text from Model 1
Store in: student_submissions.extracted_text
Next: Send to Model 2
```

### STEP 4: Model 2 Processes (Comparison + Analysis)
```
Action: Backend calls Model 2 API
Input: 
  ├─ Extracted text from Model 1
  └─ Answer key text (correct answers)
Model 2 (Hosted on HF/Replicate):
  ├─ Extract keywords from student answer
  ├─ Extract keywords from answer key
  ├─ Calculate similarity (cosine/semantic)
  ├─ Identify missing keywords
  └─ Return results
Output:
  ├─ keywords: ["operating", "system", "hardware"]
  ├─ similarity_score: 78.5
  └─ missing: ["resources", "services"]
```

### STEP 5: Backend Stores Model 2 Output
```
Action: Receive Model 2 results
Store in: evaluation_results table
  ├─ keywords (JSON array)
  ├─ similarity_score (float)
  └─ missing_keywords (JSON array)
Next: Results ready for teacher review
```

---

## 📦 REQUIRED MODELS (Free Hosting)

### Model 1: OCR + Text Extraction
**Options:**
1. **Tesseract OCR** (Free, locally deployed)
   - Best for: Accuracy with handwriting
   - Deployment: Self-hosted or Replicate

2. **TrOCR** (Microsoft, via HuggingFace)
   - Best for: Transformer-based, better accuracy
   - Deployment: HuggingFace Inference API (free)
   - Model: `microsoft/trocr-base-handwritten`

3. **Replicate** (Managed)
   - Run pre-built OCR models
   - Free tier: Very generous
   - Simple API: Just upload file, get text

**RECOMMENDATION:** TrOCR via HuggingFace (simplest)

### Model 2: Text Analysis + Similarity
**Options:**
1. **Sentence Transformers** (via HuggingFace)
   - Extract embeddings
   - Calculate cosine similarity
   - Keywords via TF-IDF or KeyBERT

2. **Custom Model** (Simple)
   - Keyword extraction: TF-IDF
   - Similarity: Cosine similarity between embeddings
   - Calculation: Simple string matching + embeddings

**RECOMMENDATION:** HuggingFace Sentence Transformers (free API)

---

## 💻 BACKEND CODE STRUCTURE (Minimal)

### API Endpoint 1: Upload Answer Sheet
```python
@app.post("/api/submit-answer")
async def submit_answer(exam_id: str, student_id: str, file: UploadFile):
    """
    Receive PDF → Save → Call Model 1
    """
    # 1. Save PDF to Supabase Storage
    pdf_path = upload_to_supabase(file)
    
    # 2. Create submission record
    submission_id = create_submission(exam_id, student_id, pdf_path)
    
    # 3. Call Model 1 (Async)
    call_model_1(pdf_path, submission_id)
    
    return {"status": "processing", "submission_id": submission_id}
```

### Async Job 1: Call Model 1
```python
async def call_model_1(pdf_path: str, submission_id: str):
    """
    Call external Model 1 → Get text → Store → Call Model 2
    """
    # 1. Call Model 1 API
    extracted_text = call_hf_api(
        model="microsoft/trocr-base-handwritten",
        input=pdf_path
    )
    
    # 2. Store extracted text
    update_submission(submission_id, extracted_text=extracted_text)
    
    # 3. Call Model 2
    call_model_2(extracted_text, submission_id)
```

### Async Job 2: Call Model 2
```python
async def call_model_2(extracted_text: str, submission_id: str):
    """
    Call external Model 2 → Get keywords + score → Store
    """
    # Get answer key for this exam
    answer_key = get_answer_key(submission_id)
    
    # Call Model 2 API
    results = call_model_2_api(
        student_answer=extracted_text,
        answer_key=answer_key.text
    )
    
    # Store results
    store_evaluation_results(
        submission_id=submission_id,
        keywords=results["keywords"],
        similarity_score=results["similarity"],
        missing=results["missing_keywords"]
    )
```

---

## 🗄️ DATABASE SCHEMA (Minimal)

### Table 1: Submissions
```sql
CREATE TABLE submissions (
  id UUID PRIMARY KEY,
  exam_id VARCHAR,
  student_id VARCHAR,
  question_id VARCHAR,
  pdf_path VARCHAR,           -- Supabase Storage path
  extracted_text TEXT,        -- From Model 1
  created_at TIMESTAMP
);
```

### Table 2: Evaluation Results
```sql
CREATE TABLE evaluation_results (
  id UUID PRIMARY KEY,
  submission_id UUID REFERENCES submissions(id),
  question_id VARCHAR,
  keywords JSON,              -- ["word1", "word2"]
  similarity_score FLOAT,     -- 78.5
  missing_keywords JSON,      -- ["word3", "word4"]
  created_at TIMESTAMP
);
```

### Table 3: Answer Keys
```sql
CREATE TABLE answer_keys (
  id UUID PRIMARY KEY,
  exam_id VARCHAR,
  question_id VARCHAR,
  answer_text TEXT,          -- Correct answer (plain text)
  created_at TIMESTAMP
);
```

---

## 🚀 IMPLEMENTATION TIMELINE

### Week 1: Setup
- [ ] Create Supabase project
- [ ] Create 3 tables (submissions, evaluation_results, answer_keys)
- [ ] Setup FastAPI project
- [ ] Create upload endpoint

### Week 2: Model 1 Integration
- [ ] Get HuggingFace API key
- [ ] Create call_model_1() function
- [ ] Test with sample PDF
- [ ] Store extracted text

### Week 3: Model 2 Integration
- [ ] Create call_model_2() function
- [ ] Implement keyword extraction
- [ ] Implement similarity scoring
- [ ] Test with sample data

### Week 4: Testing & Deployment
- [ ] Test end-to-end flow
- [ ] Add error handling
- [ ] Deploy to production (Railway/Render)
- [ ] Test with real data

---

## 📊 API ENDPOINTS (Total: 3)

### Endpoint 1: Upload Answer Sheet
```
POST /api/submit-answer
Content-Type: multipart/form-data

Input:
  - exam_id: string
  - student_id: string
  - file: PDF file

Output:
  {
    "status": "processing",
    "submission_id": "uuid"
  }
```

### Endpoint 2: Get Results
```
GET /api/results/{submission_id}

Output:
  {
    "submission_id": "uuid",
    "extracted_text": "...",
    "results": [
      {
        "question_id": "Q1",
        "keywords": ["word1", "word2"],
        "similarity_score": 78.5,
        "missing_keywords": ["word3"]
      }
    ]
  }
```

### Endpoint 3: Get Answer Keys (Optional)
```
POST /api/answer-keys/upload
Content-Type: multipart/form-data

Input:
  - exam_id: string
  - file: PDF with correct answers

Action:
  - Extract text (manual or Model 1)
  - Store in answer_keys table
```

---

## 🔑 KEY POINTS

1. **Model 1 = OCR Only**
   - Input: PDF of handwritten answers
   - Output: Plain English text
   - No comparison, no scoring
   - Hosted externally (HuggingFace/Replicate)

2. **Model 2 = Comparison Only**
   - Input: Extracted text + Answer key
   - Output: Keywords + Similarity score
   - Hosted externally (HuggingFace/Replicate)

3. **Backend = Storage Only**
   - No text processing
   - No NLP processing
   - Just receive from models and store
   - All async/background jobs

4. **Database = Simple**
   - 3 tables
   - Store extracted text
   - Store keywords
   - Store similarity scores

5. **No Processing on Backend**
   - ✅ Receive PDF → Store
   - ✅ Receive text → Store
   - ✅ Receive keywords → Store
   - ❌ No OCR
   - ❌ No text cleaning
   - ❌ No NLP
   - ❌ No embeddings

---

## 🎯 ADVANTAGES OF THIS APPROACH

1. **Simple Backend** - Just storage and API calls
2. **Scalable** - Offload processing to managed services
3. **Cost Effective** - Free model APIs (HuggingFace, Replicate)
4. **Fast** - No processing overhead on backend
5. **Reliable** - Professional OCR/ML models
6. **Easy to Debug** - Each step is independent

---

## 🔗 MODEL HOSTING

### Model 1: TrOCR (HuggingFace)
- **URL:** `https://api-inference.huggingface.co/models/microsoft/trocr-base-handwritten`
- **Cost:** Free (5000 calls/month)
- **Setup:** Get API key from huggingface.co

### Model 2: Sentence Transformers (HuggingFace)
- **URL:** `https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2`
- **Cost:** Free (5000 calls/month)
- **Setup:** Get API key from huggingface.co

### Alternative: Replicate
- Can use instead of HuggingFace
- More generous free tier
- Better for heavy processing

---

## 📝 NEXT STEP

Follow this implementation order:
1. Create Supabase database (3 tables)
2. Create FastAPI project
3. Build upload endpoint
4. Test Model 1 (OCR)
5. Build storage for Model 1 output
6. Test Model 2 (Comparison)
7. Build storage for Model 2 output
8. Test end-to-end
9. Deploy

**NO MORE DOCUMENTATION NEEDED. JUST FOLLOW THIS PLAN.**

