from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from storage.db import Base

class CallParticipant(Base):
    __tablename__ = "call_participants"

    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey("calls.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    # Use string references to avoid circular import issues
    call = relationship("Call", back_populates="participants")
    contact = relationship("Contact", back_populates="calls")
    employee = relationship("Employee", back_populates="calls")

    __table_args__ = (
        UniqueConstraint('call_id', 'contact_id', name='uix_call_contact'),
        UniqueConstraint('call_id', 'employee_id', name='uix_call_employee'),
    )
