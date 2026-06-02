import fitz  # PyMuPDF
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from groq import Groq

model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def extract_chunks(pdf_path, chunk_size=300, overlap=50):
    """Extract text from PDF and split into overlapping chunks."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    if not text.strip():
        raise ValueError("No text could be extracted from this PDF.")

    words = text.split()
    step = chunk_size - overlap
    chunks = [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), step)
        if words[i:i + chunk_size]  # skip empty trailing chunk
    ]
    return chunks


def build_index(chunks):
    """Encode chunks and build a FAISS L2 index."""
    embeddings = model.encode(chunks, show_progress_bar=False)
    embeddings = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings


def search(query, chunks, index, top_k=3):
    """Find top_k most relevant chunks for a query."""
    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")
    _, indices = index.search(query_vec, top_k)
    results = [chunks[i] for i in indices[0] if i < len(chunks)]
    return results


def generate_answer(query, context_chunks):
    """Use Groq LLM to synthesize a proper answer from retrieved chunks."""
    context = "\n\n".join(context_chunks)
    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. Answer the user's question "
                        "based only on the provided document context. "
                        "If the answer is not in the context, say so clearly."
                    )
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}"
                }
            ],
            max_tokens=512,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback: return raw chunks if LLM call fails
        return f"[LLM unavailable] Top matching context:\n\n" + "\n\n---\n\n".join(context_chunks)