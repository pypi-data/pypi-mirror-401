import copy

import pandas
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def get_bieize_dataframe_rows_by_content(
    table_to_bieize_dataframe: pandas.DataFrame,
    table_name: str,
) -> pandas.DataFrame:
    biezed_dataframe = copy.deepcopy(
        table_to_bieize_dataframe
    )

    biezed_dataframe[
        BieColumnNames.BIE_IDS.b_enum_item_name
    ] = biezed_dataframe.apply(
        lambda row: __get_b_identity_sum_for_data_frame_axis_1(
            row, table_name
        ),
        axis=1,
    )

    bie_id_column = biezed_dataframe.pop(
        BieColumnNames.BIE_IDS.b_enum_item_name
    )

    biezed_dataframe.insert(
        0,
        BieColumnNames.BIE_IDS.b_enum_item_name,
        bie_id_column,
    )

    return biezed_dataframe


def __get_b_identity_sum_for_data_frame_axis_1(
    row_series: pandas.Series,
    containing_bunit_name: str,
) -> BieIds:
    input_objects = (
        row_series.tolist()
        + [containing_bunit_name]
    )

    b_identity_for_row = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
        input_objects=input_objects
    )

    return b_identity_for_row
