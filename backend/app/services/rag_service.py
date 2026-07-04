"""
rag_service.py
---------------
RAG = Retrieval-Augmented Generation. Instead of asking the AI a
question "cold", we:

1. RETRIEVE the most relevant chunks of the document (using vector
   similarity search in pgvector).
2. AUGMENT the AI's prompt by stuffing those chunks in as context.
3. GENERATE an answer using a local LLM (Ollama running Llama 3).

This keeps the AI's answers grounded in the actual document instead of
letting it make things up from general knowledge.
"""

import requests
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Chunk
from app.services.embedding_service import embed_text


def retrieve_relevant_chunks(db: Session, document_id: int, question: str, top_k: int = 5) -> list[Chunk]:
    """
    Finds the chunks (from one specific document) whose embeddings are
    closest in meaning to the user's question.

    pgvector gives us the "<->" operator, which measures distance
    between two vectors. Smaller distance = more similar meaning.
    """
    question_vector = embed_text(question)

    results = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.embedding.l2_distance(question_vector))
        .limit(top_k)
        .all()
    )
    return results


def build_prompt(question: str, chunks: list[Chunk]) -> str:
    context = "\n\n".join(
        f"[Page {c.page_number}]\n{c.content}" for c in chunks
    )

    return f"""You are a financial research assistant. Answer the question
using ONLY the context below. If the answer isn't in the context, say so
honestly instead of guessing.

Context:
{context}

Question: {question}

Answer:"""


def ask_ollama(prompt: str) -> str:
    """
    Sends the prompt to your locally running Ollama server and returns
    the model's text response.
    """
    response = requests.post(
        f"{settings.ollama_base_url}/api/generate",
        json={
            "model": settings.ollama_model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"].strip()


def answer_question(db: Session, document_id: int, question: str) -> dict:
    chunks = retrieve_relevant_chunks(db, document_id, question)

    if not chunks:
        return {
            "answer": "I couldn't find any relevant content in this document yet. "
                      "Make sure it finished processing.",
            "sources": [],
        }

    prompt = build_prompt(question, chunks)
    answer = ask_ollama(prompt)
    sources = [f"Page {c.page_number}" for c in chunks]

    return {"answer": answer, "sources": sources}
