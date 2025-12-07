"""
Database models for conversation history using Neon Serverless Postgres.
Defines the schema for storing chat interactions in the RAG system.
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv(
    "NEON_DATABASE_URL",
    "postgresql://user:password@localhost:5432/physical_ai_education"
)

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    """
    User model for tracking users in the educational platform
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to conversations
    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    """
    Conversation model for tracking chat sessions
    """
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    module = Column(String, default="vla-integration")  # Which educational module

    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    user = relationship("User", back_populates="conversations")

class Message(Base):
    """
    Message model for storing individual chat messages
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)  # "user", "assistant", "system"
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)  # Additional metadata about the message

    # Relationship back to conversation
    conversation = relationship("Conversation", back_populates="messages")

# Create all tables
def create_tables():
    """
    Create all database tables
    """
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example usage function
def init_database():
    """
    Initialize the database with required tables
    """
    create_tables()
    print("Database tables created successfully")