from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


def report_bie_relation_already_registered(
    calling_bie_id_relations_register,
    bie_place_1_id,
    bie_place_2_id,
    bie_relation_type_id,
):
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_relations_registers import (
        BieIdRelationsRegisters,
    )

    if not isinstance(
        calling_bie_id_relations_register,
        BieIdRelationsRegisters,
    ):
        raise TypeError()

    bie_id_types_instances_register_name = (
        calling_bie_id_relations_register.owning_bie_registry.bie_registry_name
    )

    message = (
        "Bie relation id already registered: "
        + bie_id_types_instances_register_name
        + ": <"
        + str(bie_relation_type_id)
        + ">"
        + str(bie_place_1_id)
        + " --> "
        + str(bie_place_2_id)
    )

    log_inspection_message(
        message=message,
        logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.WARNING,
    )
