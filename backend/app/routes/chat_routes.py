"""
chat_routes.py
---------------
One endpoint: POST /chat/ask
Takes a document_id + a question, runs the RAG pipeline, returns an
answer with the source pages it came from.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User, Document
from app.schemas import ChatRequest, ChatResponse
from app.services.rag_service import answer_question

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
def ask(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document = (
        db.query(Document)
        .filter(Document.id == request.document_id, Document.owner_id == current_user.id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.status != "ready":
        raise HTTPException(status_code=400, detail=f"Document is still {document.status}, try again shortly")

    result = answer_question(db, request.document_id, request.question)
    return result
