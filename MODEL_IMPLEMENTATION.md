📄 MODEL_INTEGRATION_GUIDE.md
The guide tells you exactly what to do when the models are ready — in order:

Step	Action
1	Add HF_API_TOKEN to 

.env
2	Replace 

model1_ocr.py
 with real TrOCR API call via InferenceClient
3	Replace 

model2_similarity.py
 with real Sentence Transformers cosine similarity
4	Re-wire 

submissions.py
 to call both models + store results
5	Test via Swagger at http://127.0.0.1:8000/docs