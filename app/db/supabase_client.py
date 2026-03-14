import os
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

# Explicitly load from app/.env — __file__ is app/db/supabase_client.py → parent = app/db → parent = app/
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase=create_client(url,key)