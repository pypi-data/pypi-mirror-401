from bclearer_orchestration_services.file_system_snapshot_service.common.file_system_snapshot_short_names import (
    FileSystemSnapshotShortNames,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.folder_other_configurations import (
    FolderOtherConfigurations,
)


def set_common_fss_service_configuration():
    # TODO: use an enum
    FolderOtherConfigurations.B_APP_RUN_OUTPUT_SUB_FOLDER_PREFIX = (
        FileSystemSnapshotShortNames.FSS.b_enum_item_name
    )
