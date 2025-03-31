import os
import tempfile
import uuid
from pathlib import Path
from typing import List, Optional


import httpx
from google import genai

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from parser import parse_pdf, parse_image
from docx_utils import convert_docx_to_pdf

# Initialize FastAPI app
app = FastAPI(
    title="CV Parser API",
    description="API for parsing CVs from various document formats",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Allowed file types
ALLOWED_EXTENSIONS = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg", 
    "png": "image/png"
}

@app.get("/")
async def root():
    """Serve the web UI for CV parsing"""
    return FileResponse(str(static_dir / "index.html"))

app.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a document for parsing (PDF, DOCX, or image)
    """
    # Check file extension and content type
    file_ext = file.filename.split(".")[-1].lower() if file.filename else ""
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Supported types: {', '.join(ALLOWED_EXTENSIONS.keys())}"
        )
    
    # Create temp file to save the uploaded content
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp_file:
        temp_file_path = temp_file.name
        contents = await file.read()
        temp_file.write(contents)
    
    try:
        if file_ext == "pdf":
            result = parse_pdf(temp_file_path, app.client)
            return result
        elif file_ext == "docx":
            pdf_path = convert_docx_to_pdf(temp_file_path)
            result = parse_pdf(pdf_path, app.client)
            return result
        elif file_ext in ["jpg", "jpeg", "png"]:
            result = parse_image(temp_file_path, app.client)
            return result
        else:
            # Basic placeholder for other file types
            return {
                "message": f"{file_ext.upper()} parsing not fully implemented yet",
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(contents)
            }
    finally:
        # Clean up the temp file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        
        if os.path.exists(temp_file_path.replace('.docx', '.pdf')):
            os.unlink(temp_file_path.replace('.docx', '.pdf'))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=7860, reload=True)
