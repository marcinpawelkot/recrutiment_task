from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .encounter import Encounter
from .observation import Observation
from .patient import Patient
from .procedure import Procedure

__all__ = ["Encounter", "Observation", "Patient", "Procedure"]
