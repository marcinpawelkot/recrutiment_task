from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float

from . import Base


class Observation(Base):
    """Object representing observation object"""
    __tablename__ = "observation"

    id = Column(Integer, primary_key=True)
    source_id = Column(String(255), nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    encounter_id = Column(Integer, ForeignKey('encounter.id'))
    observation_date = Column(Date())
    type_code = Column(String(255), nullable=False)
    type_code_system = Column(String(255), nullable=False)
    value = Column(Float(), nullable=False)
    unit_code = Column(String(255))
    unit_code_system = Column(String(255))
