from fastapi import FastAPI, UploadFile, File
from typing import Dict, Any
import os
from algo import score_resume, recommend_skills_and_courses
from temp import parse_resume
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List allowed origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

TEMP_DIR = "temp/"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/process-resume/")
async def process_resume(file: UploadFile = File(...)):
   
    if file.content_type != 'application/pdf':
        return {"error": "Invalid file type. Only PDFs are allowed."}
    
    
    file_path = os.path.join(TEMP_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    parsed_resume = parse_resume(file_path)

    resume_score = score_resume(parsed_resume)

    recommendations = recommend_skills_and_courses(parsed_resume)
    
    return {
        "Resume Score": resume_score,
        "Recommendations": recommendations
    }

