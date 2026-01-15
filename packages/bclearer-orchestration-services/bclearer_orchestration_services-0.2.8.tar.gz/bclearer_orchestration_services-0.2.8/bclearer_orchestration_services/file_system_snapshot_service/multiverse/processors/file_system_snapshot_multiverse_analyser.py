from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverses import (
    FileSystemSnapshotMultiverses,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


def analyse_file_system_snapshot_multiverse(
    file_system_snapshot_multiverse: FileSystemSnapshotMultiverses,
) -> None:
    log_inspection_message(
        message=file_system_snapshot_multiverse.base_hr_name,
        logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.INFO,
    )

    # TODO: Export any information related with the multiverse at a wrapper level
