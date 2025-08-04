# models/call.py

from sqlalchemy import Column, String, Integer, Text, DateTime
from storage.db import Base
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from datetime import datetime

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(String, unique=True, index=True)
    filename = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    participants = relationship("CallParticipant", back_populates="call", cascade="all, delete-orphan")

    # LLM outputs
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)
    next_steps = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Call(call_id={self.call_id}, filename={self.filename}, created_at={self.created_at})>"
