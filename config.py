import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5439)
POSTGRES_DB = os.getenv("POSTGRES_DB", "patients-db")

DATA_SOURCES = {
    "patient": "https://raw.githubusercontent.com/smart-on-fhir/flat-fhir-files/master/r3/Patient.ndjson",
    "encounter": "https://raw.githubusercontent.com/smart-on-fhir/flat-fhir-files/master/r3/Encounter.ndjson",
    "procedure": "https://raw.githubusercontent.com/smart-on-fhir/flat-fhir-files/master/r3/Procedure.ndjson",
    "observation": "https://raw.githubusercontent.com/smart-on-fhir/flat-fhir-files/master/r3/Observation.ndjson",
}

COLUMNS_NAMES = {
    "patient": ["id", "address", "gender", "birthDate", "extension"],
    "encounter": ["id", "period", "type", "subject", "context"],
    "procedure": ["id", "code", "performedDateTime", "performedPeriod", "subject", "context"],
    "observation": ["id", "valueQuantity", "effectiveDateTime", "code", "subject", "context"]
}

REQUIRED_COLUMNS_NAMES = {
    "patient": ["id"],
    "encounter": ["id", "patient_db_id", "period_start", "period_end"],
    "procedure": ["id", "patient_db_id", "date", "code_coding_0_code", "code_coding_0_system"],
    "observation": ["id", "patient_db_id", "date", "code_coding_0_code", "code_coding_0_system", "valueQuantity_value"]
}
