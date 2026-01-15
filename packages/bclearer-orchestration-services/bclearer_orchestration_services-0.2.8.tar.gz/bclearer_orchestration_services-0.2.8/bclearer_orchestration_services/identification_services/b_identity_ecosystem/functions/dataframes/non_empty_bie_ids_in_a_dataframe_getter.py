from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from pandas import DataFrame


def get_non_empty_bie_ids_in_a_dataframe(
    input_dataframe: DataFrame,
    column_name: str,
):
    input_dataframe_filtered = (
        input_dataframe[
            input_dataframe[
                column_name
            ].apply(
                get_non_empty_bie_ids
            )
        ]
    )

    return input_dataframe_filtered


def get_non_empty_bie_ids(
    bie_ids: BieIds,
):
    return bie_ids.int_value > 0
