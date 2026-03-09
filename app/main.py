from fastapi import FastAPI
from app.routes.submissions import router as submission_router

app = FastAPI()

app.include_router(submission_router, prefix="/api")
