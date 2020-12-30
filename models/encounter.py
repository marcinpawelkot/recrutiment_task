from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Encounter(Base):
    """Object representing encounter object"""
    __tablename__ = "encounter"

    id = Column(Integer, primary_key=True)
    source_id = Column(String(255), nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    start_date = Column(DateTime(), nullable=False)
    end_date = Column(DateTime(), nullable=False)
    type_code = Column(String(255))
    type_code_system = Column(String(255))

    observation = relationship("Observation")
    procedure = relationship("Procedure")
