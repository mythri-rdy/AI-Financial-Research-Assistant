from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database import Base

EMBEDDING_DIMENSIONS = 384 #all-MiniLM-L6-v2" model

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    documents = relationship("Document", back_populates="owner")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="processing")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete")

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    embedding = Column(Vector(EMBEDDING_DIMENSIONS))
    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document", back_populates="chunks")
