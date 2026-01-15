from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.relative_paths import (
    RelativePaths,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_objects import (
    IndividualFileSystemSnapshotObjects,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.folder_file_byte_contents import (
    FolderFileByteContents,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.snapshot_domains import (
    SnapshotDomains,
)


class IndividualFileSystemSnapshotFolders(
    IndividualFileSystemSnapshotObjects
):
    def __init__(
        self,
        folder: Folders,
        owning_snapshot_domain: SnapshotDomains,
        relative_path: RelativePaths,
    ):
        file_byte_content = (
            FolderFileByteContents()
        )

        super().__init__(
            bie_domain_type=BieFileSystemSnapshotDomainTypes.BIE_INDIVIDUAL_FILE_SYSTEM_SNAPSHOT_FOLDERS,
            file_system_object=folder,
            owning_snapshot_domain=owning_snapshot_domain,
            relative_path=relative_path,
            object_content=file_byte_content,
        )
