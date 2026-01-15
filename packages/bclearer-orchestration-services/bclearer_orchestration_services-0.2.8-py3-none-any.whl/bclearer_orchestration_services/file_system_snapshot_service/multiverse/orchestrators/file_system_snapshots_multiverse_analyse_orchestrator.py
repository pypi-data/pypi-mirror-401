from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.checks.is_file_system_snapshots_analysis_configuration_invalid_checker import (
    is_file_system_snapshots_analysis_configuration_invalid,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.processors.file_system_snapshot_multiverse_analyser import (
    analyse_file_system_snapshot_multiverse,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverses import (
    FileSystemSnapshotMultiverses,
)


def orchestrate_file_system_snapshots_multiverse_analyse(
    file_system_snapshot_multiverse: FileSystemSnapshotMultiverses,
) -> None:
    file_system_snapshots_analysis_configuration_is_invalid = (
        is_file_system_snapshots_analysis_configuration_invalid()
    )

    if file_system_snapshots_analysis_configuration_is_invalid:
        return None

    analyse_file_system_snapshot_multiverse(
        file_system_snapshot_multiverse=file_system_snapshot_multiverse
    )

    return None
