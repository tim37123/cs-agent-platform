from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from storage.db import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    title = Column(String)
    phone = Column(String)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)

    account = relationship("Account", back_populates="contacts")
    calls = relationship("CallParticipant", back_populates="contact")
