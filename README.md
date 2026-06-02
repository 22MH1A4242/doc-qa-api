# 📄 Document Q&A API

A production-ready REST API that lets you upload any PDF and ask questions about it using semantic search and sentence embeddings.

Built with **FastAPI**, **FAISS**, **Sentence Transformers**, and **PyMuPDF** — deployed on **Railway**.

🔗 **Live API:** [doc-qa-api-production.up.railway.app](https://doc-qa-api-production.up.railway.app)  
📖 **Swagger UI:** [doc-qa-api-production.up.railway.app/docs](https://doc-qa-api-production.up.railway.app/docs)

---

## 🚀 Features

- 📤 Upload any PDF document via REST API
- 🔍 Semantic search using sentence embeddings
- ⚡ Fast similarity search with FAISS vector index
- 🧠 Context-aware answers extracted from document chunks
- 📦 Clean, lightweight FastAPI backend
- ☁️ Deployed and live on Railway (free tier)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | REST API framework |
| Sentence Transformers | Text embeddings (`all-MiniLM-L6-v2`) |
| FAISS | Vector similarity search |
| PyMuPDF | PDF text extraction |
| Uvicorn | ASGI server |
| Railway | Cloud deployment |

---

## 📡 API Endpoints

### `GET /`
Health check — confirms the API is running.

**Response:**
```json
{"message": "Document Q&A API is running!"}
```

---

### `POST /upload`
Upload a PDF file to extract and index its content.

**Request:** `multipart/form-data` with a PDF file

**Response:**
```json
{"message": "PDF processed. 42 chunks indexed."}
```

---

### `POST /ask`
Ask a natural language question about the uploaded PDF.

**Request body:**
```json
{"query": "What is the main topic of this document?"}
```

**Response:**
```json
{
  "query": "What is the main topic of this document?",
  "answer": "...relevant text extracted from the document..."
}
```

---

## 🧪 How to Test

### Option 1 — Swagger UI (Easiest)
Visit: [https://doc-qa-api-production.up.railway.app/docs](https://doc-qa-api-production.up.railway.app/docs)

### Option 2 — cURL
```bash
# Upload a PDF
curl -X POST "https://doc-qa-api-production.up.railway.app/upload" \
  -F "file=@your_document.pdf"

# Ask a question
curl -X POST "https://doc-qa-api-production.up.railway.app/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?"}'
```

### Option 3 — Python
```python
import requests

# Upload PDF
with open("document.pdf", "rb") as f:
    res = requests.post(
        "https://doc-qa-api-production.up.railway.app/upload",
        files={"file": f}
    )
print(res.json())

# Ask question
res = requests.post(
    "https://doc-qa-api-production.up.railway.app/ask",
    json={"query": "Summarize the document"}
)
print(res.json())
```

---

## 💻 Run Locally

```bash
# Clone the repo
git clone https://github.com/22MH1A4242/doc-qa-api.git
cd doc-qa-api

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

API will be available at: `http://localhost:8000/docs`

---

## 📁 Project Structure

```
doc-qa-api/
├── main.py            # FastAPI app & endpoints
├── rag_engine.py      # PDF extraction, embedding & search logic
├── requirements.txt   # Python dependencies
├── Procfile           # Railway start command
└── README.md
```

---

## 🔄 How It Works

```
PDF Upload → Text Extraction (PyMuPDF)
          → Chunking (300 words/chunk)
          → Embedding (Sentence Transformers)
          → FAISS Index Storage

Query     → Embed Query
          → FAISS Similarity Search
          → Return Top 3 Matching Chunks
```

---

## 👩‍💻 Author

**Anjali Devi Medapati**  
B.Tech CSE (AI & ML) — Aditya College of Engineering & Technology, JNTUK  
📧 medapatianjalidevi@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/anjalidevim) | [GitHub](https://github.com/22MH1A4242)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
