import pandas as pd
import psycopg2

import config
from scripts.copy_tables import (
    copy_procedures,
    copy_encounters,
    copy_observations,
    copy_patients,
)
from scripts.utils import (
    load_input_data,
    parse_to_df,
    insert_relation_column,
    format_date,
    remove_null_required_fields,
)

patients = load_input_data("patient")
encounters = load_input_data("encounter")
procedures = load_input_data("procedure")
observations = load_input_data("observation")

patients_df = parse_to_df(patients, "patient")
encounters_df = parse_to_df(encounters, "encounter")
procedures_df = parse_to_df(procedures, "procedure")
observations_df = parse_to_df(observations, "observation")

insert_relation_column(patients_df, encounters_df, "patient", "subject_reference")
insert_relation_column(patients_df, procedures_df, "patient", "subject_reference")
insert_relation_column(encounters_df, procedures_df, "encounter", "context_reference")
insert_relation_column(patients_df, observations_df, "patient", "subject_reference")
insert_relation_column(encounters_df, observations_df, "encounter", "context_reference")

procedures_df["date"] = format_date(
    pd.concat(
        [
            procedures_df["performedDateTime"].dropna(),
            procedures_df["performedPeriod_start"].dropna(),
        ]
    )
)
observations_df["date"] = format_date(observations_df["effectiveDateTime"])

remove_null_required_fields(patients_df, "patient")
remove_null_required_fields(encounters_df, "encounter")
remove_null_required_fields(procedures_df, "procedure")
remove_null_required_fields(observations_df, "observation")

connection = psycopg2.connect(
    host=config.POSTGRES_HOST,
    database=config.POSTGRES_DB,
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    port=config.POSTGRES_PORT,
)

connection.set_session(autocommit=True)
copy_patients(connection, patients_df, size=8192)
copy_encounters(connection, encounters_df, size=8192)
copy_procedures(connection, procedures_df, size=8192)
copy_observations(connection, observations_df, size=8192)

print("Data loaded succesfully!")

print(
    f"The number of rows loaded to: \n"
    f"patient table: {patients_df.size} \n"
    f"encounter table: {encounters_df.size} \n"
    f"procedure table: {procedures_df.size} \n"
    f"observation table: {observations_df.size} \n"
)
print(f'\nPatients by gender: \n {patients_df["gender"].value_counts()}')
print(f'\nThe top 10 procedures: \n {procedures_df["code_text"].value_counts().iloc[:10]}')
print(f'\nEncounters count by day of the week\n'
      f' {pd.to_datetime(encounters_df["period_start"].astype(str).str[:10]).dt.day_name().value_counts()}'
)
