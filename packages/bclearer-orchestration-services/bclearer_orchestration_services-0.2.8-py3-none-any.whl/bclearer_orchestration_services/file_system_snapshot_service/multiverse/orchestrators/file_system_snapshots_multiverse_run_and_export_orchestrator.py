from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.checks.is_file_system_snapshots_configuration_invalid_checker import (
    is_file_system_snapshots_configuration_invalid,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.file_system_snapshots_configurations import (
    FileSystemSnapshotsConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.factories.file_system_snapshot_multiverse_factory import (
    create_file_system_snapshot_multiverse,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.processors.input_root_file_system_snapshots_container_folders_processor import (
    process_input_root_file_system_snapshots_container_folders,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverses import (
    FileSystemSnapshotMultiverses,
)


def orchestrate_file_system_snapshots_multiverse_run_and_export(
    file_system_snapshots_configuration: FileSystemSnapshotsConfigurations,
) -> (
    FileSystemSnapshotMultiverses | None
):
    file_system_snapshots_configuration_is_invalid = (
        is_file_system_snapshots_configuration_invalid()
    )

    if file_system_snapshots_configuration_is_invalid:
        return None

    input_snapshot_containers_folder_configuration = (
        file_system_snapshots_configuration.input_snapshot_containers_folder_configuration
    )

    file_system_snapshot_multiverse = create_file_system_snapshot_multiverse(
        input_snapshot_containers_folder_configuration=input_snapshot_containers_folder_configuration
    )

    process_input_root_file_system_snapshots_container_folders(
        file_system_snapshot_multiverse=file_system_snapshot_multiverse,
        file_system_snapshots_configuration=file_system_snapshots_configuration,
    )

    return (
        file_system_snapshot_multiverse
    )
