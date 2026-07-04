"""
document_routes.py
--------------------
Handles uploading a PDF, processing it into chunks + embeddings, and
listing the documents a user has uploaded.
"""

import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import settings
from app.database import get_db
from app.models import User, Document, Chunk
from app.schemas import DocumentOut
from app.services.pdf_service import process_pdf_into_chunks
from app.services.embedding_service import embed_texts

router = APIRouter(prefix="/documents", tags=["documents"])


def process_document_background(document_id: int, filepath: str):
    """
    Runs AFTER the upload response has already been sent back to the
    user, so they aren't stuck waiting for embeddings to finish before
    seeing "upload successful".

    Note: this opens its own database session because background tasks
    run outside the normal request lifecycle.
    """
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        raw_chunks = process_pdf_into_chunks(filepath)

        if not raw_chunks:
            document.status = "failed"
            db.commit()
            return

        texts = [c["content"] for c in raw_chunks]
        vectors = embed_texts(texts)

        for chunk_data, vector in zip(raw_chunks, vectors):
            db.add(Chunk(
                content=chunk_data["content"],
                page_number=chunk_data["page"],
                embedding=vector,
                document_id=document.id,
            ))

        document.status = "ready"
        db.commit()
    except Exception:
        document.status = "failed"
        db.commit()
        raise
    finally:
        db.close()


@router.post("/upload", response_model=DocumentOut)
def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    os.makedirs(settings.upload_dir, exist_ok=True)
    filepath = os.path.join(settings.upload_dir, f"{current_user.id}_{file.filename}")

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = Document(
        filename=file.filename,
        filepath=filepath,
        status="processing",
        owner_id=current_user.id,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    background_tasks.add_task(process_document_background, document.id, filepath)

    return document


@router.get("/", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Document).filter(Document.owner_id == current_user.id).all()


@router.get("/{document_id}", response_model=DocumentOut)
def get_document(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document = (
        db.query(Document)
        .filter(Document.id == document_id, Document.owner_id == current_user.id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
