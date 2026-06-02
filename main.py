import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from rag_engine import extract_chunks, build_index, search, generate_answer

app = FastAPI(
    title="Document Q&A API",
    description="Upload any PDF and ask questions using semantic search + LLM.",
    version="2.0.0"
)

# Session-based store: session_id → {chunks, index}
# In production, replace with Redis or a database
store: dict = {}


# ─── Models ────────────────────────────────────────────────────────────────────

class Question(BaseModel):
    session_id: str
    query: str


# ─── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Document Q&A API is running!", "version": "2.0.0"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "active_sessions": len(store),
        "model": "all-MiniLM-L6-v2",
        "llm": "llama3-8b-8192 (Groq)"
    }


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF. Returns a session_id to use in /ask."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    session_id = str(uuid.uuid4())
    temp_path = f"temp_{session_id}.pdf"

    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        chunks = extract_chunks(temp_path)
        index, _ = build_index(chunks)

        store[session_id] = {"chunks": chunks, "index": index}

        return {
            "session_id": session_id,
            "message": f"PDF processed successfully.",
            "chunks_indexed": len(chunks),
            "usage": f"Use session_id '{session_id}' in POST /ask"
        }

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/ask")
def ask_question(q: Question):
    """Ask a question about your uploaded PDF using session_id."""
    session = store.get(q.session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found. Please upload a PDF first to get a session_id."
        )

    if not q.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    top_chunks = search(q.query, session["chunks"], session["index"], top_k=3)
    answer = generate_answer(q.query, top_chunks)

    return {
        "session_id": q.session_id,
        "query": q.query,
        "answer": answer,
        "source_chunks_used": len(top_chunks)
    }


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    """Clear a session and free memory."""
    if session_id not in store:
        raise HTTPException(status_code=404, detail="Session not found.")
    del store[session_id]
    return {"message": f"Session {session_id} deleted successfully."}