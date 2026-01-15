from typing import Optional

from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.helpers.temporary_root_workspace_folder_remover import (
    remove_temporary_root_workspace_folder,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_file_system_snapshot_object_universe_getter import (
    get_bie_file_system_snapshot_object_universe,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.file_system_snapshot_configurations import (
    FileSystemSnapshotConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universes import (
    FileSystemSnapshotUniverses,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def get_file_system_snapshot_universe(
    file_system_snapshot_configuration: FileSystemSnapshotConfigurations,
) -> FileSystemSnapshotUniverses:
    file_system_snapshot_universe = __orchestrate_windows_file_system_tool_hard_crash_wrapper(
        file_system_snapshot_configuration=file_system_snapshot_configuration
    )

    return file_system_snapshot_universe


def __orchestrate_windows_file_system_tool_hard_crash_wrapper(
    file_system_snapshot_configuration: FileSystemSnapshotConfigurations,
) -> Optional[
    FileSystemSnapshotUniverses
]:
    remove_temporary_root_folder = (
        file_system_snapshot_configuration.remove_temporary_root_folder
    )

    # TODO: unused code for FSSO tests (use cases and export) - this is inside zz_deprecate_nf_common, to move back?
    remove_temporary_root_workspace_folder(
        remove_temporary_root_folder=remove_temporary_root_folder
    )

    root_file_system_object = (
        file_system_snapshot_configuration.input_snapshot_container_folder
    )

    try:
        remove_temporary_root_workspace_folder(
            remove_temporary_root_folder=remove_temporary_root_folder
        )

        parallel_bie_universe = (
            get_bie_file_system_snapshot_object_universe()
        )

        file_system_snapshot_universe = FileSystemSnapshotUniverses(
            parallel_bie_universe=parallel_bie_universe,
            root_file_system_object=root_file_system_object,
        )

        return file_system_snapshot_universe

    except Exception as run_error:
        import traceback

        remove_temporary_root_workspace_folder(
            remove_temporary_root_folder=remove_temporary_root_folder
        )

        print(
            "A CRITICAL error occurred trying to create the FileSystemSnapshotUniverses: {0}".format(
                run_error
            )
        )
        print("Full traceback:")
        traceback.print_exc()
