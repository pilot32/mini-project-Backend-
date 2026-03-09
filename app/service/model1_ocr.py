import os
import requests

# from dotenv import load_dotenv

# load_dotenv()

# HF_API_KEY=os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/microsoft/trocr-base-handwritten"

header = {"Authorization": f"Bearer {HF_API_KEY}"}
response = requests.get(API_URL, headers=headers)

print(response.status_code)
