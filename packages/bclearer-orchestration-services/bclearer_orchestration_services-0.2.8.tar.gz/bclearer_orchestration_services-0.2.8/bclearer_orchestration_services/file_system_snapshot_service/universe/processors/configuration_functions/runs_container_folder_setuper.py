from pathlib import Path

from bclearer_orchestration_services.file_system_snapshot_service.multiverse.common_knowledge.file_system_snapshot_multiverses_folder_names import (
    FileSystemSnapshotMultiversesOutputFolderNames,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.file_system_snapshots_configurations import (
    FileSystemSnapshotsConfigurations,
)


def setup_runs_container_folder(
    file_system_snapshots_configuration: FileSystemSnapshotsConfigurations,
):
    if (
        len(
            file_system_snapshots_configuration.input_snapshot_containers_folder_configuration.folder_list
        )
        == 1
    ):
        runs_container_folder = (
            file_system_snapshots_configuration.fss_service_workspace_configuration.this_run_workspace
        )

    else:
        runs_container_folder = file_system_snapshots_configuration.fss_service_workspace_configuration.this_run_workspace.get_descendant_file_system_folder(
            relative_path=Path(
                FileSystemSnapshotMultiversesOutputFolderNames.SINGLE_FSSU_RUNS.b_enum_item_name
            )
        )

        runs_container_folder.make_me_on_disk()

    return runs_container_folder
