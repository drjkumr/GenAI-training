import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
from rag_service import rag_service, TEMP_PDF_DIR

app = FastAPI(title="Clinical Trial Protocol API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/api/upload")
async def upload_protocol(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = os.path.join(TEMP_PDF_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        chunks_created = rag_service.ingest_pdf(file_path, file.filename)
        return {"message": "Protocol uploaded and processed successfully", "chunks": chunks_created}
    except ValueError as ve:
        raise HTTPException(status_code=401, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: QueryRequest):
    try:
        if not request.question:
            raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
        result = rag_service.answer_question(request.question)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=401, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ensure static directory exists
os.makedirs("static", exist_ok=True)

# Serve static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
