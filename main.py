from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from rag_engine import extract_chunks, build_index, search
import shutil, os

app = FastAPI()

store = {}  # holds chunks + index per session

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    chunks = extract_chunks(path)
    index, _ = build_index(chunks)
    store["chunks"] = chunks
    store["index"] = index
    os.remove(path)
    return {"message": f"PDF processed. {len(chunks)} chunks indexed."}

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(q: Question):
    if "chunks" not in store:
        return {"error": "Upload a PDF first"}
    answer = search(q.query, store["chunks"], store["index"])
    return {"query": q.query, "answer": answer}

@app.get("/")
def home():
    return {"message": "Document Q&A API is running!"}