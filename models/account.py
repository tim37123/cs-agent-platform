from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from storage.db import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    website = Column(String, nullable=True)

    # One-to-many relationship to contacts
    contacts = relationship("Contact", back_populates="account")
