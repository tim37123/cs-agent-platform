from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from storage.db import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    title = Column(String)

    calls = relationship("CallParticipant", back_populates="employee")
