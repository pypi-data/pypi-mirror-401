from typing import Type

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)
from pandas import DataFrame


def create_bie_enum_table(
    bie_enum_type: Type[BieEnums],
    name_column_name: str,
) -> DataFrame:
    bie_enum_table_data = []

    for bie_enum_item in bie_enum_type:
        __add_bie_enum_item(
            bie_enum_item=bie_enum_item,
            bie_enum_table_data=bie_enum_table_data,
            name_column_name=name_column_name,
        )

    bie_enum_table = DataFrame(
        bie_enum_table_data
    )

    return bie_enum_table


def __add_bie_enum_item(
    bie_enum_item,
    bie_enum_table_data,
    name_column_name,
) -> None:
    if bie_enum_item.name == "NOT_SET":
        return

    bie_enum_table_data.append(
        {
            BieColumnNames.BIE_IDS.b_enum_item_name: bie_enum_item.item_bie_identity,
            name_column_name: bie_enum_item.b_enum_item_name,
        }
    )
