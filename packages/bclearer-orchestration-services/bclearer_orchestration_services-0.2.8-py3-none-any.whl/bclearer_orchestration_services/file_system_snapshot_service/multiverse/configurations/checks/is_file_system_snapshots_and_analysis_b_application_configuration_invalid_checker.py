from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.checks.is_file_system_snapshots_analysis_configuration_invalid_checker import (
    is_file_system_snapshots_analysis_configuration_invalid,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.checks.is_file_system_snapshots_configuration_invalid_checker import (
    is_file_system_snapshots_configuration_invalid,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


# TODO - rearchitectHandler20250910 - review name
def is_file_system_snapshots_and_analysis_b_application_configuration_invalid() -> (
    bool
):
    configuration_invalid = False

    file_system_snapshots_configuration_is_invalid = (
        is_file_system_snapshots_configuration_invalid()
    )

    if file_system_snapshots_configuration_is_invalid:
        configuration_invalid = True

    file_system_snapshots_analysis_configuration_is_invalid = (
        is_file_system_snapshots_analysis_configuration_invalid()
    )

    if file_system_snapshots_analysis_configuration_is_invalid:
        configuration_invalid = True

    if configuration_invalid:
        log_inspection_message(
            message="THE CONFIGURATION IS INVALID. PROCESS TERMINATED.",
            logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.CRITICAL,
        )

    return configuration_invalid
