from bclearer_core.configurations.workspaces.factories.workspace_configuration_factory import (
    create_workspace_configuration,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.file_system_snapshot_service.file_system_snapshot_service_module.file_system_snapshot_service_facade import (
    FileSystemSnapshotServiceFacade,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.file_system_snapshot_configurations import (
    FileSystemSnapshotConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.profiles.file_system_snapshot_container_bie_id_profile_comparers import (
    FileSystemSnapshotContainerBieIdProfileComparers,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universes import (
    FileSystemSnapshotUniverses,
)


def get_first_and_second_root_folders_bie_profile_comparer(
    first_root_folder: Folders,
    second_root_folder: Folders,
    optional_fssu_reporting_root_folder: (
        Folders | None
    ) = None,
) -> FileSystemSnapshotContainerBieIdProfileComparers:
    first_root_folder_file_system_snapshot_universe = FileSystemSnapshotServiceFacade.run_file_system_snapshot(
        file_system_snapshot_configuration=FileSystemSnapshotConfigurations(
            single_fssu_output_folder=None,
            input_snapshot_container_folder=first_root_folder,
        )
    )

    first_root_folder_file_system_snapshot_universe_bie_profile = (
        first_root_folder_file_system_snapshot_universe.get_my_bie_id_profile()
    )

    second_root_folder_file_system_snapshot_universe = FileSystemSnapshotServiceFacade.run_file_system_snapshot(
        file_system_snapshot_configuration=FileSystemSnapshotConfigurations(
            single_fssu_output_folder=None,
            input_snapshot_container_folder=second_root_folder,
        )
    )

    second_root_folder_file_system_snapshot_universe_bie_profile = (
        second_root_folder_file_system_snapshot_universe.get_my_bie_id_profile()
    )

    first_and_second_fssu_bie_profile_comparer = first_root_folder_file_system_snapshot_universe_bie_profile.compare_with_me(
        other_file_system_snapshot_container_bie_id_profile=second_root_folder_file_system_snapshot_universe_bie_profile
    )

    if optional_fssu_reporting_root_folder:
        __report_root_folders_file_system_snapshot_universes(
            first_root_folder_file_system_snapshot_universe=first_root_folder_file_system_snapshot_universe,
            second_root_folder_file_system_snapshot_universe=second_root_folder_file_system_snapshot_universe,
            fssu_reporting_root_folder=optional_fssu_reporting_root_folder,
        )

    return first_and_second_fssu_bie_profile_comparer


def __report_root_folders_file_system_snapshot_universes(
    first_root_folder_file_system_snapshot_universe: FileSystemSnapshotUniverses,
    second_root_folder_file_system_snapshot_universe: FileSystemSnapshotUniverses,
    fssu_reporting_root_folder: Folders,
) -> None:
    first_root_folder_file_system_snapshot_universe.inspect_me(
        service_workspace_configuration=create_workspace_configuration(
            parent_workspace=fssu_reporting_root_folder,
            workspace_type_prefix="first",
        )
    )

    second_root_folder_file_system_snapshot_universe.inspect_me(
        service_workspace_configuration=create_workspace_configuration(
            parent_workspace=fssu_reporting_root_folder,
            workspace_type_prefix="second",
        )
    )
