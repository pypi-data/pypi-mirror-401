from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.file_system_snapshots_configurations import (
    FileSystemSnapshotsConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverses import (
    FileSystemSnapshotMultiverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.orchestrators.file_system_snapshot_universe_run_and_export_orchestrator import (
    orchestrate_file_system_snapshot_universe_run_and_export,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.configuration_functions.file_system_snapshot_configuration_setter import (
    set_file_system_snapshot_configuration,
)


def process_input_root_file_system_snapshot_container_folder(
    input_root_file_system_snapshot_container_folder: Folders,
    file_system_snapshot_multiverse: FileSystemSnapshotMultiverses,
    file_system_snapshots_configuration: FileSystemSnapshotsConfigurations,
    iteration_index: int,
    runs_container_folder: Folders,
):
    file_system_snapshot_configuration = set_file_system_snapshot_configuration(
        input_root_file_system_snapshot_container_folder=input_root_file_system_snapshot_container_folder,
        single_universe_runs_container_folder=runs_container_folder,
        file_system_snapshots_configuration=file_system_snapshots_configuration,
        iteration_index=iteration_index,
    )

    file_system_snapshot_universe = orchestrate_file_system_snapshot_universe_run_and_export(
        file_system_snapshot_configuration=file_system_snapshot_configuration
    )

    file_system_snapshot_multiverse.add_universe_to_registry(
        file_system_snapshot_universe=file_system_snapshot_universe
    )
