from bclearer_orchestration_services.identification_services.b_identity_ecosystem.functions.dataframes.dataframe_by_table_name_and_single_column_content_biezer import (
    bieze_dataframe_by_table_name_and_single_column_content,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.functions.dataframes.row_and_column_grid_for_dataframe_creator import (
    create_row_and_column_grid_for_dataframe,
)
from pandas import DataFrame


def add_column_and_row_grid_numbers_and_bieids_to_dataframe(
    dataframe: DataFrame,
    table_name: str,
) -> DataFrame:
    dataframe_with_column_grid_number = __rename_columns_with_grid_numbers(
        dataframe=dataframe
    )

    (
        dataframe_with_row_and_column_grid,
        row_grid_number_column_name,
    ) = create_row_and_column_grid_for_dataframe(
        dataframe=dataframe_with_column_grid_number
    )

    biezed_dataframe = bieze_dataframe_by_table_name_and_single_column_content(
        dataframe=dataframe_with_row_and_column_grid,
        table_name=table_name,
        column_name=row_grid_number_column_name,
    )

    return biezed_dataframe


def __rename_columns_with_grid_numbers(
    dataframe: DataFrame,
) -> DataFrame:
    dataframe.columns = [
        f"column_no: {i}"
        for i in range(
            dataframe.shape[1]
        )
    ]

    return dataframe
