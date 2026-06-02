import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_chunks(pdf_path, chunk_size=300):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    words = text.split()
    chunks = [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size)
    ]
    return chunks

def build_index(chunks):
    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings

def search(query, chunks, index, top_k=3):
    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")
    _, indices = index.search(query_vec, top_k)
    results = [chunks[i] for i in indices[0]]
    return " ".join(results)