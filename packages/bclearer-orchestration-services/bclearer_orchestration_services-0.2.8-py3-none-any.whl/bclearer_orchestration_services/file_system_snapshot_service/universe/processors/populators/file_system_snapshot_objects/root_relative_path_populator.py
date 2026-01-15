from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.root_relative_paths import (
    RootRelativePaths,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_folders import (
    IndividualFileSystemSnapshotFolders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.file_system_snapshot_objects.file_system_snapshot_children_from_parent_adder import (
    add_file_system_snapshot_children_from_parent,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def populate_root_relative_path(
    root_relative_path: RootRelativePaths,
) -> None:
    # TODO: Think about compressed verses
    if isinstance(
        root_relative_path.snapshot,
        IndividualFileSystemSnapshotFolders,
    ):
        add_file_system_snapshot_children_from_parent(
            parent_file_system_snapshot_folder=root_relative_path.snapshot
        )
