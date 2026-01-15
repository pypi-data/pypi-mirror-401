from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.file_system_snapshot_configurations import (
    FileSystemSnapshotConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universes import (
    FileSystemSnapshotUniverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.orchestrators.file_system_snapshot_service_handler import (
    handle_file_system_snapshot_service,
)


# TODO: Find duplicates (single service test) and merge
def orchestrate_file_system_snapshot_universe_run_and_export(
    file_system_snapshot_configuration: FileSystemSnapshotConfigurations,
) -> FileSystemSnapshotUniverses:
    file_system_snapshot_universe = handle_file_system_snapshot_service(
        file_system_snapshot_configuration=file_system_snapshot_configuration
    )

    # TODO: if ENABLE_INSPECTIONS is set, call method
    # TODO: Call new method .inspect_me from the Universe - DONE
    file_system_snapshot_universe.inspect_me(
        service_workspace_configuration=file_system_snapshot_configuration.service_workspace_configuration
    )

    return file_system_snapshot_universe
