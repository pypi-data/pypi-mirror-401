from bclearer_core.configurations.workspaces.workspace_configurations import (
    WorkspaceConfigurations,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


# TODO: We may want to allow None for the parameter single_fssu_output_folder when we call it from a runner that only
#  gets the FSSU but it doesn't report anything
class FileSystemSnapshotConfigurations:
    def __init__(
        self,
        # TODO: should we allow Folders() or a new NullFolders() subclass?
        #  Should this be named workspace_folder? core_workspace_component_folder?
        # TODO: Should we have a WORKSPACE_DISABLED or WORKSPACE_ENABLED enum?
        single_fssu_output_folder: Folders,
        input_snapshot_container_folder: Folders,
        remove_temporary_root_folder: bool = True,
        this_run_human_readable_short_name: (
            str | None
        ) = None,
    ):
        # TODO: line below will be deprecated - to check
        self.remove_temporary_root_folder = (
            remove_temporary_root_folder
        )

        self.service_workspace_configuration = WorkspaceConfigurations(
            this_run_workspace=single_fssu_output_folder,
            this_run_human_readable_short_name=this_run_human_readable_short_name,
        )

        self.input_snapshot_container_folder: (
            Folders
        ) = input_snapshot_container_folder
