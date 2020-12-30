from sqlalchemy import Column, DateTime, Integer, String, ForeignKey

from . import Base


class Procedure(Base):
    """Object representing procedure object"""
    __tablename__ = "procedure"

    id = Column(Integer, primary_key=True)
    source_id = Column(String(255), nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    encounter_id = Column(Integer, ForeignKey('encounter.id'))
    procedure_date = Column(DateTime(), nullable=False)
    type_code = Column(String(255), nullable=False)
    type_code_system = Column(String(255), nullable=False)
