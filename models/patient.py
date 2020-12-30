from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from . import Base


class Patient(Base):
    """Object representing patient object"""
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True)
    source_id = Column(String(255), nullable=False)
    birth_date = Column(Date())
    gender = Column(String(255))
    race_code = Column(String(255))
    race_code_system = Column(String(255))
    ethnicity_code = Column(String(255))
    ethnicity_code_system = Column(String(255))
    country = Column(String(255))

    observation = relationship("Observation")
    encounter = relationship("Encounter")
    procedure = relationship("Procedure")
