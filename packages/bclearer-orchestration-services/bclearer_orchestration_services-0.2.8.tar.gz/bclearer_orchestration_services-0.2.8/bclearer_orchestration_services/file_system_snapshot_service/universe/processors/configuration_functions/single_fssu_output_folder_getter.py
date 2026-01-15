from pathlib import Path

from bclearer_core.configurations.workspaces.workspace_configurations import (
    WorkspaceConfigurations,
)
from bclearer_core.constants.standard_constants import (
    NAME_COMPONENT_DIVIDER,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.common_knowledge.file_system_snapshot_multiverses_folder_names import (
    FileSystemSnapshotMultiversesOutputFolderNames,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.file_system_snapshots_configurations import (
    FileSystemSnapshotsConfigurations,
)


def get_single_fssu_output_folder(
    single_universe_runs_container_folder: Folders,
    file_system_snapshots_configuration: FileSystemSnapshotsConfigurations,
    iteration_index: int,
) -> WorkspaceConfigurations:
    # if file_system_snapshot_multiverse.is_null_file_system_snapshot_multiverse():
    # TODO: This conditional ensures we still get a different output when the multiverse returned only has one universe.
    #  There must be a better way to do it without having to check the BConfigurations constants.
    #  Maybe checking the input cardinality at the beginning and storing it in a Multiverse property?
    if (
        len(
            file_system_snapshots_configuration.input_snapshot_containers_folder_configuration.folder_list
        )
        == 1
    ):
        this_run_human_readable_short_name = (
            file_system_snapshots_configuration.fss_service_workspace_configuration.this_run_human_readable_short_name
        )

        single_fssu_workpsace_configuration = WorkspaceConfigurations(
            this_run_workspace=single_universe_runs_container_folder,
            this_run_human_readable_short_name=this_run_human_readable_short_name,
        )

    else:
        single_fssu_workpsace_configuration = __get_single_fssu_output_folder_for_multiple_cardinality_configuration(
            single_universe_runs_container_folder=single_universe_runs_container_folder,
            file_system_snapshots_configuration=file_system_snapshots_configuration,
            iteration_index=iteration_index,
        )

    return single_fssu_workpsace_configuration


def __get_single_fssu_output_folder_for_multiple_cardinality_configuration(
    single_universe_runs_container_folder: Folders,
    file_system_snapshots_configuration: FileSystemSnapshotsConfigurations,
    iteration_index: int,
) -> WorkspaceConfigurations:
    single_fssu_output_folder = single_universe_runs_container_folder.get_descendant_file_system_folder(
        relative_path=Path(
            FileSystemSnapshotMultiversesOutputFolderNames.FSSU_RUN.b_enum_item_name
            + NAME_COMPONENT_DIVIDER
            + str(iteration_index)
        )
    )

    this_run_human_readable_short_name = (
        file_system_snapshots_configuration.fss_service_workspace_configuration.this_run_human_readable_short_name
        + NAME_COMPONENT_DIVIDER
        + "run_"
        + str(iteration_index)
    )

    single_fssu_workpsace_configuration = WorkspaceConfigurations(
        this_run_workspace=single_fssu_output_folder,
        this_run_human_readable_short_name=this_run_human_readable_short_name,
    )

    return single_fssu_workpsace_configuration
