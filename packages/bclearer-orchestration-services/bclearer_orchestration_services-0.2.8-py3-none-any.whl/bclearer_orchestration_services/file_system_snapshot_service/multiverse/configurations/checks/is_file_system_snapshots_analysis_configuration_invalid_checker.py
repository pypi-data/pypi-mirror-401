from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


def is_file_system_snapshots_analysis_configuration_invalid() -> (
    bool
):
    configuration_invalid = False

    if configuration_invalid:
        log_inspection_message(
            message="THE CONFIGURATION IS INVALID. PROCESS TERMINATED.",
            logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.CRITICAL,
        )
    return configuration_invalid
