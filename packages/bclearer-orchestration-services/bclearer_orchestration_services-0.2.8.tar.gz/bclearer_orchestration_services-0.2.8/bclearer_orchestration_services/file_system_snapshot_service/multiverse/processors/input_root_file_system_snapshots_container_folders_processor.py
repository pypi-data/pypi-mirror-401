from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.file_system_snapshots_configurations import (
    FileSystemSnapshotsConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.processors.input_root_file_system_snapshot_container_folder_processor import (
    process_input_root_file_system_snapshot_container_folder,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverses import (
    FileSystemSnapshotMultiverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.configuration_functions.runs_container_folder_setuper import (
    setup_runs_container_folder,
)


def process_input_root_file_system_snapshots_container_folders(
    file_system_snapshot_multiverse: FileSystemSnapshotMultiverses,
    file_system_snapshots_configuration: FileSystemSnapshotsConfigurations,
):
    input_root_file_system_snapshot_container_folders = (
        file_system_snapshots_configuration.input_snapshot_containers_folder_configuration.folder_list
    )

    runs_container_folder = setup_runs_container_folder(
        file_system_snapshots_configuration=file_system_snapshots_configuration
    )

    for (
        iteration_index,
        input_root_file_system_snapshot_container_folder,
    ) in enumerate(
        input_root_file_system_snapshot_container_folders
    ):
        process_input_root_file_system_snapshot_container_folder(
            input_root_file_system_snapshot_container_folder=input_root_file_system_snapshot_container_folder,
            file_system_snapshot_multiverse=file_system_snapshot_multiverse,
            file_system_snapshots_configuration=file_system_snapshots_configuration,
            iteration_index=iteration_index,
            runs_container_folder=runs_container_folder,
        )
