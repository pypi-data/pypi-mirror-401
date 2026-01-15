from dataclasses import dataclass

from bclearer_core.configurations.workspaces.workspace_configurations import (
    WorkspaceConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.folder_configurations import (
    FolderConfigurations,
)


@dataclass(frozen=True)
class FileSystemSnapshotsConfigurations:
    fss_service_workspace_configuration: (
        WorkspaceConfigurations
    )

    input_snapshot_containers_folder_configuration: (
        FolderConfigurations
    )
