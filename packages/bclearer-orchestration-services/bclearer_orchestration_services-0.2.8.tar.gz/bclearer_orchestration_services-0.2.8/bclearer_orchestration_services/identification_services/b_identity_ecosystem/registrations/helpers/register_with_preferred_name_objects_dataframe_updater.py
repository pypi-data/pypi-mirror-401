from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from pandas import DataFrame


def update_register_with_preferred_name_objects_dataframe(
    bie_objects_register,
    already_registered_preferred_name_objects: DataFrame,
) -> None:
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registers import (
        BieIdRegisters,
    )

    if not isinstance(
        bie_objects_register,
        BieIdRegisters,
    ):
        raise TypeError

    bie_objects_register_dataframe = (
        bie_objects_register.get_bie_register_dataframe()
    )

    bie_objects_register_updated = bie_objects_register_dataframe.merge(
        already_registered_preferred_name_objects,
        on=BieColumnNames.BIE_IDS.b_enum_item_name,
        how="left",
        suffixes=("", "_new"),
    )

    bie_objects_register_updated[
        BieColumnNames.BIE_NAMES.b_enum_item_name
    ] = bie_objects_register_updated[
        BieColumnNames.BIE_NAMES.b_enum_item_name
        + "_new"
    ].combine_first(
        bie_objects_register_updated[
            BieColumnNames.BIE_NAMES.b_enum_item_name
        ]
    )

    bie_objects_register_updated = bie_objects_register_updated.drop(
        columns=[
            BieColumnNames.BIE_NAMES.b_enum_item_name
            + "_new"
        ]
    )

    bie_objects_register.replace_dataframe(
        dataframe=bie_objects_register_updated
    )
