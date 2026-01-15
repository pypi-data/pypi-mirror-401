from nf_common_base.b_source.services.dataframe_service.dataframe_helpers.next_unique_column_grid_number_name_getter import (
    get_next_unique_column_grid_number_name,
)
from pandas import DataFrame


def create_row_and_column_grid_for_dataframe(
    dataframe: DataFrame,
) -> tuple:
    unique_column_grid_number_name = get_next_unique_column_grid_number_name(
        dataframe=dataframe,
        base_column_name="row_grid_number",
    )

    dataframe_with_row_and_column_grid = dataframe.copy(
        deep=True
    )

    end_row_grid_number = int(
        len(dataframe) + 1
    )

    # TODO: DZa to check warning
    dataframe_with_row_and_column_grid.insert(
        0,
        unique_column_grid_number_name,
        range(1, end_row_grid_number),
    )

    return (
        dataframe_with_row_and_column_grid,
        unique_column_grid_number_name,
    )
