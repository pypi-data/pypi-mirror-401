from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


def report_bie_relation_content_invalid(
    bie_place_1_id: BieIds,
    bie_place_2_id: BieIds,
    bie_relation_type_id: BieIds,
):
    message = (
        "Bie relation is invalid: "
        + "bie_relation_type_id: "
        + str(bie_relation_type_id)
        + "bie_place_1_id: "
        + str(bie_place_1_id)
        + "bie_place_2_id: "
        + str(bie_place_2_id)
    )

    log_inspection_message(
        message=message,
        logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.WARNING,
    )
