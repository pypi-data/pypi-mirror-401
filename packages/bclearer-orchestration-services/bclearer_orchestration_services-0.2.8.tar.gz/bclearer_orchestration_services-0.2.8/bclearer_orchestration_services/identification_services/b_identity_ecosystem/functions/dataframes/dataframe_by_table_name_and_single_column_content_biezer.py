import copy

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_constants import (
    BIE_ID_COLUMN_NAME,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from pandas import DataFrame, Series


def bieze_dataframe_by_table_name_and_single_column_content(
    dataframe: DataFrame,
    table_name: str,
    column_name: str,
) -> DataFrame:
    biezed_dataframe = copy.deepcopy(
        dataframe
    )

    # TODO: replace BIE_ID_COLUMN_NAME with BieColumnNames.BIE_IDS.b_enum_item_name when bEnums have been moved over to nf_common
    biezed_dataframe[
        BIE_ID_COLUMN_NAME
    ] = biezed_dataframe.apply(
        lambda row: __get_b_identity_sum_for_data_frame_axis_1(
            row, table_name, column_name
        ),
        axis=1,
    )

    bie_id_column = (
        biezed_dataframe.pop(
            BIE_ID_COLUMN_NAME
        )
    )

    biezed_dataframe.insert(
        0,
        BIE_ID_COLUMN_NAME,
        bie_id_column,
    )

    return biezed_dataframe


def __get_b_identity_sum_for_data_frame_axis_1(
    row: Series,
    table_name: str,
    row_number_column_name: str,
) -> BieIds:
    input_objects = [
        row[row_number_column_name],
        table_name,
    ]

    bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
        input_objects=input_objects
    )

    return bie_id
