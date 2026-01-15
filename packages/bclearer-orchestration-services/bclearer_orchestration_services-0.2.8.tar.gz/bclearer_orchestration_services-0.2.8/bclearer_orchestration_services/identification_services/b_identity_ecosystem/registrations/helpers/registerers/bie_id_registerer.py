import pandas
from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registries_registers_types import (
    BieRegistriesRegistersTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registry_registers_columns_dictionary import (
    BIE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registers import (
    BieIdRegisters,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.naming_service.b_sequence_names import (
    BSequenceNames,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


def register_bie_id(
    bie_id_register: BieIdRegisters,
    bie_item_id: BieIds,
    b_sequence_name: BSequenceNames,
    is_preferred_b_sequence_name: bool,
    bie_id_type_id: BieIds,
) -> None:
    if bie_item_id is None:
        raise Exception(
            "Parameter bie_item_id is None or empty."
        )

    bie_item_id_already_registered = __check_and_report_if_bie_item_id_already_registered(
        bie_id_register=bie_id_register,
        bie_item_id=bie_item_id,
        b_sequence_name=b_sequence_name,
        bie_id_type_id=bie_id_type_id,
    )

    if bie_item_id_already_registered:
        # TODO: Check if the b_sequence name already registered is the preferred one
        if is_preferred_b_sequence_name:
            __overwrite_b_sequence_name(
                bie_id_register=bie_id_register,
                bie_item_id=bie_item_id,
                preferred_b_sequence_name=b_sequence_name,
            )

        return

    new_row = [
        bie_item_id,
        b_sequence_name,
    ]

    bie_id_registers_columns = BIE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY[
        BieRegistriesRegistersTypes.BIE_OBJECTS_REGISTER
    ]

    bie_id_registers_new_row_dataframe = (
        pandas.Series(
            new_row,
            index=bie_id_registers_columns,
        )
        .to_frame()
        .T
    )

    bie_id_register.concatenate_dataframe(
        dataframe=bie_id_registers_new_row_dataframe
    )


def __check_and_report_if_bie_item_id_already_registered(
    bie_id_register: BieIdRegisters,
    bie_item_id: BieIds,
    b_sequence_name: BSequenceNames,
    bie_id_type_id: BieIds,
) -> bool:
    bie_item_id_is_already_registered = __check_bie_item_id_is_already_registered(
        bie_id_register=bie_id_register,
        bie_item_id=bie_item_id,
    )

    if bie_item_id_is_already_registered:
        if not bie_item_id.is_empty:
            bie_registry_name = (
                bie_id_register.owning_bie_registry.bie_registry_name
            )

            message = (
                "BieId already registered: "
                + bie_registry_name
                + ": "
                + str(bie_item_id)
                + ": "
                + str(
                    b_sequence_name.b_sequence_name_list
                )
                + " of type: "
                + str(bie_id_type_id)
            )

            log_inspection_message(
                message=message,
                logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.WARNING,
            )

        return True

    return False


def __check_bie_item_id_is_already_registered(
    bie_id_register: BieIdRegisters,
    bie_item_id: BieIds,
) -> bool:
    bie_id_register_dataframe = (
        bie_id_register.get_bie_register_dataframe()
    )

    registered_bie_ids = bie_id_register_dataframe[
        BieColumnNames.BIE_IDS.b_enum_item_name
    ].values

    if (
        bie_item_id
        in registered_bie_ids
    ):
        return True

    if not bie_item_id.is_empty:
        return False

    for (
        registered_bie_id
    ) in registered_bie_ids:
        if registered_bie_id.is_empty:
            return True
    return False


def __overwrite_b_sequence_name(
    bie_id_register: BieIdRegisters,
    bie_item_id: BieIds,
    preferred_b_sequence_name: BSequenceNames,
) -> None:
    bie_id_register_dataframe = (
        bie_id_register.get_bie_register_dataframe()
    )

    bie_id_register_dataframe.loc[
        bie_id_register_dataframe[
            BieColumnNames.BIE_IDS.b_enum_item_name
        ]
        == bie_item_id,
        BieColumnNames.BIE_NAMES.b_enum_item_name,
    ] = preferred_b_sequence_name

    bie_id_register.replace_dataframe(
        dataframe=bie_id_register_dataframe
    )
