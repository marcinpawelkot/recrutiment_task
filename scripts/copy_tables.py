from scripts.string_iterator import StringIteratorIO
from scripts.utils import *


def copy_patients(connection, patients_df: pd.DataFrame, size: int = 8192) -> None:
    with connection.cursor() as cursor:
        patients_string_iterator = StringIteratorIO(
            (
                "|".join(
                    map(
                        clean_csv_value,
                        (
                            patient.Index,
                            patient.id,
                            patient.birthDate,
                            patient.gender,
                            patient.extension_0_valueCodeableConcept_coding_0_code,
                            patient.extension_0_valueCodeableConcept_coding_0_system,
                            patient.extension_1_valueCodeableConcept_coding_0_code,
                            patient.extension_1_valueCodeableConcept_coding_0_system,
                            patient.address_0_country,
                        ),
                    )
                )
                + "\n"
                for patient in patients_df.itertuples()
            )
        )

        cursor.copy_from(patients_string_iterator, "patient", sep="|", size=size)


def copy_encounters(connection, encounters_df: pd.DataFrame, size: int = 8192) -> None:
    with connection.cursor() as cursor:
        encounters_string_iterator = StringIteratorIO(
            (
                "|".join(
                    map(
                        clean_csv_value,
                        (
                            encounter.Index,
                            encounter.id,
                            encounter.patient_db_id,
                            encounter.period_start,
                            encounter.period_end,
                            encounter.type_0_coding_0_code,
                            encounter.type_0_coding_0_system,
                        ),
                    )
                )
                + "\n"
                for encounter in encounters_df.itertuples()
            )
        )

        cursor.copy_from(encounters_string_iterator, "encounter", sep="|", size=size)


def copy_procedures(connection, procedures_df: pd.DataFrame, size: int = 8192) -> None:
    with connection.cursor() as cursor:
        procedures_string_iterator = StringIteratorIO(
            (
                "|".join(
                    map(
                        clean_csv_value,
                        (
                            procedure.Index,
                            procedure.id,
                            procedure.patient_db_id,
                            procedure.encounter_db_id if not pd.isnull(procedure.encounter_db_id) else None,
                            procedure.date,
                            procedure.code_coding_0_code,
                            procedure.code_coding_0_system,
                        ),
                    )
                )
                + "\n"
                for procedure in procedures_df.itertuples()
            )
        )

        cursor.copy_from(procedures_string_iterator, "procedure", sep="|", size=size)


def copy_observations(connection, observations_df: pd.DataFrame, size: int = 8192) -> None:
    with connection.cursor() as cursor:
        observations_string_iterator = StringIteratorIO(
            (
                "|".join(
                    map(
                        clean_csv_value,
                        (
                            observation.Index,
                            observation.id,
                            observation.patient_db_id,
                            observation.encounter_db_id if not pd.isnull(observation.encounter_db_id) else None,
                            observation.date,
                            observation.code_coding_0_code,
                            observation.code_coding_0_system,
                            observation.valueQuantity_value,
                            observation.valueQuantity_unit,
                            observation.valueQuantity_system,
                        ),
                    )
                )
                + "\n"
                for observation in observations_df.itertuples()
            )
        )

        cursor.copy_from(observations_string_iterator, "observation", sep="|", size=size)
