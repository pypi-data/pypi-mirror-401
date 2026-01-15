from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.checks.is_file_system_snapshots_and_analysis_b_application_configuration_invalid_checker import (
    is_file_system_snapshots_and_analysis_b_application_configuration_invalid,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.file_system_snapshots_configurations import (
    FileSystemSnapshotsConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.orchestrators.file_system_snapshots_multiverse_analyse_orchestrator import (
    orchestrate_file_system_snapshots_multiverse_analyse,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.orchestrators.file_system_snapshots_multiverse_run_and_export_orchestrator import (
    orchestrate_file_system_snapshots_multiverse_run_and_export,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverses import (
    FileSystemSnapshotMultiverses,
)


def orchestrate_file_system_snapshots_multiverse_run_export_and_analyse(
    file_system_snapshots_configuration: FileSystemSnapshotsConfigurations,
) -> (
    FileSystemSnapshotMultiverses | None
):
    file_system_snapshots_and_analysis_b_application_configuration_is_invalid = (
        is_file_system_snapshots_and_analysis_b_application_configuration_invalid()
    )

    if file_system_snapshots_and_analysis_b_application_configuration_is_invalid:
        return None

    file_system_snapshot_multiverse = orchestrate_file_system_snapshots_multiverse_run_and_export(
        file_system_snapshots_configuration=file_system_snapshots_configuration
    )

    orchestrate_file_system_snapshots_multiverse_analyse(
        file_system_snapshot_multiverse=file_system_snapshot_multiverse
    )

    return (
        file_system_snapshot_multiverse
    )
