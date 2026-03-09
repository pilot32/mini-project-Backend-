# AI-Powered Academic Answer Evaluation System

---

## 📖 Overview

The AI-Powered Academic Answer Evaluation System is designed to revolutionize the way educational institutions handle examination grading. By leveraging cutting-edge artificial intelligence, this system eliminates the tedious manual process of evaluating handwritten answer sheets, providing teachers with objective metrics and consistency in grading.

### Key Benefits

- **Time Efficiency**: Drastically reduces the time spent on manual evaluation
- **Consistency**: Ensures uniform grading standards across all answer sheets
- **Objectivity**: Provides data-driven metrics to support grading decisions
- **Cost-Effective**: Utilizes free public AI models, making it accessible for institutions of all sizes
- **Scalable**: Built on managed API services that can handle varying workloads

---

## 🏗️ Architecture

The system follows a three-layer architecture designed for modularity and maintainability:

```
┌─────────────────────────────────────────────────────────────────┐
│                     Presentation Layer                          │
│                    (FastAPI Backend)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Model Layer                               │
│  ┌───────────────┐              ┌───────────────────────────┐  │
│  │   Model 1     │              │       Model 2             │  │
│  │   (OCR)       │──────────────│   (Answer Analysis)       │  │
│  │               │              │                           │  │
│  │ Handwritten   │              │ Similarity Scoring        │  │
│  │ → Digital     │              │ Keyword Extraction        │  │
│  │ Text          │              │ Answer Comparison         │  │
│  └───────────────┘              └───────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                                │
│                     (Supabase)                                  │
│         Results Storage | User Data | Answer Keys              │
└─────────────────────────────────────────────────────────────────┘
```

### Layer Breakdown

| Layer | Component | Function |
|-------|-----------|----------|
| **Model 1** | OCR Engine | Converts handwritten examination papers into digital English text |
| **Model 2** | Answer Analyzer | Compares extracted text against answer keys, generates similarity scores and keyword analysis |
| **Backend** | FastAPI | Orchestrates workflow, handles API requests, manages data flow |
| **Database** | Supabase | Stores evaluation results, user data, and answer keys |

---

## 🚀 Features

- **OCR Text Extraction**: Advanced optical character recognition for handwritten English text
- **Similarity Scoring**: Quantitative comparison between student answers and answer keys
- **Keyword Analysis**: Identifies and matches important keywords from model answers
- **Result Storage**: Persistent storage of all evaluation results for future reference
- **RESTful API**: Clean and intuitive API endpoints for easy integration

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend Framework** | FastAPI |
| **Database** | Supabase (PostgreSQL) |
| **OCR Model** | Public AI Model |
| **Analysis Model** | Public AI Model |
| **API Documentation** | OpenAPI/Swagger |

---

## 📋 Prerequisites

- Python 3.8+
- Supabase account and project
- Required API keys for AI models

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/pilot32/mini-project-Backend-.git
cd mini-project-Backend-
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OCR_MODEL_API=your_ocr_model_endpoint
ANALYSIS_MODEL_API=your_analysis_model_endpoint
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/evaluate` | Submit answer sheet for evaluation |
| `GET` | `/results/{id}` | Retrieve evaluation results |
| `POST` | `/answer-key` | Upload answer key for a question |
| `GET` | `/health` | Check API health status |

---

## 🔬 Evaluation Workflow

1. **Upload**: Teacher uploads handwritten answer sheet image
2. **OCR Processing**: Model 1 extracts text from the image
3. **Analysis**: Model 2 compares extracted text with answer key
4. **Scoring**: System generates similarity score and keyword match percentage
5. **Storage**: Results are stored in Supabase for future reference
6. **Output**: Teacher receives comprehensive evaluation report

---

## 📊 Sample Response

```json
{
  "evaluation_id": "eval_123456",
  "student_id": "STU001",
  "question_id": "Q01",
  "extracted_text": "Photosynthesis is the process by which plants...",
  "similarity_score": 0.85,
  "keyword_matches": {
    "matched": ["photosynthesis", "plants", "sunlight", "chlorophyll"],
    "missing": ["glucose", "oxygen"]
  },
  "overall_score": 78,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**pilot32**

- GitHub: [@pilot32](https://github.com/pilot32)

---

## 🙏 Acknowledgments

- Thanks to the open-source AI community for providing free public models
- Supabase for the excellent backend-as-a-service platform
- FastAPI for the high-performance Python web framework
